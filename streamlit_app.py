import streamlit as st

from UI.styles import apply_global_styles
from UI.components import (
    chat_input_box,
    footer_note,
    header,
    init_state,
    push_assistant_message,
    push_user_message,
    render_chat,
    safe_extract_generation,
)

from graph.graph_flow import app


st.set_page_config(page_title="AI Finance RAG Assistant", page_icon="💬", layout="centered")

apply_global_styles()

st.markdown('<div class="app-shell">', unsafe_allow_html=True)

init_state()
header()
st.write("")

render_chat(st.session_state.messages)

user_text = chat_input_box(disabled=st.session_state.busy)

if user_text:
    st.session_state.busy = True
    st.session_state.pending_user_query = user_text
    push_user_message(user_text)
    st.rerun()

pending = st.session_state.pending_user_query
if pending:
    with st.spinner("Thinking with retrieval…"):
        try:
            answer = app.invoke(input={"question": pending})
            response_text = safe_extract_generation(answer)
        except Exception as e:
            response_text = f"Sorry — I ran into an error while generating a response:\n\n`{e}`"

    push_assistant_message(response_text)
    st.session_state.pending_user_query = None
    st.session_state.busy = False
    st.rerun()

footer_note()

st.markdown("</div>", unsafe_allow_html=True)
