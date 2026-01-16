# RAG Agent for AI in Finance

A **Retrieval-Augmented Generation (RAG)** agent specialized in AI in finance, built to answer domain-specific questions using a curated collection of academic and professional documents. The system retrieves relevant context from PDFs and generates grounded responses using local LLMs.

The project runs entirely locally using **Ollama**, **ChromaDB**, **LangChain**, and **LangGraph**, and exposes the agent through a chat-based **Streamlit** interface.

---

## Key Features

* **Domain-specific RAG pipeline** focused on AI in finance.
* **Local embeddings and generation** via Ollama.
* **Persistent Chroma vector store** for efficient retrieval.
* **Controlled flow** using LangGraph for robust node-based logic.
* **Interactive chat UI** built with Streamlit.

---

## Project Structure

```text
project-root/
│
├─ Dataset/                # REQUIRED (must be created manually)
│   └─ *.pdf               # PDF documents for ingestion
│
├─ ingestion.py             # Builds the Chroma vector store
├─ streamlit_app.py         # Launches the chat UI
│
├─ graph/                   # LangGraph nodes, chains, and flow logic
├─ UI/                      # Streamlit UI components and styles
│   ├─ styles.py
│   └─ components.py
│
└─ README.md

```

---

## Models (Ollama)

This project requires [Ollama](https://ollama.com/) with the following models installed locally:

* **Embedding model:** `nomic-embed-text:latest`
* **LLM:** `llama3.1:latest`

Pull the models before running the project:

```bash
ollama pull nomic-embed-text:latest
ollama pull llama3.1:latest

```

> **Note:** Make sure the Ollama service is running in the background.

---

## Dependencies

Install the required Python dependencies using your preferred environment manager (`uv`, `pip`, or `venv`):

```bash
pip install beautifulsoup4>=4.14.3 black>=25.12.0 chromadb>=1.4.0 isort>=7.0.0 langchain>=1.2.3 langchain-chroma>=1.1.0 langchain-community>=0.4.1 langchain-ollama>=1.0.1 langgraph>=1.0.6 pdfplumber>=0.11.9 pytest>=9.0.2 streamlit>=1.52.2 tiktoken>=0.12.0

```

---

## Required Setup: Dataset Folder

You **must** create a folder named exactly: `Dataset`

### Requirements

* **Location:** Project root.
* **Case-sensitive:** Must be capitalized as `Dataset`.
* **Content:** Contains all PDF documents used by the agent.

**Example:**

```text
project-root/
├─ Dataset/
│   ├─ paper1.pdf
│   ├─ paper2.pdf
│   └─ report.pdf

```

*If this folder is missing or misnamed, the ingestion process will fail.*

---

## Running the Project

### 1. Run Ingestion (Required First)

The ingestion step must be executed before starting the agent to process your documents.

```bash
python ingestion.py

```

**This step performs the following:**

1. Loads PDFs from the `Dataset/` folder.
2. Cleans and chunks the document text.
3. Generates embeddings using `nomic-embed-text:latest`.
4. Stores vectors in a local **Chroma** database.

*Re-run ingestion whenever you add, remove, or modify documents.*

### 2. Launch the Agent UI

After ingestion completes successfully, start the interface:

```bash
streamlit run streamlit_app.py

```

This starts a local Streamlit server and opens a browser-based chat interface where you can interact with the AI-in-finance agent.

---

## Usage Notes

* **Grounded Responses:** Questions are answered strictly based on the ingested documents.
* **Privacy:** The agent runs fully locally; no data leaves your machine once models are installed.
* **Quality:** Answer accuracy depends heavily on the quality and relevance of the provided PDFs.

---

## Quick Start Summary

1. **Install dependencies** via pip.
2. **Install Ollama** and pull `llama3.1` and `nomic-embed-text`.
3. **Create the `Dataset/` folder** in the project root.
4. **Add your PDF documents** to the `Dataset/` folder.
5. **Run** `python ingestion.py`.
6. **Run** `streamlit run streamlit_app.py`.