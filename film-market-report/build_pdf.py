# -*- coding: utf-8 -*-
"""将 Markdown 报告渲染为 HTML,再用 Chrome headless 打印为 PDF。

排版、配色与字体对齐《2026年中国暑期旅游市场分析报告》(report/report.html):
Noto Sans CJK SC / 藏青 #0b2a5b / 品牌蓝 #2563eb / A4 带页脚 / 渐变封面页。
"""
import os
import re
import subprocess
import markdown

BASE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(BASE, "中国电影市场深度分析报告.md")
HTML = os.path.join(BASE, "report.html")
PDF = os.path.join(BASE, "中国电影市场深度分析报告.pdf")

CSS = """
@page {
  size: A4;
  margin: 22mm 18mm 20mm 18mm;
  @bottom-center {
    content: "中国电影市场深度分析报告 · 第 " counter(page) " 页";
    font-size: 8.5pt; color: #94a3b8;
    font-family: "Noto Sans CJK SC";
  }
}
@page cover { margin: 0; @bottom-center { content: none; } }

* { box-sizing: border-box; }
body {
  font-family: "Noto Sans CJK SC", "WenQuanYi Micro Hei", sans-serif;
  font-size: 10.5pt; line-height: 1.85; color: #1e293b; margin: 0;
}

/* ---------- 封面 ---------- */
.cover {
  page: cover;
  width: 210mm; height: 296mm;
  background: linear-gradient(150deg, #0b2a5b 0%, #123e7c 55%, #1d5aa8 100%);
  color: #fff; position: relative;
  padding: 40mm 22mm;
}
.cover .tag {
  display: inline-block; border: 1px solid rgba(255,255,255,.5);
  padding: 2mm 6mm; font-size: 10pt; letter-spacing: 2px; border-radius: 2mm;
}
.cover h1 { font-size: 27pt; margin: 22mm 0 4mm; line-height: 1.5; letter-spacing: 1px; }
.cover h2 { font-size: 13.5pt; font-weight: 400; color: #bfdbfe; margin: 0 0 14mm; }
.cover .line { width: 42mm; height: 1.2mm; background: #60a5fa; margin-bottom: 12mm; }
.cover .points { font-size: 10.5pt; color: #dbeafe; line-height: 2.2; }
.cover .points span { color: #93c5fd; margin-right: 3mm; }
.cover .meta {
  position: absolute; bottom: 24mm; left: 22mm; right: 22mm;
  border-top: 1px solid rgba(255,255,255,.3); padding-top: 5mm;
  font-size: 9.5pt; color: #cbd5e1; line-height: 1.9;
}

/* ---------- 正文 ---------- */
h1.sec {
  font-size: 15pt; color: #0b2a5b;
  border-left: 4mm solid #2563eb; padding-left: 4mm;
  margin: 8mm 0 4mm; page-break-after: avoid;
}
h2.sub { font-size: 12pt; color: #123e7c; margin: 6mm 0 2mm; page-break-after: avoid; }
p { margin: 2.2mm 0; text-align: justify; }
li { text-align: justify; }
.newpage { page-break-before: always; }

.summary-box {
  background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 2.5mm;
  padding: 4mm 6mm; margin: 4mm 0;
}
.summary-box li { margin: 1.5mm 0; }

.keybox {
  background: #f8fafc; border-left: 2.5mm solid #94a3b8; border-radius: 1mm;
  padding: 3mm 5mm; margin: 3.5mm 0; font-size: 10pt;
}
blockquote {
  background: #f8fafc; border-left: 2.5mm solid #94a3b8; border-radius: 1mm;
  padding: 3mm 5mm; margin: 3.5mm 0; font-size: 10pt;
}

table {
  width: 100%; border-collapse: collapse; margin: 3.5mm 0; font-size: 9.5pt;
  page-break-inside: avoid;
}
th { background: #0b2a5b; color: #fff; padding: 2mm 3mm; text-align: left; font-weight: 500; }
td { border-bottom: 0.3mm solid #e2e8f0; padding: 2mm 3mm; vertical-align: top; }
tr:nth-child(even) td { background: #f8fafc; }

figure { margin: 4mm 0; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; }
figcaption { font-size: 8.5pt; color: #64748b; margin-top: 1mm; }

.refs { font-size: 8.8pt; color: #475569; line-height: 1.8; }
.refs li { margin: 1.2mm 0; word-break: break-all; }
.note { font-size: 9pt; color: #64748b; }
code { background: #f1f5f9; padding: 0.4mm 1.5mm; border-radius: 1mm; font-size: 9.5pt; }
"""

