import streamlit as st
# FIX: Added extract_text_from_pdf to the import list below
from backend import ingest_text, get_rag_response, extract_text_from_pdf

st.set_page_config(page_title="MongoDB RAG Test")

st.title("RAG Knowledge Base")

# --- PDF UPLOAD SECTION ---
with st.expander(" Upload PDF"):
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Ingest PDF"):
            with st.spinner("Extracting and saving to database..."):
                # 1. Convert PDF to text
                raw_text = extract_text_from_pdf(uploaded_file)
                
                # 2. Ingest the text
                success = ingest_text(raw_text)
                
                if success:
                    st.success("PDF processed and saved to MongoDB!")

st.divider()

# --- TEXT UPLOAD SECTION ---
with st.expander(" Ingest Raw Text"):
    text = st.text_area("Enter text to ingest")
    if st.button("Ingest Text"):
        with st.spinner("Saving to database..."):
            ingest_text(text)
            st.success("Text ingested successfully")

st.divider()

# --- Q&A SECTION ---
query = st.text_input("Ask a question")
if st.button("Get Answer"):
    if query:
        with st.spinner("Searching knowledge base..."):
            answer = get_rag_response(query)
            st.markdown("###  Answer")
            st.write(answer)