@echo off
REM Set code page to 936 (Simplified Chinese GBK) to ensure stability
chcp 936 >nul

title 自动化文件整理工具

echo.
echo ================================================
echo    自动化文件整理工具
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未检测到 Python。请安装 Python 3.6 或更高版本。
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Ask user for run mode
echo 请选择要运行的模式:
echo  1. 正常执行（实际移动文件）
echo  2. 试运行（仅预览，不移动文件）
echo.
set /p mode=请输入选项（1 或 2，默认是 1）：

echo.
if "%mode%"=="2" (
    echo 以试运行模式启动...
    python file_organizer.py --dry-run
) else (
    echo 开始执行文件整理...
    python file_organizer.py
)

echo.
echo 操作已完成！
echo 详细信息请查看 file_organizer.log
pause