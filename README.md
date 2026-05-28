# Multi-Agent LangChain Chatbot (Cars & Bikes)

A step-by-step revision guide and reference manual for building your first LangChain + FastAPI + LangServe application.

---

## 💡 Quick Overview of the Project
This project runs a local API server using **FastAPI** and **LangServe** that hosts two distinct chatbot agents:
1. **`/carbot` (Car Bot)**: Powered by a local **Ollama** model (`llama3.2`). Instructed to only talk about cars, and refer users asking about bikes to the Bike Bot.
2. **`/bikebot` (Bike Bot)**: Powered by **Groq** (`llama-3.1-8b-instant`). Instructed to only talk about bikes, and refer users asking about cars to the Car Bot.

---

## 🛠️ Step 1: Environment Setup

Before writing code, we set up a dedicated sandbox environment to manage Python dependencies.

1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```
2. **Activate the Virtual Environment**:
   * **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * **macOS / Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   We define our dependencies in [requirements.txt](file:///d:/langchain/chatbot/requirements.txt):
   ```text
   langchain
   langchain-community
   langchain-core
   fastapi
   uvicorn
   langserve[all]
   langchain_groq
   ```
   Install them using:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧠 Step 2: Understanding the LangChain Architecture

Our application is built on three core pillars of LangChain:

### 1. Prompts (`ChatPromptTemplate`)
Instead of sending raw user input directly to the LLM, we structure it with system instructions:
* **System Message**: Tells the model *who* it is, *what* rules to follow, and *how* to react to specific topics (e.g., restricting Carbot to only cars).
* **User Message**: Passes the dynamic input from the user (`{question}`).

### 2. Models (`ChatOllama` & `ChatGroq`)
* **`ChatOllama`**: Connects to your locally running Ollama instance to run models like `llama3.2` locally on your computer.
* **`ChatGroq`**: Connects to the cloud-hosted Groq API for lightning-fast inference on models like `llama-3.1-8b-instant`.

### 3. Chains (LangChain Expression Language - LCEL)
We connect these pieces using the pipe operator (`|`):
```python
chain = prompt | llm | StrOutputParser()
```
* **How it works**: 
  1. The user's `{question}` is injected into the `prompt`.
  2. The formatted prompt is sent to the `llm` (Ollama or Groq).
  3. The `StrOutputParser` extracts the plain text response from the model's output envelope.

---

## 🌐 Step 3: Exposing the Chains via FastAPI & LangServe

To make our chatbot accessible over the web, we use:
* **FastAPI**: The web framework that manages the server and requests.
* **LangServe**: A package that automatically generates REST API endpoints (like `input`, `invoke`, `stream`) and an interactive **Playground UI** for any LangChain chain.

We add our routes using `add_routes`:
```python
add_routes(app, chain, path="/carbot")
add_routes(app, chain2, path="/bikebot")
```

---

## 📝 Step-by-Step Code Walkthrough

Here is the exact code in [app.py](file:///d:/langchain/chatbot/app.py) explained line-by-line:

```python
from fastapi import FastAPI
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes
import uvicorn
from langchain_groq import ChatGroq
import os

# 1. Initialize our FastAPI web application
app = FastAPI(
    title="langchain llama 3.2 bot",
    description="this is my first langchain app",
    version="1.0"
)

# 2. Configure credentials for Groq API
os.environ["GROQ_API_KEY"] = "gsk_Yx9..."

# 3. Instantiate the LLM clients
# llm uses local Ollama (Llama 3.2)
llm = ChatOllama(model="llama3.2")
# llm2 uses Groq API (Llama 3.1 8B Instant)
llm2 = ChatGroq(model="llama-3.1-8b-instant")

# 4. Define Prompt Templates
prmt = ChatPromptTemplate.from_messages([
    ("system", "you are a assistant created by divyansh kharkwal and you give the results only related to cars, dont provide any information other than cars ,if anybody asks for bikes you suggest to go to my other partner assistant bikebot and also if he greets so greet him well "),
    ("user", "{question}")
])

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "you are a grok model and u are designed to do the specific task only which is to provide the data of bikes only,dont provide any information other than bikess, if anybody asks for cars you suggest to go to my other partner assistant Carbot also if he greets so greet him "),
    ("user", "{question}")
])

# 5. Build Chains using LCEL (Prompt -> LLM -> String Output)
chain = prmt | llm | StrOutputParser()
chain2 = prompt2 | llm2 | StrOutputParser()

# 6. Expose the chains as API routes
add_routes(app, chain, path="/carbot")
add_routes(app, chain2, path="/bikebot")

# 7. Start the Uvicorn web server
if __name__ == "__main__":
    uvicorn.run(app, port=8888)
```

---

## 🚀 How to Run & Use the Application

### 1. Start Ollama (Required for Carbot)
Make sure Ollama is running locally on your machine and you have pulled the `llama3.2` model:
```bash
ollama run llama3.2
```

### 2. Run the FastAPI Server
To prevent character encoding errors on Windows when LangServe prints fancy startup banners, run the app with UTF-8 mode enabled:
```powershell
$env:PYTHONUTF8=1
.\venv\Scripts\python.exe app.py
```

### 3. Open the Playgrounds
Once the server starts up, you can interact with your bots using LangServe's auto-generated web UIs:
* 🚗 **Car Bot Playground**: [http://127.0.0.1:8888/carbot/playground/](http://127.0.0.1:8888/carbot/playground/)
* 🏍️ **Bike Bot Playground**: [http://127.0.0.1:8888/bikebot/playground/](http://127.0.0.1:8888/bikebot/playground/)

---

## 🎯 Key Learnings & Takeaways
1. **LCEL (LangChain Expression Language)** simplifies creating pipelines by piping components using `|`.
2. **System Prompts** are highly effective at enforcing constraints (e.g. "only discuss cars" or "only discuss bikes").
3. **LangServe** bridges the gap between Python logic and standard REST APIs with zero boilerplate code.
4. **Environment Variables** (like `GROQ_API_KEY`) are the standard way to securely pass API keys to libraries.
