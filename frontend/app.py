import streamlit as st
import requests
import os

# --- Configuration ---
BACKEND_URL = "http://127.0.0.1:8000" # FastAPI backend address

# --- Streamlit UI ---
st.set_page_config(
    page_title="Shadow OS Ingestion",
    page_icon="💀",
    layout="centered",
)

st.title("Shadow OS - Intelligence Ingestion")
st.markdown("""
Upload `.txt` files containing mission intel. The system will process and store
this information in the vector database, making it available for G2 glasses.
""")

uploaded_file = st.file_uploader(
    "Choose a .txt file", 
    type="txt",
    help="Drag and drop or select a text file to upload."
)

if uploaded_file is not None:
    # Display a spinner while the file is being processed.
    with st.spinner(f"Processing `{uploaded_file.name}`..."):
        try:
            # The file object from Streamlit needs to be sent in a format
            # that the `requests` library can handle.
            files = {'file': (uploaded_file.name, uploaded_file, 'text/plain')}
            
            # Send the file to the FastAPI backend.
            response = requests.post(f"{BACKEND_URL}/ingest/", files=files)

            # Check the response from the backend.
            if response.status_code == 200:
                result = response.json()
                st.success(f"Success! `{result['filename']}` processed. Added {result['chunks_added']} intelligence chunks.")
            else:
                # Show an error if the backend failed.
                st.error(f"Error processing file: {response.text}")
        
        except requests.exceptions.ConnectionError:
            st.error("Connection Error: Could not connect to the backend. Is it running?")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# --- Instructions for running the system ---
st.sidebar.header("How to Run")
st.sidebar.markdown("""
1.  **Start the Backend:**
    ```bash
    pip install -r backend/requirements.txt
    uvicorn backend.main:app --reload
    ```
2.  **Run the Frontend:**
    ```bash
    pip install -r frontend/requirements.txt
    streamlit run frontend/app.py
    ```
""")

# G2 Summary: Streamlit frontend (`app.py`) created. Provides a simple drag-and-drop UI to upload `.txt` files. It sends files to the FastAPI `/ingest/` endpoint and displays the success or error response from the backend server.
