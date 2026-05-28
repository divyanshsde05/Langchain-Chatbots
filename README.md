# Multi-Agent LangChain Chatbot (Cars & Bikes)

A step-by-step revision guide and reference manual for building your first LangChain + FastAPI + LangServe application.

---

## 💡 Quick Overview of the Project
This project runs a local API server using **FastAPI** and **LangServe** that hosts two distinct chatbot agents:
1. **`/carbot` (Car Bot)**: Powered by a local **Ollama** model (`llama3.2`). Instructed to only talk about cars, and refer users asking about bikes to the Bike Bot.
2. **`/bikebot` (Bike Bot)**: Powered by **Groq** (`llama-3.1-8b-instant`). Instructed to only talk about bikes, and refer users asking about cars to the Car Bot.

--
check out the free grok api at[](https://console.groq.com/keys)
--
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
* 🏍️ **Bike Bot Playground**: [http://127.0.0.1:8888/bikebot/playground/](http://127.0.0.1:8888/bikebot/playground/)
---

## 🎯 Key Learnings & Takeaways
1. **LCEL (LangChain Expression Language)** simplifies creating pipelines by piping components using `|`.
2. **System Prompts** are highly effective at enforcing constraints (e.g. "only discuss cars" or "only discuss bikes").
3. **LangServe** bridges the gap between Python logic and standard REST APIs with zero boilerplate code.
4. **Environment Variables** (like `GROQ_API_KEY`) are the standard way to securely pass API keys to libraries.
