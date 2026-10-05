#!/usr/bin/env python3
"""将本目录下的研究报告 Markdown 章节合并生成单一 PDF。

用法：python3 build_pdf.py
依赖：pip install markdown weasyprint；系统需安装中文字体（fonts-noto-cjk）。
输出：汉至清：中国历代财税与治理制度变迁研究.pdf
"""

import datetime
import re
from pathlib import Path

import markdown
from weasyprint import HTML

BASE = Path(__file__).resolve().parent

CHAPTER_FILES = [
    "00-总论.md",
    "01-汉朝.md",
    "02-魏晋南北朝至隋.md",
    "03-唐朝.md",
    "04-宋朝.md",
    "05-元朝.md",
    "06-明朝.md",
    "07-清朝.md",
    "08-结论.md",
    "09-附录.md",
]

TITLE = "汉至清：中国历代财税与治理制度变迁研究"
OUTPUT = BASE / f"{TITLE.replace('：', '——')}.pdf"

CSS = """
@page {
    size: A4;
    margin: 2.2cm 2cm 2.2cm 2cm;
    @bottom-center {
        content: counter(page) " / " counter(pages);
        font-family: "Noto Sans CJK SC", sans-serif;
        font-size: 9pt;
        color: #888;
    }
    @top-center {
        content: "汉至清：中国历代财税与治理制度变迁研究";
        font-family: "Noto Sans CJK SC", sans-serif;
        font-size: 8.5pt;
        color: #aaa;
    }
}
@page cover {
    @bottom-center { content: none; }
    @top-center { content: none; }
}
body {
    font-family: "Noto Serif CJK SC", "Noto Sans CJK SC", serif;
    font-size: 10.5pt;
    line-height: 1.75;
    color: #1a1a1a;
}
.cover {
    page: cover;
    page-break-after: always;
    text-align: center;
    padding-top: 5.5cm;
}
.cover h1 {
    font-family: "Noto Sans CJK SC", sans-serif;
    font-size: 24pt;
    border: none;
    line-height: 1.5;
    margin-bottom: 0.8cm;
}
.cover .subtitle { font-size: 13pt; color: #555; margin-bottom: 2.2cm; }
.cover .dims {
    display: inline-block;
    text-align: left;
    font-size: 11pt;
    color: #333;
    line-height: 2.1;
}
.cover .date { margin-top: 2.5cm; font-size: 11pt; color: #777; }
.toc { page-break-after: always; }
.toc h1 { text-align: center; border: none; }
.toc ol { list-style: none; padding: 0 1cm; }
.toc li { margin: 0.45em 0; font-size: 11.5pt; }
.toc a { text-decoration: none; color: #1a1a1a; }
.toc a::after {
    content: leader('.') " " target-counter(attr(href), page);
    color: #555;
}
section.chapter { page-break-before: always; }
h1, h2, h3, h4 {
    font-family: "Noto Sans CJK SC", sans-serif;
    color: #111;
    line-height: 1.4;
}
h1 {
    font-size: 17pt;
    border-bottom: 2.5px solid #8b1a1a;
    padding-bottom: 0.3em;
    margin-top: 0;
}
h2 {
    font-size: 13.5pt;
    border-left: 5px solid #8b1a1a;
    padding-left: 0.5em;
    margin-top: 1.6em;
}
h3 { font-size: 11.5pt; margin-top: 1.3em; }
p { margin: 0.6em 0; text-align: justify; }
strong { font-weight: 700; }
table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.8em 0;
    font-size: 9pt;
    line-height: 1.5;
}
th, td { border: 0.8px solid #999; padding: 4px 6px; text-align: left; }
th { background: #f0e8e8; font-family: "Noto Sans CJK SC", sans-serif; }
tr:nth-child(even) td { background: #fafafa; }
pre {
    background: #f6f6f6;
    border: 0.8px solid #ddd;
    border-radius: 4px;
    padding: 0.7em 1em;
    font-family: "Noto Sans Mono CJK SC", "WenQuanYi Micro Hei Mono", monospace;
    font-size: 8.5pt;
    line-height: 1.6;
    white-space: pre-wrap;
}
code {
    font-family: "Noto Sans Mono CJK SC", "WenQuanYi Micro Hei Mono", monospace;
    font-size: 0.9em;
    background: #f3f3f3;
    padding: 0 3px;
    border-radius: 3px;
}
pre code { background: none; padding: 0; }
blockquote {
    border-left: 4px solid #ccc;
    margin: 0.8em 0;
    padding: 0.2em 1em;
    color: #555;
    background: #fafafa;
}
ul, ol { padding-left: 1.6em; }
li { margin: 0.3em 0; }
pre, blockquote { page-break-inside: avoid; }
tr { page-break-inside: avoid; }
h1, h2, h3 { page-break-after: avoid; }
"""


def chapter_title(md_text: str) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("章节缺少一级标题")


def main() -> None:
    md = markdown.Markdown(extensions=["tables", "fenced_code"])
    sections, toc_items = [], []
    for i, name in enumerate(CHAPTER_FILES):
        text = (BASE / name).read_text(encoding="utf-8")
        title = chapter_title(text)
        anchor = f"ch-{i:02d}"
        toc_items.append(f'<li><a href="#{anchor}">{title}</a></li>')
        body = md.reset().convert(text)
        sections.append(f'<section class="chapter" id="{anchor}">{body}</section>')

    today = datetime.date.today().strftime("%Y 年 %m 月")
    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>{TITLE}</title>
<style>{CSS}</style></head><body>
<div class="cover">
  <h1>汉至清<br>中国历代财税与治理制度变迁研究</h1>
  <div class="subtitle">土地 · 税收 · 财政 · 兵制 · 选官 · 央地关系<br>六维度的朝代比较研究</div>
  <div class="dims">
    研究范围：汉、魏晋南北朝至隋、唐、宋、元、明、清<br>
    核心命题：财政税收制度决定国家的强盛与兴衰<br>
    分析框架：生产关系变迁如何倒逼治理结构与财税制度重构
  </div>
  <div class="date">{today}</div>
</div>
<div class="toc"><h1>目 录</h1><ol>{''.join(toc_items)}</ol></div>
{''.join(sections)}
</body></html>"""

    HTML(string=html, base_url=str(BASE)).write_pdf(str(OUTPUT))
    print(f"已生成：{OUTPUT}")


if __name__ == "__main__":
    main()
