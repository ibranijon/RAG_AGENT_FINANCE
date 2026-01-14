from typing import Any, Dict
from graph.chains.retrieval_grader_chain import retrieval_grader
from graph.state import GraphState


def grade_documents_node(state: GraphState) -> Dict[str, Any]:

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state.get("documents", [])

    filtered_docs = []
    


    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score.binary_score
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)



    return {"documents": filtered_docs, "question": question,"document_relevancy":bool(filtered_docs)}