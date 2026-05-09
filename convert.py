"""
优化脚本：将670KB版本转换为更精简的版本，同时保持位置精确
"""
import pdfplumber
import os
import base64
import fitz
import io
from PIL import Image
from bs4 import BeautifulSoup

def parse_fontname(fontname):
    if '+' in fontname:
        name = fontname.split('+')[1]
    else:
        name = fontname
    font_map = {
        'ArialMT': 'Arial, sans-serif',
        'Arial-BoldMT': 'Arial, sans-serif',
        'TimesNewRomanPSMT': 'Times New Roman, serif',
    }
    return font_map.get(name, f'{name}, sans-serif')

def pdf_to_html_optimized(pdf_path, html_path, screenshot_mode=None):
    """优化版HTML转换 - 保持位置精确同时减少span数量"""
    html_parts = [
        '<!DOCTYPE html>',
        '<html><head>',
        '<meta charset="utf-8">',
        '<style>',
        '* { margin: 0; padding: 0; box-sizing: border-box; }',
        'body { background: #f0f0f0; padding: 20px; font-family: sans-serif; }',
        '.pdf-page { position: relative; margin: 0 auto 20px; background: white; box-shadow: 0 0 10px rgba(0,0,0,0.3); }',
        'span { position: absolute; white-space: pre; line-height: 1; margin: 0; padding: 0; text-align: justify; }',
        'div.rect { position: absolute; }',
        'div.line { position: absolute; z-index: 10; }',
        'img { position: absolute; max-width: none; }',
        '</style></head><body>'
    ]
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            page_width = page.width
            page_height = page.height
            html_parts.append(f'<div class="pdf-page" style="width:{page_width}pt;height:{page_height}pt;">')
            
            has_text = page.chars and len(page.chars) > 0
            
            if not has_text:
                img_b64, img_w, img_h = render_page_as_image(pdf_path, page_num, dpi=150)
                html_parts.append(f'<img src="data:image/png;base64,{img_b64}" style="left:0;top:0;width:{page_width}pt;height:{page_height}pt;" />')
                html_parts.append('</div>')
                continue
            else:
                # 提取图片
                try:
                    doc = fitz.open(pdf_path)
                    image_list = doc.get_page_images(page_num, full=True)
                    for img_idx, img_info in enumerate(image_list):
                        try:
                            xref = img_info[0]
                            base_image = doc.extract_image(xref)
                            if not base_image:
                                continue
                            img_data = base_image['image']
                            img_ext = base_image['ext'].lower()
                            img = Image.open(io.BytesIO(img_data))
                            buf = io.BytesIO()
                            if img_ext == 'png':
                                img.save(buf, format='PNG')
                            else:
                                img.convert('RGB').save(buf, format='JPEG', quality=95)
                                img_ext = 'jpeg'
                            img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                            if img_idx < len(page.images):
                                img_dict = page.images[img_idx]
                                x0 = img_dict.get('x0', 0)
                                y0 = img_dict.get('top', 0)
                                w = img_dict.get('width', base_image['width'])
                                h = img_dict.get('height', base_image['height'])
                            else:
                                x0, y0, w, h = 0, 0, base_image['width'], base_image['height']
                            html_parts.append(f'<img src="data:image/{img_ext};base64,{img_b64}" style="left:{x0}pt;top:{y0}pt;width:{w}pt;height:{h}pt;" />')
                        except: pass
                    doc.close()
                except: pass
            
            # 提取矩形
            if has_text:
                for rect in page.rects:
                    try:
                        x0, y0, w, h = rect['x0'], rect['top'], rect['width'], rect['height']
                        sc = rect.get('stroke_color')
                        fc = rect.get('fill_color')
                        stroke = '#000000'
                        if sc and isinstance(sc, (tuple, list)):
                            stroke = '#{:02x}{:02x}{:02x}'.format(*[int(c*255) for c in sc])
                        fill = 'transparent'
                        if fc and isinstance(fc, (tuple, list)):
                            fill = '#{:02x}{:02x}{:02x}'.format(*[int(c*255) for c in fc])
                        html_parts.append(f'<div class="rect" style="left:{x0}pt;top:{y0}pt;width:{w}pt;height:{h}pt;border:1pt solid {stroke};background:{fill};"></div>')
                    except: pass
                
                # 提取线条
                for line in page.lines:
                    try:
                        x0, x1, y0, y1 = line['x0'], line['x1'], line['top'], line['bottom']
                        sc = line.get('stroking_color')
                        stroke = '#000000'
                        if sc and isinstance(sc, (tuple, list)):
                            stroke = '#{:02x}{:02x}{:02x}'.format(*[int(c*255) for c in sc])
                        width = x1 - x0
                        height = y1 - y0
                        if height == 0 and width > 0:
                            html_parts.append(f'<div class="line" style="left:{x0}pt;top:{y0}pt;width:{width}pt;height:1pt;background:{stroke};"></div>')
                        elif width == 0 and height > 0:
                            html_parts.append(f'<div class="line" style="left:{x0}pt;top:{y0}pt;width:1pt;height:{height}pt;background:{stroke};"></div>')
                    except: pass
            
            # 优化版字符渲染：合并相邻相同样式字符，检测空格
            chars = page.chars
            if chars:
                sorted_chars = sorted(chars, key=lambda x: (round(x.get('top', 0) * 2) / 2, x.get('x0', 0)))
                
                i = 0
                while i < len(sorted_chars):
                    c = sorted_chars[i]
                    text = c.get('text', '')
                    x0 = c.get('x0', 0)
                    top = c.get('top', 0)
                    width = c.get('width', 0)
                    size = c.get('size', 12)
                    font = parse_fontname(c.get('fontname', 'Arial'))
                    color = c.get('color', (0,0,0))
                    if isinstance(color, (tuple, list)):
                        hex_color = '#{:02x}{:02x}{:02x}'.format(*[int(col*255) for col in color])
                    else:
                        hex_color = '#000000'
                    
                    merged_text = text
                    merged_x0 = x0
                    prev_x1 = x0 + width
                    
                    j = i + 1
                    while j < len(sorted_chars):
                        next_c = sorted_chars[j]
                        next_text = next_c.get('text', '')
                        next_x0 = next_c.get('x0', 0)
                        next_top = next_c.get('top', 0)
                        next_width = next_c.get('width', 0)
                        next_size = next_c.get('size', 12)
                        next_font = parse_fontname(next_c.get('fontname', 'Arial'))
                        next_color = next_c.get('color', (0,0,0))
                        if isinstance(next_color, (tuple, list)):
                            next_hex = '#{:02x}{:02x}{:02x}'.format(*[int(col*255) for col in next_color])
                        else:
                            next_hex = '#000000'
                        
                        same_style = (next_size == size and next_font == font and next_hex == hex_color)
                        same_line = abs(next_top - top) < 0.5
                        gap = next_x0 - prev_x1
                        
                        if same_style and same_line:
                            # 两个阈值判断：
                            # 1. gap < 0.3: 同一单词，合并
                            # 2. 0.3 < gap < size*0.5: 不同单词，添加空格继续
                            # 3. gap > size*0.5: 不同元素（如电话和邮箱），停止合并
                            if gap < 0.3:
                                merged_text += next_text
                                prev_x1 = next_x0 + next_width
                                j += 1
                            elif gap < size * 0.5:
                                merged_text += ' ' + next_text
                                prev_x1 = next_x0 + next_width
                                j += 1
                            else:
                                break
                        else:
                            break
                    
                    # 计算整段width：最后一个字符的结束位置 - 第一个字符的开始位置
                    last_char = sorted_chars[j-1] if j > i else c
                    merged_width = last_char.get('x0', 0) + last_char.get('width', 0) - merged_x0
                    
                    # 计算需要的字距：基于原始字符的平均宽度
                    char_count = len(merged_text.replace(' ', ''))
                    if char_count > 1:
                        # 从PDF字符计算平均字符宽度
                        total_char_width = sum(sorted_chars[k].get('width', size*0.6) for k in range(i, j))
                        avg_char_width = total_char_width / (j - i)
                        # 文本自然宽度（不含空格）+ 空格数 * 空格宽
                        space_count = merged_text.count(' ')
                        natural_width = avg_char_width * char_count + space_count * (size * 0.25)
                        # 需要的字距调整 = (目标宽度 - 自然宽度) / 字符数
                        letter_spacing = (merged_width - natural_width) / char_count if char_count > 0 else 0
                        letter_spacing = max(-0.5, min(letter_spacing, 2))  # 限制范围
                        spacing_css = f"letter-spacing:{letter_spacing}pt;"
                    else:
                        spacing_css = ""
                    
                    style = f"left:{merged_x0}pt;top:{top}pt;width:{merged_width}pt;font-family:{font};font-size:{size}pt;color:{hex_color};{spacing_css}"
                    html_parts.append(f'<span style="{style}">{merged_text}</span>')
                    
                    i = j
            
            html_parts.append('</div>')
    
    html_parts.append('</body></html>')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_parts))

