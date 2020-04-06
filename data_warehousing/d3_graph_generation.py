from shutil import copyfile, rmtree
#from collections import OrderedDict
import os, errno, re, sys, yaml, json
from collections import OrderedDict, defaultdict

sys.path.append('../nlp')
from utils import write_to_file

from utils_dw import *

from itertools import product

import math

import csv, copy

INPUT_TRANS_DATA_FILE				= 'output/transaction_data.csv'
OUTPUT_NODES_FILE					= 'output/d3_graph_data_nodes.js'
OUTPUT_LINKS_FILE					= 'output/d3_graph_data_links.js'
OUTPUT_INTER_CLASS_LINKS_FILE		= 'output/d3_graph_data_inter_class_links.js'
INPUT_CATEGORIES_FILE  				= 'input/categories.yml'


def process_entities(f, category_hierarchy):
	entities_dict = {}

	parent_lookup_dict = get_parent_lookup_dict(category_hierarchy)

	# Use the index of categories as they appear in the categories file to resolve the edge direction.
	with open(INPUT_CATEGORIES_FILE, "r") as f2:
		flat_categories = [l.replace(":", "").replace("\n", "").replace(" ", "") for l in f2.readlines()]
	

	#print parent_lookup_dict

	# Look up all categories, in case some are missing in the transaction data (age_group, for example)
	for category in category_hierarchy:
		sp = get_superparent_of_category(category, category_hierarchy)
		#print entity, sp
		if sp not in entities_dict:
			entities_dict[sp] = {}
		if category not in entities_dict[sp]:
			entities_dict[sp][category] = defaultdict(int)		



	links = defaultdict(dict)
	node_counts = defaultdict(int)


	def form_links(this_entity, other_entities):


		#print this_entity, other_entities


		def update_counts(this_entity, other_entity):
			if this_entity != other_entity:
				se = sorted([this_entity, other_entity])
				if se[1] in links[se[0]]:
					links[se[0]][se[1]] += 1
				else:
					links[se[0]][se[1]] = 1
				node_counts[se[0]] += 1
				node_counts[se[1]] += 1	
				entities_dict[sp][entity][other_entity] += 1

		#if this_entity == "age_15_24":
		#	print this_entity, other_entities

		sp = get_superparent_of_category(this_entity, category_hierarchy)

		for other_entity in other_entities:
			#if this_entity == "age_15_24":
			#	print this_entity, other_entity


			update_counts(this_entity, other_entity)
			for other_entity_parent in parent_lookup_dict[other_entity]:
				update_counts(this_entity, other_entity_parent)

		for this_entity_parent in parent_lookup_dict[this_entity]:
			form_links(this_entity_parent, other_entities)	# Form links between this entity's parent and all the other links


	line_index = -1
	for line in f:
		line_index += 1
		entities = line.replace("\n", "").split(",")


		#print entities
		#entities = sorted(entities, key = flat_categories.index, reverse=True)
		#print entities


		#sorted(line.replace("\n", "").split(","))
		i = 0
		for entity in entities:

			#print line_index, entity, entities[i + 1:]


			#print "---" + str(line_index)
			form_links(entity, entities[i + 1:])
			#print "---"

			i += 1

		
					#i2 += 1
		

		#first_entity = entities[0]	# Only need to map the first entity to the other entities	
		#other_entities = entities[1:]
		#entities_dict[first_entity].append(other_entities)

	#print entities_dict
	#return entities_dict
	#print(links["female"]["injury"])
	#print(links["injury"]["male"])
	#print(links["gender"]["injury"])

	#print node_counts["gender"]
	#print " --- "

	return [links, node_counts]

def generate_d3_graph_input(links, node_counts, category_hierarchy):



	#coords = ((400, 200), (400, 200), (800, 200), (1200, 200), (1600, 200), (400, 700), (800, 700), (1200, 700), (1600, 700), (1920/2, 950/2), (600, 600))


	nodes = []

	sp_ids = get_superparent_ids(category_hierarchy)


	node_ids = {}
	

	index = 0

	node_sizes_set = []
	total_links_max = 0

	# Get the total links of a node
	"""def get_total_links(node, total_links_max):
		total_links = 0
		for l in links:
			if l[0] or l[1] == node:
				total_links += 1
		if total_links > total_links_max:
			total_links_max = total_links
		node_sizes_set.append(total_links)

		return total_links"""





	# Create all the nodes
	#for c in category_hierarchy:
