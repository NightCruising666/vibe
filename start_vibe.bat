@echo off
setlocal
cd /d "%~dp0"

echo Launching VIBE backend...
start "VIBE Backend" cmd /k "cd /d ""%~dp0backend"" && call venv\Scripts\activate && python manage.py"

echo Launching VIBE frontend...
start "VIBE Frontend" cmd /k "cd /d ""%~dp0frontend"" && pnpm dev"

echo Backend and frontend dev servers are running in their own windows.
endlocal
