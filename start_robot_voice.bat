@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  set "PY=py -3"
) else (
  set "PY=python"
)

%PY% -c "import tinytuya" >nul 2>nul
if errorlevel 1 (
  echo Installing required Python package tinytuya...
  %PY% -m pip install tinytuya
  if errorlevel 1 (
    echo Failed to install tinytuya. Install it manually: pip install tinytuya
    pause
    exit /b 1
  )
)

start "" "http://127.0.0.1:8780/"
%PY% app.py
pause
