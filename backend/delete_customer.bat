@echo off
cd /d "%~dp0"
echo.
echo === Communication LTD - manage customers ===
echo.
if exist "venv\Scripts\python.exe" (
  venv\Scripts\python.exe delete_customer.py %*
) else (
  python delete_customer.py %*
)
echo.
pause
