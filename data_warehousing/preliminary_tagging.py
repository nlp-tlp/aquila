from shutil import copyfile, rmtree
#from collections import OrderedDict
import os, errno, re, sys, yaml, json
from collections import OrderedDict, defaultdict

sys.path.append('../nlp')
from utils import write_to_file

from utils_dw import *

from itertools import product

from run_pipeline import *



# Generate data for the jstree plugin (not used on the ER page anymore).
def generate_jstree(category_hierarchy, output_file, output_entity_counts_file, entity_counts):
	data = []
	for category in sorted(category_hierarchy):

		data.append({"a_attr": {"data-category": category}, "id" : "node-" + str(category), "parent": ("#" if category_hierarchy[category] is None else "node-" + category_hierarchy[category]), "text" : category + " (" + str(entity_counts[category]["count"]) + ")" })

	output_file.write("$('#jstree').jstree({ 'core' : {  'data' : ")
	json.dump(data, output_file, indent = 4)
	output_file.write("}});")

	output_file.close()





# Generate data for the d3 bar chart.
def generate_bar_chart_data(category_hierarchy, entity_counts, output_file, category_dict, superparent_ids):

	# Tally all the entity appearances. For example, "fall_from_heights" should add the appearance to its parent,
	# "fall".
	def tally_entity_appearances(category_hierarchy, entity_counts):

		entity_appearances = defaultdict(list)
		for category in category_hierarchy:		
			ea = entity_counts[category]["entries"]
			if ea == 0:
				ea = []

			# Perform the union of this category's entity appearances and the appearances seen so far
			# (in case it has been added to by a child before being seen)
			entity_appearances[category] = list(set().union(ea, entity_appearances[category]))
			#parent = category_hierarchy[category]

			top_level = False
			#top_level = False if parent is not None
			while not top_level:
				parent = category_hierarchy[category]
				entity_appearances[parent] = list(set().union(ea, entity_appearances[parent]))
				if parent is not None:
					category = parent
				else:			
					top_level = True

			#if parent is not None:
				# If this category has a parent, add its appearances to the parent as well (union so duplicates aren't a problem)
				#entity_appearances[parent] = list(set().union(ea, entity_appearances[parent]))


		#print entity_appearances
		return entity_appearances

	# Tallies the counts of the entities
	def tally_entity_counts(category_hierarchy, entity_appearances):
		entity_counts = {}
		for category in category_hierarchy:
			entity_counts[category] = len(entity_appearances[category])
		return entity_counts

	def get_chart_data(category_hierarchy, entity_counts, category_dict):
		data = {"name": "all_entities", "children": [], "size": entity_counts[max(entity_counts, key = entity_counts.get)]}

		def make_chart_data(data, category_dict):			
			for category in category_dict:
				data.append({})
				data[-1]["name"] = category
				class_id = superparent_ids[get_superparent_of_category(category, category_hierarchy)]
				data[-1]["class_id"] = class_id
				data[-1]["size"] = entity_counts[category]
				data[-1]["children"] = [{"name": "<" + category + ">", "size": entity_counts[category], "class_id": class_id }]
				if category_dict[category]:
					#bar_chart_data[category]["children"] = {}
					#data[-1]["children"] = []					
					
					
					make_chart_data(data[-1]["children"], category_dict[category])
				#else:
				#	data[-1]["size"] = entity_counts[category]	


		make_chart_data(data["children"], category_dict)
		return data

	entity_appearances  = tally_entity_appearances(category_hierarchy, entity_counts)
	entity_counts 		= tally_entity_counts(category_hierarchy, entity_appearances)
	bar_chart_data 		= get_chart_data(category_hierarchy, entity_counts, category_dict)

	write_to_file(entity_appearances, OUTPUT_ENTITY_APPEARANCES_FILE, indent = 0, export = False, variable_name = "entityAppearances")

	write_to_file(bar_chart_data, output_file, indent = 1, export = False)



