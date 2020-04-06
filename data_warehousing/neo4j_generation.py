from shutil import copyfile, rmtree
#from collections import OrderedDict
import os, errno, re, sys, yaml, json
from collections import OrderedDict, defaultdict

sys.path.append('../nlp')
from utils import write_to_file

from utils_dw import *

from itertools import product

import csv

INPUT_TRANS_DATA_FILE				= 'output/transaction_data.csv'
NEO4J_IMPORT_PATH 					= "/usr/share/neo4j/import" #'D:/neo4j_import' #
INPUT_CATEGORIES_FILE  				= 'input/categories.yml'


def process_entities(f, category_hierarchy):
	entities_dict = {}

	for line in f:
		entities = line.replace("\n", "").split(",")
		i = 0
		for entity in entities:
			sp = get_superparent_of_category(entity, category_hierarchy)
			if sp not in entities_dict:
				entities_dict[sp] = {}
			if entity not in entities_dict[sp]:
				entities_dict[sp][entity] = defaultdict(int)
			if i < len(entities) - 1 :
				entities_dict[sp][entity][entities[i + 1]] += 1
			i+= 1

		#first_entity = entities[0]	# Only need to map the first entity to the other entities	
		#other_entities = entities[1:]
		#entities_dict[first_entity].append(other_entities)

	#print entities_dict
	return entities_dict

def generate_neo4j_input(entities_dict, category_hierarchy):

	def write_neo4j_table(filename, data_source, column_headings):
		with open(filename, 'wb') as csv_file:
			csv_out = csv.writer(csv_file)
			csv_out.writerow(column_headings)
			for row in data_source:
				csv_out.writerow(row)



	csv_data = {}
	entity_ids = {}
	for sp in entities_dict:
		e_id = 0
		csv_data[sp] = []
		for entity in entities_dict[sp]:
			e_id += 1
			entity_ids[entity] = e_id
			csv_data[sp].append([e_id, entity])
	#print csv_data



	relation_data = []

	for sp in entities_dict:
		for entity_1 in entities_dict[sp]:
			for entity_2 in entities_dict[sp][entity_1]:
				sp_1 = sp
				sp_2 = get_superparent_of_category(entity_2, category_hierarchy)
				# [ sp_1 entity_1_id sp_2 entity_2_id, weight  ]
				relation_data.append([ sp_1, entity_ids[entity_1], sp_2, entity_ids[entity_2], entities_dict[sp][entity_1][entity_2] ])

	#for r in relation_data:
	#	print r
	#print "-----\n"











	# Generate a separate csv file for each superparent category (injury_type, body_part, etc)
	for sp in csv_data:
		write_neo4j_table("%s/neo4j_entities_" % NEO4J_IMPORT_PATH + sp + ".csv", csv_data[sp], ['id', 'Entity'])




	def get_input_commands_list(csv_data, relation_data):
		icl = []

		for sp in csv_data:
			icl.append('LOAD CSV WITH HEADERS FROM "file:///neo4j_entities_' + sp + '.csv" AS csvLine')
			icl.append('CREATE (n:%s { id: toInt(csvLine.id), entity: csvLine.Entity});' % sp)
			icl.append('')
			icl.append("CREATE INDEX ON :%s(Entity)" % sp)
			icl.append('CREATE CONSTRAINT ON (n:%s) ASSERT n.id IS UNIQUE;' % sp)
			icl.append('')

		icl.append('USING PERIODIC COMMIT 10000')
		#icl.append('LOAD CSV WITH HEADERS FROM "file:///neo4j_np_to_rp_to_np.csv" AS csvLine')
		#icl.append('MATCH (n:NounPhrase { id: toInt(csvLine.nounphraseId)}),(r:RelationPhrase { id: toInt(csvLine.relationphraseId)})')

		for row in relation_data:		
			# Fix this
			icl.append('MATCH(n:%s { id: %d }), (n2:%s { id: %d  })' % (row[0], row[1], row[2], row[3]))
			weight = row[4]
			weight_class = weight / 8
			if weight_class > 8:
				weight_class = 8
			icl.append('CREATE (n)-[:CONNECTED_%d' % (weight_class) + ' { weight: %d }]->(n2);' % row[4])
			icl.append('')

		return icl

	ics = get_input_commands_list(csv_data, relation_data)
	#for ic in ics:
	#	print ic


	with open('%s/import_commands.cypher' % NEO4J_IMPORT_PATH, 'wb') as input_commands_file:
		for line in ics:
			input_commands_file.write(line + "\r\n")


	#print entities_dict



def main():
	#
	with open(INPUT_CATEGORIES_FILE, 'r') as f:
		categories = ordered_load(f, yaml.SafeLoader)
	category_hierarchy 	= get_category_hierarchy(categories)


	with open(INPUT_TRANS_DATA_FILE, 'r') as f:
		entities_dict = process_entities(f, category_hierarchy)




	generate_neo4j_input(entities_dict, category_hierarchy)

	print "Generating Neo4J data..."




if __name__ == "__main__":
    main()
