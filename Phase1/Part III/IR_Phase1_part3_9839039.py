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

# Opening origin file
file_path = 'C:/Users/Samin/Desktop/University/Term 7/Information Retrieval/Project/Data/IR_data_news_12k.json'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data_raw = json.load(f)
        print("File opened successfully!")
except IOError:
    print("Error opening file.")

data = {}
for docID, body in data_raw.items():
    data[docID] = {}
    data[docID]['title'] = body['title']
    data[docID]['content'] = body['content']
    data[docID]['url'] = body['url']


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


def toPrint(sorted_docs):
    for i in range(0, 5):
        docID = sorted_docs[i][0]
        docRank = sorted_docs[i][1]
        title = data[docID]['title']
        url = data[docID]['url']
        print(f'{i+1}. DocID = {docID}  \n   Title = {title} \n   URL   = {url}')


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

    # scoring docs
    scores = {}
    # part 1 - finding accepted terms
    for term in accepted_terms:
        if term in positional_index:
            for docID, doc_data in positional_index[term].items():
                if docID != 'total':
                    if docID not in scores:
                        scores[docID] = 5  # finding one accepted term
                    else:
                        scores[docID] += 5  # finding more than one accepted word

    # # part 2 - removing docs with rejected terms
    # rejected_docs = []
    # for term in rejected_terms:
    #     if term in positional_index:
    #         rejected_docs.extend(positional_index[term].keys())
    # rejected_docs = set(rejected_docs)
    # for docID in rejected_docs:
    #     if docID in scores:
    #         scores[docID] -= 3  # decrease score of docs with rejected terms
    #
    # # part 3 - distance of accepted terms
    # for docID in scores:
    #     positions = []
    #     for term in accepted_terms:
    #         if term in positional_index and docID in positional_index[term]:
    #             positions.extend(positional_index[term][docID])
    #     if len(positions) > 1:
    #         count = sum([positions[i+1]-positions[i] for i in range(len(positions)-1)])
    #         distance_score = 1/count
    #         scores[docID] += distance_score

    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    toPrint(sorted_docs)


queryProcessor('باشگاه های فوتبال آسیا')
