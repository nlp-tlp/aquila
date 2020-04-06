from utils_dw import *
import preliminary_tagging, d3_graph_generation, process_apriori_output
import codecs, csv
from efficient_apriori import apriori


USING_STRUCTURED_DATA 				= True	# Whether to incorporate structured data into the tagging process.
											# If yes, the categories from the structured data will be added directly to the transaction data.


INPUT_CSV_FILE 						= '../nlp/data/sample_data.csv'	# Change to the name of your csv file

INPUT_DATA_FILE	 					= 'input/raw_data_clean.txt'
INPUT_STRUCTURED_DATA_FILE	 		= 'input/structured_data.csv'
INPUT_CATEGORIES_FILE  				= 'input/categories.yml'
OUTPUT_PRELIM_TAG_FILE 	 			= 'output/prelim_tagging.js'
OUTPUT_JSTREE_FILE  				= 'output/categories_jstree.js'
OUTPUT_ENTITY_APPEARANCES_FILE  	= 'output/entity_appearances.js'
OUTPUT_BARCHART_DATA_FILE  			= 'output/bar_chart_data.json'
OUTPUT_TRANS_DATA_FILE				= 'output/transaction_data.csv'

ADD_PARENTS_TO_TRANSACTION_DATA		= False 	# Whether to add all parents of each category to the transaction data, as well as the categories themself

DO_NOT_TAG_CATEGORIES				= ["location", "severity", "minor", "serious", "fatal", "male", "female", "gender"]	 # Categories not to tag via dictionary lookup

#TEXT_FIELD_NAME = "Briefdescriptionofevent" # 
TEXT_FIELD_NAME = "Detailed Description" # Change to the textual field name, e.g. Briefdescriptionofevent

#STRUCTURED_FIELDS = ["FinalRiskConsequence"] 	# A list of the structured fields to extract rules for
STRUCTURED_FIELDS = ["Age at Accident", "Severity", "Gender"] 	# A list of the structured fields to extract rules for


'''
  age_15_24:
  age_25_34:
  age_35_44:
  age_45_54:
  age_55_64:
  age_65_100:
'''

def extract_structured_fields():
	csvfile = codecs.open(INPUT_CSV_FILE, 'r', 'utf-8')
	reader = csv.DictReader( csvfile )
	data = []
	for entry in reader:
		data.append([])
		for col, val in entry.items():
			if col in STRUCTURED_FIELDS:

				if col == "Age at Accident":
					val = int(val)
					# Age at accident is treated differently - it's discretised
					if val >= 15 and val <= 24:
						l, h = 15, 24
					elif val >= 25 and val <= 34:
						l, h = 25, 34
					elif val >= 35 and val <= 44:
						l, h = 35, 44
					elif val >= 45 and val <= 54:
						l, h = 45, 54
					elif val >= 55 and val <= 64:
						l, h = 55, 64
					elif val >= 65:
						l, h = 65, 100

					data[-1].append("age_%d_%d" % (l, h))

				else:
					data[-1].append(val.replace(" ", "_").lower())	

	with codecs.open(INPUT_STRUCTURED_DATA_FILE, 'w', 'utf-8') as f:
		for i, row in enumerate(data):
			if i > 0:
				f.write("\n")
			f.write(",".join(row))
			

def run_arm():

	records = []
	with codecs.open(OUTPUT_TRANS_DATA_FILE, 'r', 'utf-8') as f:
		for line in f:
			records.append(line.strip().split(','))

	itemsets, rules = apriori(records, min_support=0.01, min_confidence=0.6)


	with codecs.open('output/apriori_output.txt', 'w', 'utf-8') as f:
		f.write('------------------------ RULES:\n')
		for rule in rules:
			f.write('Rule: %s ==> %s , %.3f' % (str(rule.lhs), str(rule.rhs), rule.confidence))
			f.write('\n')


def main():

	extract_structured_fields()

	preliminary_tagging.main()

	d3_graph_generation.main()

	run_arm()
	
	process_apriori_output.main()
	


if __name__ == "__main__":
	main()
