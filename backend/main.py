import os
import shutil
import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.prompts import PromptTemplate


# --- Settings ---
# Load settings from environment variables. Create a .env file for this.
class Settings(BaseSettings):
    gemini_api_key: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".env")

settings = Settings()

# --- Constants ---
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "uploads")
G2_OUTPUT_MAX_LENGTH = 200

# --- Generative AI Configuration ---
# You must set your GEMINI_API_KEY in a .env file in the backend directory.
genai.configure(api_key=settings.gemini_api_key)
llm = genai.GenerativeModel('models/gemini-pro-latest')

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Shadow OS Backend",
    description="API for ingesting data and streaming intelligence to G2 glasses.",
    version="0.1.0"
)

# --- Embedding Function ---
embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)

# --- ChromaDB Initialization ---
vectorstore = Chroma(
    persist_directory=CHROMA_DB_PATH,
    embedding_function=embedding_function
)

# --- Text Processing Configuration ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len
)

# --- API Models ---
class QueryRequest(BaseModel):
    question: str

# --- RAG Prompt Template ---
# This template is key. It instructs the LLM to synthesize an answer
# from the retrieved context.
rag_template = """
IDENTITY: YOU ARE A TACTICAL HUD ASSISTANT.
MISSION: ANALYZE CONTEXT AND PROVIDE A RESPONSE TO THE QUESTION.
STYLE: TELEGRAM-LIKE, UPPERCASE. NO MARKDOWN OR EMOJIS.
CONSTRAINTS: RESPONSE MUST BE UNDER 200 CHARACTERS.

CONTEXT:
---
{context}
---

QUESTION:
{question}

RESPONSE:
"""
rag_prompt = PromptTemplate.from_template(rag_template)


@app.post("/ingest/")
async def ingest_file(file: UploadFile = File(...)):
    """
    Handles .txt file uploads, processes them, and stores them in ChromaDB.
    """
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported.")

    temp_file_path = os.path.join(UPLOADS_DIR, file.filename)
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        loader = TextLoader(temp_file_path, encoding="utf-8")
        documents = loader.load()
        docs = text_splitter.split_documents(documents)
        vectorstore.add_documents(docs, persist_directory=CHROMA_DB_PATH)
        
        return {"status": "success", "filename": file.filename, "chunks_added": len(docs)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/query/")
def query_engine(query: QueryRequest):
    """
    Retrieves relevant context from ChromaDB and generates an answer using an LLM.
    Formats the output for G2 glasses.
    """
    try:
        # 1. Retrieve the 3 most relevant document chunks from the vector store.
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(query.question)
        
        # Combine the content of the retrieved documents into a single context string.
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        # 2. Format the prompt with the retrieved context and the user's question.
        formatted_prompt = rag_prompt.format(context=context, question=query.question)

        # 3. Generate an answer using the LLM.
        response = llm.generate_content(formatted_prompt)
        full_answer = response.text

        # 4. Format the output for the G2 glasses display.
        # Truncate and convert to uppercase for readability on the waveguide.
        g2_output = full_answer[:G2_OUTPUT_MAX_LENGTH].upper()

        return {
            "full_answer": full_answer,
            "g2_output": g2_output,
            "context_used": context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")


@app.get("/")
def read_root():
    return {"message": "Shadow OS is online. Ready to receive intelligence."}

# G2 Summary: FastAPI backend (`main.py`) created. Core endpoint `/ingest/` handles `.txt` uploads. It chunks text with `RecursiveCharacterTextSplitter` and embeds it into a persistent ChromaDB vector store using `all-MiniLM-L6-v2`.
