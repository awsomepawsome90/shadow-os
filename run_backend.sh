#!/bin/bash

echo ""
echo " ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗     ██████╗ ███████╗"
echo " ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║    ██╔═══██╗██╔════╝"
echo " ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║    ██║   ██║███████╗"
echo " ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║    ██║   ██║╚════██║"
echo " ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝    ╚██████╔╝███████║"
echo " ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝      ╚═════╝ ╚══════╝"
echo ""
echo " [BACKEND] Initializing RAG Engine..."
echo " ────────────────────────────────────────────────────────────────────────"
echo ""

cd "$(dirname "$0")"

if [ ! -d "backend_venv" ]; then
    echo "[ERROR] Virtual environment not found. Run setup first."
    echo "        python3 -m venv backend_venv"
    exit 1
fi

source backend_venv/bin/activate

if [ ! -f "backend/.env" ]; then
    echo "[WARNING] backend/.env not found. Copy .env.example and add your API key."
fi

echo "[STATUS] Starting FastAPI server on http://127.0.0.1:8000"
echo "[STATUS] Press Ctrl+C to stop"
echo ""

python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
