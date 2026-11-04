#!/usr/bin/env bash
echo "Starting OnboardIQ Backend (FastAPI)..."
cd "$(dirname "$0")/../backend" || exit
if [ -f "../venv/bin/activate" ]; then
    source "../venv/bin/activate"
fi
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
