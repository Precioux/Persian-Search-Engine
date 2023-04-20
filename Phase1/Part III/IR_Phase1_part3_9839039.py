import json
from hazm import *
import re

# Opening positional index file
file_path = 'C:/Users/Samin/Desktop/University/Term 7/Information Retrieval/Project/Data/IR_data_news_12k_positional_index_dic.json'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        positional_index = json.load(f)
        print("File opened successfully!")
except IOError:
    print("Error opening file.")


# preprocessing functions
def to_normalize(input_text):
    # print('Normalization..')
    output_text = Normalizer().normalize(input_text)
    # print(f'input : {input_text} ')
    # print(f'output : {output_text}')
    return output_text


def to_tokenize(input_text):
    # print('Tokenizing...')
    # remove all non-alphanumeric characters from the input_text
    input_text = re.sub(r'[^\w\s]', '', input_text)
    # tokenize the cleaned text
    output_text = word_tokenize(input_text)
    # print(f'input : {input_text} ')
    # print(f'output : {output_text}')
    return output_text


def to_remove_stop_words(input_text):
    # print('Removing Stop Words..')
    stop_words = stopwords_list()
    output_text = [word for word in input_text if not word in stop_words]
    # print(f'input : {input_text} ')
    # print(f'output : {output_text}')
    return output_text


def to_stem(input_text):
    # print('Stemming...')
    stemmer = Stemmer()
    output_text = [stemmer.stem(word) for word in input_text]
    # print(f'input : {input_text} ')
    # print(f'output : {output_text}')
    return output_text


def queryProcessor(query):
    # finding rejected terms
    rejected_terms = []
    if '!' in query:
        query_parts = query.split()
        for part in query_parts:
            if part.startswith('!'):
                rejected_terms.append(part[1:])
    print(f'Rejected terms : {rejected_terms}')

    # preprocess query
    preprocessed = to_stem(to_remove_stop_words(to_tokenize(to_normalize(query))))
    print(f'Preprocessed : {preprocessed}')

    # finding accepted terms
    accepted_terms = []
    for term in preprocessed:
        if term not in rejected_terms:
            accepted_terms.append(term)
    print(f'Accepted terms : {accepted_terms}')

    # excluding documents containing rejected terms
    docs = positional_index.keys()
    for term in rejected_terms:
        if term in positional_index:
            docs = set(docs) - set(positional_index[term].keys())

    # ranking documents based on max number of accepted terms
    doc_scores = {}
    for doc in docs:
        doc_terms = []
        for term in accepted_terms:
            if term in positional_index and doc in positional_index[term]:
                doc_terms.append(term)
        doc_scores[doc] = len(set(doc_terms))

    # sorting documents based on score
    sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

    # returning top 10 documents
    return sorted_docs[:10]


#print(queryProcessor('باشگاه های فوتبال !آسیا'))
print(positional_index)