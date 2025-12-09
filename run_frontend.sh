#!/bin/bash

echo ""
echo " ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗     ██████╗ ███████╗"
echo " ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║    ██╔═══██╗██╔════╝"
echo " ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║    ██║   ██║███████╗"
echo " ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║    ██║   ██║╚════██║"
echo " ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝    ╚██████╔╝███████║"
echo " ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝      ╚═════╝ ╚══════╝"
echo ""
echo " [FRONTEND] Launching Control Console..."
echo " ────────────────────────────────────────────────────────────────────────"
echo ""

cd "$(dirname "$0")"

if [ ! -d "backend_venv" ]; then
    echo "[ERROR] Virtual environment not found. Run setup first."
    exit 1
fi

source backend_venv/bin/activate

echo "[STATUS] Starting Streamlit UI on http://localhost:8501"
echo "[STATUS] Press Ctrl+C to stop"
echo ""

python -m streamlit run frontend/app.py --server.headless true
