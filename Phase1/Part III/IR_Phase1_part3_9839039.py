import json
from string import punctuation

from hazm import *
import re

data = {}
positional_index = {}


def openFiles():
    global data, positional_index
    # Opening positional index file
    file_path = 'C:/Users/Samin/Desktop/University/Term 7/Information Retrieval/Project/Data/IR_data_news_12k_positional_index_dic.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            positional_index = json.load(f)
            print("Positional Index File opened successfully!")
    except IOError:
        print("Error opening file.")

    # Opening origin file
    file_path = 'C:/Users/Samin/Desktop/University/Term 7/Information Retrieval/Project/Data/IR_data_news_12k.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data_raw = json.load(f)
            print("Origin File opened successfully!")
    except IOError:
        print("Error opening file.")

    for docID, body in data_raw.items():
        data[docID] = {}
        data[docID]['title'] = body['title']
        data[docID]['content'] = body['content']
        data[docID]['url'] = body['url']


# preprocessing functions
def to_normalize(input_text):
    output_text = Normalizer().normalize(input_text)
    return output_text


def to_tokenize(input_text):
    # remove all non-alphanumeric characters from the input_text
    input_text = re.sub(r'[^\w\s]', '', input_text)
    # tokenize the cleaned text
    output_text = word_tokenize(input_text)
    return output_text


def to_remove_stop_words(input_text):
    stop_words = stopwords_list()
    output_text = [word for word in input_text if not word in stop_words]
    return output_text


def to_stem(input_text):
    stemmer = Stemmer()
    output_text = [stemmer.stem(word) for word in input_text]
    return output_text


def toPrint(sorted_docs):
    global data
    if len(sorted_docs) > 100:
        for i in range(0, 5):
            docID = sorted_docs[i][0]
            docScore = sorted_docs[i][1]
            title = data[docID]['title']
            url = data[docID]['url']
            print(f'{i + 1}. DocID = {docID}  \n   Title = {title} \n   URL   = {url}\n   Score = {docScore}')
    else:
        for i in range(0, len(sorted_docs)):
            docID = sorted_docs[i][0]
            title = data[docID]['title']
            docScore = sorted_docs[i][1]
            url = data[docID]['url']
            print(f'{i + 1}. DocID = {docID}  \n   Title = {title} \n   URL   = {url}\n   Score = {docScore}')


def findRejected(query):
    # finding rejected terms
    rejected_terms = []
    if '!' in query:
        query_parts = query.split()
        for part in query_parts:
            if part.startswith('!'):
                pure_rejected = re.sub(f'[{punctuation}؟،٪×÷»«]+', '', part[1:])
                preprocessed_rejected = to_stem(to_remove_stop_words(to_tokenize(to_normalize(pure_rejected))))
                rejected_terms.append(preprocessed_rejected)
    return rejected_terms


def findPhrases(query):
    # finding phrases
    phrases = []
    phrases = re.findall('\".*?\"', query)
    phrase_dic = []
    for phrase in phrases:
        pure_phrase = re.sub(f'[{punctuation}؟،٪×÷»«]+', '', phrase)
        preprocessed_phrase = to_stem(to_remove_stop_words(to_tokenize(to_normalize(pure_phrase))))
        phrase_dic.append(preprocessed_phrase)
    return phrase_dic


def findWords(query):
    # Remove words in quotes
    query = re.sub(r'"([^"]+)"', "", query)

    # Remove words starting with !
    query = re.sub(r'!\w+\s?', "", query)
    words = query.strip()
    words_list = []
    pure_words = re.sub(f'[{punctuation}؟،٪×÷»«]+', '', words)
    preprocessed_words = to_stem(to_remove_stop_words(to_tokenize(to_normalize(pure_words))))
    words_list.append(preprocessed_words)
    return words_list


def queryProcessor(query):
    global data, positional_index
    # call funcs on query
    rejected_terms = findRejected(query)
    phrase_terms = findPhrases(query)
    actual_terms = findWords(query)
    print(f'Rejected list : {rejected_terms}')
    print(f'Phrase list : {phrase_terms}')
    print(f'Actual list : {actual_terms}')

    # scoring docs
    scores = {}
    # part 1 - finding actual terms
    for item in actual_terms:
        for term in item:
            if term in positional_index:
                for docID, doc_data in positional_index[term].items():
                    if docID != 'total':
                        if docID not in scores:
                            scores[docID] = 5  # finding one accepted term
                        else:
                            scores[docID] += 5  # finding more than one accepted word

    # part 2 - phrases scoring
    for phrase in phrase_terms:
        phrase_check = {}
        for term in phrase:
            if term in positional_index:
                if term not in phrase_check:
                    phrase_check[term] = set()
                keys = positional_index[term].keys()
                for key in keys:
                    if key != 'total':
                        phrase_check[term].add(key)

        # Find the intersection of all documents containing each term in the phrase
        common_docs = set.intersection(*phrase_check.values())

        # Check if the terms in each common document are adjacent
        for doc_id in common_docs:
            positions = {}
            for term in phrase:
                positions[term] = []
                if doc_id in positional_index[term]:
                    positions[term].append(positional_index[term][doc_id]['positions'])
            check = 1
            for item in positions[phrase[0]]:
                for position in item:
                    for i in range(1, len(phrase)):
                        p = position + i
                        for item2 in positions[phrase[i]]:
                            if p in item2:
                                check = check + 1

            if check > 1:
                if doc_id not in scores:
                    scores[doc_id] = 0
                scores[doc_id] += check

    # part 3 - removing docs with rejected terms
    rejected_docs = []
    for item in rejected_terms:
        for term in item:
            if term in positional_index:
                keys = positional_index[term].keys()
                for key in keys:
                    if key != 'total' and key not in rejected_docs:
                        rejected_docs.append(key)
        for docID in rejected_docs:
            if docID in scores:
                del scores[docID]  # remove docs with rejected words

    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    if len(sorted_docs) > 0:
        toPrint(sorted_docs)
    else:
        print('داده ای یافت نشد')


def main():
    inputQ = input('Enter Query : ')
    openFiles()
    queryProcessor(inputQ)


if __name__ == "__main__":
    main()
