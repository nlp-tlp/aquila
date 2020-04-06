import json

def fix_data(f):
	data = json.loads(f.read())
	data2 = []
	for entry in data:
		data2.append({})
		data2[-1]["Word"] = entry["Word"]
		data2[-1]["Freq"] = entry["freqs"][-1]

	with  open("wordcloud_words_flat.js", "w") as f2:
		f2.write("wcData = ")
		json.dump(data2, f2, indent=1)



with open("wordcloud_words.js", "r") as f:
	fix_data(f)