# 🚀 LibreOffice Python Docker

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-311/)
[![LibreOffice](https://img.shields.io/badge/LibreOffice-24.8.6-green.svg)](https://www.libreoffice.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

基于 Docker 的文档转换服务，支持将各种办公文档格式转换为 PDF。

## ✨ 特性

- 🐳 基于 Docker，快速部署，环境隔离
- 📄 支持多种文档格式转换为 PDF
  - Microsoft Word (DOC, DOCX)
  - Microsoft PowerPoint (PPT, PPTX)
  - Microsoft Excel (XLS, XLSX)
- 🚀 核心转换脚本

## 🛠️ 技术栈

- Python 3.11
- LibreOffice 24.8.6
- Docker

## 🚀 快速开始

### 1. 构建 Docker 镜像

```bash
docker build -t libreoffice-python-base:latest -f Dockerfile .
```

### 2. 运行容器

```bash
docker run -it -v /path/to/your/documents:/app/input -v /path/to/output:/app/output libreoffice-python-base bash
```

### 3. 执行转换

```bash
python convert.py
```

## 📁 目录结构

```plaintext
.
├── 📄 convert.py      # 核心转换脚本
├── 📄 Dockerfile      # Docker 构建文件
├── 📁 input/          # 输入文件目录
├── 📁 output/         # 输出文件目录
└── 📄 README.md       # 项目文档
```

## 💡 使用说明

1. 将需要转换的文档放入 `input` 目录
2. 支持的文件格式：
   - `.doc`, `.docx` (Word文档)
   - `.ppt`, `.pptx` (PowerPoint演示文稿)
   - `.xls`, `.xlsx` (Excel表格)
3. 转换后的 PDF 文件将保存在 `output` 目录

## 🌟 示例代码

```python
from convert import convert_to_pdf

# 转换单个文件
result = convert_to_pdf(
    input_file="input/document.docx",
    output_dir="output"
)
```

## 📝 日志输出

转换过程中会输出详细的日志信息：

```plaintext
2024-01-20 10:30:15 - convert - INFO - 开始转换文件: document.docx
2024-01-20 10:30:16 - convert - INFO - 转换成功: output/document.pdf
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 开源协议

本项目基于 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。

## 👨‍💻 维护者

- [@OSpoon](https://github.com/OSpoon)

## 🙏 致谢

- [LibreOffice](https://www.libreoffice.org/)
- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)