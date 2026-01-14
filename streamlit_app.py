from dotenv import load_dotenv
import streamlit as st
from graph.graph_flow import app

from UI.styles import inject_global_css
from UI.components import (
    sidebar_controls,
    render_chat_history,
    chat_input_box,
    add_user_message,
    add_assistant_message,
    set_status,
    clear_status,
)

load_dotenv()

st.set_page_config(
    page_title="RAG Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "status" not in st.session_state:
    st.session_state.status = None
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

with st.sidebar:
    sidebar_controls()

st.markdown('<div class="app-shell">', unsafe_allow_html=True)

st.markdown(
    """
    <div class="topbar">
      <div class="brand">
        <div class="brand-dot"></div>
        <div class="brand-title">RAG Chat</div>
        <div class="brand-subtitle">AI in Finance</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Always render whatever we have so far (including the user's newest message)
render_chat_history(st.session_state.messages)

# ---- Phase 2: if we have a pending question, run the model now ----
if st.session_state.pending_question:
    q = st.session_state.pending_question
    set_status("Thinking…")

    with st.spinner(""):
        try:
            result = app.invoke(input={"question": q})
            generation = result.get("generation", "")
        except Exception as e:
            generation = f"Something went wrong while running the agent:\n\n{e}"

    clear_status()
    add_assistant_message(generation)

    st.session_state.pending_question = None
    st.rerun()

# ---- Phase 1: accept new input and rerun immediately ----
user_text = chat_input_box()
if user_text:
    add_user_message(user_text)
    st.session_state.pending_question = user_text
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
