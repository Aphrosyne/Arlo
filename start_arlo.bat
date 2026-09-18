@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\arlo.exe" (
    echo [Arlo] Missing .venv\Scripts\arlo.exe
    echo Create the virtual environment and install the project first.
    pause
    exit /b 1
)

".venv\Scripts\arlo.exe" %*
set "exit_code=%ERRORLEVEL%"

if not "%exit_code%"=="0" (
    echo.
    echo [Arlo] Application exited with code %exit_code%.
    pause
)
