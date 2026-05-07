# PDF to HTML Converter

将PDF文件转换为HTML/DOCX/DOC，支持扫描版PDF（图片）和文字版PDF。

## 安装

### 方式一：pip 安装（推荐）

```bash
# 从 GitHub 安装
pip install git+https://github.com/你的用户名/wenpdf.git

# 或本地安装
pip install .
```

安装后可直接使用命令：
```bash
wenpdf input.pdf -o output.html
```

### 方式二：手动安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

## 使用方法

```bash
wenpdf <pdf_path> [-o output.html] [-f html|docx|doc] [--screenshot pdf|html|all ...]
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `pdf_path` | 输入的PDF文件路径 |
| `-o, --output` | 输出文件路径（默认：output.html） |
| `-f, --format` | 输出格式：html, docx, doc（默认：html） |
| `--screenshot` | 生成截图，可多次使用：pdf, html, all |

### 使用示例

```bash
# 基本转换
wenpdf input.pdf

# 指定输出文件
wenpdf input.pdf -o myfile.html

# 指定输出格式
wenpdf input.pdf -o result.docx -f docx

# 生成PDF和HTML对比截图
wenpdf input.pdf --screenshot pdf --screenshot html
# 或
wenpdf input.pdf --screenshot all

# 组合使用
wenpdf input.pdf -o output.html --screenshot all
```

## 功能特点

- 支持扫描版PDF（图片形式渲染）
- 支持文字版PDF（提取文字、图形、嵌入图片）
- 嵌入图片透明背景处理：PNG保持透明，其他格式白色背景
- 输出独立的HTML文件（图片Base64内嵌）
- 支持输出格式：HTML, DOCX, DOC（DOCX/DOC开发中）
- 跨平台支持（Windows、Linux、macOS）

## 开发

```bash
# 克隆仓库
git clone https://github.com/你的用户名/wenpdf.git
cd wenpdf

# 安装开发依赖
pip install -e .

# 运行
wenpdf test.pdf
```

## 许可证

MIT License