def render_page_as_image_to_file(pdf_path, output_dir, page_num, dpi=150):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    mat = fitz.Matrix(dpi/72, dpi/72)
    pix = page.get_pixmap(matrix=mat)
    img_path = os.path.join(output_dir, f'pdf_page_{page_num}.png')
    pix.save(img_path)
    doc.close()
    return img_path, pix.width, pix.height

def render_page_as_image(pdf_path, page_num, dpi=150):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    mat = fitz.Matrix(dpi/72, dpi/72)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    doc.close()
    return base64.b64encode(img_data).decode('utf-8'), pix.width, pix.height

if __name__ == '__main__':
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='PDF to HTML converter')
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('pdf_input', nargs='?', help='Input PDF file')
    input_group.add_argument('-i', '--input', dest='pdf_input_alt', help='Input PDF file')
    parser.add_argument('-o', '--output', dest='output', required=False, default=None, help='Output HTML file')
    parser.add_argument('-s', '--screenshot', dest='screenshot', default=None, 
                        choices=['all', 'pdf', 'html'], help='Screenshot mode: all=PDF+HTML, pdf=only PDF, html=only HTML')
    args = parser.parse_args()
    
    pdf_path = args.pdf_input if args.pdf_input else args.pdf_input_alt
    output_path = args.output
    screenshot_mode = args.screenshot
    
    if screenshot_mode == 'pdf' and not output_path:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = base_name + '.html'
        print(f"警告: 未指定输出文件，使用默认: {output_path}")
    elif not output_path:
        print("错误: 必须指定输出文件")
        sys.exit(1)
    
    print(f"DEBUG: pdf_path={pdf_path}")
    print(f"DEBUG: output_path={output_path}")
    print(f"DEBUG: screenshot_mode={screenshot_mode}")
    
    if not os.path.exists(pdf_path):
        print(f"错误: 找不到文件 '{pdf_path}'")
        print(f"当前目录: {os.getcwd()}")
        print(f"目录中的文件:")
        for f in os.listdir('.'):
            if f.endswith('.pdf'):
                print(f"  - {f}")
        sys.exit(1)
    
    output_dir = os.path.dirname(output_path) or '.'
    output_base = os.path.splitext(os.path.basename(output_path))[0]
    screenshot_dir = os.path.join(output_dir, output_base + '_screenshots')
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
    
    if screenshot_mode == 'pdf':
        os.makedirs(screenshot_dir, exist_ok=True)
        for page_num in range(total_pages):
            img_path, w, h = render_page_as_image_to_file(pdf_path, screenshot_dir, page_num)
            print(f"截图已生成: {img_path}")
        print(f"截图目录: {screenshot_dir}")
        print(f"完成（仅PDF截图，未转换）")
        sys.exit(0)
    
    if screenshot_mode in ('html', 'all'):
        pdf_to_html_optimized(pdf_path, output_path, None)
        print(f"HTML已生成: {output_path}")
        
        try:
            from playwright.sync_api import sync_playwright
            
            os.makedirs(screenshot_dir, exist_ok=True)
            
            with pdfplumber.open(pdf_path) as pdf:
                page_sizes = [(page.width, page.height) for page in pdf.pages]
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                
                html_path_abs = os.path.abspath(output_path)
                html_url = f'file:///{html_path_abs.replace("\\", "/")}'
                
                for page_num, (page_width, page_height) in enumerate(page_sizes):
                    page = browser.new_page(viewport={'width': int(page_width), 'height': int(page_height)})
                    page.goto(html_url)
                    page.wait_for_load_state('networkidle')
                    
                    pdf_page = page.locator(f'.pdf-page').nth(page_num)
                    pdf_page.screenshot(path=os.path.join(screenshot_dir, f'html_page_{page_num}.png'))
                    print(f"HTML截图已生成: {os.path.join(screenshot_dir, f'html_page_{page_num}.png')}")
                    
                    page.close()
                
                browser.close()
        except ImportError:
            print("警告: 未安装 playwright，跳过HTML截图")
            print("请运行: pip install playwright")
            print("同时运行: playwright install chromium")
        except Exception as e:
            print(f"HTML截图失败: {e}")
    
    if screenshot_mode in ('pdf', 'all'):
        os.makedirs(screenshot_dir, exist_ok=True)
        for page_num in range(total_pages):
            img_path, w, h = render_page_as_image_to_file(pdf_path, screenshot_dir, page_num)
            print(f"PDF截图已生成: {img_path}")
        print(f"截图目录: {screenshot_dir}")
    
    if screenshot_mode not in ('pdf',):
        print(f"优化版已生成: {output_path}")