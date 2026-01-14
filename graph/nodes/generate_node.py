from typing import Dict,Any
from graph.state import GraphState
from graph.chains.generate_chain import generate, extract_citation_numbers, strip_invalid_citations, format_sources_block

def generate_node(state : GraphState) -> Dict[str,Any]:

    question = state["question"]
    documents = state["documents"]

    answer = generate.invoke({"question": question, "documents": documents})

    answer = strip_invalid_citations(answer, max_cite=len(documents))
    cited = extract_citation_numbers(answer)

    sources = format_sources_block(documents, cited)
    final_output = f"{answer}\n\n{sources}" if cited else answer

    return {"question": question, "documents": documents, "generation": final_output}

 