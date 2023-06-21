
# TF-IDF based Search Engine

This is a Python Flask web application that performs search functionality using the TF-IDF (Term Frequency-Inverse Document Frequency) algorithm. 

The application reads files containing pre-computed values of TF-IDF and other data related to the search, such as the index, the vocabulary, the reverse map, and the links associated with the documents. These files are kept in specific folders in the system, and the application uses the `os` library to access them.

When a user submits a query, the application processes the query by calculating the TF-IDF score for each term in the query, and then adds up the scores for each document that includes any of the query terms. The resulting scores are sorted in decreasing order, and the top results are selected to be shown to the user.

The application displays the search results in an HTML page that is generated using templates. The user can click on a link to view the full text of the document associated with each search result.

## Instructions to set up the code locally

1. Clone the repository

```  
git clone https://github.com/MUCCHU/TF-IDF 
```

2. Install the requirements
```
pip install -r requirements.txt
```

3. Run the server
```
python app.python
```

4. If everything worked well, the application should be live at   http://localhost:5000/

## To scrape the data 
The data has been already scraped and stored in the problems folder. However if you need to run the scraping process again, follow the steps below:

Note: The scraping file 

1. Scrape the links of all leetcode problems.

```
python scraper.py
```
2. Scrape the details of each problem.
```
python get_que.py
```

3. Pre-process the data.
```
python preprocess_data.py
```
