import os
import math
import json
PROBLEMS_FOLDER = "problems"
DATA_FOLDER = "tf-idf"
corpus = []
def get_index():
    """
    Returns a list of problem names in the order they were scraped
    Also removes the first word ie the unwanted number
    """
    with open("index.txt", "r") as f:
        # also convert to lowercase
        return [line.split(" ", 1)[1].strip().lower() for line in f]
        # return [line.split(" ", 1)[1].strip() for line in f]

def generate_vocab(problem_set):
    """
    Generates a vocab dictionary from all the problems' titles
    """
    vocab = {}
    for problem in problem_set:
        for word in problem.split(" "):
            if word not in vocab:
                vocab[word] = 1
            else:
                vocab[word] += 1
    return vocab

def generate_reverse_map():
    """
    Generates a reverse map of tokens to their document index
    """
    reverse_map = {}
    for i, problem in enumerate(corpus):
        unique_words = set(problem.split(" "))
        for word in unique_words:
            if word not in reverse_map:
                reverse_map[word] = [i]
            else:
                reverse_map[word].append(i)
    return reverse_map

def generate_tf():
    """
    Generate Term Frequencies for each document's tokens
    """
    tfs = []
    for i, problem in enumerate(corpus):
        words = problem.split(" ")
        total_words = len(words)
        current_tf = {}
        for word in words:
            if word not in current_tf:
                current_tf[word] = 1
            else:
                current_tf[word] += 1
        for word in current_tf:
            # idf = log(total words in a particular doc/ the frequency of the word in that doc )
            # handle the case when the word is not present in the doc
            if current_tf[word] != 0 and total_words != 0:
                current_tf[word] = (current_tf[word]/total_words)
            else:
                current_tf[word] = 0
        tfs.append(current_tf)
    return tfs

def generate_idf():
    """
    Generate Inverse Document Frequency for each token
    """
    idfs = {}
    for word in reverse_map:
        idfs[word] = math.log(len(corpus)/len(reverse_map[word]))
    return idfs

def generate_tfidf():
    """Function to generate the TF-IDF matrix"""
    tfidf = []
    for i, problem in enumerate(corpus):
        words = problem.split(" ")
        total_words = len(words)
        current_tfidf = {}
        for word in words:
            if word not in current_tfidf:
                current_tfidf[word] = 1
            else:
                current_tfidf[word] += 1
        for word in current_tfidf:
            # idf = log(total words in a particular doc/ the frequency of the word in that doc )
            # handle the case when the word is not present in the doc
            if current_tfidf[word] != 0 and total_words != 0:
                current_tfidf[word] = (current_tfidf[word]/total_words) * idf[word]
            else:
                current_tfidf[word] = 0
        tfidf.append(current_tfidf)
    return tfidf
    
corpus = get_index()
vocab = generate_vocab(corpus)
reverse_map = generate_reverse_map()
term_frequencies = generate_tf()
idf = generate_idf()
tfidf = generate_tfidf()
# print(corpus)
# print(vocab)
# print(reverse_map)
# print(term_frequencies)
# print(idf)
# print(tfidf[0])
# store the generated tfidf matrix in a json file

with open(os.path.join(DATA_FOLDER, "tfidf.json"), "w") as f:
    json.dump(tfidf, f)

# store the generated idf matrix in a json file
with open(os.path.join(DATA_FOLDER, "idf.json"), "w") as f:
    json.dump(idf, f)

# store the generated reverse map in a json file
with open(os.path.join(DATA_FOLDER, "reverse_map.json"), "w") as f:
    json.dump(reverse_map, f)

# store vocab in a json file
with open(os.path.join(DATA_FOLDER, "vocab.json"), "w") as f:
    json.dump(vocab, f)


# store the index in a json file
with open(os.path.join(DATA_FOLDER, "index.json"), "w") as f:
    json.dump(corpus, f)