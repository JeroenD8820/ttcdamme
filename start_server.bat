@echo off
chcp 65001 >nul
echo ============================================
echo   TTC Damme - Lokale Server Starten
echo ============================================
echo.

cd /d "%~dp0"

echo Controleren of Flask geïnstalleerd is...
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo Flask installeren...
    python -m pip install flask --quiet
)

echo.
echo Server starten op http://localhost:5000
echo Druk op CTRL+C om te stoppen.
echo.
python server.py
pause
