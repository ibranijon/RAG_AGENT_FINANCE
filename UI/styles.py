import streamlit as st

def inject_global_css() -> None:
    st.markdown(
        """
        <style>
          :root {
            --bg: #0b0f19;
            --panel: #0f1629;
            --panel-2: #0c1222;
            --text: #e8eefc;
            --muted: #a7b3d3;
            --border: rgba(255,255,255,0.08);
            --user: #1a2a52;
            --assistant: #0f1629;
            --accent: #7aa2ff;
            --shadow: 0 10px 30px rgba(0,0,0,0.35);
            --radius: 16px;
          }

          html, body, [data-testid="stAppViewContainer"] {
            background: radial-gradient(1200px 800px at 20% 0%, rgba(122,162,255,0.12), transparent 60%),
                        radial-gradient(900px 700px at 80% 10%, rgba(120,255,214,0.08), transparent 55%),
                        var(--bg) !important;
            color: var(--text) !important;
          }

          [data-testid="stSidebar"] {
            background: rgba(15, 22, 41, 0.72) !important;
            border-right: 1px solid var(--border);
            backdrop-filter: blur(10px);
          }

          .app-shell {
            max-width: 920px;
            margin: 0 auto;
            padding: 18px 14px 30px 14px;
          }

          .topbar {
            position: sticky;
            top: 0;
            z-index: 10;
            padding: 10px 8px;
            margin-bottom: 14px;
            background: linear-gradient(to bottom, rgba(11,15,25,0.85), rgba(11,15,25,0));
            backdrop-filter: blur(10px);
          }

          .brand {
            display: flex;
            align-items: baseline;
            gap: 10px;
          }

          .brand-dot {
            width: 10px;
            height: 10px;
            border-radius: 999px;
            background: var(--accent);
            box-shadow: 0 0 18px rgba(122,162,255,0.55);
            margin-top: 6px;
          }

          .brand-title {
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 0.2px;
          }

          .brand-subtitle {
            font-size: 12px;
            color: var(--muted);
            margin-left: 8px;
          }

          .chat-wrap {
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding-bottom: 8px;
          }

          .msg-row {
            display: flex;
            width: 100%;
          }

          .msg-row.user { justify-content: flex-end; }
          .msg-row.assistant { justify-content: flex-start; }

          .bubble {
            max-width: 84%;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 12px 14px;
            box-shadow: var(--shadow);
            line-height: 1.55;
            white-space: pre-wrap;
            word-wrap: break-word;
          }

          .bubble.user {
            background: linear-gradient(180deg, rgba(122,162,255,0.16), rgba(122,162,255,0.06));
          }

          .bubble.assistant {
            background: rgba(15, 22, 41, 0.74);
          }

          .meta {
            font-size: 11px;
            color: var(--muted);
            margin: 6px 4px 0 6px;
          }

          .status-pill {
            display: inline-flex;
            gap: 8px;
            align-items: center;
            padding: 8px 10px;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: rgba(15,22,41,0.55);
            color: var(--muted);
            font-size: 12px;
            margin: 6px 0 10px 0;
          }

          .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: var(--accent);
            box-shadow: 0 0 14px rgba(122,162,255,0.55);
          }

          div[data-testid="stChatInput"] textarea {
            background: rgba(15, 22, 41, 0.72) !important;
            border: 1px solid var(--border) !important;
            color: var(--text) !important;
          }

          div[data-testid="stChatInput"] {
            position: sticky;
            bottom: 0;
            padding-top: 12px;
            background: linear-gradient(to top, rgba(11,15,25,0.92), rgba(11,15,25,0));
            backdrop-filter: blur(10px);
          }

          .tiny-hint {
            font-size: 12px;
            color: var(--muted);
          }
        </style>
        """,
        unsafe_allow_html=True,
    )
