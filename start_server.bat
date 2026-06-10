@echo off
chcp 65001 >nul
echo ============================================
echo   TTC Damme - Lokale Server Starten
echo ============================================
echo.

cd /d "%~dp0"

echo Controleren of Flask geinstalleerd is...
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo Flask niet gevonden - installeren...
    python -m pip install flask
    if %errorlevel% neq 0 (
        echo FOUT: Flask kon niet geinstalleerd worden.
        echo Probeer handmatig: python -m pip install flask
        pause
        exit /b 1
    )
    echo Flask succesvol geinstalleerd!
) else (
    echo Flask is al geinstalleerd.
)

echo.
echo ============================================
echo   Server starten op http://localhost:5000
echo   Open deze URL in je browser.
echo   Druk op CTRL+C om te stoppen.
echo ============================================
echo.
python server.py
pause
