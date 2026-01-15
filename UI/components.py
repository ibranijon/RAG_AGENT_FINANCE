from __future__ import annotations

from typing import Dict, List, Optional
import streamlit as st


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hey! Ask me anything about AI in Finance — I’ll answer using the documents in my knowledge base.",
            }
        ]

    if "pending_user_query" not in st.session_state:
        st.session_state.pending_user_query = None

    if "busy" not in st.session_state:
        st.session_state.busy = False


def header() -> None:
    st.markdown(
        """
        <div class="topbar">
          <h1>AI in Finance RAG Assistant</h1>
          <p>Chat with your document-grounded assistant.</p>
          <div class="badge"><span class="dot"></span><span>RAG mode enabled</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat(messages) -> None:
    for m in messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])


def push_user_message(text: str) -> None:
    st.session_state.messages.append({"role": "user", "content": text})


def push_assistant_message(text: str) -> None:
    st.session_state.messages.append({"role": "assistant", "content": text})


def chat_input_box(disabled: bool) -> Optional[str]:
    return st.chat_input("Ask a question about AI in Finance…", disabled=disabled)


def footer_note() -> None:
    st.markdown(
        '<div class="disclaimer">Responses are grounded in retrieved finance documents.</div>',
        unsafe_allow_html=True,
    )


def safe_extract_generation(answer) -> str:
    if isinstance(answer, dict) and "generation" in answer:
        return str(answer["generation"])
    return str(answer)
