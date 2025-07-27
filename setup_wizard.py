#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件设置向导
帮助用户快速创建配置文件
"""

import json
import os
from pathlib import Path


def setup_wizard():
    """配置向导"""
    print("=" * 50)
    print("    文件整理工具配置向导")
    print("=" * 50)
    print()
    
    config = {
        "source_directory": "",
        "target_directories": {
            "documents": {
                "path": "",
                "extensions": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"]
            },
            "images": {
                "path": "",
                "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".ico"]
            },
            "videos": {
                "path": "",
                "extensions": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".3gp"]
            },
            "audio": {
                "path": "",
                "extensions": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".opus"]
            },
            "archives": {
                "path": "",
                "extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"]
            },
            "executables": {
                "path": "",
                "extensions": [".exe", ".msi", ".deb", ".rpm", ".dmg", ".pkg"]
            },
            "code": {
                "path": "",
                "extensions": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".php", ".rb", ".go", ".rs"]
            }
        },
        "settings": {
            "create_subdirectories_by_date": True,
            "date_format": "%Y-%m",
            "handle_duplicates": "rename",
            "log_level": "INFO",
            "dry_run": False,
            "recursive": False,
            "min_file_size": 0,
            "max_file_size": None
        },
        "exclude_patterns": [
            "*.tmp",
            "*.temp",
            "~*",
            ".*"
        ]
    }
    
    # 获取源目录
    print("请设置要整理的文件夹路径（例如：C:\\Users\\用户名\\Downloads）")
    source_dir = input("源文件夹路径: ").strip()
    if source_dir:
        config["source_directory"] = source_dir
    
    print()
    print("请设置各类文件的整理目标文件夹（留空使用默认值）")
    
    # 设置目标目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for category, cat_config in config["target_directories"].items():
        default_path = os.path.join(base_dir, "Organized", category.capitalize())
        user_path = input(f"{category} 文件整理到: ({default_path}) ").strip()
        
        if user_path:
            config["target_directories"][category]["path"] = user_path
        else:
            config["target_directories"][category]["path"] = default_path
    
    print()
    print("高级设置（直接按回车使用默认值）")
    
    # 日期子目录
    use_date = input("是否按日期创建子目录？(y/n, 默认y): ").strip().lower()
    if use_date == 'n':
        config["settings"]["create_subdirectories_by_date"] = False
    
    # 重复文件处理
    print("重复文件处理方式:")
    print("1. 重命名 (默认)")
    print("2. 跳过")
    print("3. 覆盖")
    duplicate_choice = input("请选择 (1-3): ").strip()
    
    if duplicate_choice == "2":
        config["settings"]["handle_duplicates"] = "skip"
    elif duplicate_choice == "3":
        config["settings"]["handle_duplicates"] = "overwrite"
    
    # 保存配置
    config_path = "config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 50)
    print("配置完成！")
    print(f"配置文件已保存为: {config_path}")
    print()
    print("使用方法:")
    print("1. 双击 '运行文件整理工具.bat'")
    print("2. 或运行: python file_organizer.py")
    print()
    print("建议先使用试运行模式检查设置！")


if __name__ == "__main__":
    setup_wizard()
    input("\n按任意键退出...")