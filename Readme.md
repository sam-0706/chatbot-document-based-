# Chatbot Document-Based Application

This repository contains the code for a chatbot application that processes documents. Below are the instructions to set up the environment, install dependencies, and run the application.

## Clone the Repository

To get started, clone this repository to your local machine using the following command:

```bash
git clone https://github.com/sam-0706/chatbot-document-based-.git
```

Navigate into the cloned repository:

```bash
cd chatbot-document-based-
```

## Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. To create and activate a virtual environment, follow these steps:

### On Windows:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```

### On macOS/Linux:

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

## Install Requirements

Once the virtual environment is activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

To start the Streamlit application, run the following command:

```bash
streamlit run openai+HF.py
```

This will launch the application in your default web browser. If it does not open automatically, copy the URL shown in the terminal and paste it into your browser.

---

For any issues or queries, feel free to raise an issue in the repository or contact the maintainer.

