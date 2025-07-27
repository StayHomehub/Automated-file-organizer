@echo off
REM Set code page to 936 (Simplified Chinese GBK) to ensure stability
chcp 936 >nul

title �Զ����ļ�������

echo.
echo ================================================
echo    �Զ����ļ�������
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ����δ��⵽ Python���밲װ Python 3.6 ����߰汾��
    echo ���ص�ַ��https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Ask user for run mode
echo ��ѡ��Ҫ���е�ģʽ:
echo  1. ����ִ�У�ʵ���ƶ��ļ���
echo  2. �����У���Ԥ�������ƶ��ļ���
echo.
set /p mode=������ѡ�1 �� 2��Ĭ���� 1����

echo.
if "%mode%"=="2" (
    echo ��������ģʽ����...
    python file_organizer.py --dry-run
) else (
    echo ��ʼִ���ļ�����...
    python file_organizer.py
)

echo.
echo ��������ɣ�
echo ��ϸ��Ϣ��鿴 file_organizer.log
pause