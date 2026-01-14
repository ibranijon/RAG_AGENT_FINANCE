from typing import Any, Dict
from graph.state import GraphState
from ingestion_retrival import retriever



def retrieve_node(state: GraphState) -> Dict[str,Any]:
    print("RETRIVE NODE")

    question = state["question"]
    documents = retriever.invoke(question)

    return {'question':question,'documents':documents}


