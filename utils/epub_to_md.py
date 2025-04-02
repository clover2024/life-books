#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
import argparse
from pathlib import Path
import re

def process_html_content(soup):
    """
    处理HTML内容，保持原始顺序处理标题和段落
    
    Args:
        soup (BeautifulSoup): BeautifulSoup对象
        
    Returns:
        list: 处理后的文本行列表
    """
    lines = []
    processed_texts = set()  # 用于记录已处理的文本
    
    # 首先处理所有<b>标签
    for b_tag in soup.find_all('b'):
        text = b_tag.get_text().strip()
        if text:
            # 将<b>标签替换为加粗文本
            b_tag.replace_with(f"**{text}**")
    
    # 然后按照文档顺序处理其他元素
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            # 处理标题
            level = int(element.name[1])
            title_text = element.get_text().strip()
            if title_text and title_text not in processed_texts:
                lines.append(f"{'#' * level} {title_text}")
                processed_texts.add(title_text)
        else:
            # 处理段落
            text = element.get_text().strip()
            # 如果文本不在已处理列表中，则添加
            if text and text not in processed_texts:
                lines.append(text)
                processed_texts.add(text)
    
    return lines

def epub_to_md(epub_path, output_dir=None):
    """
    将EPUB文件转换为Markdown格式
    
    Args:
        epub_path (str): EPUB文件的路径
        output_dir (str, optional): 输出目录的路径
    """
    # 读取EPUB文件
    book = epub.read_epub(epub_path)
    
    # 如果没有指定输出目录，使用EPUB文件所在目录
    if output_dir is None:
        output_dir = os.path.dirname(epub_path)
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取书名
    title = book.get_metadata('DC', 'title')[0][0]
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    
    # 创建主markdown文件
    md_path = os.path.join(output_dir, f"{safe_title}.md")
    
    with open(md_path, 'w', encoding='utf-8') as f:
        # 写入标题
        f.write(f"# {title}\n\n")
        
        # 遍历所有文档
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # 解析HTML内容
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                
                # 移除脚本和样式标签
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # 处理内容并写入文件
                lines = process_html_content(soup)
                for line in lines:
                    if line.strip():
                        f.write(f"{line.strip()}\n\n")

def main():
    parser = argparse.ArgumentParser(description='将EPUB文件转换为Markdown格式')
    parser.add_argument('epub_file', help='EPUB文件的路径')
    parser.add_argument('--output-dir', '-o', help='输出目录的路径（可选）')
    
    args = parser.parse_args()
    
    try:
        epub_to_md(args.epub_file, args.output_dir)
        print("转换完成！")
    except Exception as e:
        print(f"转换过程中出现错误：{str(e)}")

if __name__ == '__main__':
    main() 