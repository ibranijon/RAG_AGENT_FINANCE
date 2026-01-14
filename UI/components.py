import streamlit as st
from datetime import datetime

def sidebar_controls() -> None:
    st.markdown("### Controls")
    st.caption("Your RAG agent is stateless; the UI only *displays* chat history.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.status = None
            st.rerun()

    with col2:
        st.download_button(
            "Export chat",
            data=_export_chat_text(st.session_state.get("messages", [])),
            file_name="rag_chat.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        '<div class="tiny-hint">Ask questions about AI in Finance. Each question runs a fresh retrieval + generation call.</div>',
        unsafe_allow_html=True,
    )

def render_chat_history(messages: list[dict]) -> None:
    if st.session_state.get("status"):
        st.markdown(
            f"""
            <div class="status-pill">
              <div class="status-dot"></div>
              <div>{st.session_state.status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

    if not messages:
        st.markdown(
            """
            <div class="msg-row assistant">
              <div>
                <div class="bubble assistant">
                  Ask me something about <b>AI in Finance</b> (e.g., fraud detection, credit scoring, risk modeling).
                </div>
                <div class="meta">Assistant</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for m in messages:
            role = m.get("role", "assistant")
            content = m.get("content", "")
            ts = m.get("ts", "")

            if role == "user":
                st.markdown(
                    f"""
                    <div class="msg-row user">
                      <div>
                        <div class="bubble user">{_escape_html(content)}</div>
                        <div class="meta">You • {ts}</div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="msg-row assistant">
                      <div>
                        <div class="bubble assistant">{_escape_html(content)}</div>
                        <div class="meta">Assistant • {ts}</div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)

def chat_input_box() -> str | None:
    return st.chat_input("Message RAG Chat…")

def add_user_message(text: str) -> None:
    st.session_state.messages.append(
        {"role": "user", "content": text, "ts": _now_hhmm()}
    )

def add_assistant_message(text: str) -> None:
    st.session_state.messages.append(
        {"role": "assistant", "content": text, "ts": _now_hhmm()}
    )

def set_status(text: str) -> None:
    st.session_state.status = text

def clear_status() -> None:
    st.session_state.status = None

def _now_hhmm() -> str:
    return datetime.now().strftime("%H:%M")

def _export_chat_text(messages: list[dict]) -> str:
    lines = []
    for m in messages:
        role = "YOU" if m.get("role") == "user" else "ASSISTANT"
        ts = m.get("ts", "")
        content = m.get("content", "")
        lines.append(f"[{ts}] {role}:\n{content}\n")
    return "\n".join(lines).strip()

def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )
