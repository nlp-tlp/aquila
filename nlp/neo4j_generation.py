from utils import *
import os

NEO4J_IMPORT_PATH = "/usr/share/neo4j/import"

# Process all of the noun_relation_phrases and create a csv file to import into Neo4J
def generate_neo4j_input(noun_relation_phrases):

	print(DASH_LINE)
	print("GENERATING NEO4J DATA")
	print(DASH_LINE)

	# 1. For each noun and relation phrase, generate a dictionary that maps the phrase to its id in the table

	np_id_table = {}	# Dictionary. np maps to id, i.e. "man" -> 2
	rp_id_table = {}
	for row in noun_relation_phrases:
		nps = (row[0], row[2])
		rp = row[1].replace(" ", "_") # Convert spaces to underscores to be considered valid Neo4J edges
		for np in nps:
			if np not in np_id_table:
				np_id_table[np] = len(np_id_table) + 1
		if rp not in rp_id_table:
			rp_id_table[rp] = len(rp_id_table) + 1

	# 2. Iterate through noun_relation_phrases again, substituting
	#    phrases for their ids in the id tables and placing them into a new list of tuples.
	#	 noun_phrase -> relation_phrase -> noun_phrase
	# 	 i.e. subject -> verb -> object 

	np_to_rp_to_np = []
	#NP_to_RP = []
	#RP_to_NP = []

	for row in noun_relation_phrases:
		#np_rp = row[0:2]
		#rp_np = row[1:3]
		#NP_to_RP.append((np_id_table[row[0]], rp_id_table[row[1]]))
		#RP_to_NP.append((rp_id_table[row[1]], np_id_table[row[2]]))

		# id -> relation phrase -> id
		np_to_rp_to_np.append((np_id_table[row[0]], row[1].replace(" ", "_"), np_id_table[row[2]]))

	# 3. Convert NP -> id and RP -> id dictionary to tuples for output, and sort them

	np_id_table_out = []
	rp_id_table_out = []

	for k in sorted(np_id_table, key = np_id_table.get):
		np_id_table_out.append((np_id_table[k], k))				

	for k in sorted(rp_id_table, key = rp_id_table.get):
		rp_id_table_out.append((rp_id_table[k], k))


	# 4. Output the four tables to csv 

	def write_neo4j_table(filename, data_source, column_headings):
		with open(filename, 'wb') as csv_file:
			csv_out = csv.writer(csv_file)
			csv_out.writerow(column_headings)
			for row in data_source:
				csv_out.writerow(row)

	write_neo4j_table("%s/neo4j_np_ids.csv" 		% NEO4J_IMPORT_PATH, np_id_table_out, ['id', 'Phrase'])
	write_neo4j_table("%s/neo4j_rp_ids.csv" 		% NEO4J_IMPORT_PATH, rp_id_table_out, ['id', 'Phrase'])
	write_neo4j_table("%s/neo4j_np_to_rp_to_np.csv" % NEO4J_IMPORT_PATH, np_to_rp_to_np,  ['nounphrase_subject_Id', 'relationphraseId', 'nounphrase_object_Id'])

	# Write the input string to a file as well, so it's easier to import the data

	def get_input_commands_list(np_to_rp_to_np):
		icl = []
		icl.append('LOAD CSV WITH HEADERS FROM "file:///neo4j_np_ids.csv" AS csvLine')
		icl.append('CREATE (n:NounPhrase { id: toInt(csvLine.id), phrase: csvLine.Phrase});')
		icl.append('')
		icl.append("CREATE INDEX ON :NounPhrase(phrase)")
		icl.append('CREATE CONSTRAINT ON (n:NounPhrase) ASSERT n.id IS UNIQUE;')
		icl.append('')
		icl.append('USING PERIODIC COMMIT 10000')
		#icl.append('LOAD CSV WITH HEADERS FROM "file:///neo4j_np_to_rp_to_np.csv" AS csvLine')
		#icl.append('MATCH (n:NounPhrase { id: toInt(csvLine.nounphraseId)}),(r:RelationPhrase { id: toInt(csvLine.relationphraseId)})')
		for row in np_to_rp_to_np:
			icl.append('MATCH(n: NounPhrase { id: %d }), (n2: NounPhrase { id: %d  })' % (row[0], row[2]))
			icl.append('CREATE (n)-[:%s]->(n2);' % row[1])
			icl.append('')

		return icl

	def write_input_commands(np_to_rp_to_np):
		input_commands_list = get_input_commands_list(np_to_rp_to_np)
		with open('%s/import_commands.cypher' % NEO4J_IMPORT_PATH, 'wb') as input_commands_file:
			for line in input_commands_list:
				input_commands_file.write(line + "\r\n")

	write_input_commands(np_to_rp_to_np)

	print("... done.\n")
