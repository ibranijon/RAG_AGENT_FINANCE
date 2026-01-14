from dotenv import load_dotenv


from graph.state import GraphState
from langgraph.graph import StateGraph, END
from graph.consts import WEBSEARCH,GENERATE,RETRIVE,GRADE_DOC
from graph.nodes import generate_node,grade_document_node,retrive_node,web_search_node


#from graph.chains.hallucinate_grade import hallucinate_grade
#from graph.chains.answer_grade import answer_grade


#Conditional Edge Functions

load_dotenv()

def router(state: GraphState):
    question = state['question']
    route = router_res.invoke({"question":question})


    print("First check between vectorstore and websearch")
    if route.datasource == 'vectorstore':
        print('GO TO VECTORSTORE')
        return RETRIVE
    
    elif route.datasource == 'websearch':
        print("GO TO WEBSEARCH")
        return WEBSEARCH


def decide_to_generate(state):

    if state["web_search"]:
        return WEBSEARCH
    else:
        return GENERATE


def reponse_checker(state: GraphState):


    question = state['question']
    documents = state['documents']
    generation = state['generation']

    print("Check for hallucination")
    score = hallucinate_grade.invoke({'documents': documents, 'generation': generation})



    if hallucinate_result := score.binary_score:

        print("Check Answer based or not")
        score = answer_grade.invoke({'question':question,'generation':generation})

        if answer_result := score.binary_score:

            print("ITS BASED")
            return END
        else:
            print("Its not based, back to searching")
            return WEBSEARCH

    else:
        print("its hallucinating")
        return GENERATE

workflow = StateGraph(GraphState)

#Nodes
workflow.add_node(RETRIVE,retrive_node)

workflow.add_node(GRADE_DOC, grade_document_node)

workflow.add_node(WEBSEARCH, web_search_node)

workflow.add_node(GENERATE, generate_node)



#Edges
workflow.set_conditional_entry_point(router,{
    RETRIVE : RETRIVE,
    WEBSEARCH : WEBSEARCH
})

workflow.add_edge(RETRIVE, GRADE_DOC)

workflow.add_conditional_edges(GRADE_DOC, decide_to_generate,
                               {
                                   WEBSEARCH : WEBSEARCH,
                                   GENERATE : GENERATE
                               })

workflow.add_edge(WEBSEARCH, GENERATE)

workflow.add_conditional_edges(GENERATE, reponse_checker, {
    WEBSEARCH : WEBSEARCH,
    GENERATE : GENERATE,
    END : END
})



#App
app = workflow.compile()