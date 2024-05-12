@echo off
set "pvar=%cd%"
echo %pvar%
cd dist
python.exe "%pvar%\run.py"