import nltk
from nltk.tokenize  	import sent_tokenize, word_tokenize
from nltk.corpus 		import stopwords
from nltk.stem.wordnet 	import WordNetLemmatizer
import json, csv
from collections import Counter
import sys, time, random, csv, re, codecs


# Global variables
stop_words = set(stopwords.words('english'))
stop_words.update('.', ',', '[', ']', '(', ')', '&') # Remove punctuation

lmtzr = WordNetLemmatizer()

using_stopwords	= True
using_lemmatization = True

DATA_FOLDER 	= "data/"
DATA_FILENAME 	= "sample_data"
DATA_ENTRIES 	= None 		# Set to None to use all entries
#DESCRIPTION_FIELDNAME = "Briefdescriptionofevent"
DESCRIPTION_FIELDNAME = "Detailed Description"
CONVERT_TO_JSON = True



DASH_LINE = "====================================================================================="

# Read in the original csv data, and convert it to a JSON file (for easier reading). Return the data
# in the form of a list of descriptions.
def read_in_data():
	if(CONVERT_TO_JSON):
		print("Converting csv to json...", end="")
		csvfile = codecs.open(DATA_FOLDER + DATA_FILENAME + ".csv", 'r', 'utf-8')
		jsonfile = codecs.open(DATA_FOLDER + DATA_FILENAME + ("_" + str(DATA_ENTRIES) if DATA_ENTRIES else "") + ".json", 'w', 'utf-8')

		reader = csv.DictReader( csvfile )
		data = []
		i = 0;
		for entry in reader:
			data.append({})
			data[-1]["Description"] = entry[DESCRIPTION_FIELDNAME]
			i += 1
			if(i == DATA_ENTRIES):
				break
		json.dump(data, jsonfile, indent = 1)
		csvfile.close()
		jsonfile.close()
		print(" done.\n")

	with codecs.open(DATA_FOLDER + DATA_FILENAME + ("_" + str(DATA_ENTRIES) if DATA_ENTRIES else "") + ".json", 'r', 'utf-8') as data_file:
		data = json.load(data_file)		

	return data

# Read in the cleaned data.
def read_in_cleaned_data():
	with codecs.open(DATA_FOLDER + DATA_FILENAME + '_cleaned.json', 'utf-8') as data_file:
		data = json.load(data_file)
	return data

# Read in the preprocessed data.
def read_in_preprocessed_data():
	with codecs.open(DATA_FOLDER + DATA_FILENAME + '_preprocessed.json', 'utf-8') as data_file:
		data = json.load(data_file)
	return data

# Write objects to a file, for use by the Node app.
def write_to_file(data, filename, indent = 0, export = False, variable_name = None):
	with codecs.open(filename, 'w', 'utf-8') as data_output_file:
		if export:
			data_output_file.write("module.exports = {  data: function() { return ")
		elif variable_name:
			data_output_file.write(variable_name + " = ")
		if indent > 0:
			json.dump(data, data_output_file, indent = indent)
		else:
			json.dump(data, data_output_file)
		if export:
			data_output_file.write("} }")

