@echo off
echo Starting JobFlow Backend and Frontend...

start "JobFlow Backend API" cmd /k "set PYTHONPATH=backend && backend\venv\Scripts\python.exe -m uvicorn app.main:app --port 8000 --reload"

start "JobFlow Frontend UI" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers are running!
echo Dashboard: http://localhost:5173
echo API Docs:  http://localhost:8000/docs
