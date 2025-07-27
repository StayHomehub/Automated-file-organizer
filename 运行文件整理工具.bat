@echo off
chcp 65001 >nul
title File Organizer Tool

echo.
echo ================================================
echo    File Organizer Tool
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not detected. Please install Python 3.6 or higher
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Ask user for run mode
echo Please select run mode:
echo 1. Normal run (actually move files)
echo 2. Dry run (preview only, no file movement)
echo.
set /p mode=Enter choice (1 or 2, default 1):

echo.
if "%mode%"=="2" (
    echo Starting in dry-run mode...
    python file_organizer.py --dry-run
) else (
    echo Starting file organization...
    python file_organizer.py
)

echo.
echo Operation completed!
echo Check file_organizer.log for details
pause