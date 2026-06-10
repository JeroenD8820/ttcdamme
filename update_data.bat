@echo off
chcp 65001 >nul
echo ============================================
echo   TTC Damme - Data Update Script
echo ============================================
echo.

cd /d "%~dp0"

echo [1/5] Rangschikkingen en spelersstats ophalen...
python get_all_rankings.py
if %errorlevel% neq 0 (
    echo FOUT bij get_all_rankings.py
    pause
    exit /b 1
)
echo.

echo [2/5] Individuele ELO en klassering per speler ophalen...
python get_individual_elo.py
if %errorlevel% neq 0 (
    echo FOUT bij get_individual_elo.py
    pause
    exit /b 1
)
echo.

echo [3/5] Teamkalenders ophalen...
python get_team_calendars.py
if %errorlevel% neq 0 (
    echo FOUT bij get_team_calendars.py
    pause
    exit /b 1
)
echo.

echo [4/5] Wedstrijddetails ophalen...
python get_match_details.py
if %errorlevel% neq 0 (
    echo FOUT bij get_match_details.py
    pause
    exit /b 1
)
echo.

echo [5/5] JSON naar data.js converteren...
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
