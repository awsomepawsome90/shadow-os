# Shadow OS - Quick Start Guide

## One-Command Setup (Recommended)

### Windows
```bash
# 1. Clone and navigate
git clone https://github.com/awsomepawsome90/shadow-os.git
cd shadow-os

# 2. Create virtual environment
python -m venv backend_venv
backend_venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# 4. Configure API key
copy backend\.env.example backend\.env
# Edit backend\.env and add your GEMINI_API_KEY

# 5. Launch services
# In terminal 1:
run_backend.bat

# In terminal 2:
run_frontend.bat
```

### macOS/Linux
```bash
git clone https://github.com/awsomepawsome90/shadow-os.git
cd shadow-os

python3 -m venv backend_venv
source backend_venv/bin/activate

pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

cp backend/.env.example backend/.env
# Edit backend/.env and add your GEMINI_API_KEY

# In terminal 1:
chmod +x run_backend.sh run_frontend.sh
./run_backend.sh

# In terminal 2:
./run_frontend.sh
```

## Access Points

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Frontend UI**: http://localhost:8501 (Streamlit)
- **Health Check**: http://localhost:8000/status

## Key Endpoints

### Upload Documents
```bash
curl -X POST -F "file=@document.txt" http://localhost:8000/ingest/
```

### Query RAG
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question":"What is X?"}' \
  http://localhost:8000/query/
```

### Check Status
```bash
curl http://localhost:8000/status/
```

### Reset Vector DB
```bash
curl -X POST http://localhost:8000/db/reset
```

## Testing

Test the RAG pipeline end-to-end:
```bash
backend_venv\Scripts\python test_brain.py
```

## Directory Structure

```
shadow-os/
├── backend/              # FastAPI server
│   ├── main.py          # Core API
│   ├── ingest_docs.py   # Batch ingestion
│   └── requirements.txt
├── frontend/             # Streamlit UI
│   ├── app.py
│   └── requirements.txt
├── data/
│   ├── chroma_db/       # Vector store (generated)
│   └── uploads/         # Temp file storage
├── g2_bridge.py         # Hardware integration
├── test_brain.py        # RAG test script
└── run_*.bat/.sh        # Convenience launchers
```

## Troubleshooting

**Backend won't start**: Ensure `backend/.env` exists and has `GEMINI_API_KEY`

**Frontend can't connect**: Check backend is running on port 8000

**File upload fails**: Ensure file is .txt or .pdf, and under 50MB

**Query timeout**: Backend may be overloaded; check `http://localhost:8000/status`

See `SECURITY.md` for security considerations and recommendations.
