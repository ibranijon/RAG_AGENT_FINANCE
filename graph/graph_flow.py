from dotenv import load_dotenv

from graph.state import GraphState
from langgraph.graph import StateGraph, END
from graph.consts import GENERATE,RETRIEVE,GRADE_DOCUMENTS, FALLBACK
from graph.nodes import generate_node, grade_documents_node, retrieve_node, fallback_node
from graph.chains.hallucination_grader_chain import hallucination_grader
from graph.chains.answer_grader_chain import answer_grader

load_dotenv()

#Conditional Edge Functions

def relevancy_check(state: GraphState):
    if state.get("document_relevancy", False):
        return GENERATE
    return FALLBACK   


def response_checker(state: GraphState):
    question = state["question"]
    documents = state.get("documents", [])
    generation = state.get("generation", "")

    print("Check grounding (hallucination)")
    grounded = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    ).binary_score

    if not grounded:
        print("Not grounded -> generate back")
        return GENERATE

    print("Check if it answers the question")
    answers = answer_grader.invoke(
        {"question": question, "generation": generation}
    ).binary_score

    if not answers:
        print("answer not based")
        return FALLBACK

    print("Grounded and answers -> end")
    return END


#Nodes
workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE,retrieve_node)

workflow.add_node(GRADE_DOCUMENTS, grade_documents_node)

workflow.add_node(GENERATE, generate_node)

workflow.add_node(FALLBACK, fallback_node)



#Edges

workflow.set_entry_point(RETRIEVE)

workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)

workflow.add_conditional_edges(GRADE_DOCUMENTS, relevancy_check, {
    FALLBACK : FALLBACK,
    GENERATE : GENERATE
})


workflow.add_conditional_edges(GENERATE, response_checker, {
    FALLBACK : FALLBACK,
    GENERATE : GENERATE,
    END : END
})

workflow.add_edge(FALLBACK, END)

#App
app = workflow.compile()