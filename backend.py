from pymongo import MongoClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.schema import Document
import streamlit as st  

MONGO_URI = st.secrets["MONGO_URI"]
DB_NAME = "vector_storedb"
COLLECTION_NAME = "embeddings_rag"
ATLAS_VECTOR_SEARCH = "vector_index_rag"

def get_vector_store():
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION_NAME] # to connect to mongo collection

    embeddings = GoogleGenerativeAIEmbeddings(model = "model/embeddings-001")

    vector_store = MongoDBAtlasVectorSearch(
        collection=collection,
        embedding=embeddings,
        index_name=ATLAS_VECTOR_SEARCH,
        text_key="text"
    )
    return vector_store