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
    answer_only = generation.split("\n\nSources:", 1)[0]

    print("---HALLUCINATION: CHECK IF RESPONSE BASED ON CONTEXT---")
    grounded = hallucination_grader.invoke(
        {"documents": documents, "generation": answer_only}
    ).binary_score

    if not grounded:
        print("---RESPONSE NOT BASED ON CONTEXT, BACK TO GENERATION---")
        return GENERATE

    print("---GRADER: DOES RESPONSE ANSWER USER QUESTION---")
    answers = answer_grader.invoke(
        {"question": question, "generation": answer_only}
    ).binary_score

    if not answers:
        print("---ANSWER DOES NOT SATISFY QUESTION---")
        return FALLBACK

    print("---ANSWER IS SATISFACTORY---")
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