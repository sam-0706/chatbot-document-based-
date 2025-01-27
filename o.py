import os
import openai
from dotenv import load_dotenv
from pathlib import Path

# If you haven't installed these yet, be sure to install them first:
# pip install llama-index
from llama_index.readers.file.docs import PDFReader
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI

# Load environment variables if needed (optional):
load_dotenv()

# Set up your Azure OpenAI credentials
openai.api_type = "azure"
openai.api_base = "***********************"
openai.api_version = "2023-07-01-preview"
openai.api_key = "**************************"
openai.azure_endpoint = "*************************************"

# Initialize the Azure OpenAI LLM
# Make sure the value of `model` matches the *deployment name* in your Azure OpenAI resource
llm = OpenAI(
    model="gpt-3.5-turbo"
    # If needed, you can also specify other parameters such as temperature, max_tokens, etc.
)

# Load your PDF document
pdf_path = Path("test.pdf")
loader = PDFReader()
documents = loader.load_data(file=pdf_path)

# Create an index from the loaded documents
index = VectorStoreIndex.from_documents(documents)

# Create a query engine
query_engine = index.as_query_engine(llm=llm)

# Define a helper function to query the document
def query_document(question: str):
    response = query_engine.query(question)
    return response

# Example usage
questions = [
    "What is the main topic of the document?",
    "Who is the author of the document?",
    "What are the key findings?"
]

if __name__ == "__main__":
    for question in questions:
        print(f"Question: {question}")
        answer = query_document(question)
        print(f"Answer: {answer}\n")
