@echo off
setlocal
set PYTHONUTF8=1
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 -B scripts\try_demo.py
  goto done
)
where python >nul 2>nul
if not errorlevel 1 (
  python -B scripts\try_demo.py
  goto done
)
echo Python 3.11+ is required. Install Python, then run this file again.
:done
pause
