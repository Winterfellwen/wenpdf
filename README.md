# WenPDF

将 PDF 文件转换为 HTML/DOCX/DOC 格式。

## 功能特性

- 📄 支持扫描版 PDF（图片形式渲染）
- 📝 支持文字版 PDF（提取文字、图形、嵌入图片）
- 🖼️ 嵌入图片透明背景处理
- 🌐 输出独立的 HTML 文件（图片 Base64 内嵌）
- 📎 支持输出格式：HTML, DOCX, DOC
- 💻 跨平台支持（Windows、Linux、macOS）

## 安装

### 1. 克隆项目

```bash
git clone https://github.com/Winterfellwen/wenpdf.git
cd wenpdf
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 安装 Playwright 浏览器（可选，仅截图功能需要）

```bash
pip install playwright
playwright install chromium
```

## 快速开始

```bash
# PDF 转 HTML
python convert.py input.pdf -o output.html

# PDF 转 HTML 并生成对比截图
python convert.py input.pdf -o output.html --screenshot all
```

## 命令参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `pdf_path` | - | 输入的 PDF 文件 | - |
| `--output` | `-o` | 输出文件路径 | output.html |
| `--format` | `-f` | 输出格式：html/docx/doc | html |
| `--screenshot` | - | 生成截图：pdf/html/all | - |

## 使用示例

```bash
# 基本转换
python convert.py document.pdf

# 指定输出文件名
python convert.py document.pdf -o result.html

# 指定输出格式（目前支持 html）
python convert.py document.pdf -o result.html -f html

# 只生成 PDF 截图
python convert.py document.pdf --screenshot pdf

# 只生成 HTML 截图
python convert.py document.pdf --screenshot html

# 生成 PDF 和 HTML 对比截图
python convert.py document.pdf --screenshot all
```

## 许可证

MIT License