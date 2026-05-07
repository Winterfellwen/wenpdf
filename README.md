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

```bash
pip install git+https://github.com/Winterfellwen/wenpdf.git
```

或本地安装：

```bash
git clone https://github.com/Winterfellwen/wenpdf.git
cd wenpdf
pip install -e .
```

### 依赖安装

首次使用需要安装 Playwright 浏览器：

```bash
playwright install chromium
```

## 快速开始

```bash
# PDF 转 HTML
wenpdf input.pdf -o output.html

# PDF 转 HTML 并生成对比截图
wenpdf input.pdf -o output.html --screenshot all
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
wenpdf document.pdf

# 指定输出文件名
wenpdf document.pdf -o result.html

# 指定输出格式（目前支持 html）
wenpdf document.pdf -o result.html -f html

# 只生成 PDF 截图
wenpdf document.pdf --screenshot pdf

# 只生成 HTML 截图
wenpdf document.pdf --screenshot html

# 生成 PDF 和 HTML 对比截图
wenpdf document.pdf --screenshot all
```

## 开发

```bash
# 克隆项目
git clone https://github.com/Winterfellwen/wenpdf.git
cd wenpdf

# 安装开发依赖
pip install -e .

# 运行
wenpdf test.pdf

# 运行测试
python -m convert test.pdf -o output.html
```

## 许可证

MIT License