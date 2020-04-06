from utils import *
import data_cleaning
import data_preprocessing
import wordcloud_generation
import neo4j_generation
import timeline_generation

# This is the main file that calls the core modules in the pipline.



data = read_in_data()

timeline_generation.build_timeline()

# Clean data
# Note: this does not work on Windows as Windows does not appear to support the pyenchant library 
data = data_cleaning.clean_data(data)


# Preprocess data
preprocessed_data = data_preprocessing.preprocess_data(data)



data 		= preprocessed_data["Data"]
nr_phrases  = preprocessed_data["Noun Relation Phrases"]

# Neo4J input
#neo4j_generation.generate_neo4j_input(nr_phrases)

#data = read_in_preprocessed_data()

# Wordcloud input
wordcloud_generation.create_wordcloud(data)