COVER = """
<div class="cover">
  <div class="tag">行业研究 · 影视传媒专题</div>
  <h1>中国电影市场深度分析报告</h1>
  <h2>—— 制度、人群、供给、冲击与全球坐标下的产业前瞻</h2>
  <div class="line"></div>
  <div class="points">
    <div><span>◆</span>大盘：2025年票房518.32亿元（+21.95%），《哪吒2》以154.46亿单片拉动近三成</div>
    <div><span>◆</span>制度：获"龙标"影片同比腰斩至373部，供给收缩成为产业最大风险</div>
    <div><span>◆</span>人群：情绪对位取代类型偏好，"平视小人物"美学接管青年文化</div>
    <div><span>◆</span>专题：2026年《牛来》从7千元翻至2千万元，照亮审查只拦红线、院线靠短视频发现内容的缝隙</div>
    <div><span>◆</span>冲击：微短剧产值约1000亿元、接近电影票房两倍，2025年为"AI短剧元年"</div>
    <div><span>◆</span>全球：全球票房约335.5亿美元；韩国本土片份额跌至40%，为中国提供压力测试预演</div>
  </div>
  <div class="meta">
    <div>报告期间：数据截至2025年度行业统计（部分为2026年初发布口径）</div>
    <div>编制日期：2026年8月19日（《牛来》专题跟踪至8月18日）</div>
    <div>数据来源：国家电影局、猫眼研究院、灯塔专业版、DataEye研究院、韩国电影振兴委员会（KOFIC）、Gower Street Analytics、Box Office Mojo 及公开媒体报道（详见文末参考资料）</div>
  </div>
</div>
"""


def build_body() -> str:
    with open(MD, encoding="utf-8") as f:
        text = f.read()

    # 封面已承载标题与要点,正文从"核心数据速览"开始(跳过标题块与目录)
    idx = text.find("## 核心数据速览")
    text = text[idx:]

    body = markdown.markdown(text, extensions=["tables", "fenced_code"])

    # 标题层级映射到参考报告的样式类
    body = body.replace("<h2>", '<h1 class="sec">').replace("</h2>", "</h1>")
    body = body.replace("<h3>", '<h2 class="sub">').replace("</h3>", "</h2>")

    # 图片包装为 figure
    body = re.sub(
        r'<p><img alt="([^"]*)" src="([^"]*)"\s*/?></p>',
        r'<figure><img alt="\1" src="\2"><figcaption>\1</figcaption></figure>',
        body,
    )

    # 分节符 hr 移除(参考报告不使用通栏分割线)
    body = re.sub(r"<hr\s*/?>", "", body)

    # 附录参考资料:另起一页并使用小字号列表
    body = body.replace(
        '<h1 class="sec">附录:主要数据来源</h1>',
        '<h1 class="sec newpage">附录：主要数据来源</h1>',
    )
    appendix_pos = body.find("附录：主要数据来源")
    if appendix_pos != -1:
        body = body[:appendix_pos] + body[appendix_pos:].replace("<ul>", '<ul class="refs">', 1)

    # 末尾说明使用弱化样式
    body = re.sub(r"<p><em>(注:[^<]*)</em></p>", r'<p class="note"><em>\1</em></p>', body)

    return body


html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>中国电影市场深度分析报告</title>
<style>{CSS}</style>
</head>
<body>
{COVER}
{build_body()}
</body>
</html>"""

with open(HTML, "w", encoding="utf-8") as f:
    f.write(html)
print("HTML written:", HTML)

proc = subprocess.Popen([
    "google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
    "--user-data-dir=/tmp/chrome-pdf-profile-niulai",
    f"--print-to-pdf={PDF}", "--no-pdf-header-footer",
    f"file://{HTML}",
])
for _ in range(40):
    if os.path.exists(PDF) and os.path.getsize(PDF) > 100000:
        import time
        time.sleep(2)
        proc.kill()
        break
    import time
    time.sleep(1)
else:
    proc.kill()
    raise RuntimeError("PDF was not written in time")
print("PDF written:", PDF, os.path.getsize(PDF))
