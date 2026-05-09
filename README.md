# WenPDF

将 PDF 文件转换为 HTML 格式。

## 功能特性 / Features

- 📄 支持扫描版 PDF（图片形式渲染）
- 📝 支持文字版 PDF（提取文字、图形、嵌入图片）
- 🖼️ 嵌入图片透明背景处理
- 🌐 输出独立的 HTML 文件（图片 Base64 内嵌）
- 📎 支持生成独立截图文件
- 💻 跨平台支持（Windows、Linux、macOS）

## 安装 / Installation

### 1. 克隆项目 / Clone Project

```bash
git clone https://github.com/Winterfellwen/wenpdf.git
cd wenpdf
```

### 2. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. 安装 Playwright（HTML截图功能需要 / Required for HTML Screenshot）

```bash
pip install playwright
playwright install chromium
```

## 快速开始 / Quick Start

```bash
# PDF 转 HTML
python convert.py input.pdf -o output.html

# 生成截图
python convert.py input.pdf -o output.html --screenshot all
```

## 命令参数 / Command Options

| 参数 / Parameter | 简写 / Short | 说明 / Description | 默认值 / Default |
|------|------|------|--------|
| `input` | - | 输入的 PDF 文件（位置参数） | - |
| `--input` | `-i` | 输入的 PDF 文件 | - |
| `--output` | `-o` | 输出文件路径（`-s pdf` 时可选） | - |
| `--screenshot` | `-s` | 截图模式：all/pdf/html | - |

## 使用示例 / Usage Examples

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

## 截图功能说明 / Screenshot Feature

当使用 `--screenshot` 参数时，会在输出目录生成 `{输出文件名}_screenshots/` 目录：

- `-s pdf`：只截原PDF的截图，不运行转换 / Only capture PDF, no conversion
- `-s html`：生成HTML并截转换后的HTML截图 / Generate HTML and capture HTML screenshots
- `-s all`：截原PDF的截图 + 生成HTML并截HTML截图 / Capture both PDF and HTML screenshots

PDF截图命名 / PDF screenshot naming: `pdf_page_0.png`、`pdf_page_1.png`...
HTML截图命名 / HTML screenshot naming: `html_page_0.png`、`html_page_1.png`...

## 许可证 / License

MIT License