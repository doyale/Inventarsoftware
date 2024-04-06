@echo off
set "pvar=%cd%"
echo %pvar%
cd dist
python.exe "%pvar%\UI_main.py"
pause