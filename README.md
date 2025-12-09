# Shadow OS 💀

> A custom RAG system that streams intelligence to Even Realities G2 Smart Glasses

Shadow OS transforms your G2 glasses into an intelligent, context-aware wearable computing platform. Upload documents, build a knowledge base, and get real-time answers displayed directly in your field of vision.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 What is Shadow OS?

Shadow OS is a **Retrieval-Augmented Generation (RAG) system** that:
- Ingests documents (PDFs, text files, and more)
- Stores them in a vector database for semantic search
- Answers questions using your personal knowledge base
- Streams responses to G2 Smart Glasses via Bluetooth

Think of it as having a research assistant that lives in your glasses, always ready to pull information from your documents.

---

## ✨ Features

- **📄 Document Ingestion**: Upload `.txt` and `.pdf` files to build your knowledge base
- **🔍 Semantic Search**: Vector-based retrieval finds relevant context automatically
- **🤖 AI-Powered Answers**: Google Gemini Pro synthesizes responses from your documents
- **👓 G2 Integration**: Bluetooth Low Energy streaming to Even Realities G2 glasses
- **💻 Web Interface**: Streamlit frontend for easy document management and queries
- **🏥 Medical Database**: Optional ICD-10 medical codes integration (74,719 codes)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Git
- Even Realities G2 Smart Glasses (for hardware integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/awsomepawsome90/shadow-os.git
   cd shadow-os
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv backend_venv
   source backend_venv/bin/activate  # On Windows: backend_venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure API key**
   
   Create `backend/.env`:
   ```bash
   touch backend/.env
   ```
   
   Add your Gemini API key:
   ```
   GEMINI_API_KEY="your_api_key_here"
   ```

5. **Populate knowledge base**
   
   **Option A: Use ICD-10 Medical Database (Recommended for testing)**
   ```bash
   python setup_icd10.py
   ```
   
   **Option B: Use your own documents**
   ```bash
   # Place .txt or .pdf files in data/ directory
   python backend/ingest_docs.py
   ```

---

## 🏃 Running Shadow OS

### Start the Backend

```bash
# Using the launch script (recommended)
./run_backend.sh  # Linux/Mac
run_backend.bat    # Windows

# Or manually
./backend_venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/status/`

### Start the Frontend

```bash
# Using the launch script
./run_frontend.sh  # Linux/Mac
run_frontend.bat   # Windows

# Or manually
streamlit run frontend/app.py
```

### Connect G2 Glasses

```bash
python g2_bridge.py
```

Follow the prompts to connect and start querying your knowledge base.

---

## 📁 Project Structure

```
shadow-os/
├── backend/              # FastAPI backend
│   ├── main.py          # Main API server
│   ├── ingest_docs.py   # Document ingestion script
│   └── requirements.txt  # Python dependencies
├── frontend/            # Streamlit web interface
│   ├── app.py           # Main UI
│   └── requirements.txt
├── data/                # Knowledge base storage
│   ├── chroma_db/       # Vector database (auto-generated)
│   └── uploads/         # Temporary uploads
├── g2_bridge.py         # G2 glasses integration
├── test_brain.py        # Test script
└── setup_icd10.py       # ICD-10 database setup
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint |
| `/status/` | GET | Health check |
| `/ingest/` | POST | Upload documents |
| `/query/` | POST | Query knowledge base |
| `/db/info` | GET | Database information |
| `/db/reset` | POST | Reset database |
| `/docs` | GET | Swagger UI |

### Example Query

```bash
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Type 2 Diabetes?"}'
```

---

## 🏥 ICD-10 Medical Database

Shadow OS includes optional integration with the official CDC ICD-10-CM medical codes database:

- **74,719 diagnostic codes** from CDC/NCHS
- Natural language search over medical conditions
- AI-powered explanations optimized for G2 display

**Important**: This is for informational and educational purposes only. Never use as a replacement for professional medical diagnosis.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **LLM**: Google Gemini Pro
- **Text Processing**: LangChain
- **Hardware**: Even Realities G2 Smart Glasses (BLE)

---

## 📝 Configuration

### Environment Variables

Create `backend/.env`:

```env
GEMINI_API_KEY="your_gemini_api_key"
```

### G2 Glasses Setup

Edit `g2_bridge.py` and set your device address:

```python
G2_DEVICE_ADDRESS = "G2-1234"  # Your device address
```

Use a BLE scanner to find your device's address if needed.

---

## 🧪 Testing

Test the RAG pipeline:

```bash
python test_brain.py
```

You should see a success message with a JSON response.

---

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [GEMINI.md](GEMINI.md) - Technical specifications
- [ICD10_INTEGRATION_SUMMARY.md](ICD10_INTEGRATION_SUMMARY.md) - Medical database details

---

## 🔒 Security

- API keys stored in `.env` (git-ignored)
- Input validation on all endpoints
- File type whitelisting
- Size limits (50MB max)
- UUID-based secure file naming


---

## 🙏 Acknowledgments

- Even Realities for the G2 Smart Glasses hardware
- Google for Gemini Pro API
- The open-source community

---

**Built with 💀 by the Shadow OS team**

*Last updated: 2025-12-08*
