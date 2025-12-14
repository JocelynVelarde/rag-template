# RAG System Template with Google Gemini & MongoDB Atlas

This project is a Retrieval-Augmented Generation (RAG) system template. It leverages **Google Gemini** for generation and embeddings, and **MongoDB Atlas** as the vector store to manage and retrieve context for answering user queries.

Slides for the GHW stream can be found [here](https://docs.google.com/presentation/d/1Gc8J4m8BhTV75zy3ucVO8pPW-5iZwjdtxBIzBAYyA3w/edit?usp=sharing) 

## Features

* **Vector Store**: Uses MongoDB Atlas Vector Search to store and retrieve document embeddings.
* **Embeddings**: Powered by Google's `model/embeddings-001`.
* **LLM**: Uses Google's `gemini-2.5-flash` model for generating responses.
* **Framework**: Built using [LangChain](https://www.langchain.com/) and [Streamlit](https://streamlit.io/).

## Prerequisites

Before running the application, ensure you have the following:

1.  **Python 3.8+** installed.
2.  A **MongoDB Atlas** cluster with a vector search index configured.
3.  A **Google Cloud Project** with the Generative AI API enabled and an API key.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

This project uses `streamlit.secrets` for managing sensitive configuration. You typically need to configure two main components: MongoDB and Google AI.

1.  **Create a secrets file:**
    Create a folder named `.streamlit` in your project root and add a file named `secrets.toml`:

    ```toml
    # .streamlit/secrets.toml
    MONGO_URI = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
    ```

2.  **Environment Variables:**
    The LangChain Google integration typically requires the `GOOGLE_API_KEY` environment variable. You can set this in your terminal or add it to a `.env` file (if you extend the setup to load it):

    ```bash
    export GOOGLE_API_KEY="your-google-api-key"
    ```

3.  **MongoDB Atlas Setup:**
    Ensure your MongoDB collection (`vector_store_database.embeddings_stream`) has a Vector Search Index named `vector_index_ghw`.

    * **Database Name:** `vector_store_database`
    * **Collection Name:** `embeddings_stream`
    * **Index Name:** `vector_index_ghw`

    *Example Index Definition:*
    ```json
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

## Usage

The core logic is contained in `backend.py`. You can import these functions into a Streamlit frontend or another Python script.

### Key Functions

* `ingest_text(text_content)`: Takes a string of text, creates a document, calculates its embedding, and stores it in MongoDB.
* `get_rag_response(query)`: Performs a similarity search for the top 3 relevant documents in MongoDB and uses the Gemini LLM to answer the `query` based on that context.
