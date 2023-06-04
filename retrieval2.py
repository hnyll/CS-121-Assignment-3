# imports
import sys
import json
import json #
import math#
import nltk
import time
from nltk.corpus import stopwords
from urllib import request
from pathlib import Path
from nltk.stem.snowball import SnowballStemmer#
from bs4 import BeautifulSoup#
from collections import defaultdict
from nltk.tokenize import word_tokenize

# global variables
stemmer = SnowballStemmer(language="english")
urls_path = "/mnt/c/users/paolo/code/UCI/CS121/CS-121-Assignment-3/urls.json"
NUM_DOCUMENTS = 55393
with open(urls_path, "r") as json_file:
    urls = json.load(json_file)

def get_top_urls(scores, top=5):
    """Gets the top urls based on the scores for the given query"""

    scores = sorted(scores.items(), key=lambda key_value:key_value[1], reverse=True)
    # print(scores[:top])
    top_urls = list() # front of the list is the #1 ranked URL
    for i in range(len(scores)):
        top_urls.append(urls[scores[i][0]])
    
    return top_urls[:top]

def get_posting(input, exact):
    """Gets the posting list based on the query input"""

    edited = input[len(exact) + 4:-3] # removes the word, beginning bracket, ending bracket, and newline from string
    find = edited.split(",") #splits everything into tuples in list
    posting = {int(str_pair.split(":")[0]):float(str_pair.split(":")[1]) for str_pair in find} # convert posting string to a posting dictionary with doc id as key and tf as value
    return posting # return posting

def get_scores(input):
    """Using the lnc.ltc to ranks scores"""

    query_vector = defaultdict(float)
    document_vectors = defaultdict(dict)
    scores = defaultdict(float)

    words = [stemmer.stem(word) for word in word_tokenize(input.lower())]
    for word in words:

        # Calculate posting for particular search word
        first_letter = word[0]
        stemmedword = stemmer.stem(word)
        posting = parse_index(first_letter, stemmedword) 

        # Calculate tf-idf for particular search word in input search query
        query_tf_raw = words.count(word) # raw term frequency (tf) for word
        query_tf_wt = math.log(query_tf_raw) + 1 # tf-weighted for word
        try:
            query_idf = NUM_DOCUMENTS / math.log(len(posting)) if math.log(len(posting)) != 0 else 0 # idf for word 
        except:
            query_idf = 0
        query_tfidf = round(query_tf_wt * query_idf, 4) 
        query_vector[word] = query_tfidf

        # Place term frequencies for each document
        for doc_id, tf in posting.items():
            document_vectors[doc_id][word] = tf

    # Normalize vectors
    query_vector_length = math.sqrt(sum(list(map(lambda x:x**2, query_vector.values())))) 
    normalized_query_vector = {word:(tfidf/query_vector_length) for word, tfidf in query_vector.items() if query_vector_length > 0}
    normalized_document_vectors = defaultdict(dict)
    for doc_id, doc_vector in document_vectors.items():
        doc_vector_length = math.sqrt(sum(list(map(lambda x:x**2, doc_vector.values()))))
        for word in doc_vector.keys():
            normalized_document_vectors[doc_id][word] = document_vectors[doc_id][word]/doc_vector_length if doc_vector_length > 0 else 0

    # Calculate cosine scores by performing dot product of each query vector to each document vector
    for doc_id, doc_vector in normalized_document_vectors.items():
        
        for word, norm_tfidf in normalized_query_vector.items():
            scores[doc_id] += norm_tfidf * doc_vector[word] if word in doc_vector.keys() else 0.0


    # print(query_vector)
    # print(normalized_query_vector)
    # print(list(document_vectors.items())[:10])
    # print(list(normalized_document_vectors.items())[:10])
    return scores

def parse_index(letter, word):
    # index_file = r"C:\Users\srb71\Documents\GitHub\CS-121-Assignment-3\indexes\index" + letter + ".txt"   SHOB'S path
    index_file = "/mnt/c/users/paolo/code/UCI/CS121/CS-121-Assignment-3/indexes/index" + letter + ".txt"
    with open(index_file, "r", encoding="utf-8") as readfile:
        #js = json.loads(readfile.read())
        exact = "\"" + word + "\""
        for entry in readfile:
            if exact in entry:
                return get_posting(entry, exact) # return posting if found
        
        return {} # returns empty posting if not found in inverted index

if __name__ == "__main__":
    while True:
        query = input("Input Search Query (-1 to exit): ")
        if query == "-1":
            break
        start_time = time.process_time() * 1000 # start time in milliseconds
        print("Generating results for \'" + query + "\'...")
        scores = get_scores(query)
        top_urls = get_top_urls(scores)
        end_time = time.process_time() * 1000 # ending time in milliseconds
        print("\nYour top", len(top_urls), "results")
        for url in top_urls:
            print(url)
        print("Elapsed time (ms):", end_time - start_time, "\n")   # performance speeds needs to be < 300 ms
    

    