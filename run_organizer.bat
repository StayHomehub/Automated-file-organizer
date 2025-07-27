@echo off
chcp 65001 >nul
title File Organizer Tool

echo.
echo ================================================
echo    File Organizer Tool / 文件整理工具
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not detected. Please install Python 3.6 or higher
    echo 错误：未检测到Python。请安装Python 3.6或更高版本
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Ask user for run mode
echo Please select run mode / 请选择运行模式:
echo 1. Normal run (actually move files) / 正常执行（实际移动文件）
echo 2. Dry run (preview only, no file movement) / 试运行（仅预览，不移动文件）
echo.
set /p mode=Enter choice (1 or 2, default 1) / 请输入选项（1或2，默认1）:

echo.
if "%mode%"=="2" (
    echo Starting in dry-run mode... / 以试运行模式启动...
    python file_organizer.py --dry-run
) else (
    echo Starting file organization... / 开始执行文件整理...
    python file_organizer.py
)

echo.
echo Operation completed! / 操作已完成！
echo Check file_organizer.log for details / 详细信息请查看 file_organizer.log
pause
