from utils import *
from collections import OrderedDict
import enchant
from collections import defaultdict
import operator, itertools, math


# The following method was written by metanl as part of the following library:
# https://github.com/commonsense/metanl/blob/master/metanl/token_utils.py
def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .', '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
        "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()


''' Clean the data:
		1. Ensure there are no sentences with full capitalisation.
		2. Convert any acronyms to their full words.
'''
def clean_data(data):

	d = enchant.Dict("en_GB")

	# Checks to see if the word is invalid
	def is_invalid_word(w):
		return (not d.check(w) and not w[0].isupper() and w.isalpha())

	def generate_report_data(report_data, changes_dict, original_description, index):
		# Set the modified description to the original so that the correct report is given.
		# (this avoids the problem of tagging the wrong occurences of an acronym when it is already expanded in the original description).
		modified_description = original_description

		# Add <span> tags to the data to make it easier to visualise in the HTML page.
		for k in changes_dict:					
			original_description 	= original_description.replace(k, "<span class=\"replaced\">" + k + "</span>")
			modified_description 	= modified_description.replace(k, "<span class=\"replaced\">" + changes_dict[k] + "</span>")

		# Report data
		report_data.append({})
		report_data[-1]["Index"] = index 
		report_data[-1]["Original"] = original_description
		report_data[-1]["Modified"] = modified_description 

		return report_data



	print(DASH_LINE)
	print("CLEANING DATA")
	print(DASH_LINE)

	count = 0	

	# 1. Convert fully uppercase sentences to normalised sentences
	#	 For example, "HELLO HOW ARE YOU" becomes "Hello how are you"
	def normalise_capitalisation(data):
		print("Normalising capitalisation...", end="")
		report_data = []
		count = 0
		for entry in data:
			entry_description = entry["Description"]
			count += 1
			sentences = sent_tokenize(entry_description)
			modified_sentences = []
			entry_modified = False
			capitalisation_changes = {}
			for sentence in sentences:
				processed_sentence = nltk.word_tokenize(sentence)
				ccw   = 0 					# Consecutive capitalised words
				index = 0					# Index of word in the sentence
				decapitalise_indexes = []	# The indexes of words to decapitalise
				for word in processed_sentence:					
					capitalised_characters 	= sum(1 for c in word if c.isupper() or not c.isalpha())	# Treat non-alphabetical characters as capital letters
					total_characters 		= len(word)

					# Check whether the word is entirely non-alphabetic. If it is, it shouldn't count as a capitalised word.
					# If it's something like "(HELLO)", then it should.
					alphabetical_characters 	= sum(1 for c in word if c.isalpha())
					if alphabetical_characters == 0:
						capitalised_characters = 0
					
					# If this word is completely capitalised, add one to the consecutive capitalised words counter (ccw) and append the index
					# of this word in the sentence to the decapitalise_indexes list, along with the previous word's index.
					if total_characters == capitalised_characters:
						ccw += 1
						if ccw > 1:
							decapitalise_indexes.append(index)
							decapitalise_indexes.append(index - 1)
					# If this word is not completely capitalised, reset the ccw list.
					else:
						ccw = 0
					index += 1

				if len(decapitalise_indexes) > 0:					
					original_sentence = sentence
					
					for index in decapitalise_indexes:
						processed_sentence[index] = processed_sentence[index].lower()	
					processed_sentence[0] = processed_sentence[0][0].upper() + processed_sentence[0][1:]

					modified_sentence = untokenize(processed_sentence)
					modified_sentences.append(modified_sentence)

					capitalisation_changes[original_sentence] = modified_sentence 
					entry_modified = True
				else:
					modified_sentences.append(sentence)


			if entry_modified:		
				sys.stdout.write('.')
				modified_description = " ".join([s for s in modified_sentences])
				entry["Description"] = modified_description

				report_data = generate_report_data(report_data, capitalisation_changes, entry_description, count)


		def write_report(report_data):
			write_to_file(report_data, 'data/reports/capitalisation_normalisation.js', indent = 1, export = True)

		write_report(report_data)

		print(" done.\n")
		
		return data

	# 2.0 Count all words in the dataset.
	# The report shows a list of words that are not standard English.

	def count_words(data):
		print("Counting all words in the data...", end="")
		
		# Global variables
		stop_words_v2 = set(stopwords.words('english'))
		stop_words_v2.update(',', '[', ']', '(', ')', '&') # Remove punctuation, but not full stops (so sentence endings can be marked)

		def get_prev_next_word(tokenized_corpus, i, stop_words_v2):
			prev_word = None
			next_word = None
			dist = 1
			# Check that the previous word isn't a stop_word (including a punctuation mark)
			while prev_word in stop_words_v2 and i > 0:
				prev_word = tokenized_corpus[i - dist]
				dist += 1
			dist = 1
			while next_word in stop_words_v2 and ((i + dist) < len(tokenized_corpus)):
				next_word = tokenized_corpus[i + dist]
				dist += 1
			if prev_word:
				prev_word = prev_word.lower()
			if next_word:
				next_word = next_word.lower()
			return [prev_word, next_word]



		# Create a big corpus by combining all of the descriptions, and tokenising it into words.
		descriptions = [nltk.word_tokenize(e["Description"]) for e in data]
		tokenized_corpus = list(itertools.chain(*descriptions))


		punctuation = [',', '[', ']', '(', ')', '&', None] # Include None to represent a non-word

		# Count all the words in the corpus using Counter to get a dictionary of unique words and their frequencies.	
		counter = Counter(tokenized_corpus)
		counter_dict = counter
		counter = counter.most_common()

		print(" done (%s words total).\n" % len(tokenized_corpus))

		print("Getting suggestions for each error word using Pyenchant...", end="")

		error_words = {}
		weighted_suggestions = {}
		domain_specific_words = []

		unique_suggestions = {} 	# A set of unique suggested words, so that bi-grams may be constructed
		
		# 1. Count all words and determine the suggestions for any 'errors' that are caught by Pyenchant,
		#    or define it as a 'domain specific word' if it is more common than its potential replacements.
		#	 This does not look at the context of each error. It stores the errors in a dictionary, and keeps track of
		#	 every unique suggestion given by Pyenchant. 
		#	 It is relatively quick because it is iterating over counter, not over the entire corpus. (it iterates over
		# 	 every unique word, not every occurence of every word).
		for c in counter:
			word  = c[0]
			count = c[1]
			if is_invalid_word(word):

				error_words[word] = {}
				error_words[word]["Count"] = count
				suggestions = d.suggest(word)

				# Get a string representation of suggestions for the purposes of the error words report
				# Comes in the form of (count) suggestion   (where count is the number of times the suggestion appears in the entire corpus)
				vals = [("(" + str(counter_dict[suggestions[i]]) + ") " + suggestions[i] if len(suggestions) > i else "-") for i in range(10)]
				error_words[word]["Suggestions"] = vals

				# Also get a list of the first 10 suggested words for the error, without any formatting.
				error_words[word]["Suggestions List"] = suggestions[:min(10, len(suggestions))]

				# Compare the original occurences of the word to the occurences of the suggestions.
				# Assume it is domain specific (i.e. not an error) until proven otherwise.
				domain_specific = True 
				cmax = c[1]

				# Iterate over the first 10 suggestions given by Pyenchant
				for suggested_word in error_words[word]["Suggestions List"]:
					# Find the suggestion with the highest frequency and use it as the replacement
					# If there is a suggestion with a higher frequency than the original term, the term is not 'domain specific'
					if suggested_word not in unique_suggestions:
						unique_suggestions[suggested_word] = None
					if counter_dict[suggested_word] > cmax:
						cmax = counter_dict[suggested_word]
						domain_specific = False 
						#spelling_dictionary[word] = suggested_word
						error_words[word]["Replacement"] = suggested_word

				if domain_specific:
					domain_specific_words.append(word)
					# Remove it from error words as it is no longer an error
					del error_words[word]
				sys.stdout.write('.')


		''' Note: I need to figure out how to include 2-word suggestions, such as "pain in". At this stage it is impossible for 
			a word to be split into two words because two words won't appear as one token. '''



		write_to_file(unique_suggestions, 'data/reports/unique_suggestions.js', indent = 1, export = True)

	





		''' Instead of iterating over the tokenized corpus, iterate over each description, and each word in each description '''
		''' Get the tf * idf of each prev/next word and store it in another column '''

		print(" done.\n")
		print("Generating idf dictionary for all unique words in the corpus...")

		# Some progress report variables so you can see how long it's going to take ...
		progress_count = 0
		progress_count_total = len(counter)

		df_dict = {}

		# Generate an idf dict that stores the number of documents each word appears in.

		for c in counter:
			df_dict[c[0].lower()] = sum([1 for desc in descriptions if c[0] in desc])

			progress_count += 1		
			sys.stdout.write('.')
			if progress_count % 50 == 0:
				sys.stdout.write (' ' + str(progress_count) + '/' + str(progress_count_total) + "\n")
			sys.stdout.flush()		

		write_to_file(df_dict, 'data/reports/df_dict.js', indent = 1, export = True)




		print(" done.\n")

		# 2. Build all bi-grams for every word in the unique suggestions to see the context in which they may appear in the text.
		#    Store it in a dictionary, like this:
		#    word -> [ {w1: 4, w2: 5, w3: 7}, {w1: 3, w5: 6, w7: 1}    ]	# d[word][0] is previous words, d[word][1] is next words
		# 	 If the suggestion does not appear in the corpus, discard it entirely as it is most likely not the right correction.

		print("Generating bi-grams for all " + str(len(tokenized_corpus)) + " words in the corpus...")

		# Get bi-grams for every single word in the corpus.
		# It's quicker to do it this way, than rather just for suggestion words only. (only have to scan corpus once, rather than many
		# times to check whether the word is in it).
		ii = 0
		bigram_dictionary = {}

		# Some progress report variables so you can see how long it's going to take ...
		progress_count = 0
		progress_count_total = len(tokenized_corpus)

		total_descriptions = len(descriptions)
		for description in descriptions:

			description_counter = Counter(description)
			description_length = len(description)

			for word in description:
				if word not in bigram_dictionary:
					bigram_dictionary[word] = [{}, {}] # Dicts of prev, next
				#prev_words = {}
				#next_words = {}

				


				[prev_word, next_word] = get_prev_next_word(tokenized_corpus, ii, stop_words_v2)	
				if(prev_word):
					if prev_word not in bigram_dictionary[word][0]:
						bigram_dictionary[word][0][prev_word] = [0, 0, 0]	# [frequency, frequency/total, tf * idf]
						bigram_dictionary[word][0][prev_word][0] = 1

					else:
						bigram_dictionary[word][0][prev_word][0] += 1
				if next_word:
					if next_word not in bigram_dictionary[word][1]:
						bigram_dictionary[word][1][next_word] = [0, 0, 0]
						bigram_dictionary[word][1][next_word][0] = 1
					else:
						bigram_dictionary[word][1][next_word][0] += 1


				''' tf * idf '''
				''' note: forget about tf for now, I think idf only might be better '''
				if prev_word:				
					#p_tf = 1.0 * description_counter[prev_word] / description_length
					p_idf = 1.0 * math.log(total_descriptions / df_dict[prev_word])
					bigram_dictionary[word][0][prev_word][2] = p_idf # * p_tf

				if next_word:
					#n_tf = 1.0 * description_counter[next_word] / description_length
					n_idf = 1.0 * math.log(total_descriptions / df_dict[next_word])
					bigram_dictionary[word][1][next_word][2] = n_idf # * n_idf

				ii += 1
				progress_count += 1
				if progress_count % 20 == 0:
					sys.stdout.write('.')
				if progress_count % 1000 == 0:
					sys.stdout.write (' ' + str(progress_count) + '/' + str(progress_count_total) + "\n")
					sys.stdout.flush()

		'''
		for word in unique_suggestions:
			prev_words = {}
			next_words = {}

			#if word in tokenized_corpus:
			indices = [i for i, w in enumerate(tokenized_corpus) if w == word]
			for i in indices:
				[prev_word, next_word] = get_prev_next_word(tokenized_corpus, i)
				if prev_word not in prev_words:
					prev_words[prev_word] = [0, 0]	# A list, which stores [frequency, frequency/total]
				if next_word not in next_words:
					next_words[next_word] = [0, 0]
				prev_words[prev_word][0] += 1
				next_words[next_word][0] += 1	
			unique_suggestions_dict[word] = [prev_words, next_words]

			progress_count += 1
			sys.stdout.write('.')
			if progress_count % 50 == 0:
				sys.stdout.write (' ' + str(progress_count) + '/' + str(progress_count_total) + "\n")
			sys.stdout.flush()
		'''


		# Calculate the probabilities associated with the previous and next word appearing before and after the suggestion.
		for word in bigram_dictionary:
			# Calculate the sum of all frequencies and use it to determine the frequency/total frequency of each prev/next word.
			total_prev = sum([freq[1][0] for freq in bigram_dictionary[word][0].items()])
			for prev_word in bigram_dictionary[word][0]:
				bigram_dictionary[word][0][prev_word][1] = 1.0 * bigram_dictionary[word][0][prev_word][0] / total_prev		
	
			total_next = sum([freq[1][0] for freq in bigram_dictionary[word][1].items()])
			for next_word in bigram_dictionary[word][1]:
				bigram_dictionary[word][1][next_word][1] = 1.0 * bigram_dictionary[word][1][next_word][0] / total_next	

		# Write the bi-grams to a file.
		write_to_file(bigram_dictionary, 'data/reports/bigram_dictionary.js', indent = 1, export = True)



		# 3. Parse the context information associated with the suggestion of each word.
		#	 Ignore the words defined as 'domain specific'

		print(" done.\n")
		print("Generating replacement dictionary for " + str(len(error_words)) + " unique error words...")

		# Some progress report variables so you can see how long it's going to take ...
		progress_count = 0
		progress_count_total = len(error_words)

		# The replacement_dictionary maps indexes to the replacement terms
		replacement_dictionary = {}

		for word in error_words:
	
			# Get the positions in which the error word appears in the corpus
			indices = [i for i, w in enumerate(tokenized_corpus) if w == word]

			# Iterate over every occurence of the error in the corpus and get the previous/next words
			for i in indices:

				# Create a dictionary to store the suggested words and their scores
				suggestion_scores = {}

				# Keep track of whether any suggestions have been made using the previous/next words
				suggestion_found = False

				# Get the previous and next word of the error as it appears in the corpus
				[prev_word, next_word] = get_prev_next_word(tokenized_corpus, i, stop_words_v2)

				# Iterate through the suggestions for the word and determine a score for the suggestion, based on the similarity
				# of the suggestion's previous/next words, and the error's previous/next words.
				# Reminder: the dictionary looks like this:
				# bigrams_dict[suggestion] -> [{ prev_word_1: 4, prev_word_2: 6 }, { next_word_1: 2, next_word_2: 5 }]					

				for suggestion in error_words[word]["Suggestions List"]:												
					if suggestion in bigram_dictionary:		
						pw_score = 0
						nw_score = 0
						pw_idf_score = 1
						nw_idf_score = 1			
						spws = bigram_dictionary[suggestion][0] # Suggestion previous words, as a dict { 'word': count }
						for spw in spws:
							# If the error word's previous word matches the suggestion's previous word,
							# get the probability that the previous word comes before the suggested word using the values
							# already defined in the bi-grams dictionary.
							# Add this value to a dictionary so that the scores for each suggestion can be compared.
							if spw == prev_word:
								probability = spws[spw][1]	# Use the frequency of the previous word as a baseline for the score
								#print "PREV:", spw + " -> " + word + " (" + str(probability) + ")"
								pw_score = probability
								pw_idf_score = spws[spw][2]
								suggestion_found = True
							
						# Do the exact same process for the next words
						snws = bigram_dictionary[suggestion][1] # Suggestion next words 
						for snw in snws:	
							if snw == next_word:
								probability = snws[snw][1]
								#print "NEXT:", word + " -> " + snw + " (" + str(probability) + ")"
								nw_score = probability
								nw_idf_score = snws[snw][2]
								suggestion_found = True

						''' IDEA:

						Use tf * idf of the previous/after word to weight the scores better 

						'''

						suggestion_scores[suggestion] = (pw_score + nw_score) * pw_idf_score * nw_idf_score

				# If no suitable suggestion has been found based on the previous and next words, simply use the 'best' suggestion
				# (the suggestion that was previously found to occur most frequently in the corpus)
				if not suggestion_found:
					chosen_suggestion = error_words[word]["Replacement"]
					#print "NO SUGGESTION FOUND FOR: ", str(word), "... using: " + str(chosen_suggestion)
				# Otherwise, choose the suggestion with the highest score from the suggestion_scores dict
				else:
					chosen_suggestion = max(suggestion_scores.iteritems(), key = operator.itemgetter(1))[0]

				# Append the index: suggestion to the new spelling dictionary
				replacement_dictionary[i] = chosen_suggestion

			progress_count += 1
			sys.stdout.write('.')
			if progress_count % 50 == 0:
				sys.stdout.write (' ' + str(progress_count) + '/' + str(progress_count_total) + "\n")
			sys.stdout.flush()
					
	
		# Write the replacement dictionary to a file.
		write_to_file(replacement_dictionary, 'data/reports/replacement_dictionary.js', indent = 1, export = True)


		ordered_error_words = OrderedDict()
		print(error_words)
		for e in sorted(error_words, key = lambda x: error_words[x]['Count'], reverse = True):			
			ordered_error_words[e] = error_words[e]

		print(ordered_error_words)

		def write_report(error_words):
			write_to_file(ordered_error_words, 'data/reports/error_words.js', indent = 1, export = True)

		write_report(ordered_error_words)
		print(" done.\n")

		# No need to return domain specific words at this stage...

		return replacement_dictionary



	# 2. Correct any spelling errors that appear in the data.
	# Need to modify this to take replacement_dictionary
	def correct_spelling_errors(data, replacement_dictionary):
		print("Correcting spelling errors...")
		count = 0

		# Some progress report variables so you can see how long it's going to take ...
		progress_count = 0
		progress_count_total = len(replacement_dictionary)


		# Create a big corpus by combining all of the descriptions, and tokenising it into words.
		descriptions = [nltk.word_tokenize(e["Description"]) for e in data]
		tokenized_corpus = list(itertools.chain(*descriptions))

		# Go through the entire corpus and replace any words whose index appear in the replacement dictionary
		# with their corresponding replacement words.
		# This is in linear time. I couldn't think of a faster way to do it.
		report_data = [] # For the report

		for entry in data:
			errors = False
			entry_description_tokenized = nltk.word_tokenize(entry["Description"])
			entry_description_tokenized_after = nltk.word_tokenize(entry["Description"])

			# Create a 'before and after' report
			report_description_before = nltk.word_tokenize(entry["Description"])	
			report_description_after  = nltk.word_tokenize(entry["Description"])	
					
			for i in range(len(entry_description_tokenized)):
				# Swap the word with its replacement if its index appears in the replacement dictionary
				if count in replacement_dictionary:								
					errors = True		
					entry_description_tokenized_after[i] = replacement_dictionary[count]
					# Generate some report data
					report_description_before[i] = "<span class=\"replaced\">" + report_description_before[i] + "</span>"	
					report_description_after[i]  = "<span class=\"replaced\">" + replacement_dictionary[count] + "</span>"	
						
					progress_count += 1
					sys.stdout.write('.')
					if progress_count % 50 == 0:
						sys.stdout.write (' ' + str(progress_count) + '/' + str(progress_count_total) + "\n")
					sys.stdout.flush()
					
				count += 1
				
			# If there were any errors in the entry, append the data to the report data list
			if errors:
				report_data.append({})
				report_data[-1]["Index"] = count 
				report_data[-1]["Original"] = untokenize(report_description_before)
				report_data[-1]["Modified"] = untokenize(report_description_after)		


		def write_report(report_data):
			write_to_file(report_data, 'data/reports/spelling_errors.js', indent = 1, export = True)

		write_report(report_data)
		
		print("... done.\n")
		return data

	# 3. Count the occurences of acronyms in the text.
	#	 Acronyms are defined as two or more consecutive words that are capitalised on the first letter only.
	def process_acronyms(data):
		print("Processing acronyms...", end="")
		# Returns all possible combinations of an acronym (len > 1). For example, ["The", "Injured", "Person"] ->
		# The Injured Person, The Injured, Injured Person	
		def get_combinations(acronym):
			length = len(acronym)
			if len(acronym) < 3:
				return [acronym]
			combinations = []
			for x in range(length):
				combination = []
				combinations_x = []
				for y in range(x, length):
					if y == x + 1:
						combination = [acronym[x], acronym[x + 1]]
						combinations_x.append(combination)
					if y > x + 1:
						combination = [c for c in combination]
						combination.append(acronym[y])
						combinations_x.append(combination)
				for c in combinations_x:
					combinations.append(c)
			return combinations

		acronyms = {} # Acronym, and number of times they appear
		for entry in data:
			entry_description = entry["Description"]
			sentences = sent_tokenize(entry_description)
			for sentence in sentences:
				processed_sentence = nltk.word_tokenize(sentence)
				cw = [w if (len(w) > 1 and w[0].isupper() and w[1].islower()) else None for w in processed_sentence] 
				current_acronym = []
				for w in cw:
					if w: # a word, meaning it must be added to the current_acronym
						if w[0].isupper():
							current_acronym.append(w)
					else: # not a word, so the acronym has ended
						if current_acronym and len(current_acronym) > 1:
							# Get all combinations of each acronym (The Injured Person, The Injured, Injured Person)
							combinations = get_combinations(current_acronym)
							sys.stdout.write('.')
							for c in combinations:
								#  Add a string representation of the acronym to the acronyms dictionary, or increase the count of that
								#  acronym in the dictionary if the key is already present
								ca_string = " ".join(c)
								if ca_string in acronyms:
									acronyms[ca_string] += 1
								else:
									acronyms[ca_string] = 1
						current_acronym = []
		# Return only acronyms that appear more than once.
		common_acronyms = {}
		#print "Acronyms found: "
		for a in acronyms:
			if acronyms[a] > 1:
				common_acronyms[a] = acronyms[a]
				#print a, acronyms[a]
		#print ""

		def write_report(acronyms):
			sorted_acronyms = OrderedDict()
			for a in sorted(acronyms, key = acronyms.get, reverse = True):
				sorted_acronyms[a] = acronyms[a]
			write_to_file(sorted_acronyms, 'data/reports/common_acronyms.js', indent = 1, export = True)

		write_report(common_acronyms)
		print(" done.\n")
		return common_acronyms

	# 4. Scan the data again to replace lowercase versions of the acronyms found with the uppercase versions.
	# 	 For example, all occurences of "injured person" will be replaced with the acronym, "Injured Person".

	def capitalise_uncapitalised_acronyms(acronyms):
		acronyms_list = []

		# Generate variants for alternate capitalisations, i.e. "Camp medical centre", "Camp Medical centre", "camp Medical Centre", etc
		# n ^ 2 different outcomes

		def generate_capitalisation_variants(word_tokens):
			# Cap options is a list that encapsulates the capitalisation options of each word, i.e. "Camp" and "camp"
			cap_options = []
			for e in word_tokens:
				cap_options.append((e[0].upper() + e[1:], e[0].lower() + e[1:]))

			# Set up a list of variations, where each list element represents all n-word variations of the term.
			# i.e. variations = [[["Camp", "camp"]], [["Camp", "Medical"], ...]

			variations = []
			variations.append([])
			variations[0].append([cap_options[0][0]])
			variations[0].append([cap_options[0][1]])

			# Generate all possible capitalisation variations of the term.
			i = 1
			for c in cap_options[1:]:
				variations.append([])
				for v in variations[i - 1]:
					for v2 in c:
						variations[i].append(v + [v2])
				i += 1

			# Turn the variations into strings
			variation_strings = []

			for v in variations[-1]:
				variation_strings.append(" ".join(v))

			# Remove the first variation as it is the capitalised term
			variation_strings.pop(0)

			return variation_strings

		# Sort the acronyms so the longer variants (The Injured Person) are corrected after the shorter variants (Injured Person) are.
		sorted_acronyms = sorted(acronyms, key = len, reverse = True)
		for k in sorted_acronyms:
			# Acronym term (initials), e.g. Injured Person -> IP
			# Note: still unable to deal with multiple acronyms with the same initials
			word_tokens = word_tokenize(k)
			acronym_term = "".join([w[0].upper() for w in word_tokens])

			# 4 different variants. Normal, lower, UPPER, and AT, plus all possible capitalisation variation strings.
			acronyms_list.append([k, k.lower(), k.upper(), acronym_term] + generate_capitalisation_variants(word_tokens)) 

		print("Converting acronyms and uncapitalised acronyms to full capitalised acronyms...", end="")

		# Initialise a list to use for reporting
		modified_descriptions = []
		count = 0
		for entry in data:
			entry_description = entry["Description"]	
			count += 1
			sentences = sent_tokenize(entry_description)
			modified_sentences = []
			modified = False
			acronyms_present = []	# Holds tuples of (variant, original_term)
			for sentence in sentences:
				sentence_original = '%s' % sentence				
				for a in acronyms_list:
					# a[0] is the Original Term, a[1] is lowercase, a[2] is UPPERCASE
					original_term = a[0]
					for variant in a[1:-1]:
						if variant in sentence:
							sys.stdout.write('.')

							#indexes = [m.start() for m in re.finditer(variant, sentence)]
							#print indexes

							acronyms_present.append((variant, original_term))

							sentence = sentence.replace(variant, original_term)

							modified = True

				# Replace the first letter of the sentence with a capital letter.
				sentence = sentence[0].upper() + sentence[1:]
				modified_sentences.append(sentence)			


			if modified:
				modified_description = " ".join([s for s in modified_sentences])
				entry["Description"] = modified_description

				# Set the modified description back to the original so that the correct report is given.
				# (this avoids the problem of tagging the wrong occurences of an acronym when it is already expanded in the original description).
				modified_description = entry_description

				# Generate data for reporting
				modified_descriptions.append({})
				modified_descriptions[-1]["Index"] = count 

				# Add <span> tags to the data to make it easier to visualise in the HTML page.
				# Create some lists to stop it duplicating tags when the same acronym occurs more than once.
				variants_seen  = []
				originals_seen = []
				for a in acronyms_present:					
					if a[0] not in variants_seen:
						entry_description 		= entry_description.replace(a[0], "<span class=\"replaced\">" + a[0] + "</span>")
						variants_seen.append(a[0])
						modified_description 	= modified_description.replace(a[0], "<span class=\"replaced\">" + a[1] + "</span>")

				modified_descriptions[-1]["Original"] = entry_description 
				modified_descriptions[-1]["Modified"] = modified_description

		def write_report(modified_descriptions):
			write_to_file(modified_descriptions, 'data/reports/acronym_replacement.js', indent = 1, export = True)

		write_report(modified_descriptions)

		print(" done.\n")
		return data				



	# Print out all the acronyms and their counts	
	def print_acronyms(acronyms):		
		if len(acronyms) > 0:
			for a in sorted(acronyms, key = acronyms.get, reverse = True):
				print(a, acronyms[a])
	
	data = normalise_capitalisation(data)
	replacement_dictionary = count_words(data)
	data = correct_spelling_errors(data, replacement_dictionary)
	acronyms = process_acronyms(data)

	data = capitalise_uncapitalised_acronyms(acronyms)

	write_to_file(data, DATA_FOLDER + DATA_FILENAME + '_cleaned.json')

	with codecs.open('../data_warehousing/input/raw_data_clean.txt', 'w', 'utf-8') as f:
		f.write('\n'.join([d["Description"] for d in data]))

	return data

