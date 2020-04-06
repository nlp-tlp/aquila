from utils import *
import codecs

def create_wordcloud(data):
	print(DASH_LINE)
	print("GENERATING WORDCLOUD DATA")
	print(DASH_LINE)
	def generate_wordcloud(data, words_or_phrases):

		MAX_TOKENS = 200	# Minimum number of words appearing in the word cloud


		wordcloud_data = [None] * (len(data) + 1)

		# Discover all words

		words_discovered = []
		paragraphs_cumulative = []
		counts_cumulative = []
		counter = 0

		print("Generating Wordcloud data for", words_or_phrases + "... ")

		for d in data:
			entry_description = d['Description']
			if words_or_phrases == "Words":
				sentences = sent_tokenize(entry_description)
			elif words_or_phrases == "Noun Phrases":
				sentences = d["Noun Phrases"]
			elif words_or_phrases == "Relation Phrases":
				sentences = d["Relation Phrases"]				

			paragraphs_cumulative.append([])
			
			if counter > 0:
				for word in paragraphs_cumulative[counter - 1]:
					paragraphs_cumulative[counter].append(word)

			for sentence in sentences:
				if words_or_phrases == "Words":
					word_tokens = word_tokenize(sentence)
					filtered_sentence = [w for w in word_tokens if w not in stop_words]
					for word_or_phrase in filtered_sentence:
						paragraphs_cumulative[counter].append(word_or_phrase)
				elif words_or_phrases == "Noun Phrases" or words_or_phrases == "Relation Phrases":
					paragraphs_cumulative[counter].append(sentence)


			#print paragraphs_cumulative
			cc = Counter(paragraphs_cumulative[counter])
			counts_cumulative.append(cc)

			counter += 1
			sys.stdout.write('.')

		counts = Counter(paragraphs_cumulative[len(data) - 1]).most_common(MAX_TOKENS)
		
		wordcloud_data = []

		counter = 0
		for c in counts:
			wordcloud_data.append({})
			wordcloud_data[counter][words_or_phrases[:-1]] = c[0]
			wordcloud_data[counter]["freqs"] = []
			counter += 1

		#print "\nCounting most common", words_or_phrases[:-1], "s"
		for w in wordcloud_data:
			for x in range(len(data)):
				if w[words_or_phrases[:-1]] in counts_cumulative[x]:
					w["freqs"].append(counts_cumulative[x][w[words_or_phrases[:-1]]])
				else:
					w["freqs"].append(0)
			sys.stdout.write('.')

		print("... done.\n")
		return wordcloud_data

	def write_wordcloud(wordcloud_data, filename, var):
		with codecs.open(filename, 'w') as wc_output_file:
			wc_output_file.write(var + " = ")			
			json.dump(wordcloud_data, wc_output_file)	

	# Words
	w_wordcloud_data = generate_wordcloud(data, "Words")
	write_wordcloud(w_wordcloud_data, '../public/javascripts/wordcloud_data/wordcloud_words.js', "wcData")

	# Noun phrases
	n_wordcloud_data = generate_wordcloud(data, "Noun Phrases")
	write_wordcloud(n_wordcloud_data, '../public/javascripts/wordcloud_data/wordcloud_noun_phrases.js', "npcData")

	# Relation phrases
	r_wordcloud_data = generate_wordcloud(data, "Relation Phrases")
	write_wordcloud(r_wordcloud_data, '../public/javascripts/wordcloud_data/wordcloud_relation_phrases.js', "rpcData")


