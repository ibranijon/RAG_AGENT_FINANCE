import re
from typing import Any, Dict, List, Set
from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableSequence


llm = ChatOllama(model="llama3.1:latest", temperature=0)

SYSTEM_PROMPT = """You are a RAG assistant. Answer the user's question using ONLY the provided sources.
Rules:
- Do NOT restate the question.
- Do NOT write "According to [1]" / "Source [1] says" repeatedly.
- Write a single coherent answer that synthesizes the sources.
- Put citations like [1][2] at the end of the sentence they support.
- If the sources are insufficient, output exactly: I don't know based on the provided sources.
- Keep the answer concise (8 sentences maximum)."""



def _fmt_page(md: Dict[str, Any]) -> str:
    p = md.get("page_start")
    if p is None:
        p = md.get("page")
    return "?" if p is None else str(p)

def _format_documents_for_prompt(docs: List[Document]) -> str:
    parts: List[str] = []
    for i, d in enumerate(docs, 1):
        txt = (d.page_content or "").strip()
        if not txt:
            continue
        parts.append(f"[{i}] {txt}")
    return "\n\n".join(parts).strip()




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
