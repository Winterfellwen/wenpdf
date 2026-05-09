# WenPDF Technical Documentation

[English](#english) | [中文](#中文)

---

# English

## Architecture Overview

```
Input PDF → PDF Plumber → Text/Shapes/Images Extraction → HTML Generation → Output HTML
                           ↓
                    Playwright → Screenshot Capture
```

## Core Components

### 1. PDF Parsing (pdfplumber)

- **Text Extraction**: `page.chars` - extracts all characters with position, font, size, color
- **Shape Extraction**: `page.rects`, `page.lines` - extracts rectangles and lines
- **Image Extraction**: `page.images` - extracts embedded images
- **Page Metadata**: `page.width`, `page.height`, `page.number`

### 2. HTML Generation

- **Character Merging Algorithm**: Combine adjacent characters with same style
  - Same style = same font, size, color
  - Same line = y-position within 0.5pt tolerance
  - Word detection: gap < 0.3pt (same word), gap < size*0.5 (different word)
- **Position Precision**: Use PDF coordinate system (72 DPI base)
- **Style Optimization**: letter-spacing calculation based on actual vs natural width

### 3. Screenshot Capture (Playwright)

- **PDF Screenshot**: Use PyMuPDF (`fitz`) to render PDF pages
- **HTML Screenshot**: Use Playwright to capture rendered HTML
  - Viewport: Set to match PDF page size (width × height)
  - Element: Select `.pdf-page` locator, use `nth(index)` for each page
  - Format: PNG output

## Key Algorithms

### Character Merging

```python
# Sort by position (y first, then x)
sorted_chars = sorted(chars, key=lambda x: (round(x['top'] * 2) / 2, x['x0']))

# Merge logic
while j < len(sorted_chars):
    next_c = sorted_chars[j]
    same_style = (next_size == size and next_font == font)
    same_line = abs(next_top - top) < 0.5
    gap = next_x0 - prev_x1
    
    if same_style and same_line:
        if gap < 0.3:  # Same word
            merged_text += next_text
        elif gap < size * 0.5:  # Different word
            merged_text += ' ' + next_text
        else:  # Different element
            break
```

### Letter Spacing Calculation

```python
# Calculate natural width
char_count = len(merged_text.replace(' ', ''))
total_char_width = sum(char.get('width', size*0.6) for char in chars[i:j])
avg_char_width = total_char_width / (j - i)
natural_width = avg_char_width * char_count + space_count * (size * 0.25)

# Calculate required spacing
letter_spacing = (merged_width - natural_width) / char_count
letter_spacing = max(-0.5, min(letter_spacing, 2))  # Clamp
```

### HTML Screenshot

```python
# Get page sizes from PDF
with pdfplumber.open(pdf_path) as pdf:
    page_sizes = [(page.width, page.height) for page in pdf.pages]

# Capture each page with correct viewport
browser = p.chromium.launch(headless=True)
for page_num, (page_width, page_height) in enumerate(page_sizes):
    page = browser.new_page(viewport={'width': int(page_width), 'height': int(page_height)})
    page.goto(html_url)
    page.wait_for_load_state('networkidle')
    
    pdf_page_element = page.locator('.pdf-page').nth(page_num)
    pdf_page_element.screenshot(path=f'html_page_{page_num}.png')
```

## File Structure

```
wenpdf/
├── convert.py          # Main converter
├── README.md         # User documentation
├── TECH.md           # Technical documentation
└── requirements.txt  # Python dependencies
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pdfplumber | >=0.10.0 | PDF text/shape extraction |
| pymupdf | >=1.23.0 | PDF rendering |
| pillow | >=10.0.0 | Image processing |
| playwright | >=1.40.0 | HTML screenshot |
| python-docx | >=1.1.0 | DOCX generation |
| beautifulsoup4 | >=4.12.0 | HTML parsing |
| lxml | >=4.9.0 | XML/HTML processing |

## Playwright Installation

```bash
pip install playwright
playwright install chromium
```

---

# 中文

## 架构概述

```
输入 PDF → PDF Plumber → 文本/图形/图片提取 → HTML生成 → 输出HTML
                          ↓
                   Playwright → 截图捕获
```

## 核心组件

### 1. PDF解析 (pdfplumber)

- **文本提取**：`page.chars` - 提取所有字符的位置、字体、大小、颜色
- **图形提取**：`page.rects`、`page.lines` - 提取矩形和线条
- **图片提取**：`page.images` - 提取嵌入的图片
- **页面元数据**：`page.width`、`page.height`、`page.number`

### 2. HTML生成

- **字符合并算法**：合并相邻且样式相同的字符
  - 相同样式 = 相同字体、大小、颜色
  - 相同行 = y坐标在0.5pt内
  - 单词检测：间距 < 0.3pt（同一单词），间距 < 大小*0.5（不同单词）
- **位置精度**：使用PDF坐标系统（72 DPI基准）
- **样式优化**：根据实际宽度与自然宽度计算letter-spacing

### 3. 截图捕获 (Playwright)

- **PDF截图**：使用PyMuPDF (`fitz`) 渲染PDF页面
- **HTML截图**：使用Playwright捕获渲染后的HTML
  - 视口：设置为PDF页面尺寸（宽×高）
  - 元素：选择`.pdf-page`定位器，使用`nth(index)`遍历每页
  - 格式：PNG输出

## 关键算法

### 字符合并

```python
# 按位置排序（先y后x）
sorted_chars = sorted(chars, key=lambda x: (round(x['top'] * 2) / 2, x['x0']))

# 合并逻辑
while j < len(sorted_chars):
    next_c = sorted_chars[j]
    same_style = (next_size == size and next_font == font)
    same_line = abs(next_top - top) < 0.5
    gap = next_x0 - prev_x1
    
    if same_style and same_line:
        if gap < 0.3:  # 同一单词
            merged_text += next_text
        elif gap < size * 0.5:  # 不同单词
            merged_text += ' ' + next_text
        else:  # 不同元素
            break
```

### 字间距计算

```python
# 计算自然宽度
char_count = len(merged_text.replace(' ', ''))
total_char_width = sum(char.get('width', size*0.6) for char in chars[i:j])
avg_char_width = total_char_width / (j - i)
natural_width = avg_char_width * char_count + space_count * (size * 0.25)

# 计算所需间距
letter_spacing = (merged_width - natural_width) / char_count
letter_spacing = max(-0.5, min(letter_spacing, 2))  # 限制范围
```

### HTML截图

```python
# 从PDF获取页面尺寸
with pdfplumber.open(pdf_path) as pdf:
    page_sizes = [(page.width, page.height) for page in pdf.pages]

# 使用正确视口捕获每页
browser = p.chromium.launch(headless=True)
for page_num, (page_width, page_height) in enumerate(page_sizes):
    page = browser.new_page(viewport={'width': int(page_width), 'height': int(page_height)})
    page.goto(html_url)
    page.wait_for_load_state('networkidle')
    
    pdf_page_element = page.locator('.pdf-page').nth(page_num)
    pdf_page_element.screenshot(path=f'html_page_{page_num}.png')
```

## 文件结构

```
wenpdf/
├── convert.py          # 主转换器
├── README.md         # 用户文档
├── TECH.md           # 技术文档
└── requirements.txt  # Python依赖
```

## 依赖包

| 包名 | 版本 | 用途 |
|---------|---------|---------|
| pdfplumber | >=0.10.0 | PDF文本/图形提取 |
| pymupdf | >=1.23.0 | PDF渲染 |
| pillow | >=10.0.0 | 图片处理 |
| playwright | >=1.40.0 | HTML截图 |
| python-docx | >=1.1.0 | DOCX生成 |
| beautifulsoup4 | >=4.12.0 | HTML解析 |
| lxml | >=4.9.0 | XML/HTML处理 |

## Playwright安装

```bash
pip install playwright
playwright install chromium
```

---

# Implementation Notes / 实现说明

## Coordinate System / 坐标系统

- PDF uses bottom-left origin (0,0 at bottom-left)
- HTML/CSS uses top-left origin (0,0 at top-left)
- Conversion: `css_top = pdf_height - pdf_top`

## Units / 单位

- PDF coordinates: points (pt), 72 points = 1 inch
- CSS: pixels (px) or points (pt)
- DPI: 72 (PDF native), can be scaled

## Performance Considerations / 性能考虑

- Character merging reduces span count by ~70%
- Base64 encoding increases size by ~33%
- For large PDFs, consider lazy loading or pagination