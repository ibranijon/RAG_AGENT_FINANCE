from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

llm = ChatOllama(model='llama3.1:latest', temperature=0)


class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """You are a strict grader assessing whether a retrieved document is relevant to a user question.

Rules:
- Answer 'yes' ONLY if the document contains direct evidence that it can help answer the question.
- For named-entity questions (person, character, company name), answer 'yes' ONLY if the exact name appears in the document text.
- If the connection is vague, indirect, or you are uncertain, answer 'no'.

Return exactly 'yes' or 'no'."""
grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader