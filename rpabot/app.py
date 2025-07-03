import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from dotenv import load_dotenv
import hashlib
import pickle

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

prompt = ChatPromptTemplate.from_template(
    """
    You are a warm, friendly assistant named RPABot that specializes in robotic process automation. 
    Your goal is to be helpful while maintaining clear boundaries about your knowledge domain.
    
    Guidelines:
    1. Always be polite, cheerful, and approachable in your tone.
    2. If the question is answerable from the exact context:
       - Respond precisely using only the provided context
       - Keep answers clear and concise
    3. If the question is clearly within the robotic process automation domain (even if not in context):
       - Answer helpfully while noting when you're going beyond the provided materials
       - Example: "While not in my materials, typically in robotic process automation we..."
    4. For completely unrelated questions (e.g., weather, personal advice):
       - Gently explain you specialize in robotic process automation
       - Example: "I'm afraid I don't have information about that topic."
    5. For greetings/small talk:
       - Respond warmly but briefly, then guide toward robotic process automation
    
    <context>
    {context}
    </context>
    Question: {input}
    """
)

PDF_FOLDER = "./materials"
VECTORSTORE_FILE = "vectorstore.pkl"
HASH_FILE = "content_hash.txt"

def calculate_content_hash():
    hasher = hashlib.sha256()
    for root, _, files in os.walk(PDF_FOLDER):
        for file in files:
            if file.endswith('.pdf'):
                filepath = os.path.join(root, file)
                with open(filepath, 'rb') as f:
                    hasher.update(f.read())
    return hasher.hexdigest()

def save_content_hash(content_hash):
    with open(HASH_FILE, 'w') as f:
        f.write(content_hash)

def load_content_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            return f.read().strip()
    return None

def create_vectorstore():
    embeddings = OllamaEmbeddings()
    loader = PyPDFDirectoryLoader(PDF_FOLDER)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs)
    vectors = FAISS.from_documents(final_documents, embeddings)
    
    with open(VECTORSTORE_FILE, 'wb') as f:
        pickle.dump(vectors, f)
    
    current_hash = calculate_content_hash()
    save_content_hash(current_hash)
    
    return vectors

def load_vectorstore():
    current_hash = calculate_content_hash()
    saved_hash = load_content_hash()
    
    if current_hash == saved_hash and os.path.exists(VECTORSTORE_FILE):
        with open(VECTORSTORE_FILE, 'rb') as f:
            return pickle.load(f)
    
    return create_vectorstore()

if "vectors" not in st.session_state:
    st.session_state.vectors = load_vectorstore()

st.title("RPABot")
st.write("Ask me anything related to robotic process automation...")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({'input': user_input})
    
    with st.chat_message("assistant"):
        st.markdown(response['answer'])
    
    st.session_state.messages.append({"role": "assistant", "content": response['answer']})