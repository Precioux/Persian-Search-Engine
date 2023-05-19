import json
import math

# Load positional index dictionary from the previous step
file_path = 'C:/Users/Samin/Desktop/University/Term 7/Information Retrieval/Project/Data/IR_data_news_12k_positional_index_dic.json'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        positional_index_dic = json.load(f)
        print("Positional index dictionary loaded successfully!")
except IOError:
    print("Error opening file.")

# Number of all docs
N = 12202


def tf_idf(nt, ftd):
    global N
    tf = 1 + math.log(ftd) if ftd > 0 else 0
    idf = math.log(N / nt)
    return tf * idf


postings_list = {}
for term, postings in positional_index_dic.items():
    postings_list[term] = []
    nt = postings['total']['count']
    for docID, data in postings.items():
        if docID != 'total':
            ftd = data['count']
            tfidf = tf_idf(nt, ftd)
            postings_list[term].append({'docID': docID, 'tfidf': tfidf})


# Print or process the postings lists for each term
for term, list in postings_list.items():
    print(f"Term: {term}")
    for entry in list:
        print(f"DocID: {entry['docID']}, tf-idf: {entry['tfidf']}")