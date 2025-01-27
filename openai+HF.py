#pip install llama-index-core llama-index-llms-openai llama-index-embeddings-huggingface llama-index-readers-file transformers python-dotenv

import os
from pathlib import Path
import streamlit as st

from llama_index.readers.file.docs import PDFReader
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI

# ------------------------------------------------------------------------------
# 1. Set up Azure OpenAI credentials (HARDCODED)
# ------------------------------------------------------------------------------
import openai
openai.api_type = "azure"
openai.api_base = "*******************"
openai.api_version = "2023-07-01-preview"
openai.api_key = "*****************************"  # Replace with your actual Azure OpenAI key
openai.azure_endpoint = "*****************************"  # Optional if required

# Initialize OpenAI LLM with Azure credentials
# Replace "gpt-3.5-turbo" with your Azure deployment name if different
llm = OpenAI(model="gpt-3.5-turbo")

# ------------------------------------------------------------------------------
# 2. Initialize Hugging Face embedding model
# ------------------------------------------------------------------------------
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ------------------------------------------------------------------------------
# 3. Streamlit App Interface
# ------------------------------------------------------------------------------
st.title("PDF Document Q&A using Azure OpenAI + Hugging Face Embeddings")
st.write("Upload a PDF document, and ask questions about its content.")

# File uploader for PDF
uploaded_pdf = st.file_uploader("Upload your PDF file", type=["pdf"])

# Initialize session state to store the index
if "index" not in st.session_state:
    st.session_state["index"] = None

# If a PDF is uploaded
if uploaded_pdf is not None:
    # Save the uploaded file to a temporary location
    temp_pdf_path = Path("temp_document.pdf")
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_pdf.read())

    # Load the PDF document using PDFReader
    loader = PDFReader()
    documents = loader.load_data(file=temp_pdf_path)

    # Create an index from the documents
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

    # Save the index in session state
    st.session_state["index"] = index
    st.success("Document has been processed and indexed! You can now ask questions.")

# ------------------------------------------------------------------------------
# 4. Q&A Section
# ------------------------------------------------------------------------------
if st.session_state["index"] is not None:
    question = st.text_input("Ask a question about your document:")
    if st.button("Get Answer"):
        if question.strip() == "":
            st.warning("Please enter a valid question.")
        else:
            # Create a query engine and get an answer
            query_engine = st.session_state["index"].as_query_engine(llm=llm)
            response = query_engine.query(question)
            st.write(f"**Answer:** {response}")
