from typing import Any, Dict
from graph.state import GraphState



def fallback_node(state: GraphState) -> Dict[str, Any]:


    question = state["question"]
    documents = state.get("documents", [])
    FALLBACK_MESSAGE = "I don't know based on the provided sources."

    return {"question": question, "documents": documents,"generation": FALLBACK_MESSAGE,}