# 🧠 RAG Agent for AI in Finance

A **Retrieval-Augmented Generation (RAG)** system designed to answer **finance-focused AI questions** using a local knowledge base of academic and professional PDFs.  
The agent retrieves relevant document context and produces grounded responses using locally hosted language models.

The entire stack runs **offline** with **Ollama**, **ChromaDB**, **LangChain**, and **LangGraph**, and is accessed through a **chat-style Streamlit interface**.

---

## ✨ Core Capabilities

- Specialized question answering for **AI in finance**
- Fully **local inference and embeddings**
- Persistent vector storage via **Chroma**
- Deterministic retrieval and generation control using **LangGraph**
- Interactive conversational UI powered by **Streamlit**

---

## 📁 Repository Layout

```text
project-root/
│
├─ Dataset/                 # REQUIRED – created manually
│   └─ *.pdf                # Source documents for ingestion
│
├─ ingestion.py             # Builds and persists the vector database
├─ streamlit_app.py         # Starts the chat interface
│
├─ graph/                   # LangGraph flow, nodes, and chains
├─ UI/                      # Streamlit styles and UI components
│   ├─ styles.py
│   └─ components.py
│
└─ README.md