#
#		node_ids[c] = index		
#		sp_id = sp_ids[get_superparent_of_category(c, category_hierarchy)]	# Superparent ID of the node
#
#		node_sizes_set.append(node_sizes[c])
#
#		index += 1


	for c in node_counts:
		node_sizes_set.append(node_counts[c])

	node_sizes_set = sorted(node_sizes_set)
	node_sizes_set_total = len(node_sizes_set)
	total_links = 0

	# Get the size of the node
	def get_node_size(total_links):
		i = node_sizes_set.index(total_links) * 1.0
		ii = i / node_sizes_set_total * 20 ** (1 + (i / node_sizes_set_total)/4)	# 
		size = 10 + ii 
		return size

	# Create the nodes
	index = 0
	for c in node_counts:
		node_ids[c] = index	
		node_size = node_counts[c]
		sp_id = sp_ids[get_superparent_of_category(c, category_hierarchy)]
		if node_size > 0:
			nodes.append({  "sp_id": sp_id,  "name": c, "size": get_node_size(node_size) })
		index += 1

	

	#print links

	# Calculate link sizes set
	link_sizes_set_unsorted = []
	link_sizes_set_unsorted_nonunique = []
	
	"""for entity_1 in links:
		for entity_2 in links[entity_1]:
			print entity_1, entity_2
			count1 = links[entity_1][entity_2]
			#print "count1 %s" % count1
			if entity_1 in links[entity_2]:
				count2 = links[entity_2][entity_1]
			#	print count2
			else:
				count2 = 0
			link_value = count1 + count2
			if link_value not in link_sizes_set_unsorted:		
				link_sizes_set_unsorted.append(link_value)"""

	for e1 in links:
		for e2 in links[e1]:
			#print links[e1][e2]
			if links[e1][e2] not in link_sizes_set_unsorted:
				link_sizes_set_unsorted.append(links[e1][e2])
			link_sizes_set_unsorted_nonunique.append(links[e1][e2])




	link_sizes_set = sorted(link_sizes_set_unsorted)
	#print link_sizes_set
	link_sizes_set_total = len(link_sizes_set)





	def get_link_width(link_value):
		i = link_sizes_set.index(link_value) * 1.0
		ii = (i / link_sizes_set_total) * 10	# 
		width = ii + 0.2
		return width

	ii = 0
	output_links = []
	for entity_1 in links:
		for entity_2 in links[entity_1]:
			#count1 = links[entity_1][entity_2]
			#if entity_1 in links[entity_2]:
			#	count2 = links[entity_2][entity_1]
			#else:
			#	count2 = 0
			#link_value = count1 + count2
			link_value = link_sizes_set_unsorted_nonunique[ii]

			output_links.append({ "source": node_ids[entity_1], "target": node_ids[entity_2], "value": link_value, "strokeWidth": get_link_width(link_value) })
			ii += 1





	inter_class_links = []

	for category in category_hierarchy:		
		sp_id = sp_ids[get_superparent_of_category(category, category_hierarchy)]
		if category in node_ids and category_hierarchy[category] in node_ids:
			inter_class_links.append( {"source": node_ids[category], "target": node_ids[category_hierarchy[category]], "sp_id": sp_id})






	# Create the links
	"""for l in links:
		l_s = sorted(l)	# Sort in alphabetical order, so the edge always draws the same way

	links_aggregated = defaultdict(int)

	print len(links)

	count = 0
	for l in links:

		#node_1 = l[0]
		#node_2 = l[1]
		for l2 in links:
			if l[0] == l2[0] and l[1] == l2[1]:
				links_aggregated[(l[0], l[1])] += 1

	for l in links_aggregated:
		print l

	"""


	"""
	# Figure out the max number of links

	maxsize_nodes = 0
	maxsize_links = 0
	for key in entities_dict:
		for key2 in entities_dict[key]:
			for v in entities_dict[key][key2]:
				total_links = sum(entities_dict[key][key2][v] for v in entities_dict[key][key2])
				if total_links > maxsize_nodes:
					maxsize_nodes = total_links
				if entities_dict[key][key2][v] > maxsize_links:
					maxsize_links = entities_dict[key][key2][v]

	print maxsize_nodes
	print maxsize_links


	# Generate node sizes
	node_sizes_set = []
	for key in entities_dict:
		for key2 in entities_dict[key]:
			total_links = sum(entities_dict[key][key2][v] for v in entities_dict[key][key2])
			if total_links not in node_sizes_set:
				node_sizes_set.append(total_links)
	node_sizes_set = sorted(node_sizes_set)
	node_sizes_set_total = len(node_sizes_set)
	total_links = 0
	"""



	"""
	# Generate nodes
	node_ids = {}
	index = 0
	#print entities_dict
	for key in entities_dict:
		#print key 
		sp_id = sp_ids[key]
		for key2 in entities_dict[key]:

			total_links = sum(entities_dict[key][key2][v] for v in entities_dict[key][key2])
			#print "    " + key2 + " (" + str(total_links) + ")"
			x = 0
			y = 0
			# , 
			if total_links > 0:
			
				nodes.append({  "sp_id": sp_id,  "name": key2, "size": get_node_size(total_links) })
				node_ids[key2] = index
				index += 1

	"""
		# Add missing keys
	"""for category in category_hierarchy:
		if category not in appearing_categories:

			sp_id = sp_ids[get_superparent_of_category(category, category_hierarchy)]
			nodes.append({  "sp_id": sp_id,  "name": category, "size": 0 })
			node_ids[category] = index
			index += 1"""



	"""
	# Generate links sizes
	link_sizes_set = []

	for sp in entities_dict:
		for entity_1 in entities_dict[sp]:
			for entity_2 in entities_dict[sp][entity_1]:
				link_size = entities_dict[sp][entity_1][entity_2]
				if link_size not in link_sizes_set:
					link_sizes_set.append(link_size)

	link_sizes_set = sorted(link_sizes_set)
	link_sizes_set_total = len(link_sizes_set)

	# Get the width of the link
	def get_link_width(total_links):
		i = link_sizes_set.index(total_links) * 1.0
		ii = i / link_sizes_set_total * 10 ** (1 + (i / link_sizes_set_total/5)/5)	# 
		width = ii + 1
		return width

	
	# Generate links
	links = []



	for sp in entities_dict:
		for entity_1 in entities_dict[sp]:
			for entity_2 in entities_dict[sp][entity_1]:
				sp_1 = sp
				sp_2 = get_superparent_of_category(entity_2, category_hierarchy)
				# [ sp_1 entity_1_id sp_2 entity_2_id, weight  ]

				#print node_ids[entity_2]
				#print entities_dict[sp][entity_1][entity_2]
				#print 
				tl1 = sum(entities_dict[sp_1][entity_1][v] for v in entities_dict[sp_1][entity_1])
				tl2 = sum(entities_dict[sp_2][entity_2][v] for v in entities_dict[sp_2][entity_2])

				if tl1 > 0 and tl2 > 0:
					links.append({ "source": node_ids[entity_1], "target": node_ids[entity_2], "value": entities_dict[sp][entity_1][entity_2], "strokeWidth": get_link_width(entities_dict[sp][entity_1][entity_2]), "strokeAlpha": max(0.15, math.floor((entities_dict[sp][entity_1][entity_2] * 1.4 / maxsize_links))) })


	# Generate links between classes ?

	# code ...

	"""
	# Write the nodes and links to files
	write_to_file(nodes, OUTPUT_NODES_FILE, indent = 0, export = False, variable_name = "nodes")
	write_to_file(output_links, OUTPUT_LINKS_FILE, indent = 0, export = False, variable_name = "links")
	write_to_file(inter_class_links, OUTPUT_INTER_CLASS_LINKS_FILE, indent = 0, export = False, variable_name = "interClassLinks")
	


def copy_files():
	copyfile(OUTPUT_NODES_FILE, '../public/javascripts/data_warehousing/d3_graph_data_nodes.js')
	copyfile(OUTPUT_LINKS_FILE, '../public/javascripts/data_warehousing/d3_graph_data_links.js')
	copyfile(OUTPUT_INTER_CLASS_LINKS_FILE, '../public/javascripts/data_warehousing/d3_graph_data_inter_class_links.js')



def main():
	#
	with open(INPUT_CATEGORIES_FILE, 'r') as f:
		categories = ordered_load(f, yaml.SafeLoader)
	category_hierarchy 	= get_category_hierarchy(categories)


	with open(INPUT_TRANS_DATA_FILE, 'r') as f:
		[links, node_counts] = process_entities(f, category_hierarchy)



	print("Generating D3 Graph data...")
	generate_d3_graph_input(links, node_counts, category_hierarchy)
	print("... done.")
	copy_files()
	



if __name__ == "__main__":
    main()
