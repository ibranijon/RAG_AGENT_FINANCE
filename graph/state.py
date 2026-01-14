from typing import TypedDict, List
from langchain_core.documents import Document


class GraphState(TypedDict, total=False):
    question : str
    generation : str
    ground_truth : bool
    documents : List[Document]