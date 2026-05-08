@echo off
setlocal
cd /d "%~dp0.."
uv run pytest tests/unit -v
endlocal
