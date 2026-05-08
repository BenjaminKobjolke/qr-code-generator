@echo off
setlocal
cd /d "%~dp0.."
uv run pytest tests/integration -v
endlocal
