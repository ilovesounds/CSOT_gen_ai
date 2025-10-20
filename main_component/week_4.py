from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from langchain_community.utilities import SQLDatabase
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent

from langchain_openai import ChatOpenAI  # or your LLM

import re
import streamlit as st
import sqlite3

st.write("hello world")
load_dotenv()  #


api_key = os.getenv("GROQ_API_KEY")


@st.cache_resource
def get_qdrant():
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-large-en",
        encode_kwargs={'normalize_embeddings': False}
    )
    client = QdrantClient(
        url="http://localhost:6333",
        prefer_grpc=False,
    )
    qdrant = Qdrant(
        client=client,
        collection_name="vector_db",
        embeddings=embeddings,
    )
    return qdrant

qdrant = get_qdrant()

llm = ChatGroq(
    api_key=api_key,
    model="llama-3.1-8b-instant"
)

st.title("Interactive Chatbot with Qdrant and Groq")
st.write("Ask any question, and the chatbot will respond using context from the vector database!")

retriever = qdrant.as_retriever(search_type="similarity", search_kwargs={"k": 5})

prompt = ChatPromptTemplate.from_template(
    """You are an intelligent assistant tasked with answering user queries based on provided context.
Use the following context to respond to the user's question.

Context:
{context}

Question:
{query}

Answer:
"""
)

chain = (
    {"context": retriever, "query": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


db = SQLDatabase.from_uri("sqlite:///your_database.db")


llm_sql = ChatGroq(
    api_key=api_key,
    model="llama-3.1-8b-instant"
)


agent_executor = create_sql_agent(
    llm=llm_sql,
    db=db,
    agent_type="zero-shot-react-description",  
    handle_parsing_errors=True,
    verbose=True,
)


# 3. Add an option to use SQLite context
st.write("Choose context source:")
context_source = st.radio("Context source", ["Qdrant", "SQLite"])

if "history" not in st.session_state:
    st.session_state["history"] = []

user_query = st.text_input("Enter your question:", key="question_input")

if st.button("Get Response") and user_query:
    with st.spinner("Generating response..."):
        try:
            if context_source == "Qdrant":
                response = chain.invoke(user_query)
            else:
                result = agent_executor.invoke({"input": user_query})
                response = result["output"]

            
            conn = sqlite3.connect("your_database.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_history (question, answer) VALUES (?, ?)",
                (user_query, response)
            )
            conn.commit()
            conn.close()
            

            st.session_state["history"].append((user_query, response))
            st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {e}")

for q, a in st.session_state["history"]:
    st.write(f"**You:** {q}")
    st.write(f"**Bot:** {a}")