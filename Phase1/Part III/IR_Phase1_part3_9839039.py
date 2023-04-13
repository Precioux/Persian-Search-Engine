import json

#opening preprocessed file
file_path = 'C:/Users/Samin/Desktop/University/Term 7/Information Retrieval/Project/Data/IR_data_news_12k_positional_index_dic.json'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        preprocessed_data = json.load(f)
        print("File opened successfully!")
except IOError:
    print("Error opening file.")

