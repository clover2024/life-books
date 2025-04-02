# EPUB 转 Markdown 转换器

这是一个简单的Python程序，用于将EPUB格式的电子书转换为Markdown格式。

## 安装依赖

在使用之前，请先安装所需的依赖包：

```bash
pip install -r requirements.txt
```

## 使用方法

基本用法：

```bash
python epub_to_md.py 你的电子书.epub
```

指定输出目录：

```bash
python epub_to_md.py 你的电子书.epub -o 输出目录
```

## 功能特点

- 自动提取EPUB文件中的文本内容
- 保持基本的段落结构
- 自动创建输出目录
- 使用书名作为输出文件名
- 支持UTF-8编码

## 注意事项

- 转换后的Markdown文件将保存在与EPUB文件相同的目录下（除非指定了输出目录）
- 输出文件名将基于EPUB文件的标题生成
- 程序会自动清理HTML标签和样式 