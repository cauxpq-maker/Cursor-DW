# -*- coding: utf-8 -*-
"""将 report.html 渲染为完整版 PDF，并拆出两菜专项附件。"""
import os
import sys

import fitz
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "report.html")
DST = os.path.join(HERE, "旅顺口区海产品养殖加工产业专题分析报告（完整版）.pdf")
DST2 = os.path.join(HERE, "annex", "旅顺口区两菜产业发展报告（独立报送稿）.pdf")


def split_two_veg(src_pdf, dest_pdf):
    src = fitz.open(src_pdf)
    start = None
    end = None
    for i, page in enumerate(src):
        text = page.get_text() or ""
        if start is None and "A1. 一句话定位" in text:
            start = i
        if start is not None and end is None and ("B1. 口径使用规则" in text or text.strip().startswith("参考资料")):
            end = i
            break
    if start is None:
        print("warn: two-veg appendix start not found")
        return
    if end is None:
        end = src.page_count
    out = fitz.open()
    out.insert_pdf(src, from_page=start, to_page=end - 1)
    os.makedirs(os.path.dirname(dest_pdf), exist_ok=True)
    out.save(dest_pdf)
    print(f"wrote {dest_pdf} pages {start+1}-{end} ({os.path.getsize(dest_pdf)} bytes)")
    out.close()
    src.close()


def main():
    if not os.path.isfile(SRC):
        sys.exit(f"missing {SRC}")
    HTML(filename=SRC, base_url=HERE).write_pdf(DST)
    print(f"wrote {DST} ({os.path.getsize(DST)} bytes)")
    split_two_veg(DST, DST2)


if __name__ == "__main__":
    main()

