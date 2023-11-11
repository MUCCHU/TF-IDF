import json
import os
import nltk
from nltk.corpus import stopwords
from flask import Flask, render_template, request

DATA_FOLDER = "tf-idf"
PROBLEMS_FOLDER = "problems"
app = Flask(__name__)

stp_words = ['ourselves', 'aren', 'any', 'such', "you'd", 'yourself', 'll', 'you', "wasn't", 'here', 'so', 'haven', 'did', 'and', 'there', 'of', 'own', 'than', 'ain', 'both', 'above', 'between', "hadn't", "shouldn't", 'been', 'what', 'few', 'don', 'i', "she's", 'whom', 'these', 'for', 'after', 'but', 'with', 'until', 'myself', 'himself', 'won', "isn't", 'below', 'needn', 'those', 'am', 'now', 'were', "that'll", 'have', 'most', 'because', 'on', 'over', 'wouldn', 'my', 'other', 've', 'he', 'does', 'me', 'before', 'some', "aren't", 'it', 'if', 'against', 'can', "haven't", 'or', 'again', 'couldn', 'him', 'having', 'be', 'too', 'once', "it's", 'itself', 'up', 'down', 'hadn', "should've", 'an', 'they', 'them', 'from', 'will', 'weren', 'a', 'which', 'off', 'through', 'during', 'into', 'then', 'm', 'didn', "didn't", 'yourselves', 'why', 'out', 'just', 'each', 'hers', 'the', 'ma', 'o', 'about', 'very', 'her', 're', 'all', "you'll", 'nor', 'herself', 'at', "you've", 'his', 'not', 'their', 'themselves', 'being', 'who', 'how', 'd', 'theirs', 'mightn', 
"wouldn't", 'we', 'y', 'only', 'isn', 'its', 'she', 'in', "weren't", 'by', 'further', 'no', 'our', 'when', 'has', 'where', 'doing', "mustn't", 'wasn', "don't", "needn't", 'yours', "won't", 'is', 'ours', 'are', 'should', "shan't", 'same', 'was', 'mustn', 's', 'shouldn', 'under', "couldn't", 't', 'while', "you're", 'do', 'shan', 'had', "mightn't", 
'doesn', "hasn't", 'as', 'more', 'your', 'hasn', 'that', "doesn't", 'to', 'this']

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

def get_problem_statement(index):
    #read the problem statement from problems folder
    with open(os.path.join(os.path.join(PROBLEMS_FOLDER, str(index)), str(index) + ".txt"), "r", encoding="Latin-1", errors="ignore") as f:
        return f.read()


def get_results(query_string):
    tfidf =  get_tfidf()
    vocab = get_vocab()
    reverse_map = get_reverse_map()
    documents = get_index()
    links = get_links()
    query_string = query_string.lower()
    results = {}
    # stop_words = set(stopwords.words('english'))
    query_words = query_string.split(" ")
    for word in query_words:
        if word not in vocab:
            continue
        if word in stp_words:
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
        res['idx'] = key[0]
        res['title'] = documents[key[0]]
        res['link'] = links[key[0]]
        res['score'] = key[1]
        try:
            res['problem_statement'] = get_problem_statement(key[0]+1).strip()  
        except:
            res['problem_statement'] = "Problem statement not available"
            # print("Problem statement not available")
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
        # print(query)
        # print(results)
        return render_template('results.html', results=results, query=query)
    return render_template('search.html')


if __name__ == '__main__':
    nltk.download('stopwords')
    app.run(debug=True)