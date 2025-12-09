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
echo  [FRONTEND] Launching Control Console...
echo  ────────────────────────────────────────────────────────────────────────
echo.

cd /d "%~dp0"

if not exist "backend_venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found. Run setup first.
    pause
    exit /b 1
)

call backend_venv\Scripts\activate.bat

echo [STATUS] Starting Streamlit UI on http://localhost:8501
echo [STATUS] Press Ctrl+C to stop
echo.

python -m streamlit run frontend/app.py --server.headless true

endlocal
