#from collections import OrderedDict
import os, errno, re, sys, yaml, json
from collections import OrderedDict, defaultdict

sys.path.append('../nlp')
from utils import write_to_file

from utils_dw import *


USING_STRUCTURED_DATA 				= True	# Whether to incorporate structured data into the tagging process.
											# If yes, the categories from the structured data will be added directly to the transaction data.

INPUT_APRIORI_DATA_FILE				= 'output/apriori_output.txt'
INPUT_CATEGORIES_FILE  				= 'input/categories.yml'
INPUT_CATEGORIES_FILE  				= 'input/categories.yml'
INPUT_TRANS_DATA_FILE				= 'output/transaction_data.csv'



OUTPUT_ARM_BARCHART_DATA_FILE  		= 'output/association_rule_mining_bar_chart_data.json'
OUTPUT_ARM_DATA_FILE				= 'output/association_rule_mining_data.js'
OUTPUT_ARM_ENTITY_APPEARANCES_FILE	= 'output/association_rule_mining_entity_appearances.js'



def process_apriori_output(f, category_hierarchy, superparent_ids, parent_lookup_dict, category_dict):
	lines = f.readlines()

	print("Number of lines in apriori output: ", len(lines))
	print("--------")

	# Get the line where the rules start
	rules_start = lines.index("------------------------ RULES:\n")
	#print rules_start

	entity_appearances = defaultdict(list)
	line_index = 1


	# Generate the data for the hierarchical bar chart on the assocation rule mining page
	# (same as the function for preliminary_tagging. Would be good to combine them into one function and call it here instead.)
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






	def clean_string(str):
		return str.replace(")", "").replace("(", "").replace(",", " ").replace("'", "").split()

	# Tags the data with the appropriate span tags.
	def tag_data(data_list):
		#data_list = data.replace(")", "").replace("(", "").replace(",", " ").replace("'", "").split()#.split("', '")
		tagged_line = ""
		tagged_line_list = []		
		for tag in data_list:
			superparent = get_superparent_of_category(tag, category_hierarchy)
			superparent_id = superparent_ids[superparent]
			span_tag = "<span data-tagname=\"" + superparent + ": " + tag + "\" class=\"tag category-" + str(superparent_id) + "\">" + tag + "</span>"
			tagged_line_list.append(span_tag)


			entity_appearances[tag].append(line_index)
	
			for t in parent_lookup_dict[tag]:
				entity_appearances[t].append(line_index)

		tagged_line = ", ".join(tagged_line_list)
		return tagged_line
		

	# Returns the unconditional probabilities of every tag
	# (i.e. the number of times the tag appears in a transaction, divided by the number of transactions)
	def get_unconditional_probabilities():
		unconditional_probabilities = defaultdict(int)
		with open(INPUT_TRANS_DATA_FILE, "r") as f2:
			lines = f2.readlines()
			nlines = len(lines)
			for line in lines:
				tags = set(line.replace("\n", "").split(","))
				for tag in tags:
					unconditional_probabilities[tag] += 1
		for tag in unconditional_probabilities:
			unconditional_probabilities[tag] = unconditional_probabilities[tag] * 1.0 / nlines 
			#print(unconditional_probabilities[tag])

	#unconditional_probabilities = get_unconditional_probabilities()

	# Returns the lift of the tag
	def get_lift(tag):
		return 0

	def get_unconditional_probability(consequent):
		unconditional_probability = 0.0
		with open(INPUT_TRANS_DATA_FILE, "r") as f2:
			lines = [set(line.replace("\n", "").split(",")) for line in f2.readlines()]		
		consequent = set(consequent)
		count = 0
		for line in lines:
			if consequent.issubset(line):
				count += 1
		unconditional_probability = count * 1.0 / len(lines)
		return unconditional_probability



	# Process the rules
	arm_data = []
	for line in lines[rules_start + 1:]:
		arm_data.append([0, "", "", 0, 0])
		arm_data[-1][0] = line_index

		antecedent 		= clean_string(re.search('%s(.*)%s' % ('Rule: (', ') ==>'), line).group(1))	
		arm_data[-1][1] = tag_data(antecedent)

		consequent 		= clean_string(re.search('%s(.*)%s' % ('==> (', ',)'), line).group(1))
		arm_data[-1][2] = tag_data(consequent)

		#print antecedent, consequent



		# Slow way of determining unconditional probability because I'm running out of time.

		


		confidence = float(line[-6:-1])

		unconditional_probability = get_unconditional_probability(consequent)

		lift = confidence / unconditional_probability


		arm_data[-1][3] = lift
		arm_data[-1][4] = confidence

		line_index += 1
		#print(line_index, end="")



	arm_data.sort(reverse = True, key = lambda x: x[3])	# Sort by lift
	# Format the floats (after sorting)
	for a in arm_data:
		a[3] = "%.3f" % a[3]
		a[4] = "%.3f" % a[4]
	



	write_to_file(arm_data, OUTPUT_ARM_DATA_FILE, indent = 1, export = True, variable_name = "armData")
	write_to_file(entity_appearances, OUTPUT_ARM_ENTITY_APPEARANCES_FILE, indent = 0, export = False, variable_name = "entityAppearances")

	# Also generate the bar chart data (to go on the hierarchical bar chart under /association_rule_mining)
	# Turn the chart data into entity_counts rather than entity_appearances first
	entity_counts = {}
	for k in category_hierarchy:
		entity_counts[k] = 0
	#print entity_counts
	#print "------//"
	for k in entity_appearances:
		entity_counts[k] = len(entity_appearances[k])
	#print entity_counts

	#print "------"

	bar_chart_data 		= get_chart_data(category_hierarchy, entity_counts, category_dict)

	write_to_file(bar_chart_data, OUTPUT_ARM_BARCHART_DATA_FILE, indent = 1, export = False)




def copy_files():
	# Copy the file into the public folder
	copyfile(OUTPUT_ARM_DATA_FILE, '../nlp/data/reports/association_rule_mining_data.js')
	copyfile(OUTPUT_ARM_ENTITY_APPEARANCES_FILE, '../public/javascripts/data_warehousing/association_rule_mining_entity_appearances.js')
	copyfile(OUTPUT_ARM_BARCHART_DATA_FILE, '../public/javascripts/data_warehousing/association_rule_mining_bar_chart_data.json')


def main():
	with open(INPUT_CATEGORIES_FILE, 'r') as f:
		categories = ordered_load(f, yaml.SafeLoader)

	category_hierarchy 	= get_category_hierarchy(categories)
	superparent_ids 	= get_superparent_ids(category_hierarchy)
	parent_lookup_dict 	= get_parent_lookup_dict(category_hierarchy)


	with open(INPUT_APRIORI_DATA_FILE, 'r') as f:
		arm_data = process_apriori_output(f, category_hierarchy, superparent_ids, parent_lookup_dict, categories)

	copy_files()

if __name__ == "__main__":
    main()
