from utils import *

def preprocess_data(data):
	count = 0

	noun_relation_phrases = [] # For use in Neo4J. No need to save them to each entry

	print(DASH_LINE)
	print("PREPROCESSING DATA")
	print(DASH_LINE)

	for entry in data:
		entry_description = entry["Description"];
		sentences = sent_tokenize(entry_description)

		filtered_sentences 			= []
		#pos_tagged_sentences 		= []
		#named_entity_sentences 	= []

		noun_phrases 				= []
		relation_phrases 			= []
		

		# Scan each sentence within each entry
		for sentence in sentences:
			processed_sentence = nltk.word_tokenize(sentence)

			# Apply part-of-speech tagging
			tagged_sentence = nltk.pos_tag(processed_sentence)

			grammar = 	r"""
							NP: 
								{<DT>?<JJ>*<NN>+}	
								{<NNP>+}

						"""
			# Apply noun-phrase chunking
			chunk_parser = nltk.RegexpParser(grammar)
			result = chunk_parser.parse(tagged_sentence)

			# Determine the subject, object and relation phrases within each sentence
			subject_phrase 			= []
			relation_phrase 		= []
			object_phrase			= []			

			# Process a list of words and return a lemmatized, stopword-removed list (if toggled on).
			def process_words(words):
				phrase = []
				for word in words:
					if using_lemmatization:
						word = lmtzr.lemmatize(word)
					if using_stopwords:
						if word in stop_words:
							word = None
					if word:
						phrase.append(word)

				return phrase

			for chunk in result:
				phrase_type = str(chunk)[1:3]

				# Noun phrases appear as trees in the result
				if chunk.__class__.__name__ == "Tree" and phrase_type == "NP":
					# Get the entire phrase in the chunk. process_words applies lemmatization and stop words if toggled on.
					phrase = process_words([w[0] for w in chunk])
					if phrase:
						noun_phrases.append(" ".join(phrase))
						# If the current subject phrase does exist (i.e. this is the object of a sentence),
						# set the object_phrase to this one	and reset the subject_phrase to this one
						if subject_phrase:
							object_phrase = phrase	
							# Ensure that the relation phrase isn't an empty list before adding the subject, relation, and object phrases to the
							# noun_relation_phrase list
							if relation_phrase:
								noun_relation_phrases.append((" ".join(subject_phrase), " ".join(relation_phrase), " ".join(object_phrase)))
							subject_phrase = object_phrase 
						# If the current subject phrase does not exist (i.e. this is the subject of a sentence),
						# set the current noun phrase to this phrase
						else:
							subject_phrase = phrase
						# Write all words from the relation phrase to the relation_phrases list and reset the relation phrase variable
						#for w in relation_phrase:
						if relation_phrase:
							relation_phrases.append(" ".join([w for w in relation_phrase]))
						relation_phrase = []
				else:
					# If there is a current subject phrase, append this word to the relation_phrase.
					if subject_phrase:
						if using_lemmatization:
							word = lmtzr.lemmatize(chunk[0])
						else:
							word = chunk[0]
						if using_stopwords:
							if word not in stop_words:
								relation_phrase.append(word)
						else:
							relation_phrase.append(word)


		# Save the noun and relation phrases to the entry
		# (for visualisation later in the word cloud)
		entry["Noun Phrases"] 		= noun_phrases
		entry["Relation Phrases"] 	= relation_phrases

		count += 1
		sys.stdout.write('.')
		if count % 50 == 0:
			sys.stdout.write (' ' + str(count) + '/' + str(len(data)) + "\n")
		#print "Finished parsing entry", count, "of", str(len(data)) + "."



	print("... done.\n")
	preprocessed_data = { "Data": data, "Noun Relation Phrases": noun_relation_phrases }
	write_to_file(data, DATA_FOLDER + DATA_FILENAME + '_preprocessed.json')
	return preprocessed_data
