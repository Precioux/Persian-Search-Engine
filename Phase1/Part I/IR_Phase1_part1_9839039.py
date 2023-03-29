import json
from string import punctuation
import re
from hazm import *

file_path = 'C:/Users/Samin/Desktop/University/Term 7/Information Retrieval/Project/Data/IR_data_news_12k.json'

try:
    f = open(file_path, 'r', encoding='utf-8')
    data_raw = json.load(f)
    print("File opened successfully!")
    f.close()
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
    print('Normalization..')
    output_text = Normalizer().normalize(input_text)
    print(f'input : {input_text} ')
    print(f'output : {output_text}')
    return output_text


def to_tokenize(input_text):
    print('Tokenizing...')
    # remove all non-alphanumeric characters from the input_text
    input_text = re.sub(r'[^\w\s]','',input_text)
    # tokenize the cleaned text
    output_text = word_tokenize(input_text)
    print(f'input : {input_text} ')
    print(f'output : {output_text}')
    return output_text



def to_remove_stop_words(input_text):
    print('Removing Stop Words..')
    stop_words = stopwords_list()
    output_text = [word for word in input_text if not word in stop_words]
    print(f'input : {input_text} ')
    print(f'output : {output_text}')
    return output_text


def to_stem(input_text):
    print('Stemming...')
    stemmer = Stemmer()
    output_text = [stemmer.stem(word) for word in input_text]
    print(f'input : {input_text} ')
    print(f'output : {output_text}')
    return output_text


# preprocessed data dictionary
def preprocess(data):
    # create a new dictionary to store the preprocessed data
    preprocessed_data = {}

    for docID, doc in data.items():
        preprocessed_doc = {}
        print(f'Doc Content: {doc["content"]}')
        pure_content = re.sub(f'[{punctuation}؟،٪×÷»«]+', '', doc['content'])
        print(f'Pure Content : {pure_content}')
        preprocessed_doc['content'] = to_stem(to_remove_stop_words(to_tokenize(to_normalize(pure_content))))
        preprocessed_doc['url'] = doc['url']
        preprocessed_data[docID] = preprocessed_doc

    return preprocessed_data


# # Check the changes in preprocessed data
# data_test = {
#     'docID_1': {
#         'title': 'Test Dox',
#         'content': 'این یک متن نمونه‌ی فارسی است که حاوی بسیاری از کلمات رایج مثل به، از، و، با، در و ... می‌باشد و برای بررسی کارکرد توابع پیش‌پردازش به کار می‌رود.',
#         'url': 'http://example.com/test_document'
#     }
# }
#
# preprocessed_data = preprocess(data_test)
# # Check the changes in preprocessed data
# print(preprocessed_data['docID_1']['content'])

# real data preprocessing
preprocessed_data = preprocess(data)
# print(preprocessed_data)

# save preprocessed data as a JSON file
output_file_path = 'C:/Users/Samin/Desktop/University/Term 7/Information Retrieval/Project/Data/IR_data_news_12k_preprocessed.json'
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(preprocessed_data, f, ensure_ascii=False, indent=4)