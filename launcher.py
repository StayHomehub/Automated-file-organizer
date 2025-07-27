#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件整理工具启动器
File Organizer Tool Launcher
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 6):
        print("错误：需要Python 3.6或更高版本")
        print("Error: Python 3.6 or higher is required")
        return False
    return True

def main():
    """主函数"""
    # 设置控制台编码
    if platform.system() == "Windows":
        os.system("chcp 65001 >nul")
    
    print()
    print("=" * 50)
    print("    文件整理工具 / File Organizer Tool")
    print("=" * 50)
    print()
    
    # 检查Python版本
    if not check_python_version():
        input("按任意键退出... / Press any key to exit...")
        return
    
    # 显示选项
    print("请选择运行模式 / Please select run mode:")
    print("1. 正常执行（实际移动文件） / Normal run (actually move files)")
    print("2. 试运行（仅预览，不移动文件） / Dry run (preview only, no file movement)")
    print()
    
    # 获取用户选择
    while True:
        choice = input("请输入选项（1或2，默认1）/ Enter choice (1 or 2, default 1): ").strip()
        if choice == "" or choice == "1":
            mode = "normal"
            break
        elif choice == "2":
            mode = "dry-run"
            break
        else:
            print("无效选择，请输入1或2 / Invalid choice, please enter 1 or 2")
    
    print()
    
    # 执行文件整理工具
    try:
        if mode == "dry-run":
            print("以试运行模式启动... / Starting in dry-run mode...")
            result = subprocess.run([sys.executable, "file_organizer.py", "--dry-run"], 
                                  capture_output=False, text=True)
        else:
            print("开始执行文件整理... / Starting file organization...")
            result = subprocess.run([sys.executable, "file_organizer.py"], 
                                  capture_output=False, text=True)
        
        print()
        if result.returncode == 0:
            print("操作已完成！/ Operation completed!")
        else:
            print("操作过程中出现错误 / Error occurred during operation")
        
        print("详细信息请查看 file_organizer.log / Check file_organizer.log for details")
        
    except FileNotFoundError:
        print("错误：找不到 file_organizer.py 文件")
        print("Error: file_organizer.py not found")
    except Exception as e:
        print(f"错误：{e}")
        print(f"Error: {e}")
    
    print()
    input("按任意键退出... / Press any key to exit...")

if __name__ == "__main__":
    main()
