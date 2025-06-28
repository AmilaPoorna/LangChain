from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes
import uvicorn
from langchain_community.llms import Ollama

app=FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server"
)

## Ollama Gemma 3
llm1=Ollama(model="gemma3:1b")
## Ollama Moondream 2
llm2=Ollama(model="moondream")

prompt1=ChatPromptTemplate.from_template("Write me an 100 word essay on {topic}.")
prompt2=ChatPromptTemplate.from_template("Write me a poem on {topic}.")

add_routes(
    app,
    prompt1|llm1,
    path="/essay"
)

add_routes(
    app,
    prompt2|llm2,
    path="/poem"
)

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)