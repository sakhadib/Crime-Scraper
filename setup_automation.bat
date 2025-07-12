@echo off
REM Crime Data Scraper - Windows Automation Setup
REM This script helps set up Windows Task Scheduler for automated scraping

echo ===============================================
echo Crime Data Scraper - Windows Automation Setup
echo ===============================================
echo.

REM Get current directory
set SCRIPT_DIR=%~dp0
set PYTHON_PATH=%SCRIPT_DIR%venv\Scripts\python.exe
set MAIN_SCRIPT=%SCRIPT_DIR%main.py

echo Current directory: %SCRIPT_DIR%
echo Python path: %PYTHON_PATH%
echo Main script: %MAIN_SCRIPT%
echo.

REM Check if Python exists
if not exist "%PYTHON_PATH%" (
    echo ERROR: Python virtual environment not found!
    echo Please make sure you have set up the virtual environment correctly.
    echo Expected path: %PYTHON_PATH%
    pause
    exit /b 1
)

echo Python virtual environment found: %PYTHON_PATH%
echo.

REM Test the installation
echo Testing installation...
"%PYTHON_PATH%" "%SCRIPT_DIR%test_installation.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Installation test failed!
    echo Please fix the issues above before setting up automation.
    pause
    exit /b 1
)

echo.
echo Installation test passed!
echo.

REM Create a batch file for running the scraper
echo Creating run_scraper.bat...
echo @echo off > "%SCRIPT_DIR%run_scraper.bat"
echo cd /d "%SCRIPT_DIR%" >> "%SCRIPT_DIR%run_scraper.bat"
echo "%PYTHON_PATH%" "%MAIN_SCRIPT%" --mode full >> "%SCRIPT_DIR%run_scraper.bat"
echo Created: %SCRIPT_DIR%run_scraper.bat

echo.
echo ===============================================
echo Windows Task Scheduler Setup Instructions
echo ===============================================
echo.
echo To set up automated scraping using Windows Task Scheduler:
echo.
echo 1. Open Task Scheduler (search for "Task Scheduler" in Start menu)
echo 2. Click "Create Basic Task..." in the right panel
echo 3. Name your task (e.g., "Crime Data Scraper")
echo 4. Choose when to trigger (Daily recommended)
echo 5. Set the time (e.g., 9:00 AM)
echo 6. Choose "Start a program"
echo 7. In "Program/script" field, enter:
echo    %SCRIPT_DIR%run_scraper.bat
echo 8. In "Start in" field, enter:
echo    %SCRIPT_DIR%
echo 9. Click "Finish"
echo.
echo ===============================================
echo Alternative: Use the built-in scheduler
echo ===============================================
echo.
echo You can also use the built-in Python scheduler:
echo.
echo For daily scraping at 9 AM:
echo "%PYTHON_PATH%" "%SCRIPT_DIR%scheduler.py" --schedule daily --time 09:00
echo.
echo For hourly scraping:
echo "%PYTHON_PATH%" "%SCRIPT_DIR%scheduler.py" --schedule hourly
echo.
echo For custom interval (every 6 hours):
echo "%PYTHON_PATH%" "%SCRIPT_DIR%scheduler.py" --schedule custom --hours 6
echo.
echo ===============================================
echo Manual Testing
echo ===============================================
echo.
echo To test the scraper manually:
echo.
echo Run configuration test:
echo "%PYTHON_PATH%" "%MAIN_SCRIPT%" --mode test
echo.
echo Run full scrape:
echo "%PYTHON_PATH%" "%MAIN_SCRIPT%" --mode full
echo.
echo View statistics:
echo "%PYTHON_PATH%" "%MAIN_SCRIPT%" --mode stats
echo.
echo ===============================================

pause
