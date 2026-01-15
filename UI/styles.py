import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #FFF7ED;
            --card: rgba(255,255,255,0.75);
            --border: rgba(120, 53, 15, 0.18);
            --text: #2B1B12;
            --muted: rgba(43, 27, 18, 0.70);
            --accent: #FB923C;
            --accent2: #F97316;
            --shadow: 0 10px 30px rgba(43, 27, 18, 0.10);
            --radius: 18px;
        }

        .stApp {
            background: radial-gradient(1200px 700px at 15% 0%, rgba(251, 146, 60, 0.18), transparent 55%),
                        radial-gradient(1100px 700px at 85% 10%, rgba(249, 115, 22, 0.16), transparent 55%),
                        linear-gradient(180deg, var(--bg), #FFFFFF);
            color: var(--text);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .app-shell {
            max-width: 980px;
            margin: 0 auto;
        }

        .topbar {
            padding: 18px 18px 6px 18px;
            border: 1px solid var(--border);
            background: var(--card);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
        }

        .topbar h1 {
            font-size: 1.25rem;
            margin: 0;
            line-height: 1.2;
        }

        .topbar p {
            margin: 6px 0 0 0;
            color: var(--muted);
            font-size: 0.95rem;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 10px;
            padding: 7px 10px;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: rgba(255,255,255,0.65);
            color: var(--muted);
            font-size: 0.85rem;
        }

        .dot {
            width: 9px;
            height: 9px;
            border-radius: 999px;
            background: linear-gradient(180deg, var(--accent), var(--accent2));
            box-shadow: 0 0 0 4px rgba(251, 146, 60, 0.20);
        }

        [data-testid="stChatInput"] {
            padding-top: 8px !important;
            padding-left: 0 !important;     /* removes the left grey gutter */
            padding-right: 0 !important;
            background: transparent !important;
        }

        /* Streamlit adds padding on inner wrappers too */
        [data-testid="stChatInput"] > div {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        [data-testid="stChatInput"] > div > div {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }

        /* Your textarea styling + force where text starts */
        [data-testid="stChatInput"] textarea {
            border-radius: 16px !important;
            border: 1px solid rgba(120, 53, 15, 0.22) !important;
            background: rgba(255,255,255,0.95) !important;
            color: var(--text) !important;

            padding-left: 16px !important;   /* aligns text to the start */
            padding-right: 56px !important;  /* space for the send icon */
            margin: 0 !important;
        }

        /* Optional: some Streamlit versions use baseweb wrapper background */
        [data-testid="stChatInput"] [data-baseweb="textarea"] {
            background: transparent !important;
        }

        /* ===== ADD THIS to align answers with the input start ===== */
        [data-testid="stChatMessage"] {
            border: 1px solid rgba(120, 53, 15, 0.10);
            background: rgba(255,255,255,0.62);
            box-shadow: 0 8px 22px rgba(43, 27, 18, 0.06);

            padding-left: 16px !important;
            padding-right: 16px !important;
        }
        .disclaimer {
            margin-top: 8px;
            color: var(--muted);
            font-size: 0.85rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
