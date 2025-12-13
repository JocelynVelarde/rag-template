# 🦜🔗 RAG 

This is a Retrieval-Augmented Generation (RAG) application built with **Streamlit**, **MongoDB Atlas**, and **Google Gemini**. It allows users to upload PDF documents or enter raw text, which is then embedded and stored in a vector database. Users can then chat with their data to get accurate, context-aware answers.

##  Features

* **Dual Ingestion:** Support for uploading PDF files and entering raw text manually.
* **Vector Search:** Uses MongoDB Atlas Vector Search to store and retrieve relevant context.
* **Google Gemini Integration:**
    * **Embeddings:** Uses `text-embedding-004` for high-quality text representation.
    * **LLM:** Uses `gemini-2.5-flash` for fast and accurate answer generation.
* **Rate Limit Handling:** Includes batch processing to respect Google's free tier API limits.
* **Interactive UI:** Clean web interface built with Streamlit.

##  Tech Stack

* **Language:** Python 3.11+
* **Frontend:** Streamlit
* **Database:** MongoDB Atlas (Vector Search)
* **AI/LLM:** Google Gemini (via `langchain-google-genai`)
* **Framework:** LangChain
* **PDF Parsing:** `pypdf`

---

##  Setup & Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd rag-template
```
### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```bash 
pip install -r requirements.txt
```
### 4. MongoDB Atlas Setup
* Create a cluster on MongoDB Atlas.
* Create a database named `vector_storedb`.
* Create a collection named `embeddings_rag`.
* Go to the Atlas Search tab, click Create Search Index, select JSON Editor, and paste the following configuration (select the `embeddings_rag` collection):
```bash
{
  "fields": [
    {
      "numDimensions": 768,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}
```
* Name the index: `vector_index_rag`.

### 5. Configuration (Secrets)
Create a .streamlit folder in the root directory and add a secrets.toml file:
```bash
mkdir .streamlit
# Create file .streamlit/secrets.toml
```
Add your MongoDB URI and Google API Key to secrets.toml:
```bash
[general]
MONGO_URI = "mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority&appName=Cluster0"
GOOGLE_API_KEY = "your_google_gemini_api_key"
```
Note: Ensure your MongoDB user has read/write permissions and your IP is whitelisted in Network Access.

## Usage
Run the Streamlit application:
```bash
streamlit run app.py
```
### Ingest Data:

* Upload a PDF in the "Upload PDF" section.
* Paste text in the "Ingest Raw Text" section.
* Wait for the success message (data is being chunked and saved to MongoDB).

### Ask Questions:

* Type a question in the chat box (e.g., "What is the summary of the document I just uploaded?").
* The app will retrieve the most relevant chunks from MongoDB and generate an answer using Gemini.
## Project Structure
```bash
rag-template/
│
├── .streamlit/
│   └── secrets.toml         # API Keys (Do not commit to GitHub)
│
├── app.py                   # Frontend UI (Streamlit)
├── backend.py               # Logic for DB connection, Ingestion & RAG
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
└── test.py                  # (Optional) Script for testing backend functions
```

## 🙏 Acknowledgements
* This project was initially based on/inspired by the work of [JocelynVelarde](https://github.com/JocelynVelarde/rag-template.git).
* Enhanced with PDF support, rate-limit handling, and UI improvements by [Noor Fatima](https://github.com/NNoorFatima/RAG.git).