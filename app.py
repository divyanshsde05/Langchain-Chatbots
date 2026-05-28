from fastapi import FastAPI
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes
import uvicorn
from langchain_groq import ChatGroq
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app=FastAPI(
    title="langchain llama 3.2 bot",
    description="this is my first langchain app",
    version="1.0"
)

llm=ChatOllama(model="llama3.2")
llm2=ChatGroq(model="llama-3.1-8b-instant")

prmt=ChatPromptTemplate.from_messages(

    [
        ("system", "you are a assistant created by divyansh kharkwal and you give the results only related to cars, dont provide any information other than  cars ,if anybody asks for cars the you suggest to go to my other partner assistant bikebot and also if he greets so greet him well "),
        ("user", "{question}" )

    ]

)
prompt2=ChatPromptTemplate.from_messages(
    [
     ("system","you are a grok model and u are designed to do the specific task only which is to provide the data of bikes only,dont provide any information other than  bikess,  if anybody asks for cars the you suggest to go to my other partner assistant Carbot also if he greets so greet him "),
     ("user","{question}")
    ]
)

chain=prmt|llm|StrOutputParser()
chain2=prompt2|llm2|StrOutputParser()
add_routes(app,
chain,
path="/carbot"
)
add_routes(app,chain2,path="/bikebot")

if(__name__=="__main__"):
    uvicorn.run(app,port=8888)
