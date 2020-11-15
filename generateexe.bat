@echo off
setlocal enabledelayedexpansion
cd %~dp0

pyinstaller main.py --onefile --noconsole --icon="./resource/rpos_icon.ico"
copy dist\main.exe rpos.exe