# Perform some preliminary tagging (just tag everything in the data with the entities from the list of categories) and write it to a single file.
def simple_preliminary_tagging(lines, category_hierarchy, superparent_ids, structured_lines): 
	# Perform preliminary tagging on the line.
	# This stage automatically tags the entry based on the categories specified in the categories.yml file.
	# Any tokens that directly match the tokens specified in the categories.yml file will be tagged accordingly.
	def preliminary_tag(line, category_hierarchy):

		lowercase_line = line.lower()

		# A tag string, which will be written to the annotation file afterwards
		tag_str = ""
		tag_list = []
		tag_index = 0

		for c in category_hierarchy:
			c_replaced = c.replace("_", " ")
			if c not in DO_NOT_TAG_CATEGORIES:
				for m in re.finditer(r"\b" + re.escape(c_replaced) + r"\b", lowercase_line):
					tag_index += 1
					tag_list.append([c, m.start(), m.end(), line[m.start():m.end()]])

		def determine_duplicates(tag_list):
			for t in tag_list:
				for t2 in tag_list:
					if t[3] in t2[3] and t[3] != t2[3]:
						# This means that one tag is inside another (i.e. "person" inside "injured person")
						if t[1] >= t2[1] and t[2] <= t2[2]:
							# This means that the tag is literally inside another in terms of its position in the paragraph
							t[3] = "<DUPLICATE>"
			return tag_list

		tag_list = determine_duplicates(tag_list)

		t_index = 1
		tag_str_list = []
		for t in tag_list:
			if t[3] != "<DUPLICATE>":
				tag_str_list.append("T%d\t%s %d %d\t%s" % (t_index, t[0], t[1], t[2], t[3]))
				t_index += 1

		tag_str = "\n".join(tag_str_list)

		return tag_str

	# Adds the entity to the entity counts dictionary.
	def add_to_entity_appearances(category, line_index, entity_counts):

		def add_to_data(category, line_index, entity_appearances):
			#entity_counts[category]["count"] = 0	# WRONG! needs to be fixed (just count total number afterwards)
			if not entity_appearances[category]["entries"]:
				entity_appearances[category]["entries"]	= []
			if line_index not in entity_appearances[category]["entries"]:
				entity_appearances[category]["entries"].append(line_index)	
			return entity_appearances

		entity_appearances = add_to_data(category, line_index, entity_counts)

		# Add one to all the parent categories as well.
		top_level = False 
		while not top_level:
			parent = category_hierarchy[category]
			entity_appearances = add_to_data(parent, line_index, entity_appearances)
			if parent is not None:
				category = parent
			else:			
				top_level = True

		return entity_counts

	# Takes a tag str and turns it into a html-ready line with <span> tags in it.
	def generate_tagged_line(line, line_index, tag_str, category_hierarchy, superparent_ids, entity_appearances, transaction_data, structured_lines):


		

		lines = tag_str.split("\n")
		ac = 0	# Additional Characters (to keep up with new span tags being added to the string)
		span_tag_add = len("<span data-tagname=\"\" class=\"tag category-\"></span>")

		# Sort them by index order first (so tags don't get mixed up)
		sorted_lines = []
		structured_lines2 = []

		# Add the structured data if using structured data
		if USING_STRUCTURED_DATA:

			structured_data = structured_lines[line_index-1].replace("\n", "").split(",")
			for c in structured_data:
				lines.append("<STRUCTURED>\t%s\t-1\t-1\t" % c)
				structured_lines2.append("<STRUCTURED>\t%s\t-1\t-1\t" % c)

		#print(structured_lines2)


		#transaction_data.append([])

		cl = []	# Category list

		for l in lines:
			vals = l.replace("\t", " ").split(" ")
			#vals[2] = int(vals[2])
			sorted_lines.append(vals)


			# Also add the categories' parents to the transaction data
			
			category = vals[1]
			top_level = False
			can_add = True
			
			#cl[-1].append(category)

			if ADD_PARENTS_TO_TRANSACTION_DATA:
				cl.append([])
			#cl[-1].append(str(line_index) + "|")

			for c in cl: # Avoid duplicates (person, person for example)
				
				if len(c) > 0:
					for c2 in c:
						test = c2
						if test == category:
							can_add = False

			if can_add:
				

				if ADD_PARENTS_TO_TRANSACTION_DATA:
					cl[-1].append(category)

					while not top_level:
						parent = category_hierarchy[category]				
						
						if parent is not None:							
							cl[-1].append(parent)
							category = parent							

						else:			
							top_level = True
				else:
					if category not in cl:
						cl.append(category)

		#print cl				

		# Add the categories to the transaction data
		# Add every combination (leg, person | body_part, person) etc
		if ADD_PARENTS_TO_TRANSACTION_DATA:
			cl_expanded = list(product(*cl))
			#print cl_expanded
			for cle in cl_expanded:
				ls = [i for i in cle]
				#if USING_STRUCTURED_DATA:
				#	structured_data = structured_lines[line_index-1].replace("\n", "").split(",")
				#	for c in structured_data:
				#		ls.append(c)
				#	ls.append("age_group")	# Need to fix this to be modular later. This part is very specific to DMP!
				#	ls.append("gender")
				#	ls.append("severity")
				transaction_data.append(ls)
		else:
			#if USING_STRUCTURED_DATA:
			#	structured_data = structured_lines[line_index-1].replace("\n", "").split(",")
			#	for c in structured_data:
			#		cl.append(c)
			#		cl.append("age_group")
			#		cl.append("gender")
			#		cl.append("severity")
			transaction_data.append(cl)



		#print transaction_data
		#print "\n"



		#print cl_expanded

		

		#if vals[1] not in transaction_data[-1]:
		#	transaction_data[-1].append(vals[1])



		sorted_lines.sort(key=lambda x: int(x[2]))
		lldiff = 0
		if USING_STRUCTURED_DATA:
			llenstart = len(line)

			di = 0
			extra_tags = ""
			for d in STRUCTURED_FIELDS:
				tag = structured_lines2[di].replace("\t", " ").split(" ")[1]
				superparent 	= get_superparent_of_category(tag, category_hierarchy)
				superparent_id  = superparent_ids[superparent]
				extra_tags = extra_tags + "<b>" + d + ": </b><span data-tagname=\"" + superparent + ": " + tag + "\" class=\"tag category-" + str(superparent_id) + "\">" + tag + "</span><br/>"
				di += 1

			extra_tags = extra_tags + "<hr/>"
			line = extra_tags + line

			llenend = len(line)
			lldiff = llenend - llenstart

		for l in sorted_lines:
			

			tag = l[1]
			start = int(l[2]) + lldiff
			end = int(l[3]) + lldiff
			add = end - start

			superparent 	= get_superparent_of_category(tag, category_hierarchy)
			superparent_id  = superparent_ids[superparent]

			entity_appearances = add_to_entity_appearances(tag, line_index, entity_appearances)

			if l[0] != "<STRUCTURED>":
				#print(">>", superparent_id)
				line = line[0:start + ac] + "<span data-tagname=\"" + superparent + ": " + tag + "\" class=\"tag category-" + str(superparent_id) + "\">" + line [start + ac : end + ac] + "</span>" + line[end + ac:]
				ac = ac + add + span_tag_add + len(str(superparent)) + len(str(superparent_id)) + 2 # 2 is for the ": "


		return line

	report_data = []
	line_index = 1	
	entity_appearances = defaultdict(lambda: defaultdict(int))
	transaction_data = []	# To use for association rule learning

	for line in lines:

		tag_str = preliminary_tag(line, category_hierarchy)

		
		if len(tag_str) > 0:
			tagged_line = generate_tagged_line(line, line_index, tag_str, category_hierarchy, superparent_ids, entity_appearances, transaction_data, structured_lines)
		else:
			tagged_line = line
		report_data.append({})
		report_data[-1]["Index"] 		= line_index 
		report_data[-1]["Tagged Entry"] = tagged_line
		line_index += 1 
		#print(line_index, end="")

	write_to_file(report_data, OUTPUT_PRELIM_TAG_FILE, indent = 1, export = True)



	with open(OUTPUT_TRANS_DATA_FILE, 'w') as f:
		for line in transaction_data:
			f.write(",".join(line) + "\n")
	


	

	copyfile(OUTPUT_PRELIM_TAG_FILE, '../nlp/data/reports/prelim_tagging.js')

	# Tallies all the entity counts correctly, based on the number of records appearing in each entity.
	#def tally_entity_counts(entity_counts):
	#	for category in entity_counts:
	#		num_entries = len(entity_counts[category]["entries"])



	return entity_appearances



