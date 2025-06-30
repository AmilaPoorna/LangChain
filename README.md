# LangChain

## What is LangChain?

LangChain is an open-source framework designed to simplify the development of applications powered by large language models (LLMs).
This repository contains tutorials and simple end-to-end projects that I have created by following the [Updated LangChain](https://www.youtube.com/watch?v=KmQOlg5YfU0&list=PLZoTAELRMXVOQPRG7VAuHL--y97opD5GQ) YouTube playlist of **Krish Naik**.
For all the end-to-end projects, Streamlit is used as the frontend. Furthermore, all the LLMs used are open source.

## General Instructions

1. **Clone the repository using:**
   ```bash
   git clone https://github.com/AmilaPoorna/LangChain.git

2. **Creating a virtual environment beforehand is highly recommended. (I personally created a Python 3.10 Conda environment.)**

3. **Install the requirements using:**
   ```bash
   pip install -r requirements.txt

## Chatbot

The chatbot uses the Ollama Gemma 3 LLM with LangChain Tracing.

### What is Ollama?
[Ollama](https://github.com/ollama/ollama) is a platform that allows users to run and manage large language models (LLMs) locally on their computers.

The model takes a user prompt as input and responds with output.

Run this using:
1. ```bash
   streamlit run app.py

## API

The backend is in `client.py`, which uses LangChain + FastAPI, and the frontend is in `app.py`.
The app uses Ollama Gemma 3 for generating a 100-word essay on a user-given topic, and Ollama Moondream 2 for generating a poem similarly on a user-given topic.

Run this in two separate terminals using:
1. ```bash
   python client.py
2. ```bash
   streamlit run app.py

## RAG
`simplerag.ipynb` demonstrates data ingestion methods such as TextLoader, WebBaseLoader, and PyPDFLoader.
It also demonstrates vector embedding using Ollama and vector storage into Chroma, FAISS, and Lance vector databases.

`retriever.ipynb` demonstrates how a retriever is used to return documents in a PDF ingested with PyPDFLoader, which are vector-embedded using Ollama and stored in a FAISS vector database. Ollama Gemma 3 LLM is also used here.

## Agents
`agents.ipynb` demonstrates how to create tools by combining individual tools such as Wikipedia, Arxiv, and a retriever-based tool that retrieves documents from a web page ingested with WebBaseLoader, vector-embedded using Ollama, and stored in a FAISS vector database.
Ollama Mistral LLM is used here, since models like Gemma 3 do not perform well in this context.

## Groq
The app uses Mistral-Saba-24b, called using a Groq API key, which acts as an agent. The agent uses a retriever tool to fetch documents from a web page ingested with WebBaseLoader, vector-embedded using Ollama, and stored in a FAISS vector database.

Run this using:
1. ```bash
   streamlit run app.py

## Final Project
The app uses Llama3-8b-8192, called using a Groq API key. It uses a retriever tool to fetch documents from a PDF folder ingested with PyPDFLoader, vector-embedded using Ollama, and stored in a FAISS vector database.

Run this using:
1. ```bash
   streamlit run app.py
