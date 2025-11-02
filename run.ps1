# Run script for News Sentiment Analysis (PowerShell)
# Automatically activates virtual environment and runs main application

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "News Sentiment Analysis - PowerShell Launcher" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "[+] Activating virtual environment..." -ForegroundColor Green
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "[!] Virtual environment not found" -ForegroundColor Red
    Write-Host "[!] Please create one: python -m venv venv" -ForegroundColor Yellow
    Write-Host "[!] Then install dependencies: pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Run the application
Write-Host "[+] Starting application..." -ForegroundColor Green
Write-Host ""
python main.py

# Deactivate virtual environment
deactivate

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Application closed" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"
