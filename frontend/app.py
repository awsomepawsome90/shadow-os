import os
import requests
import streamlit as st

# --- Configuration ---
DEFAULT_BACKEND = "http://127.0.0.1:8000"
BACKEND_URL = os.environ.get("SHADOW_BACKEND_URL", DEFAULT_BACKEND).rstrip("/")

# --- Simple Clean Styling ---
st.set_page_config(
    page_title="Shadow OS",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        * {font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;}
        body, .stApp {background: #ffffff; color: #1a1a1a;}
        .block-container {max-width: 600px; padding: 2rem 1rem;}
        .stButton>button {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {transform: translateY(-2px); box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);}
        .stTextArea textarea {border-radius: 8px; border: 2px solid #e0e0e0; padding: 12px;}
        .stFileUploader {border-radius: 8px;}
        .metric-box {background: #f5f7fa; padding: 16px; border-radius: 8px; margin: 10px 0;}
        h1 {color: #667eea; text-align: center; margin-bottom: 10px;}
        h2 {color: #764ba2; margin-top: 20px; margin-bottom: 15px;}
        .success-box {background: #d4edda; padding: 12px; border-radius: 8px; color: #155724; margin: 10px 0;}
        .error-box {background: #f8d7da; padding: 12px; border-radius: 8px; color: #721c24; margin: 10px 0;}
        .info-box {background: #d1ecf1; padding: 12px; border-radius: 8px; color: #0c5460; margin: 10px 0;}
    </style>
    """,
    unsafe_allow_html=True,
)


# --- Helpers ---
def ping_backend():
    try:
        resp = requests.get(f"{BACKEND_URL}/status/", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return True, data
    except Exception:
        pass
    return False, {}


def ingest_file(file_obj):
    files = {"file": (file_obj.name, file_obj, file_obj.type)}
    return requests.post(f"{BACKEND_URL}/ingest/", files=files, timeout=120)


def run_query(question: str):
    return requests.post(f"{BACKEND_URL}/query/", json={"question": question}, timeout=60)


def fetch_db_info():
    return requests.get(f"{BACKEND_URL}/db/info", timeout=10)


def reset_db():
    return requests.post(f"{BACKEND_URL}/db/reset", timeout=10)


# --- Layout ---
st.title("Shadow OS")
st.write("RAG Intelligence System for Smart Glasses")

# --- Status Bar ---
status_ok, status_data = ping_backend()
if status_ok:
    st.markdown(f"""
    <div class="info-box">
        ✓ Backend: <strong>ONLINE</strong> | Vectors: <strong>{status_data.get('vectors', '?')}</strong>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="error-box">
        × Backend: <strong>OFFLINE</strong> - Start the backend to continue
    </div>
    """, unsafe_allow_html=True)

# --- Navigation ---
mode = st.radio("What would you like to do?", ["Ask Questions", "Upload Documents"], horizontal=True)

if mode == "Ask Questions":
    st.markdown("## Ask the Brain")
    question = st.text_area(
        "Enter your question:",
        placeholder="What is the G2 protocol?",
        height=100,
        label_visibility="collapsed"
    )

    if st.button("Get Answer", type="primary", use_container_width=True, disabled=not question.strip()):
        if not status_ok:
            st.error("Backend is offline. Start it and retry.")
        else:
            with st.spinner("Thinking..."):
                resp = run_query(question)

            if resp.status_code == 200:
                data = resp.json()

                # Split layout: Glasses preview on left, info on right
                col_glasses, col_info = st.columns([1, 1])

                with col_glasses:
                    st.markdown("### G2 Display Preview")
                    g2_output = data.get("g2_output", "")

                    # G2 Glasses Display Simulator
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #1a3a52 0%, #0d1f2d 100%);
                        border: 3px solid #00d4ff;
                        border-radius: 16px;
                        padding: 24px;
                        margin: 16px 0;
                        box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
                        font-family: 'Courier New', monospace;
                        color: #00ff00;
                        text-align: center;
                        min-height: 240px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    ">
                        {g2_output[:200]}
                        <div style="margin-top: 16px; font-size: 11px; opacity: 0.8; letter-spacing: 1px;">
                            G2 DISPLAY MODE
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.caption("Live preview of what appears on the G2 waveguide display")

                with col_info:
                    st.markdown("### Full Answer")
                    st.info(data.get("full_answer", "No answer"))

                st.markdown("---")

                with st.expander("Source Context"):
                    st.text(data.get("context_used", ""))
            else:
                st.error(f"Error: {resp.text}")

else:  # Upload Documents
    st.markdown("## Upload Documents")
    uploaded_files = st.file_uploader(
        "Select files to upload (.txt or .pdf):",
        type=["txt", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if st.button("Upload & Process", type="primary", use_container_width=True, disabled=not uploaded_files):
        if not status_ok:
            st.error("Backend is offline. Start it and retry.")
        else:
            progress_bar = st.progress(0)
            for i, file in enumerate(uploaded_files):
                with st.spinner(f"Processing {file.name}..."):
                    resp = ingest_file(file)

                if resp.status_code == 200:
                    data = resp.json()
                    st.markdown(f"""
                    <div class="success-box">
                        ✓ <strong>{file.name}</strong><br>
                        {data.get('chunks_added')} chunks | Total vectors: {data.get('vector_count')}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="error-box">
                        × <strong>{file.name}</strong> failed: {resp.text}
                    </div>
                    """, unsafe_allow_html=True)

                progress_bar.progress((i + 1) / len(uploaded_files))

# --- Footer ---
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("Database Info", use_container_width=True):
        resp = fetch_db_info()
        if resp.status_code == 200:
            data = resp.json()
            st.json(data)
        else:
            st.error("Could not fetch DB info")

with col2:
    if st.button("Reset Database", use_container_width=True):
        resp = reset_db()
        if resp.status_code == 200:
            st.success("Database cleared!")
        else:
            st.error("Reset failed")
