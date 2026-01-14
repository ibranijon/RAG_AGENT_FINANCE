from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

PERSIST_DIR = "./.chroma"
COLLECTION = "rag-chroma"

llm = OllamaEmbeddings(model="nomic-embed-text:latest")

retriever = Chroma(
    collection_name=COLLECTION,
    embedding_function=llm,
    persist_directory=PERSIST_DIR,
).as_retriever(search_kwargs={"k": 5})   # This returns 5 chunks








# query = "AI impact on finance"
# docs = vs.similarity_search(query, k=5)

# print(f"Returned: {len(docs)} chunks\n")

# for i, d in enumerate(docs, 1):
#     md = d.metadata
#     print(f"[{i}] source={md.get('source')} pages={md.get('page_start')}-{md.get('page_end')} chunk_id={md.get('chunk_id')}")
#     print(d.page_content[:300].replace("\n", " "))
#     print("-" * 80)
