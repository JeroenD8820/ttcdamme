@echo off
chcp 65001 >nul
echo ============================================
echo   TTC Damme - Data Update Script
echo ============================================
echo.

cd /d "%~dp0"

echo [1/4] Rangschikkingen en spelersstats ophalen...
python get_all_rankings.py
if %errorlevel% neq 0 (
    echo FOUT bij get_all_rankings.py
    pause
    exit /b 1
)
echo.

echo [2/4] Teamkalenders ophalen...
python get_team_calendars.py
if %errorlevel% neq 0 (
    echo FOUT bij get_team_calendars.py
    pause
    exit /b 1
)
echo.

echo [3/4] Wedstrijddetails ophalen...
python get_match_details.py
if %errorlevel% neq 0 (
    echo FOUT bij get_match_details.py
    pause
    exit /b 1
)
echo.

echo [4/4] JSON naar data.js converteren...
python json_to_js.py
if %errorlevel% neq 0 (
    echo FOUT bij json_to_js.py
    pause
    exit /b 1
)
echo.

echo ============================================
echo   Data succesvol bijgewerkt!
echo   Open index.html in de browser om de
echo   nieuwe data te bekijken.
echo ============================================
pause
