import re
from typing import Any, Dict, List, Set
from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableSequence


llm = ChatOllama(model="llama3.1:latest", temperature=0)

SYSTEM_PROMPT = """You are a careful assistant answering questions using ONLY the provided sources.
Rules:
- Use citations in the form [1], [2], etc. corresponding to the numbered sources in the context.
- Every factual claim must be supported by at least one citation.
- If the context does not contain enough evidence to answer, say: "I don't know based on the provided sources."
- Do not invent sources, page numbers, or details not present in the context.
- Prefer concise, direct answers.
"""


def _fmt_page(md: Dict[str, Any]) -> str:
    p = md.get("page_start")
    if p is None:
        p = md.get("page")
    return "?" if p is None else str(p)


def _format_documents_for_prompt(docs: List[Document]) -> str:
    lines: List[str] = []
    for i, d in enumerate(docs, 1):
        md = d.metadata or {}
        src = md.get("source", "unknown")
        page = _fmt_page(md)
        chunk_id = md.get("chunk_id", "?")

        lines.append(f"[{i}] source={src} page={page} chunk_id={chunk_id}")
        lines.append(d.page_content.strip())
        lines.append("")

    return "\n".join(lines).strip()


def _to_prompt_inputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
    question = inputs["question"]
    documents = inputs.get("documents", [])
    context = _format_documents_for_prompt(documents)
    return {"question": question, "context": context}


response_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "Question: {question}\n\nSources:\n{context}\n\nAnswer:"),
    ]
)

generate: RunnableSequence = (
    RunnableLambda(_to_prompt_inputs)
    | response_prompt
    | llm
    | StrOutputParser()
)


#Format Citation


_CITATION_RE = re.compile(r"\[(\d+)\]")

def extract_citation_numbers(text: str) -> List[int]:
    nums = [int(m.group(1)) for m in _CITATION_RE.finditer(text)]
    seen: Set[int] = set()
    out: List[int] = []
    for n in nums:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out

def strip_invalid_citations(text: str, max_cite: int) -> str:
    def repl(m: re.Match) -> str:
        n = int(m.group(1))
        return m.group(0) if 1 <= n <= max_cite else ""
    return _CITATION_RE.sub(repl, text)

def format_sources_block(docs: List[Document], cited_nums: List[int]) -> str:
    lines = ["Sources:"]
    for n in cited_nums:
        idx = n - 1
        if idx < 0 or idx >= len(docs):
            continue

        md = docs[idx].metadata or {}
        src = md.get("source", "unknown")

        p_start = md.get("page_start", md.get("page"))
        p_end = md.get("page_end", p_start)

        if p_start is None:
            page_str = "?"
        elif p_end is None or p_end == p_start:
            page_str = str(p_start)
        else:
            page_str = f"{p_start}-{p_end}"

        lines.append(f"[{n}] {src}, page {page_str}")

    return "\n".join(lines)
