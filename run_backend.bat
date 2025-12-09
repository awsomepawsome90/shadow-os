@echo off
setlocal

echo.
echo  ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗     ██████╗ ███████╗
echo  ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║    ██╔═══██╗██╔════╝
echo  ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║    ██║   ██║███████╗
echo  ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║    ██║   ██║╚════██║
echo  ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝    ╚██████╔╝███████║
echo  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝      ╚═════╝ ╚══════╝
echo.
echo  [BACKEND] Initializing RAG Engine...
echo  ────────────────────────────────────────────────────────────────────────
echo.

cd /d "%~dp0"

if not exist "backend_venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found. Run setup first.
    echo         python -m venv backend_venv
    pause
    exit /b 1
)

call backend_venv\Scripts\activate.bat

if not exist "backend\.env" (
    echo [WARNING] backend\.env not found. Copy .env.example and add your API key.
)

echo [STATUS] Starting FastAPI server on http://127.0.0.1:8000
echo [STATUS] Press Ctrl+C to stop
echo.

python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

endlocal
