@echo off
if exist setup.exe (
    call setup.exe
    del setup.bat
)
python UI_main.py