def copy_files():
	# Copy the file into the public folder
	#copyfile(OUTPUT_JSTREE_FILE, '../public/javascripts/data_warehousing/categories_jstree.js')
	copyfile(OUTPUT_ENTITY_APPEARANCES_FILE, '../public/javascripts/data_warehousing/entity_appearances.js')
	copyfile(OUTPUT_ENTITY_APPEARANCES_FILE, 'input/entity_appearances.js')
	copyfile(OUTPUT_BARCHART_DATA_FILE, '../public/javascripts/data_warehousing/bar_chart_data.json')


def main():
	with open(INPUT_CATEGORIES_FILE, 'r') as f:
		categories = ordered_load(f, yaml.SafeLoader)

	category_hierarchy 	= get_category_hierarchy(categories)
	superparent_ids 	= get_superparent_ids(category_hierarchy)

	with codecs.open(INPUT_DATA_FILE, 'r', 'utf-8') as f:
		lines = f.readlines()
		if USING_STRUCTURED_DATA:
			structured_data = open(INPUT_STRUCTURED_DATA_FILE, "r")
			structured_lines = structured_data.readlines()
		else:
			structured_lines = None
		entity_counts = simple_preliminary_tagging(lines, category_hierarchy, superparent_ids, structured_lines)

	#with open(OUTPUT_JSTREE_FILE, 'w') as f:
	#	generate_jstree(category_hierarchy, f, 0, entity_counts)

	generate_bar_chart_data(category_hierarchy, entity_counts, OUTPUT_BARCHART_DATA_FILE, categories, superparent_ids)

	copy_files()



if __name__ == "__main__":
    main()
