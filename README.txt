There are two files for our search engine, indexer.py and retrieval2.py, and a dataset urls.json
To create an inverted index and all the index files, you have to run index.py

For index.py you need need to change two variables to get it to work


Indexpath
Path to data that they want to index, so where the DEV folder is located
Data path
Path to folder that you want the index to be in, so an empty folder 

Then run the program to create an index split between 25 different lettered indexes.

If you wish to recreate the index, good practice is to empty your index folder. 


For the search engine/query part, you have to run retrieval2.py.

Before you run it, change the file path in retrieval2.py

After you run it, you will be prompted by a terminal prompt in which you enter your query.

The program will return a set of urls which best fit your query as well as the time it took to retrieve your query.

