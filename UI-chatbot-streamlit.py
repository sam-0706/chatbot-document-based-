# pip install llama-index-core llama-index-llms-openai llama-index-readers-file python-dotenv


import os
import openai
import streamlit as st

from pathlib import Path
from llama_index import VectorStoreIndex
from llama_index.readers.file.docs import PDFReader
from llama_index.llms.openai import OpenAI

######################
# 1. Configure Azure OpenAI credentials
######################
openai.api_type = "azure"
openai.api_base = "********************************"
openai.api_version = "2023-07-01-preview"
openai.api_key = "*********************"  # <-- Replace with your Azure OpenAI key
openai.azure_endpoint = "*******************************"

# NOTE: The value you set for `model` here must match the *deployment name* 
# you created in Azure for your GPT-3.5/4 model, e.g. "my-gpt35-deployment"
DEPLOYMENT_NAME = "gpt-3.5-turbo"

######################
# 2. Initialize the Streamlit app
######################
st.title("PDF Document Q&A with Azure OpenAI (llama_index)")

# Explanation or instructions
st.write(
    "Upload a PDF document. Once uploaded, you can ask questions about its content."
)

######################
# 3. File uploader for PDF
######################
uploaded_pdf = st.file_uploader("Upload your PDF", type=["pdf"])

# We will create a session state variable to store our index
if "index" not in st.session_state:
    st.session_state["index"] = None

# If the user has uploaded a PDF file, build an index
if uploaded_pdf is not None:
    # Save the uploaded file temporarily
    with open("temp_uploaded.pdf", "wb") as f:
        f.write(uploaded_pdf.read())

    # Initialize the PDFReader and load the PDF
    pdf_path = Path("temp_uploaded.pdf")
    loader = PDFReader()
    documents = loader.load_data(file=pdf_path)

    # Create the LLM wrapper for Azure OpenAI
    llm = OpenAI(model=DEPLOYMENT_NAME) 

    # Build the index from the document
    index = VectorStoreIndex.from_documents(documents)
    st.session_state["index"] = index

    st.success("Index created! You can now ask questions below.")

######################
# 4. Question/Answer Interface
######################
if st.session_state["index"] is not None:
    question = st.text_input("Ask a question about your PDF:")
    if st.button("Get Answer"):
        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            # Use the stored index
            query_engine = st.session_state["index"].as_query_engine(
                llm=OpenAI(model=DEPLOYMENT_NAME)
            )
            response = query_engine.query(question)
            st.write("**Answer:** ", response)
