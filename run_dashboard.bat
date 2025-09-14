@echo off
echo Starting Marketing Intelligence Dashboard...
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import streamlit, pandas, plotly, numpy" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

REM Check if data files exist
if not exist "data\business.csv" (
    echo Error: data\business.csv not found
    pause
    exit /b 1
)

if not exist "data\Facebook.csv" (
    echo Error: data\Facebook.csv not found
    pause
    exit /b 1
)

if not exist "data\Google.csv" (
    echo Error: data\Google.csv not found
    pause
    exit /b 1
)

if not exist "data\TikTok.csv" (
    echo Error: data\TikTok.csv not found
    pause
    exit /b 1
)

echo All checks passed. Starting dashboard...
echo Dashboard will be available at: http://localhost:8501
echo ================================================

REM Start the dashboard
python -m streamlit run app.py --server.port 8501 --server.address localhost --browser.gatherUsageStats false

pause
