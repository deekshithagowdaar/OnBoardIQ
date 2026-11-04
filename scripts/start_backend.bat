@echo off
echo Starting OnboardIQ Backend (FastAPI)...
cd /d "%~dp0\..\backend"
if exist "..\venv\Scripts\activate.bat" (
    call "..\venv\Scripts\activate.bat"
)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
