# WenPDF

[English](#english) | [中文](#中文)

---

# English

## Features

- 📄 Support scanned PDF (rendered as images)
- 📝 Support text-based PDF (extract text, shapes, embedded images)
- 🖼️ Transparent background handling for embedded images
- 🌐 Standalone HTML output (Base64 embedded images)
- 📎 Generate standalone screenshot files
- 💻 Cross-platform support (Windows, Linux, macOS)

## Installation

### 1. Clone Project

```bash
git clone https://github.com/Winterfellwen/wenpdf.git
cd wenpdf
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright (Required for HTML Screenshot)

```bash
pip install playwright
playwright install chromium
```

## Quick Start

```bash
# PDF to HTML
python convert.py input.pdf -o output.html

# Generate screenshots
python convert.py input.pdf -o output.html --screenshot all
```

## Command Options

| Parameter | Short | Description | Default |
|------|------|------|--------|
| `input` | - | Input PDF file (positional) | - |
| `--input` | `-i` | Input PDF file | - |
| `--output` | `-o` | Output file path (optional with `-s pdf`) | - |
| `--screenshot` | `-s` | Screenshot mode: all/pdf/html | - |

## Usage Examples

```bash
# Basic conversion
python convert.py document.pdf -o result.html

# Using parameter aliases
python convert.py --input document.pdf -o result.html
python convert.py -i document.pdf -o result.html

# PDF screenshot only, no output needed (auto-generates same name HTML)
python convert.py document.pdf -s pdf

# PDF screenshot only (with output)
python convert.py document.pdf -o result.html -s pdf

# Generate HTML and screenshot
python convert.py document.pdf -o result.html -s html

# PDF + HTML screenshots
python convert.py document.pdf -o result.html -s all
```

## Screenshot Feature

When using `--screenshot`, screenshots are saved to `{output_filename}_screenshots/` directory:

- `-s pdf`: Only capture PDF, no conversion
- `-s html`: Generate HTML and capture HTML screenshots
- `-s all`: Capture both PDF and HTML screenshots

PDF screenshots: `pdf_page_0.png`, `pdf_page_1.png`...
HTML screenshots: `html_page_0.png`, `html_page_1.png`...

## License

MIT License

---

# 中文

## 功能特性

- 📄 支持扫描版 PDF（图片形式渲染）
- 📝 支持文字版 PDF（提取文字、图形、嵌入图片）
- 🖼️ 嵌入图片透明背景处理
- 🌐 输出独立的 HTML 文件（图片 Base64 内嵌）
- 📎 支持生成独立截图文件
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

### 3. 安装 Playwright（HTML截图功能需要）

```bash
pip install playwright
playwright install chromium
```

## 快速开始

```bash
# PDF 转 HTML
python convert.py input.pdf -o output.html

# 生成截图
python convert.py input.pdf -o output.html --screenshot all
```

## 命令参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `input` | - | 输入的 PDF 文件（位置参数） | - |
| `--input` | `-i` | 输入的 PDF 文件 | - |
| `--output` | `-o` | 输出文件路径（`-s pdf` 时可选） | - |
| `--screenshot` | `-s` | 截图模式：all/pdf/html | - |

## 使用示例

```bash
# 基本转换
python convert.py document.pdf -o result.html

# 使用参数别名
python convert.py --input document.pdf -o result.html
python convert.py -i document.pdf -o result.html

# 只截PDF的截图，无需指定输出（自动使用同名HTML）
python convert.py document.pdf -s pdf

# 只截PDF的截图（指定输出）
python convert.py document.pdf -o result.html -s pdf

# 生成HTML并截HTML的截图
python convert.py document.pdf -o result.html -s html

# PDF截图 + HTML截图
python convert.py document.pdf -o result.html -s all
```

## 截图功能说明

当使用 `--screenshot` 参数时，会在输出目录生成 `{输出文件名}_screenshots/` 目录：

- `-s pdf`：只截原PDF的截图，不运行转换
- `-s html`：生成HTML并截转换后的HTML截图
- `-s all`：截原PDF的截图 + 生成HTML并截HTML截图

PDF截图命名：`pdf_page_0.png`、`pdf_page_1.png`...
HTML截图命名：`html_page_0.png`、`html_page_1.png`...

## 许可证

MIT License