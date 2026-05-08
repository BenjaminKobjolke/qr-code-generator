@echo off
setlocal
cd /d "%~dp0"

echo [update] uv lock --upgrade
uv lock --upgrade
if errorlevel 1 exit /b 1

echo [update] uv sync --all-extras
uv sync --all-extras
if errorlevel 1 exit /b 1

echo [update] ruff check
uv run ruff check
if errorlevel 1 exit /b 1

echo [update] ruff format --check
uv run ruff format --check
if errorlevel 1 exit /b 1

echo [update] mypy
uv run mypy app
if errorlevel 1 exit /b 1

echo [update] tests
call "%~dp0tools\run_tests.bat"
if errorlevel 1 exit /b 1

echo [update] done
endlocal
