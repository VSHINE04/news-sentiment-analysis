@echo off
REM Run script for News Sentiment Analysis
REM Automatically activates virtual environment and runs main application

echo ================================================
echo News Sentiment Analysis - Windows Launcher
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

REM Run the application
echo [+] Starting application...
echo.
python main.py

REM Deactivate virtual environment
deactivate

echo.
echo ================================================
echo Application closed
echo ================================================
pause
