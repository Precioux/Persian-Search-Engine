# Persian Search Engine

This project is a Persian search engine developed as part of the Information Retrieval course at Amirkabir University of Technology, spring 2023.

## Phase I

### Part 1: Preprocessing

In this part, the project performs data preprocessing on a JSON file containing news data. The data preprocessing steps include:

1. Normalization: Normalizes the input text using the `hazm.Normalizer` class.
2. Tokenization: Tokenizes the cleaned text by removing non-alphanumeric characters and using the `word_tokenize` function.
3. Stop Word Removal: Removes stop words from the tokenized text using a predefined list of Persian stop words.
4. Stemming: Stems the words in the text using the `hazm.Stemmer` class.

The preprocessing functions are defined in the code:

- `to_normalize(input_text)`
- `to_tokenize(input_text)`
- `to_remove_stop_words(input_text)`
- `to_stem(input_text)`

The preprocessing is applied to the content of each document in the input data, and the preprocessed data is stored in a new dictionary.

### Part 2: Positional Index Creation

In this part, the project creates a positional index dictionary based on the preprocessed data. The positional index dictionary maps each term to the documents it appears in, along with the count and positions of the term within each document.

The code reads the preprocessed data from a JSON file and iterates over each document. For each term in a document, the code updates the positional index dictionary with the corresponding document ID, count, and positions.

The positional index dictionary is then saved to a JSON file for further use.

### Part 3: Query Processing

In this part, the project processes user queries and retrieves relevant documents based on the search query. The query processing steps include:

1. Parsing the query to find rejected terms, phrases, and actual terms.
2. Scoring documents based on the presence of accepted terms and phrases.
3. Removing documents with rejected terms from the scores.
4. Sorting the scored documents and printing the top results.

The code provides the `queryProcessor` function, which takes a query as input and performs the above steps to retrieve relevant documents.

## Phase II

The Phase II code includes additional functionality for processing queries using a champion list. The champion list is created based on the positional index dictionary and consists of a selected number of top documents for each term. The Phase II code includes the following functions:

- `create_champion_list()`: Creates a champion list based on the positional index dictionary. The champion list selects the top N documents for each term, where N is a predefined number (e.g., 10).
- `calc_vectors_by_champion(query)`: Calculates document vectors using the champion list. The function retrieves the champion list for each term in the query and calculates the document vectors based on the TF-IDF scores.
- `calc_vectors_cosine_by_champion(query)`: Calculates document vectors using the champion list and cosine similarity. The function retrieves the champion list for each term in the query and calculates the document vectors based on the TF-IDF scores. It also handles cases where a term is not present in a document by assigning a TF-IDF score of 0.
- `toPrint(sorted_docs)`: Prints the search results in a formatted manner.

To use the Phase II functionality, set the `mode` parameter in the `queryProcessor` function to 1.

## How to Use

1. Make sure the input JSON files containing the data and positional index are in the correct file paths.
2. Run the code to perform the desired phase of the search engine.
