@echo off
setlocal
cd /d "%~dp0"
call "%~dp0qr-create.bat" --url https://nrl.li/leadmagnete --width 96 --height 128 --margin 15 --output sample.png
endlocal
