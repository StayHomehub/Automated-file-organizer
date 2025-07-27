#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化文件整理脚本
根据配置文件将文件按类型分类整理到指定目录
"""

import os
import json
import shutil
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import fnmatch


class FileOrganizer:
    """文件整理器主类"""
    
    def __init__(self, config_path: str = "config.json"):
        """初始化文件整理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config = self.load_config()
        self.setup_logging()
        
    def load_config(self) -> Dict:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.validate_config(config)
            return config
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"配置文件格式错误: {e}")
    
    def validate_config(self, config: Dict) -> None:
        """验证配置文件格式"""
        required_keys = ['source_directory', 'target_directories', 'settings']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"配置文件缺少必要字段: {key}")
    
    def setup_logging(self) -> None:
        """设置日志"""
        log_level = self.config['settings'].get('log_level', 'INFO')
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            handlers=[
                logging.FileHandler('file_organizer.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def should_exclude(self, filename: str) -> bool:
        """检查文件是否应该被排除"""
        exclude_patterns = self.config.get('exclude_patterns', [])
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(filename.lower(), pattern.lower()):
                return True
        return False
    
    def get_file_category(self, file_path: Path) -> Optional[str]:
        """根据文件扩展名确定文件类别"""
        extension = file_path.suffix.lower()
        target_dirs = self.config['target_directories']
        
        for category, config in target_dirs.items():
            if extension in [ext.lower() for ext in config['extensions']]:
                return category
        return None
    
    def get_target_path(self, category: str, original_path: Path) -> Path:
        """获取目标文件路径"""
        target_config = self.config['target_directories'][category]
        base_path = Path(target_config['path'])
        
        # 如果需要按日期创建子目录
        if self.config['settings'].get('create_subdirectories_by_date', False):
            date_format = self.config['settings'].get('date_format', '%Y-%m')
            date_str = datetime.fromtimestamp(original_path.stat().st_mtime).strftime(date_format)
            base_path = base_path / date_str
        
        # 确保目标目录存在
        base_path.mkdir(parents=True, exist_ok=True)
        
        return base_path / original_path.name
    
    def handle_duplicate(self, target_path: Path) -> Path:
        """处理重复文件名"""
        if not target_path.exists():
            return target_path
        
        method = self.config['settings'].get('handle_duplicates', 'rename')
        
        if method == 'skip':
            return None
        elif method == 'overwrite':
            return target_path
        elif method == 'rename':
            counter = 1
            stem = target_path.stem
            suffix = target_path.suffix
            parent = target_path.parent
            
            while True:
                new_name = f"{stem}_{counter:03d}{suffix}"
                new_path = parent / new_name
                if not new_path.exists():
                    return new_path
                counter += 1
    
    def check_file_size(self, file_path: Path) -> bool:
        """检查文件大小是否符合要求"""
        file_size = file_path.stat().st_size
        min_size = self.config['settings'].get('min_file_size', 0)
        max_size = self.config['settings'].get('max_file_size', None)
        
        if file_size < min_size:
            return False
        
        if max_size is not None and file_size > max_size:
            return False
        
        return True
    
    def move_file(self, source_path: Path, target_path: Path) -> bool:
        """移动文件到目标位置"""
        try:
            if self.config['settings'].get('dry_run', False):
                self.logger.info(f"[DRY RUN] 将移动文件: {source_path} -> {target_path}")
                return True
            
            shutil.move(str(source_path), str(target_path))
            self.logger.info(f"成功移动文件: {source_path} -> {target_path}")
            return True
        except Exception as e:
            self.logger.error(f"移动文件失败: {source_path} -> {target_path}, 错误: {e}")
            return False
    
    def organize_files(self) -> Dict[str, int]:
        """整理文件的主方法"""
        source_dir = Path(self.config['source_directory'])
        if not source_dir.exists():
            raise FileNotFoundError(f"源目录不存在: {source_dir}")
        
        stats = {
            'total_files': 0,
            'moved_files': 0,
            'skipped_files': 0,
            'errors': 0
        }
        
        self.logger.info(f"开始整理文件，源目录: {source_dir}")
        
        # 获取文件列表
        if self.config['settings'].get('recursive', False):
            files = source_dir.rglob('*')
        else:
            files = source_dir.iterdir()
        
        for item in files:
            if not item.is_file():
                continue
                
            stats['total_files'] += 1
            
            # 检查是否应该排除
            if self.should_exclude(item.name):
                self.logger.debug(f"跳过排除的文件: {item}")
                stats['skipped_files'] += 1
                continue
            
            # 检查文件大小
            if not self.check_file_size(item):
                self.logger.debug(f"跳过不符合大小要求的文件: {item}")
                stats['skipped_files'] += 1
                continue
            
            # 确定文件类别
            category = self.get_file_category(item)
            if not category:
                self.logger.debug(f"未识别的文件类型: {item}")
                stats['skipped_files'] += 1
                continue
            
            # 获取目标路径
            target_path = self.get_target_path(category, item)
            final_path = self.handle_duplicate(target_path)
            
            if final_path is None:
                self.logger.debug(f"跳过重复文件: {item}")
                stats['skipped_files'] += 1
                continue
            
            # 移动文件
            if self.move_file(item, final_path):
                stats['moved_files'] += 1
            else:
                stats['errors'] += 1
        
        self.logger.info(f"文件整理完成: 总共{stats['total_files']}个文件, 移动{stats['moved_files']}个, 跳过{stats['skipped_files']}个, 错误{stats['errors']}个")
        return stats


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='自动化文件整理脚本')
    parser.add_argument('-c', '--config', default='config.json', help='配置文件路径')
    parser.add_argument('--dry-run', action='store_true', help='试运行模式')
    
    args = parser.parse_args()
    
    try:
        organizer = FileOrganizer(args.config)
        
        # 如果命令行指定了dry-run，覆盖配置
        if args.dry_run:
            organizer.config['settings']['dry_run'] = True
        
        stats = organizer.organize_files()
        
        print(f"\n整理结果:")
        print(f"总文件数: {stats['total_files']}")
        print(f"已移动: {stats['moved_files']}")
        print(f"已跳过: {stats['skipped_files']}")
        print(f"错误数: {stats['errors']}")
        
    except Exception as e:
        logging.error(f"文件整理失败: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())