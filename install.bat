@echo off
setlocal
cd /d "%~dp0"

where uv >nul 2>&1
if errorlevel 1 (
    echo [ERROR] uv is not installed. Install from https://github.com/astral-sh/uv
    exit /b 1
)

echo [install] uv sync --all-extras
uv sync --all-extras
if errorlevel 1 exit /b 1

if not exist "%~dp0config.ini" (
    echo [install] creating config.ini from config.ini.example
    copy "%~dp0config.ini.example" "%~dp0config.ini" >nul
)

echo [install] running unit tests
call "%~dp0tools\run_tests.bat"
if errorlevel 1 exit /b 1

echo [install] done
endlocal
