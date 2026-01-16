RAG Agent for AI in Finance

A Retrieval-Augmented Generation (RAG) agent specialized in AI in finance, built to answer domain-specific questions using a curated collection of academic and professional documents. The system retrieves relevant context from PDFs and generates grounded responses using local LLMs.

The project runs entirely locally using Ollama, ChromaDB, LangChain, and LangGraph, and exposes the agent through a chat-based Streamlit interface.

Key Features

Domain-specific RAG pipeline focused on AI in finance

Local embeddings and generation via Ollama

Persistent Chroma vector store

Controlled retrieval and generation flow using LangGraph

Interactive chat UI built with Streamlit

Project Structure
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

Models (Ollama)

This project requires Ollama with the following models installed locally:

Embedding model: nomic-embed-text:latest

LLM: llama3.1:latest

Pull the models before running the project:

ollama pull nomic-embed-text:latest
ollama pull llama3.1:latest


Make sure the Ollama service is running.

Dependencies

Install the required Python dependencies:

beautifulsoup4>=4.14.3
black>=25.12.0
chromadb>=1.4.0
isort>=7.0.0
langchain>=1.2.3
langchain-chroma>=1.1.0
langchain-community>=0.4.1
langchain-ollama>=1.0.1
langgraph>=1.0.6
pdfplumber>=0.11.9
pytest>=9.0.2
streamlit>=1.52.2
tiktoken>=0.12.0


Use your preferred environment manager (uv, pip, or venv).

Required Setup: Dataset Folder

You must create a folder named exactly:

Dataset

Requirements

Located in the project root

Case-sensitive

Contains all PDF documents used by the agent

Example:

project-root/
├─ Dataset/
│   ├─ paper1.pdf
│   ├─ paper2.pdf
│   └─ report.pdf


⚠️ If this folder is missing or misnamed, ingestion will fail.

Running the Project
1. Run Ingestion (Required First)

The ingestion step must be executed before starting the agent.

python ingestion.py


This step:

Loads PDFs from Dataset/

Cleans and chunks documents

Generates embeddings using nomic-embed-text:latest

Stores vectors in a local Chroma database

Re-run ingestion if you add, remove, or modify documents.

2. Launch the Agent UI

After ingestion completes successfully:

streamlit run streamlit_app.py


This starts a local Streamlit server and opens a browser-based chat interface where you can interact with the AI-in-finance agent.

Usage Notes

Questions are answered strictly based on ingested documents

The agent runs fully locally once models are installed

Answer quality depends on the quality and relevance of the provided PDFs

Quick Start Summary

Install dependencies

Install Ollama and pull required models

Create the Dataset/ folder in the project root

Add PDF documents to Dataset/

Run python ingestion.py

Run streamlit run streamlit_app.py

You now have a locally running RAG agent for AI in finance accessible through a chat interface.