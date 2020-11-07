@echo off
setlocal enabledelayedexpansion
cd %~dp0

pyinstaller main.py --onefile --noconsole
copy dist\main.exe rpos.exe
