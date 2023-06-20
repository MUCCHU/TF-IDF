
# TF-IDF based Search Engine

This project uses TF-IDF technique to match a given query with the existing database of leetcode problems

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
