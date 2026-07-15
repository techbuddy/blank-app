@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo   SafetyPulse - Windows Local Launcher
echo ==========================================

where py >nul 2>nul
if %errorlevel%==0 (
  set "PYTHON=py"
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Python was not found.
    echo Install Python 3.10 or newer from https://www.python.org/downloads/
    pause
    exit /b 1
  )
  set "PYTHON=python"
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating local virtual environment...
  %PYTHON% -m venv .venv
  if errorlevel 1 goto :error
)

echo Installing or updating required packages...
call ".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
call ".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo Starting SafetyPulse at http://localhost:8501
start "SafetyPulse" http://localhost:8501
call ".venv\Scripts\python.exe" -m streamlit run streamlit_app.py --server.address localhost --server.port 8501
exit /b 0

:error
echo.
echo SafetyPulse could not be started. Review the error shown above.
pause
exit /b 1
