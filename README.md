# README #
  
## Setting up ##

To run the web application, you must install NodeJS.

All of the code under the /nlp folder requires Python 3+. In addition to Python 3, the NLP tasks require:

* nltk
* pyenchant

MongoDB must also be installed and running to run the web server.

## Running the code

First, install the dependencies:

    $ pip install nltk pyenchant
    $ npm install .

Then install the relevant NLTK libraries:

    $ python
      > import nltk
      > nltk.download('stopwords')
      > nltk.download('wordnet')

To run the NLP pipeline, navigate to the `nlp` folder and run `nlp.py`:

    $ cd nlp
    $ python nlp.py

Then, navigate to the `data_warehousing` folder and run the data warehousing pipeline:
  
  $ cd ../data_warehousing
  $ python run_pipeline.py

After both pipelines are complete, you can run the webserver via `npm`:

    $ cd ..
    $ npm start

Once the web server is running, visit `localhost:3000` in your browser.

## File/folder Structure ##

```
aquila
│   README.md       // This readme
│   app.js          // Nodejs app file
│   filesearch.rb       // A ruby script I made for easily searching files
│   package.js        // Contains all the nodejs package information  
│
└───bin           // The nodejs server config
└───data_warehousing    // All of the data warehousing code, including the preliminary tagging and association rule mining code
└───helpers         // A helper file for the timeline chart
└───nlp           // The data cleaning, preprocessing, neo4j graph generation, and wordcloud generation Python code
└───node_modules      // Nodejs modules required to run the app
└───public          // All of the assets (images, javascripts, stylesheets)
└───routes          // Maps each URL to a specific page in the web app
└───scss          // The SCSS stylesheets which are compiled and saved to the public folder when changed
└───view          // The HTML pages that are rendered by the web app

```

## Running the code on a different dataset ##

The sample dataset is located at `nlp/data/sample_data.csv`. To run the pipelines on a new dataset, replace this file with your own and run the pipelines as shown above.

### Notes ###

When Aquila was originally built it was designed for a specific dataset. There are some components in the code that are unfortunately hardcoded, and your dataset must currently adhere to the hardcoded requirements:

- The date column must be in the form dd/mm/yyyy.

The hardcoding takes place in `nlp/utils.py`, `data_warehousing/run_pipeline.py`, and `helpers/timeline_chart_helper.js`. You'll need to modify the capitalised variables at the top of each of these datasets to suit your dataset. Please see the comments in each file for more info.

### Modifying the category hierarchy

The category hierarchy is stored in `data_warehousing/input/categories.yml`. This can be modified to suit your needs, though the structured fields mentioned in the list above will need to be present for the code to work correctly.

You'll also need to modify `data_warehousing/input/categories.yml` to suit your dataset. For example, if your dataset has the categorical variable "Consequence_level" and there are four different consequence levels in that column, you'll need to add a node to the hierarchy:

    Consequence_level:
      1:
      2:
      3:
      4:

### Adjusting the association rule mining parameters

The ARM visualisation is built using two parameters: min support, and confidence threshold. These parameters can be adjusted in `data_warehousing/run_pipeline.py`, line 86. conf is the confidence threshold (i.e. only rules above the threshold will be generated) and support is the minimum support, i.e. the consequent must occur in the corresponding percentage of all records. The best value for min support will depend on your dataset.

### Note about the sample dataset

The sample dataset (`nlp/data/sample_data.csv`) is taken from the US Accidents Injuries Dataset (https://catalog.data.gov/dataset/accident-injuries). The required columns (above) have been added, and the values in those columns are randomised. *The sample dataset is purely for demonstration purposes and will not yield useful information extraction results*.

## Currently ongoing work

The application is currently split into back end (Python) and front end (Javascript). The Python scripts generate JS files which are used by the web app, which means only one project can be visualised at a time. It is not yet possible to upload a new project via the web interface. Work is currently ongoing to seperate Aquila into two distinct applications - one for the back-end, and one for the front end. Rather than storing the visualisation data as flat files, they will be stored in a database.

The NLP pipeline in this prototype is fairly simplistic, and was written early on in my PhD. We have since developed our own algorithms for lexical normalisation (text cleaning) and entity typing which is being incorporated into the back-end component of Aquila in order to improve the quality of the tool.

The hardcoded requirements will be removed in future stable releases of Aquila - in particular, the user will be able to specify the structured fields they want to include in the data warehousing visualisations based on the columns present in their dataset.

## Contact ##

Email: michael.stewart@research.uwa.edu.au
