#pip install llama-index-core llama-index-llms-openai llama-index-embeddings-openai llama-index-readers-file python-dotenv


import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
from llama_index.readers.file.docs import PDFReader
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai_api_key = "**************************"
if not openai_api_key:
    st.error("OpenAI API key is missing. Please set it in your environment variables.")
    st.stop()

# Initialize OpenAI LLM and embedding model
llm = OpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)
embed_model = OpenAIEmbedding(api_key=openai_api_key)

st.title("PDF Document Query System")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
if uploaded_file:
    # Save the uploaded file temporarily
    temp_pdf_path = Path("temp_uploaded.pdf")
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load PDF document
    loader = PDFReader()
    documents = loader.load_data(file=temp_pdf_path)

    # Create an index from the documents
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    query_engine = index.as_query_engine(llm=llm)

    # Query input
    question = st.text_input("Enter your question about the document:")
    if question:
        response = query_engine.query(question)
        st.write("### Answer:")
        st.write(response.response)

    # Cleanup temporary file
    temp_pdf_path.unlink()
