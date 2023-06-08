import json
import math
from string import punctuation
from hazm import *
import re
import math
import numpy as np

data = {}
positional_index_dic = {}
postings_list = {}
data_preprocessed = {}
docs = {}
N = 0


def tf_idf(nt, ftd):
    global N
    tf = 1 + math.log(ftd) if ftd > 0 else 0
    idf = math.log(N / nt)
    return tf * idf


def openFiles():
    global data, positional_index_dic, N, postings_list, data_preprocessed, docs
    # Opening positional index file
    file_path = 'C:/Users/Samin/Desktop/University/Term 7/Information Retrieval/Project/Data/IR_data_news_12k_positional_index_dic.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            positional_index_dic = json.load(f)
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

    # Opening preprocessed file
    file_path = 'C:/Users/Samin/Desktop/University/Term 7/Information Retrieval/Project/Data/IR_data_news_12k_preprocessed.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data_preprocessed = json.load(f)
            print("Preprocessed File opened successfully!")
    except IOError:
        print("Error opening file.")

    for docID, data in data_preprocessed.items():
        docs[docID] = data['content']

    for docID, body in data_raw.items():
        N = N + 1
        data[docID] = {}
        data[docID]['title'] = body['title']
        data[docID]['content'] = body['content']
        data[docID]['url'] = body['url']

    for term, postings in positional_index_dic.items():
        if term not in postings_list:
            postings_list[term] = []
        nt = postings['total']['count']
        for docID, data in postings.items():
            if docID != 'total':
                ftd = data['count']
                tfidf = tf_idf(nt, ftd)
                postings_list[term].append({'docID': docID, 'tfidf': tfidf})


def normalize_vector(input):
    vector = []
    for term in input.items():
        vector.append(term[1])
    norm = math.sqrt(sum(x ** 2 for x in vector))
    normalized_vector = [x / norm for x in vector]
    return normalized_vector


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


def calculate_query_vector(query):
    global positional_index_dic, N
    # Calculate term frequency (tf) in the query
    tf_query = {}
    for term in query:
        if term not in tf_query:
            tf_query[term] = 0
        tf_query[term] += 1

    # Calculate inverse document frequency (idf) for each query term
    idf_query = {}
    for term in tf_query:
        if term in positional_index_dic:
            nt = positional_index_dic[term]['total']['count']
            idf_query[term] = math.log(N / nt)
        else:
            idf_query[term] = 0  # Term not found in the positional index, assign idf as 0

    # Calculate query term weight (tf-idf)
    query_vector = {}
    for term in tf_query:
        tf = 1 + math.log(tf_query[term])
        tfidf = tf * idf_query[term]
        query_vector[term] = tfidf

    return query_vector


def calc_vectors(query):
    global postings_list, docs
    doc_vectors = {}
    for term in query.items():
        list = postings_list[term[0]]
        for l in range(len(list)):
            docID = list[l]['docID']
            if docID not in doc_vectors:
                doc_vectors[docID] = {}
            # print(f'docID : {docID}')
            for t in docs.get(docID):
                # print(f'Term : {t}')
                docs_of_term = postings_list[t]
                for d in range(len(docs_of_term)):
                    if docs_of_term[d]['docID'] == docID:
                        doc_vectors[docID][t] = docs_of_term[d]['tfidf']
    # for docID,list in doc_vectors.items():
    #     print(f'docID : {docID}')
    #     print(list)




            # doc_vectors[docID][term[0]] = list[l]['tfidf']

    # for term, l in query.items():
    #     for docID, list in doc_vectors.items():
    #         if term not in list:
    #             doc_vectors[docID][term] = 0
    #
    # return doc_vectors


# def calc_vectors(query):
#     global postings_list
#     doc_vectors = {}
#     for term in query.items():
#         list = postings_list[term[0]]
#         for l in range(len(list)):
#             docID = list[l]['docID']
#             if docID not in doc_vectors:
#                 doc_vectors[docID] = {}
#             doc_vectors[docID][term[0]] = list[l]['tfidf']
#
#     for term, l in query.items():
#         for docID, list in doc_vectors.items():
#             if term not in list:
#                 doc_vectors[docID][term] = 0
#
#     return doc_vectors


def jaccard_similarity(query_vector, doc_vectors):
    similarities = {}

    for docID, doc_vector in doc_vectors.items():
        print(f'Doc : {docID}')
        q_vec = set(query_vector)
        d_vec = set(doc_vector)
        # UNION
        union = list(set(q_vec) | set(d_vec))
        print(f'union : {union}')
        # INTERSECT
        intersect = list(set(q_vec) & set(d_vec))
        print(f'intersect : {intersect}')
        # norms
        # norm_union = np.linalg.norm(union)
        # print(f'norm union : {norm_union}')
        # norm_intersect = np.linalg.norm(intersect)
        # print(f'norm intersect : {norm_intersect}')
        similarities[docID] = len(intersect) / len(union)
        print(f'sim {similarities[docID]}')

    # Sort the similarities in descending order
    sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

    return sorted_similarities


def cosine_similarity(query_vector, doc_vectors):
    similarities = {}
    # print(f'q vec : {query_vector}')
    for docID, doc_vector in doc_vectors.items():
        # print(f'doc : {docID}')
        # print(f'doc vec : {doc_vector}')
        dot_product = 0
        a2 = 0
        b2 = 0
        # Calculate dot product and a2 b2
        for i in range(len(query_vector)):
            # print(f'i : {i}')
            dot_product += query_vector[i] * doc_vector[i]
            # print(f'query_vector[i] {query_vector[i]} doc_vector[i] {doc_vector[i]} dot_product {dot_product}')
            a2 += query_vector[i] * query_vector[i]
            # print(f'a2 : {a2}')
            b2 += doc_vector[i] * doc_vector[i]
            # print(f'b2 : {b2}')

        cosine = dot_product / (math.sqrt(a2) + math.sqrt(b2))
        # print(f'cosine : {cosine}')
        similarities[docID] = cosine

    # Sort the similarities in descending order
    sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

    return sorted_similarities


# def toPrint(sorted_docs):
#     global data
#     i = 0
#     for docID, score in sorted_docs:
#         print(f'docID : {docID} , score : {score}')
#         title = data[docID]['title']
#         url = data[docID]['url']
#         print(f'{i + 1}. DocID = {docID}  \n   Title = {title} \n   URL   = {url}')
#         i += 1


def queryProcessor(query):
    global data, positional_index_dic, postings_list
    # preprocess query
    preprocessed_query_1 = re.sub(f'[{punctuation}؟،٪×÷»«]+', '', query)
    preprocessed_query = to_stem(to_remove_stop_words(to_tokenize(to_normalize(preprocessed_query_1))))
    # calculating tf-idf
    query_tfidf = calculate_query_vector(preprocessed_query)
    # calculating available docs tf-idf
    docs_vectors = []
    #
    calc_vectors(query_tfidf)
    # # normalize query
    # normalized_query_vector = {}
    # normalized_query_vector = normalize_vector(query_tfidf)
    # # normalize doc vectors
    # normalized_docs_vector = {}
    # for docID, vector in docs_vectors.items():
    #     normalized_docs_vector[docID] = normalize_vector(vector)
    # c_sim = cosine_similarity(normalized_query_vector, normalized_docs_vector)
    # j_sim = jaccard_similarity(normalized_query_vector,normalized_docs_vector)
    # print(j_sim)


def main():
    inputQ = input('Enter Query : ')
    openFiles()
    queryProcessor(inputQ)


if __name__ == "__main__":
    main()
