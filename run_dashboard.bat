@echo off
REM Run script for Streamlit Dashboard
REM Automatically activates virtual environment and launches dashboard

echo ================================================
echo News Sentiment Dashboard - Windows Launcher
echo ================================================
echo.

REM Check if virtual environment exists
if exist venv\Scripts\activate.bat (
    echo [+] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [!] Virtual environment not found
    echo [!] Please create one: python -m venv venv
    echo [!] Then install dependencies: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Run the dashboard
echo [+] Starting Streamlit dashboard...
echo [+] Dashboard will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.
streamlit run dashboard.py

REM Deactivate virtual environment
deactivate

echo.
echo ================================================
echo Dashboard closed
echo ================================================
pause
