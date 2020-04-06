import codecs
from utils import *

# Take the csv file and convert it to JSON (for the timeline)
def build_timeline():
	csvfile = codecs.open(DATA_FOLDER + DATA_FILENAME + ".csv", 'r', 'utf-8')
	reader = csv.DictReader( csvfile )
	data = []
	for entry in reader:
		data.append(entry)
	print(len(data))
	write_to_file(data, 'data/timeline_chart_data.js', indent = 1, export = True, variable_name = 'data')