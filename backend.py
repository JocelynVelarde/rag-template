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


# covnert text to embeddings 
def ingest_text(texts):
    vector_store = get_vector_store()
    #input to db 
    docs = Document(page_content=texts)
    vector_store.add_documents(docs) #the documents are added to the vector store
    return True

def get_rag_response(query):
    vector_store = get_vector_store()
    #define the llm we are using {u can select temp also}
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3}) #k is the number of documents to retrieve

    #prompt template
    prompt_template = """Use the following context from the user in order to provide and accurate answer."""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=['context', 'question']
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever,
        # chain_type_kwargs={"prompt": PROMPT}
    )

    response = qa_chain.run({"query": query})
    return response