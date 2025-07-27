@echo off
title 清理测试文件
echo 正在清理测试文件...

if exist "test_source" (
    rmdir /s /q "test_source"
    echo 已删除 test_source 目录
)

if exist "test_organized" (
    rmdir /s /q "test_organized"
    echo 已删除 test_organized 目录
)

if exist "test_config.json" (
    del /f /q "test_config.json"
    echo 已删除 test_config.json 文件
)

if exist "file_organizer.log" (
    del /f /q "file_organizer.log"
    echo 已删除日志文件
)

echo.
echo 清理完成！
pause