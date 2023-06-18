import json
import os
import nltk
from nltk.corpus import stopwords
from flask import Flask, render_template, request

DATA_FOLDER = "tf-idf"
app = Flask(__name__)


def get_tfidf():
    # read the tfidf.json file and return the tfidf matrix
    f = open(os.path.join(DATA_FOLDER, "tfidf.json"))
    data = json.load(f)
    f.close()
    return data

def get_vocab():
    # read the vocab.json file and return the vocab
    f = open(os.path.join(DATA_FOLDER, 'vocab.json'))
    data = json.load(f)
    f.close()
    return data

def get_reverse_map():
    # read the reverse_map.json file and return the reverse_map
    f = open(os.path.join(DATA_FOLDER, 'reverse_map.json'))
    data = json.load(f)
    f.close()
    return data

def get_index():
    # read the index.json file and return the index
    with open("index.txt", "r", encoding="Latin-1", errors="ignore") as f:
        return [line.split(" ", 1)[1].strip() for line in f]

def get_links():
    #read the links.txt file in problems folder and return array of links
    links = []
    with open("qindex.txt", "r", encoding="Latin-1", errors="ignore") as f:
        for link in f:
            links.append(link.strip())
    return links

def get_results(query_string):
    tfidf =  get_tfidf()
    vocab = get_vocab()
    reverse_map = get_reverse_map()
    documents = get_index()
    links = get_links()
    query_string = query_string.lower()
    results = {}
    stop_words = set(stopwords.words('english'))
    query_words = query_string.split(" ")
    for word in query_words:
        if word not in vocab:
            continue
        if word in stop_words:
            continue

        docs = reverse_map[word]
        for doc in docs:
            if doc not in results:
                results[doc] = tfidf[doc][word]
            else:
                results[doc] += tfidf[doc][word]
        
    # sort the dictionary results by the values
    results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    # print(results)
    ans = []
    for key in results:
        res = {}
        res['title'] = documents[key[0]]
        res['link'] = links[key[0]]
        res['score'] = key[1]
        ans.append(res)
        # print(documents[key[0]], "score = ", str(key[1]))
    return ans
        # print(documents[key], "score = ", str(results[key]))

@app.route('/', methods=['GET', 'POST'])
def home():
    # print("Hello")
    # print(request.method)
    if request.method == 'POST':
        query = request.form['query']
        results = get_results(query)
        print(query)
        # print(results)
        return render_template('results.html', results=results, query=query)
    return render_template('search.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    return render_template('results.html')

if __name__ == '__main__':
    nltk.download('stopwords')
    app.run(debug=True)