# CSOT_gen_ai
## Instructions
Here are the specific instructions to start the Streamlit:
1 -  Install all the required packages by pip install requirements.txt

2- This will give you an option to create a virtual environment for it[in VS Code] click yes, and then use the 
command in the terminal
```
.\.venv\Scripts\activate
```
3-  Also, you should enable your local host port, and you can do it by running the Docker command
```
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
```
4-  Now use this command python create_database.py to create your  SQLITE database
```
python create_database.py
```
5- Use this command python preprocess.py  to process your documents
```
python preprocess.py
```
6-  Finally use this command streamlit run week_4.py to run the streamlit
```
streamlit run week_4.py
```
7-wait for some seconds and then write the question
8-8-there are two options SQLite or Qdrant ,the difference being that SQLlite uses memory and Qdrant scans the document
