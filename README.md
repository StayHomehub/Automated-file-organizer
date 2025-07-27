# 自动化文件整理工具

这是一个高效、可靠的Python脚本，能够根据文件扩展名将指定文件夹内的文件自动分类整理到预设的目录中。

## 功能特点

- 🗂️ **智能分类**: 根据文件扩展名自动识别文件类型并分类
- 📅 **日期归档**: 可按修改时间创建子目录进行归档
- 🔄 **重复处理**: 支持重命名、跳过或覆盖重复文件
- 📝 **详细日志**: 完整的操作日志记录，便于追踪和调试
- 🛡️ **安全模式**: 支持试运行模式，先预览再执行
- ⚙️ **灵活配置**: JSON配置文件，易于自定义规则和路径

## 支持的文件类型

| 类别 | 扩展名示例 |
|------|------------|
| 文档 | .pdf, .doc, .docx, .txt, .xlsx, .pptx |
| 图片 | .jpg, .png, .gif, .bmp, .svg, .webp |
| 视频 | .mp4, .avi, .mkv, .mov, .wmv, .flv |
| 音频 | .mp3, .wav, .flac, .aac, .ogg, .m4a |
| 压缩包 | .zip, .rar, .7z, .tar, .gz |
| 程序 | .exe, .msi, .deb, .dmg |
| 代码 | .py, .js, .html, .css, .java, .cpp |

## 安装使用

### 1. 环境要求

- Python 3.6 或更高版本
- 无需额外依赖库，仅使用Python标准库

### 2. 配置文件设置

编辑 `config.json` 文件，设置您的目录路径：

```json
{
  "source_directory": "C:\\Users\\您的用户名\\Downloads",
  "target_directories": {
    "documents": {
      "path": "D:\\Documents\\整理文档",
      "extensions": [".pdf", ".docx", ".txt"]
    }
  },
  "settings": {
    "create_subdirectories_by_date": true,
    "date_format": "%Y-%m",
    "handle_duplicates": "rename"
  }
}
```

### 3. 运行脚本

#### 命令行运行
```bash
# 正常运行
python file_organizer.py

# 试运行模式（仅预览，不实际移动文件）
python file_organizer.py --dry-run

# 使用自定义配置文件
python file_organizer.py -c my_config.json
```

#### 双击运行
直接双击 `file_organizer.py` 即可运行（使用默认配置）

## 配置说明

### 主要配置项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| source_directory | string | - | 源文件夹路径（需要整理的文件夹） |
| create_subdirectories_by_date | boolean | true | 是否按日期创建子目录 |
| date_format | string | "%Y-%m" | 日期格式（如2024-01） |
| handle_duplicates | string | "rename" | 重复文件处理方式：rename/skip/overwrite |
| dry_run | boolean | false | 试运行模式，只显示不执行 |
| recursive | boolean | false | 是否递归处理子目录 |
| min_file_size | int | 0 | 最小文件大小（字节） |
| max_file_size | int | null | 最大文件大小（字节） |

### 排除文件模式

在配置文件中可以设置要排除的文件模式：

```json
"exclude_patterns": [
  "*.tmp",
  "*.temp",
  "~*",
  ".*"
]
```

## 使用示例

### 示例1：整理下载文件夹

假设您的下载文件夹路径为 `C:\Users\Alice\Downloads`，想要整理到 `D:\Organized`：

1. 修改配置文件：
```json
{
  "source_directory": "C:\\Users\\Alice\\Downloads",
  "target_directories": {
    "documents": {
      "path": "D:\\Organized\\Documents",
      "extensions": [".pdf", ".doc", ".docx", ".txt"]
    },
    "images": {
      "path": "D:\\Organized\\Images",
      "extensions": [".jpg", ".png", ".gif"]
    }
  }
}
```

2. 运行脚本：
```bash
python file_organizer.py --dry-run
```

### 示例2：定期自动整理

使用Windows任务计划程序实现定期自动整理：

1. 创建批处理文件 `organize.bat`：
```batch
@echo off
cd /d E:\PythonProject
python file_organizer.py
```

2. 在Windows任务计划程序中创建基本任务，设置触发器为每天运行。

## 日志查看

脚本会生成详细的日志文件 `file_organizer.log`，包含：
- 文件移动记录
- 错误信息
- 处理统计信息

查看日志：
```bash
type file_organizer.log
```

## 常见问题

### Q1: 如何处理中文文件名？
A: 脚本完全支持中文文件名和路径，确保配置文件使用UTF-8编码。

### Q2: 文件被误移动怎么办？
A: 在试运行模式下先检查操作，所有移动操作都会记录在日志中，可根据日志手动恢复。

### Q3: 如何添加新的文件类型？
A: 在配置文件的对应类别中添加扩展名即可，如：
```json
"extensions": [".pdf", ".doc", ".新的扩展名"]
```

### Q4: 如何排除特定文件夹？
A: 在exclude_patterns中添加文件夹名称模式，如：
```json
"exclude_patterns": ["node_modules/*", "temp/*"]
```

## 故障排除

### 权限错误
- 确保对源目录和目标目录有读写权限
- 以管理员身份运行脚本

### 路径错误
- 检查配置文件中的路径是否存在
- 使用双反斜杠 `\\` 或正斜杠 `/` 作为路径分隔符

### 文件被占用
- 关闭可能使用该文件的程序
- 检查是否有其他进程锁定文件

### bat文件版本
- 如果喜欢英文界面，使用原始的批处理文件
- 如果喜欢中文界面，使用新创建的运行文件整理工具_中文.bat
- 两个文件功能完全相同，只是界面语言不同

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本文件分类和移动
- 添加配置文件支持
- 实现日志记录功能

## 技术支持

如有问题或建议，请查看日志文件或联系开发者。

## 许可证

本项目采用MIT许可证，允许自由使用和修改。