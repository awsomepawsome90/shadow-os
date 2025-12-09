import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# --- Constants ---
# Re-using the same configuration as the main backend app for consistency.
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
SOURCE_DOCS_PATH = os.path.join(os.path.dirname(__file__), "..", "data")

# --- Supported File Loaders ---
# Maps file extensions to their corresponding LangChain loader class.
LOADER_MAPPING = {
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
}

def main():
    """
    Scans the SOURCE_DOCS_PATH for .txt and .pdf files,
    processes them, and ingests them into the ChromaDB vector store.
    """
    print("--- Shadow OS Ingestion Script ---")
    
    # --- Initialize Core Components ---
    print(f"Initializing embedding model '{EMBEDDING_MODEL_NAME}'...")
    embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    print(f"Connecting to vector store at '{CHROMA_DB_PATH}'...")
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embedding_function
    )
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )
    
    # --- Scan and Process Files ---
    documents_to_ingest = []
    for filename in os.listdir(SOURCE_DOCS_PATH):
        file_path = os.path.join(SOURCE_DOCS_PATH, filename)
        file_ext = os.path.splitext(filename)[1].lower()

        if file_ext in LOADER_MAPPING:
            print(f"Found supported file: '{filename}'")
            try:
                # Select the appropriate loader based on the file extension.
                loader_class = LOADER_MAPPING[file_ext]
                loader = loader_class(file_path)
                
                # Load and split the document into chunks.
                docs = loader.load_and_split(text_splitter)
                documents_to_ingest.extend(docs)
                print(f"  - Loaded and split into {len(docs)} chunks.")
                
            except Exception as e:
                print(f"  - ERROR: Failed to process '{filename}': {e}")
        
    # --- Ingest into ChromaDB ---
    if not documents_to_ingest:
        print("\nNo new documents to ingest.")
        return

    print(f"\nIngesting a total of {len(documents_to_ingest)} chunks into ChromaDB...")
    try:
        # The add_documents method handles embedding and storage.
        vectorstore.add_documents(documents_to_ingest, persist_directory=CHROMA_DB_PATH)
        print("--- Ingestion Complete ---")
    except Exception as e:
        print(f"--- ERROR: Failed to ingest documents: {e} ---")

if __name__ == "__main__":
    main()

