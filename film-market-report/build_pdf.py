# -*- coding: utf-8 -*-
"""将 Markdown 报告渲染为 HTML,再用 Chrome headless 打印为 PDF。"""
import os
import subprocess
import markdown

BASE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(BASE, "中国电影市场深度分析报告.md")
HTML = os.path.join(BASE, "report.html")
PDF = os.path.join(BASE, "中国电影市场深度分析报告.pdf")

CSS = """
body { font-family: "WenQuanYi Micro Hei", "Noto Sans CJK SC", sans-serif;
       max-width: 900px; margin: 0 auto; padding: 40px 30px;
       color: #1a202c; line-height: 1.85; font-size: 14px; }
h1 { font-size: 26px; border-bottom: 3px solid #2b6cb0; padding-bottom: 12px; color: #1a365d; }
h2 { font-size: 20px; color: #2b6cb0; border-left: 5px solid #2b6cb0;
     padding-left: 10px; margin-top: 36px; page-break-after: avoid; }
h3 { font-size: 16px; color: #2d3748; margin-top: 24px; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 13px; }
th, td { border: 1px solid #cbd5e0; padding: 7px 10px; text-align: left; }
th { background: #ebf4ff; color: #2a4365; }
tr:nth-child(even) { background: #f7fafc; }
img { max-width: 100%; display: block; margin: 18px auto; page-break-inside: avoid;
      border: 1px solid #e2e8f0; }
blockquote { border-left: 4px solid #d69e2e; margin: 12px 0; padding: 4px 14px;
             background: #fffff0; color: #4a5568; }
code { background: #edf2f7; padding: 1px 5px; border-radius: 3px; font-size: 13px; }
strong { color: #c53030; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 28px 0; }
a { color: #2b6cb0; text-decoration: none; }
li { margin: 4px 0; }
"""

with open(MD, encoding="utf-8") as f:
    body = markdown.markdown(f.read(), extensions=["tables", "toc", "fenced_code"])

html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>中国电影市场深度分析报告</title>
<style>{CSS}</style></head>
<body>{body}</body></html>"""

with open(HTML, "w", encoding="utf-8") as f:
    f.write(html)
print("HTML written:", HTML)

subprocess.run([
    "google-chrome", "--headless", "--disable-gpu", "--no-sandbox",
    f"--print-to-pdf={PDF}", "--no-pdf-header-footer",
    "--virtual-time-budget=10000", f"file://{HTML}",
], check=True)
print("PDF written:", PDF)
