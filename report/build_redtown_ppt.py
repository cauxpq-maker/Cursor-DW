# -*- coding: utf-8 -*-
"""
丹东红色文旅小镇可行性与全链路旅游体系 PPT 生成脚本(文旅风格模板)
- 全部图表为 PowerPoint 原生图表(数据可编辑)
- 地图与示意图为原生形状/自由多边形(可自由编辑)
运行: python3 build_redtown_ppt.py
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.oxml.ns import qn

# ---------------- 文旅风设计系统 ----------------
CREAM = RGBColor(0xFA, 0xF5, 0xEC)     # 米白底
INK = RGBColor(0x3F, 0x3A, 0x34)       # 墨色文字
VERMI = RGBColor(0xC4, 0x53, 0x3C)     # 朱砂红(红色文化)
GOLD = RGBColor(0xDE, 0xA4, 0x4E)      # 暖金(银杏)
PINE = RGBColor(0x4C, 0x85, 0x77)      # 松绿(生态)
RIVER = RGBColor(0x4A, 0x7F, 0xA5)     # 江蓝(鸭绿江)
SOFT = RGBColor(0x8A, 0x82, 0x76)      # 浅墨(次要文字)
CARD = RGBColor(0xFF, 0xFF, 0xFF)      # 卡片白
CARDLINE = RGBColor(0xE7, 0xDD, 0xCC)  # 卡片描边
SEAB = RGBColor(0xD9, 0xE8, 0xF0)      # 海面浅蓝
LANDB = RGBColor(0xF1, 0xE9, 0xD8)     # 陆地浅米

FONT = "微软雅黑"
SW, SH = Inches(13.333), Inches(7.5)

prs = Presentation()
prs.slide_width = SW
prs.slide_height = SH
BLANK = prs.slide_layouts[6]
PAGE = [0]


def new_slide(bg=CREAM):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = bg
    return s


def shp(slide, shape, x, y, w, h, fill=None, line=None, lw=0.75, dash=None, rot=0):
    o = slide.shapes.add_shape(shape, x, y, w, h)
    if fill is None:
        o.fill.background()
    else:
        o.fill.solid()
        o.fill.fore_color.rgb = fill
    if line is None:
        o.line.fill.background()
    else:
        o.line.color.rgb = line
        o.line.width = Pt(lw)
        if dash:
            d = o.line._get_or_add_ln()
            pd = d.makeelement(qn('a:prstDash'), {'val': dash})
            d.append(pd)
    o.shadow.inherit = False
    if rot:
        o.rotation = rot
    return o


def txt(slide, x, y, w, h, paras, size=13, color=INK, bold=False,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, ls=1.15, sa=0):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    if isinstance(paras, str):
        paras = [(paras, {})]
    first = True
    for text, ov in paras:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = ov.get("align", align)
        p.line_spacing = ov.get("ls", ls)
        p.space_after = Pt(ov.get("sa", sa))
        segs = text if isinstance(text, list) else [(text, {})]
        for st, so in segs:
            r = p.add_run()
            r.text = st
            f = r.font
            f.name = FONT
            f.size = Pt(so.get("size", ov.get("size", size)))
            f.bold = so.get("bold", ov.get("bold", bold))
            f.color.rgb = so.get("color", ov.get("color", color))
    return tb


def deco(slide):
    """轻松文旅风的角部装饰"""
    shp(slide, MSO_SHAPE.OVAL, Inches(12.55), Inches(-0.55), Inches(1.5), Inches(1.5), None, GOLD, 1.5)
    shp(slide, MSO_SHAPE.OVAL, Inches(12.9), Inches(-0.2), Inches(0.5), Inches(0.5), GOLD)
    shp(slide, MSO_SHAPE.OVAL, Inches(-0.6), Inches(6.7), Inches(1.3), Inches(1.3), None, RIVER, 1.25)


def header(slide, part, title, subtitle=None, accent=VERMI):
    PAGE[0] += 1
    deco(slide)
    shp(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(0.35), Inches(1.9), Inches(0.42), accent)
    txt(slide, Inches(0.55), Inches(0.35), Inches(1.9), Inches(0.42), part,
        size=11, color=CARD, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(slide, Inches(0.58), Inches(0.85), Inches(11.6), Inches(0.6), title,
        size=25, color=INK, bold=True)
    shp(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.5), Inches(0.9), Inches(0.06), accent)
    if subtitle:
        txt(slide, Inches(0.6), Inches(1.62), Inches(11.9), Inches(0.35), subtitle, size=12, color=SOFT)
    txt(slide, Inches(0.55), Inches(7.15), Inches(7), Inches(0.3),
        "丹东红色文旅小镇可行性与全链路旅游体系研究", size=9, color=CARDLINE)
    txt(slide, Inches(12.35), Inches(7.15), Inches(0.55), Inches(0.3),
        str(PAGE[0] + 1), size=9, color=SOFT, align=PP_ALIGN.RIGHT)


def card(slide, x, y, w, h, top_color=None):
    c = shp(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, CARD, CARDLINE, 1)
    if top_color:
        shp(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.18), y - Inches(0.09),
            Inches(0.85), Inches(0.18), top_color)
    return c


def bullets(slide, x, y, w, h, items, size=12.5, gap=7, ls=1.16, mark_color=GOLD):
    paras = []
    for lead, body in items:
        segs = [("✦ ", {"color": mark_color, "size": size - 2})]
        if lead:
            segs.append((lead, {"bold": True, "color": VERMI}))
        segs.append((body, {}))
        paras.append((segs, {"sa": gap, "ls": ls}))
    txt(slide, x, y, w, h, paras, size=size, color=INK)


def view_bar(slide, x, y, w, text, h=Inches(0.56), size=11.5):
    shp(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, RGBColor(0xF6, 0xEA, 0xDA), GOLD, 1)
    txt(slide, x + Inches(0.2), y, w - Inches(0.4), h,
        [([("观点  ", {"bold": True, "color": VERMI}), (text, {})], {})],
        size=size, color=INK, anchor=MSO_ANCHOR.MIDDLE)


def style_chart(chart, size=10, legend=True, labels=True, fmt='0.0"%"', lsize=9):
    chart.font.name = FONT
    chart.font.size = Pt(size)
    chart.font.color.rgb = INK
    chart.has_legend = legend
    if legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(size)
    if labels:
        for plot in chart.plots:
            plot.has_data_labels = True
            dl = plot.data_labels
            dl.font.size = Pt(lsize)
            dl.font.bold = True
            dl.font.color.rgb = INK
            dl.number_format = fmt
            dl.number_format_is_linked = False
            try:
                dl.position = XL_LABEL_POSITION.OUTSIDE_END
            except Exception:
                pass


def col_chart(slide, x, y, w, h, cats, series, title=None, colors=None,
              fmt='0.0"%"', legend=None, lsize=9):
    data = CategoryChartData()
    data.categories = cats
    for n, v in series:
        data.add_series(n, v)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, w, h, data)
    ch = gf.chart
    if legend is None:
        legend = len(series) > 1
    style_chart(ch, legend=legend, fmt=fmt, lsize=lsize)
    if title:
        ch.has_title = True
        ch.chart_title.text_frame.text = title
        tp = ch.chart_title.text_frame.paragraphs[0]
        tp.font.size = Pt(12); tp.font.bold = True
        tp.font.name = FONT; tp.font.color.rgb = INK
    else:
        ch.has_title = False
    pal = colors or [VERMI, GOLD, PINE, RIVER]
    for i, sr in enumerate(ch.series):
        sr.format.fill.solid()
        sr.format.fill.fore_color.rgb = pal[i % len(pal)]
    try:
        ch.plots[0].gap_width = 55
        ch.plots[0].overlap = -15 if len(series) > 1 else 0
    except Exception:
        pass
    va = ch.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor(0xEC, 0xE4, 0xD4)
    va.format.line.fill.background()
    va.tick_labels.font.size = Pt(9); va.tick_labels.font.name = FONT
    ca = ch.category_axis
    ca.format.line.color.rgb = CARDLINE
    ca.tick_labels.font.size = Pt(9.5); ca.tick_labels.font.name = FONT
    return ch


def radar_chart(slide, x, y, w, h, cats, series, title=None, colors=None):
    data = CategoryChartData()
    data.categories = cats
    for n, v in series:
        data.add_series(n, v)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.RADAR, x, y, w, h, data)
    ch = gf.chart
    ch.font.name = FONT
    ch.font.size = Pt(10)
    ch.font.color.rgb = INK
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(10.5)
    if title:
        ch.has_title = True
        ch.chart_title.text_frame.text = title
        tp = ch.chart_title.text_frame.paragraphs[0]
        tp.font.size = Pt(12); tp.font.bold = True
        tp.font.name = FONT; tp.font.color.rgb = INK
    else:
        ch.has_title = False
    pal = colors or [SOFT, VERMI, GOLD]
    for i, sr in enumerate(ch.series):
        ln = sr.format.line
        ln.color.rgb = pal[i % len(pal)]
        ln.width = Pt(2.25)
    return ch


def table(slide, x, y, w, h, rows, widths=None, header_fill=VERMI, fs=10.5, hs=11):
    n_r, n_c = len(rows), len(rows[0])
    t = slide.shapes.add_table(n_r, n_c, x, y, w, h).table
    if widths:
        tot = sum(widths)
        for i, cw in enumerate(widths):
            t.columns[i].width = Emu(int(w * cw / tot))
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            c = t.cell(ri, ci)
            c.margin_left = Inches(0.06); c.margin_right = Inches(0.06)
            c.margin_top = Inches(0.03); c.margin_bottom = Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.fill.solid()
            c.fill.fore_color.rgb = header_fill if ri == 0 else (CARD if ri % 2 == 1 else RGBColor(0xF6, 0xF0, 0xE4))
            tf = c.text_frame; tf.word_wrap = True; tf.clear()
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER
            r = p.add_run(); r.text = str(val)
            f = r.font; f.name = FONT
            f.size = Pt(hs if ri == 0 else fs)
            f.bold = (ri == 0) or (ci == 0)
            f.color.rgb = CARD if ri == 0 else (VERMI if ci == 0 else INK)
    return t


def divider(no, title, points, accent=VERMI):
    s = new_slide(RGBColor(0xF3, 0xEB, 0xDB))
    PAGE[0] += 1
    shp(s, MSO_SHAPE.OVAL, Inches(9.2), Inches(-1.8), Inches(6.2), Inches(6.2), None, GOLD, 1.5)
    shp(s, MSO_SHAPE.OVAL, Inches(10.3), Inches(-0.7), Inches(4.0), Inches(4.0), None, accent, 1.25)
    shp(s, MSO_SHAPE.OVAL, Inches(-1.5), Inches(5.3), Inches(3.6), Inches(3.6), None, RIVER, 1.25)
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(1.85), Inches(1.35), Inches(0.5), accent)
    txt(s, Inches(0.95), Inches(1.85), Inches(1.35), Inches(0.5), f"第 {no} 章",
        size=14, color=CARD, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(0.95), Inches(2.6), Inches(10.5), Inches(1.0), title, size=32, color=INK, bold=True)
    txt(s, Inches(1.0), Inches(3.75), Inches(10.2), Inches(2.2),
        [([("— ", {"color": GOLD, "bold": True}), (p, {})], {"sa": 8}) for p in points],
        size=14, color=SOFT)
    txt(s, Inches(12.35), Inches(7.05), Inches(0.55), Inches(0.3),
        str(PAGE[0] + 1), size=9, color=SOFT, align=PP_ALIGN.RIGHT)
    return s


def freeline(slide, pts_in, color, width=2.0, dash=None, close=False, fill=None):
    """pts_in: [(x_inch, y_inch)] 折线/多边形"""
    x0, y0 = pts_in[0]
    fb = slide.shapes.build_freeform(Emu(int(Inches(x0))), Emu(int(Inches(y0))), scale=1.0)
    fb.add_line_segments([(Emu(int(Inches(px))), Emu(int(Inches(py)))) for px, py in pts_in[1:]],
                         close=close)
    o = fb.convert_to_shape()
    if fill is None:
        o.fill.background()
    else:
        o.fill.solid()
        o.fill.fore_color.rgb = fill
    o.line.color.rgb = color
    o.line.width = Pt(width)
    if dash:
        ln = o.line._get_or_add_ln()
        ln.append(ln.makeelement(qn('a:prstDash'), {'val': dash}))
    o.shadow.inherit = False
    return o


class GeoMap:
    """经纬度 → 幻灯片坐标(单位:英寸浮点数,勿传 Length 对象)"""
    def __init__(self, x, y, w, h, lon0, lon1, lat0, lat1):
        self.x, self.y, self.w, self.h = float(x), float(y), float(w), float(h)
        self.lon0, self.lon1, self.lat0, self.lat1 = lon0, lon1, lat0, lat1

    def pt(self, lon, lat):
        px = self.x + (lon - self.lon0) / (self.lon1 - self.lon0) * self.w
        py = self.y + (self.lat1 - lat) / (self.lat1 - self.lat0) * self.h
        return px, py

    def line(self, slide, coords, color, width=2.0, dash=None, close=False, fill=None):
        return freeline(slide, [self.pt(lo, la) for lo, la in coords], color, width, dash, close, fill)

    def node(self, slide, lon, lat, r_in, color, label=None, lsize=9, dx=0.08, dy=-0.02,
             star=False, lcolor=None, lbold=True):
        px, py = self.pt(lon, lat)
        shape = MSO_SHAPE.STAR_5_POINT if star else MSO_SHAPE.OVAL
        o = shp(slide, shape, Inches(px - r_in), Inches(py - r_in),
                Inches(2 * r_in), Inches(2 * r_in), color)
        if label:
            txt(slide, Inches(px + dx), Inches(py + dy - 0.09), Inches(1.4), Inches(0.3),
                label, size=lsize, color=lcolor or INK, bold=lbold)
        return o


CHINA = [(73.8, 39.7), (74.8, 37.0), (78.9, 34.3), (78.7, 31.5), (81.0, 30.2), (85.0, 28.6),
         (89.0, 28.0), (92.0, 27.7), (95.0, 29.3), (97.5, 28.2), (98.7, 25.8), (97.6, 23.9),
         (100.2, 21.5), (102.0, 22.4), (105.3, 23.3), (108.0, 21.5), (110.1, 21.2), (113.2, 22.0),
         (114.8, 22.6), (116.5, 23.2), (119.2, 25.4), (120.2, 27.2), (121.5, 29.9), (121.9, 31.2),
         (120.3, 32.5), (119.6, 34.6), (120.9, 36.0), (122.6, 37.4), (119.3, 37.7), (117.8, 38.9),
         (119.5, 39.9), (121.7, 40.9), (122.3, 40.5), (121.2, 38.8), (122.5, 39.5), (124.35, 40.0),
         (125.0, 40.47), (126.2, 41.15), (126.9, 41.8), (128.1, 41.4), (128.1, 42.03), (129.0, 42.44),
         (130.65, 42.32), (131.3, 44.0), (133.1, 45.1), (134.7, 48.3), (132.6, 47.7), (130.5, 48.5),
         (127.5, 49.8), (126.0, 52.0), (123.5, 53.3), (121.5, 53.3), (119.9, 52.5), (119.8, 50.1),
         (117.4, 49.6), (115.6, 47.9), (116.7, 46.6), (111.9, 45.0), (106.8, 42.3), (104.5, 41.9),
         (101.8, 42.5), (97.2, 42.8), (95.0, 44.3), (91.0, 45.2), (90.9, 47.7), (87.8, 49.1),
         (85.6, 47.0), (83.0, 47.2), (82.3, 45.5), (80.2, 45.0), (76.9, 41.0)]

G331 = [(124.37, 40.12), (125.0, 40.47), (126.19, 41.12), (126.9, 41.8), (128.17, 41.42),
        (128.1, 42.03), (129.5, 42.9), (130.36, 42.86), (131.12, 44.06), (131.87, 45.55),
        (132.98, 45.76), (134.0, 46.8), (132.5, 47.65), (127.5, 50.24), (126.66, 51.73),
        (122.53, 52.97), (119.9, 51.35), (120.18, 50.24), (117.38, 49.6), (115.6, 47.9),
        (113.6, 43.9), (111.98, 43.65), (101.1, 42.0), (97.0, 41.8), (94.7, 43.1),
        (89.5, 46.6), (88.14, 47.85)]

G228 = [(124.37, 40.0), (122.5, 39.5), (121.2, 38.8), (122.3, 40.5), (121.7, 40.9), (119.5, 39.9),
        (117.8, 38.9), (119.3, 37.7), (122.6, 37.4), (120.9, 36.0), (119.6, 34.6), (120.3, 32.5),
        (121.9, 31.2), (121.5, 29.9), (120.2, 27.2), (119.2, 25.4), (116.5, 23.2), (113.2, 22.0),
        (110.1, 21.2), (108.0, 21.5)]

G219 = [(88.14, 47.85), (85.6, 47.0), (82.3, 45.5), (76.9, 41.0), (75.2, 38.4), (79.0, 33.5),
        (80.0, 31.0), (85.0, 28.6), (92.0, 27.7), (97.5, 28.2), (98.7, 25.8), (100.2, 21.5),
        (104.0, 22.8), (108.0, 21.5)]

YALU = [(124.35, 39.95), (124.52, 40.22), (124.9, 40.47), (125.68, 40.87), (126.19, 41.12),
        (126.9, 41.83), (127.6, 41.6), (128.17, 41.42), (128.07, 41.99)]

TUMEN = [(128.07, 41.99), (129.0, 42.44), (129.85, 42.97), (130.65, 42.32)]


# ============================================================
# 封面
# ============================================================
s = new_slide()
shp(s, MSO_SHAPE.OVAL, Inches(9.4), Inches(-2.4), Inches(7.5), Inches(7.5), RGBColor(0xF3, 0xE7, 0xD2))
shp(s, MSO_SHAPE.OVAL, Inches(10.6), Inches(-1.2), Inches(5.1), Inches(5.1), None, GOLD, 1.5)
shp(s, MSO_SHAPE.OVAL, Inches(-2.2), Inches(4.9), Inches(5.4), Inches(5.4), RGBColor(0xE9, 0xF0, 0xEE))
shp(s, MSO_SHAPE.OVAL, Inches(-1.2), Inches(5.9), Inches(3.4), Inches(3.4), None, RIVER, 1.25)
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(1.15), Inches(2.5), Inches(0.5), VERMI)
txt(s, Inches(0.95), Inches(1.15), Inches(2.5), Inches(0.5), "专 题 研 究 · 可 行 性",
    size=13, color=CARD, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0.92), Inches(1.95), Inches(11.6), Inches(1.0),
    "鸭绿江 · 1950", size=48, color=VERMI, bold=True)
txt(s, Inches(0.95), Inches(3.1), Inches(11.6), Inches(0.7),
    "丹东红色文旅小镇可行性与全链路旅游体系研究", size=24, color=INK, bold=True)
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.95), Inches(1.6), Inches(0.07), GOLD)
txt(s, Inches(0.98), Inches(4.25), Inches(11.4), Inches(1.0),
    [("项目吸引力比较 · 双层人流分析 · G331双图谱 · 虎山—叆河选址论证 · 全链路动线与门票重构", {"sa": 5}),
     ("让IP维度更丰富 · 让客群停留更长 · 让收入告别门票依赖", {"color": SOFT})],
    size=13.5, color=INK, ls=1.5)
tags = [("选址 · 虎山长城—叆河片区", VERMI), ("渡江实景 + 小剧场群 + 夜演", GOLD), ("免大门票 · 开放式街区", PINE)]
tx = Inches(0.98)
for t, c in tags:
    w = Inches(3.5)
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, tx, Inches(5.55), w, Inches(0.55), CARD, c, 1.25)
    txt(s, tx, Inches(5.55), w, Inches(0.55), t, size=12, color=c, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tx += w + Inches(0.35)
txt(s, Inches(0.98), Inches(6.55), Inches(10), Inches(0.4),
    "2026年8月 · 提纲确认后完整稿(V1) · 前序:《丹东城市旅游价值提升策略报告》", size=11.5, color=SOFT)

# ============================================================
# 目录
# ============================================================
s = new_slide()
header(s, "CONTENTS", "目录")
toc = [
    ("壹", "项目吸引力比较", "东北热点项目 vs 丹东项目 · 六要素雷达 · 缺口诊断", VERMI),
    ("贰", "人流双层比较与G331双图谱", "城市客流 vs 项目客流 · 锚定效应 · 全国图 + 东北鸭绿江流域图", RIVER),
    ("叁", "G331节点城市比较", "同江以南边境段节点 · 丹东「首站+首夜」独占位", PINE),
    ("肆", "红色文旅小镇可行性研判", "对标延安红街/遵义1935 · 虎山—叆河选址 · 八大内容模块 · 投资分级", VERMI),
    ("伍", "全链路动线与门票重构", "两日三夜动线 · 免票/低票/付费分层 · 收入模型再平衡", GOLD),
    ("陆", "实施路径与结论", "三步走 · 指标体系 · 可行性总结", PINE),
]
y = Inches(1.85)
for no, t, d, c in toc:
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.75), y, Inches(11.8), Inches(0.78), CARD, CARDLINE, 1)
    shp(s, MSO_SHAPE.OVAL, Inches(1.0), y + Inches(0.14), Inches(0.5), Inches(0.5), c)
    txt(s, Inches(1.0), y + Inches(0.14), Inches(0.5), Inches(0.5), no, size=14, color=CARD,
        bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(1.75), y + Inches(0.08), Inches(4.7), Inches(0.4), t, size=15, color=INK, bold=True)
    txt(s, Inches(1.75), y + Inches(0.45), Inches(10.5), Inches(0.3), d, size=10.5, color=SOFT)
    y += Inches(0.9)

# ============================================================
# 第壹章 项目吸引力比较
# ============================================================
divider("壹", "项目吸引力比较:丹东缺什么",
        ["东北热点项目的共同基因:强IP、高体验密度、夜间供给、四季运营",
         "六要素雷达:丹东强在心智独占,弱在体验载体",
         "诊断结论:缺一个承载3小时+停留、带动过夜的沉浸型旗舰"])

# 东北热点项目盘点
s = new_slide()
header(s, "壹 · 项目比较", "东北热点项目:游客为什么专程而来", "四类标杆,四种吸引力构造")
items = [
    ("哈尔滨冰雪大世界", "68天356万人次 · 单日峰值10万", "百万㎡冰雪奇观+24条冰滑梯+摩天轮;亚冬会加持;四季馆延续全年", VERMI),
    ("延吉民俗园/网红墙", "清明客流同比+617%", "朝鲜族服饰写真「人人可参与」;游客即内容生产者,社媒自传播", GOLD),
    ("沈阳老北市/中街", "春节沈阳1342万人次", "夜经济+民俗场景+洗浴文化;「不太远不太冷不太贵」都市休闲", PINE),
    ("长白山(沈白高铁)", "「朝发午至」改写可达性", "世界级自然IP+高铁红利;池南/二道白河集散配套成熟", RIVER),
]
x = Inches(0.62)
for t, kpi, d, c in items:
    w = Inches(3.0)
    card(s, x, Inches(2.05), w, Inches(3.3), c)
    txt(s, x + Inches(0.2), Inches(2.3), w - Inches(0.4), Inches(0.75), t, size=14.5, color=c, bold=True, ls=1.1)
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.2), Inches(3.06), w - Inches(0.4), Inches(0.52),
        RGBColor(0xF6, 0xF0, 0xE4))
    txt(s, x + Inches(0.3), Inches(3.06), w - Inches(0.6), Inches(0.52), kpi, size=10, color=INK,
        bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + Inches(0.2), Inches(3.75), w - Inches(0.4), Inches(1.5), d, size=10.5, color=INK, ls=1.25)
    x += w + Inches(0.11)
view_bar(s, Inches(0.62), Inches(5.65), Inches(12.1),
         "四个标杆的共同基因:让游客「有事可做」——高体验密度、强参与感、夜间有去处、离开时带走内容(照片/故事/纪念物)。")
txt(s, Inches(0.62), Inches(6.45), Inches(12.1), Inches(0.5),
    "数据来源:新华社、央广网、吉林省文旅厅、沈阳市文旅局公开报道(2024–2025)", size=9, color=SOFT)

# 六要素雷达
s = new_slide()
header(s, "壹 · 项目比较", "吸引力六要素:雷达对比", "0–10分专家评估口径(完整版报告附逐项评分依据)")
radar_chart(s, Inches(0.55), Inches(1.9), Inches(6.3), Inches(4.6),
            ["IP独占性", "体验密度", "停留时长", "夜间供给", "二消占比", "社交传播力"],
            [("丹东现状项目均值", (8, 3, 3, 2, 3, 5)),
             ("东北热点项目均值", (9, 9, 8, 9, 8, 9)),
             ("红色文旅城(规划目标)", (9, 8, 8, 9, 8, 8))],
            colors=[SOFT, RIVER, VERMI])
bullets(s, Inches(7.15), Inches(2.0), Inches(5.6), Inches(3.6), [
    ("IP独占性 8分:", "断桥+纪念馆+双起点,心智资产全国唯一——这是丹东最硬的底牌。"),
    ("体验密度 3分:", "断桥30分钟、纪念馆90分钟、虎山长城2小时,全程「观看型」,可参与项目稀缺。"),
    ("夜间供给 2分:", "断桥亮化之外,夜间消费载体近乎空白;游客「白天看完、晚上没事」。"),
    ("传播力 5分:", "零公里打卡已出圈,但缺少「人人可拍可晒」的体验符号(对比延吉服饰写真)。"),
], size=11.5, gap=7)
view_bar(s, Inches(7.15), Inches(5.75), Inches(5.6),
         "丹东的病症不是「没人知道」,而是「来了没处使劲」——补体验密度是第一要务。", size=10.5, h=Inches(0.72))

# 丹东项目对标表
s = new_slide()
header(s, "壹 · 项目比较", "丹东现有项目体检表", "逐项对标:游览方式、停留时长、夜间与二消能力")
rows = [
    ["项目", "游览方式", "平均停留", "夜间供给", "二消场景", "诊断"],
    ["鸭绿江断桥", "观看/凭吊", "30–50分钟", "亮化观赏", "少量文创", "心智极强,体验单薄"],
    ["抗美援朝纪念馆", "参观(免费)", "1.5–2小时", "无", "无", "精神原点,不宜商业化"],
    ["虎山长城", "登临观光", "2小时", "夜游试点中", "弱", "「起点」叙事待激活"],
    ["鸭绿江游船", "乘船观光", "40–60分钟", "少量夜航", "船票为主", "分层产品缺失"],
    ["安东老街", "逛街餐饮", "1–2小时", "有(室内)", "餐饮为主", "体量小,内容化不足"],
    ["凤凰山/青山沟等", "山岳观光", "半天–1天", "无", "弱", "距城区远,串联不足"],
]
table(s, Inches(0.6), Inches(1.95), Inches(12.15), Inches(3.7), rows,
      widths=[1.2, 1.0, 0.95, 0.95, 0.9, 1.6], fs=10.5, hs=11)
view_bar(s, Inches(0.6), Inches(5.95), Inches(12.15),
         "全市30个A级景区无一能承载3小时以上沉浸停留;红色文旅城的使命,就是补上这个「旗舰缺口」,并把纪念馆的敬仰客流转化为体验消费。")

# ============================================================
# 第贰章 人流比较与地图
# ============================================================
divider("贰", "人流双层比较与G331双图谱",
        ["同口径比:城市差距2–3倍,项目差距10倍以上",
         "旗舰项目锚定效应:头部城市都有「客流锚」",
         "两张图:G331全国走向 + 东北段(同江以南·鸭绿江流域)"], accent=RIVER)

# 双层客流比较
s = new_slide()
header(s, "贰 · 人流比较", "城市客流 vs 项目客流:差距在项目层", "城市级用2025春节同口径;项目级折算为日均客流", accent=RIVER)
col_chart(s, Inches(0.55), Inches(1.95), Inches(6.0), Inches(4.1),
          ["沈阳", "哈尔滨", "延吉\n(延边)", "丹东"],
          [("2025春节接待游客(万人次)", (1342, 1200, 466, 424))],
          title="城市级:2025春节假期客流(万人次)",
          colors=[RIVER], fmt='0"万"', legend=False, lsize=10)
col_chart(s, Inches(6.75), Inches(1.95), Inches(6.0), Inches(4.1),
          ["延安红街\n(开业首月)", "冰雪大世界\n(68天季)", "遵义1935\n(单月)", "抗美援朝\n纪念馆(春节)", "断桥\n(春节)"],
          [("日均客流(万人次/日)", (6.7, 5.2, 3.9, 1.0, 0.38))],
          title="项目级:标杆项目日均客流(万人次/日)",
          colors=[VERMI], fmt='0.0"万"', legend=False, lsize=10)
view_bar(s, Inches(0.55), Inches(6.3), Inches(12.2),
         "城市级丹东与延吉几乎同量级(424 vs 466万),但项目级差距在10倍以上——丹东的短板不在「城市没人来」,而在「没有一个项目锁住人」。")

# 锚定效应
s = new_slide()
header(s, "贰 · 人流比较", "旗舰项目「锚定效应」", "头部旅游城市都有1–2个客流锚,丹东客流散在30个景区里", accent=RIVER)
rows = [
    ["城市", "客流锚项目", "锚的作用", "丹东对应缺口"],
    ["哈尔滨", "冰雪大世界(356万/季)", "制造「专程理由」,锁定首日行程与过夜", "断桥是「顺路凭吊」,非过夜理由"],
    ["延安", "延安红街(月200万)", "把纪念地客流转化为街区消费,拉长停留", "纪念馆客流看完即走,无承接载体"],
    ["遵义", "1935街区(月120万)", "免门票聚客,纪念馆—街区15分钟生态圈", "老街体量小,与纪念馆动线未打通"],
    ["开封", "万岁山(三季度1550万)", "低票高频+高频内容,撑起复游与二消", "全市无沉浸型内容产品"],
]
table(s, Inches(0.6), Inches(1.95), Inches(12.15), Inches(3.4), rows,
      widths=[0.8, 1.6, 2.0, 1.8], fs=10.5, hs=11)
txt(s, Inches(0.6), Inches(5.55), Inches(12.15), Inches(0.4),
    [([("锚定率概念:", {"bold": True, "color": VERMI}),
       ("  旗舰项目客流 ÷ 城市总客流。头部城市锚定率普遍在15%–30%;丹东最高单体(纪念馆)锚定率不足10%,且为免费敬仰型客流,无消费转化。", {})], {})],
    size=11.5, color=INK)
view_bar(s, Inches(0.6), Inches(6.15), Inches(12.15),
         "红色文旅城的目标锚定率:开业三年内达到城市客流的15%——按丹东现状客流测算即年100万人次量级,与延安红街/遵义1935同档。")

# 全国图
s = new_slide()
header(s, "贰 · G331双图谱", "图一:G331全线与「黄金大外环」(全国示意)", "位置为示意,均为可编辑形状;完整版另附高精地图", accent=RIVER)
m = GeoMap(0.7, 1.85, 8.6, 4.7, 72, 136, 17, 55)
m.line(s, CHINA, RGBColor(0xD8, 0xCB, 0xB2), 1.25, close=True, fill=LANDB)
m.line(s, G219, PINE, 1.5, dash="dash")
m.line(s, G228, RIVER, 2.0, dash="sysDash")
m.line(s, G331, GOLD, 2.75)
for lon, lat, name, dx, dy in [
        (126.19, 41.12, "集安", 0.06, -0.05), (128.1, 42.03, "长白山", 0.07, -0.1),
        (129.5, 42.9, "延吉", 0.07, -0.22), (130.36, 42.86, "珲春", 0.12, 0.05),
        (132.5, 47.65, "同江", 0.08, -0.05), (127.5, 50.24, "黑河", 0.08, -0.05),
        (122.53, 52.97, "漠河", 0.02, -0.28), (117.38, 49.6, "满洲里", -0.75, -0.25),
        (111.98, 43.65, "二连浩特", -0.45, 0.1), (101.1, 42.0, "额济纳", -0.35, 0.12)]:
    m.node(s, lon, lat, 0.05, GOLD, name, lsize=8.5, dx=dx, dy=dy, lbold=False)
m.node(s, 88.14, 47.85, 0.07, PINE, "阿勒泰(终点)", lsize=9.5, dx=-1.15, dy=-0.3)
m.node(s, 108.0, 21.5, 0.06, RIVER, "东兴(G228终点)", lsize=8.5, dx=-0.6, dy=0.12, lbold=False)
m.node(s, 116.4, 39.9, 0.045, SOFT, "北京", lsize=8.5, dx=-0.5, dy=-0.05, lbold=False)
m.node(s, 124.37, 40.12, 0.1, VERMI, "丹东(双起点)", lsize=11, dx=0.14, dy=0.02, star=True, lcolor=VERMI)
# 图例
card(s, Inches(9.6), Inches(1.85), Inches(3.15), Inches(2.15))
txt(s, Inches(9.8), Inches(1.98), Inches(2.8), Inches(0.35), "图例", size=12, color=INK, bold=True)
for i, (c, t, dsh) in enumerate([(GOLD, "G331 沿边(9333km)", None), (RIVER, "G228 沿海(7800km)", "sysDash"),
                                  (PINE, "G219 西部边境", "dash")]):
    yy = 2.4 + i * 0.42
    freeline(s, [(9.82, yy + 0.1), (10.35, yy + 0.1)], c, 2.5, dash=dsh)
    txt(s, Inches(10.45), Inches(yy - 0.04), Inches(2.3), Inches(0.3), t, size=9.5, color=INK)
txt(s, Inches(9.8), Inches(3.62), Inches(2.9), Inches(0.35),
    [([("★ ", {"color": VERMI, "bold": True}), ("丹东:G331+G228 双起点", {})], {})], size=9.5, color=INK)
bullets(s, Inches(9.6), Inches(4.25), Inches(3.2), Inches(2.3), [
    ("", "「十五五」全面贯通三条通道,构成中国「黄金大外环」"),
    ("", "丹东是全国唯一的沿边+沿海双起点城市"),
    ("", "环线自驾兴起 → 起点城市天然承接「首站仪式+首夜停留」"),
], size=10, gap=6)

# 东北图
s = new_slide()
header(s, "贰 · G331双图谱", "图二:东北段重点(同江以南·鸭绿江流域)", "气泡大小=客流量级;红星=红色文旅城选址(虎山—叆河)", accent=RIVER)
m2 = GeoMap(0.65, 1.9, 8.2, 4.75, 120.5, 136.0, 39.2, 48.6)
# 海面
txt(s, Inches(1.15), Inches(6.25), Inches(1.2), Inches(0.35), "黄 海", size=11, color=RIVER, bold=True)
sea2 = m2.pt(133.2, 41.5)
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(sea2[0] - 1.2), Inches(sea2[1] - 0.5), Inches(2.3), Inches(1.4), SEAB)
txt(s, Inches(sea2[0] - 0.9), Inches(sea2[1] - 0.1), Inches(2.0), Inches(0.4), "日 本 海", size=11, color=RIVER, bold=True)
# 边境水系
m2.line(s, YALU, RIVER, 2.75)
m2.line(s, TUMEN, RIVER, 2.0, dash="sysDash")
ya = m2.pt(125.85, 41.05)
txt(s, Inches(ya[0]), Inches(ya[1] + 0.06), Inches(1.6), Inches(0.3), "鸭绿江", size=10, color=RIVER, bold=True)
# 叆河支流
m2.line(s, [(124.52, 40.22), (124.45, 40.45), (124.6, 40.62)], PINE, 1.75)
# G331东北段
m2.line(s, G331[:13], GOLD, 2.5)
# 高铁
m2.line(s, [(123.43, 41.8), (125.94, 41.68), (126.4, 41.94), (128.1, 42.03)], SOFT, 1.5, dash="dash")
m2.line(s, [(124.37, 40.12), (123.6, 39.9), (122.3, 39.6), (121.61, 38.91)], SOFT, 1.5, dash="dash")
# 城市气泡(大小~客流)
for lon, lat, r, name, c, dx, dy in [
        (126.53, 45.80, 0.17, "哈尔滨", RIVER, 0.2, -0.05),
        (125.32, 43.88, 0.13, "长春", RIVER, 0.16, -0.05),
        (123.43, 41.80, 0.15, "沈阳", RIVER, -0.62, -0.08),
        (121.61, 38.91, 0.13, "大连", RIVER, -0.6, -0.02),
        (129.50, 42.90, 0.11, "延吉", PINE, 0.13, -0.25),
        (128.10, 42.03, 0.11, "长白山", PINE, 0.1, -0.3),
        (126.19, 41.12, 0.07, "集安", GOLD, 0.1, 0.03),
        (126.90, 41.80, 0.06, "临江", GOLD, 0.03, 0.1),
        (130.36, 42.86, 0.07, "珲春", GOLD, 0.12, 0.04),
        (132.98, 45.76, 0.06, "虎林", GOLD, 0.1, -0.03),
        (134.00, 46.80, 0.06, "饶河", GOLD, 0.1, -0.03),
        (129.63, 44.55, 0.08, "牡丹江", SOFT, 0.11, -0.05)]:
    m2.node(s, lon, lat, r, c, name, lsize=9.5, dx=dx, dy=dy, lbold=False)
m2.node(s, 132.5, 47.65, 0.07, INK, "同江(本图北界)", lsize=9.5, dx=-1.5, dy=-0.28)
m2.node(s, 124.37, 40.05, 0.13, VERMI, "丹东", lsize=11.5, dx=-0.55, dy=0.02, lcolor=VERMI)
star_pt = m2.pt(124.52, 40.28)
m2.node(s, 124.52, 40.28, 0.1, VERMI, None, star=True)
freeline(s, [(star_pt[0] + 0.08, star_pt[1] + 0.1), (star_pt[0] + 0.95, star_pt[1] + 0.42)], VERMI, 1.0)
txt(s, Inches(star_pt[0] + 1.0), Inches(star_pt[1] + 0.28), Inches(2.9), Inches(0.32),
    "★ 红色文旅城选址(虎山—叆河)", size=9.5, color=VERMI, bold=True)
lb = m2.pt(127.9, 40.75)
txt(s, Inches(lb[0]), Inches(lb[1]), Inches(1.2), Inches(0.3), "朝 鲜", size=11, color=SOFT, bold=True)
lb2 = m2.pt(133.6, 44.3)
txt(s, Inches(lb2[0]), Inches(lb2[1]), Inches(1.2), Inches(0.3), "俄罗斯", size=10, color=SOFT, bold=True)
# 右侧图例+要点
card(s, Inches(9.15), Inches(1.9), Inches(3.6), Inches(2.35))
txt(s, Inches(9.35), Inches(2.02), Inches(3.2), Inches(0.35), "图例", size=12, color=INK, bold=True)
for i, (c, t, dsh) in enumerate([(GOLD, "G331(丹东—同江段)", None), (RIVER, "鸭绿江/图们江界河", None),
                                  (SOFT, "沈白高铁 / 丹大快铁", "dash"), (PINE, "叆河(内河支流)", None)]):
    yy = 2.42 + i * 0.4
    freeline(s, [(9.37, yy + 0.1), (9.9, yy + 0.1)], c, 2.5, dash=dsh)
    txt(s, Inches(10.0), Inches(yy - 0.04), Inches(2.7), Inches(0.3), t, size=9.5, color=INK)
bullets(s, Inches(9.15), Inches(4.4), Inches(3.65), Inches(2.2), [
    ("", "鸭绿江流域(丹东—集安—临江—长白山)是G331景观与人文最富集段"),
    ("", "丹东是全段唯一具备完整城市服务的节点"),
    ("", "选址红星紧扣「渡江原址+虎山起点」双叙事"),
], size=10, gap=6)

# ============================================================
# 第叁章 G331节点比较
# ============================================================
divider("叁", "G331节点城市比较",
        ["同江以南边境段:一串「风景点」,一座「城市港」",
         "丹东独占「首站+首夜」:仪式、补给、体验、过夜四合一"], accent=PINE)

s = new_slide()
header(s, "叁 · 节点比较", "G331重点节点城市与丹东比较", "同江以南边境段主要节点(自南向北)", accent=PINE)
rows = [
    ["节点", "核心资源", "客流量级", "住宿/服务配套", "在G331中的角色"],
    ["丹东", "双起点+断桥+纪念馆+虎山长城+江海温泉", "全年千万级(全市)", "完整城市配套/机场/高铁", "唯一「城市型始发港」"],
    ["集安", "高句丽世遗/鸭绿江国门", "假期单景区万级", "县级配套,精品民宿兴起", "文化型驿站"],
    ["临江/长白", "望天鹅/沿江风光", "小众自驾", "薄弱", "风景廊道"],
    ["长白山池南/二道白河", "长白山世界级IP", "景区年数百万级", "度假区级配套", "全线流量高峰"],
    ["延吉/珲春", "民族风情/防川一眼望三国", "延边假期数百万级", "州府级配套", "东段消费中心"],
    ["虎林/饶河/同江", "乌苏里江/湿地/赫哲族", "小众", "薄弱", "生态秘境段"],
]
table(s, Inches(0.6), Inches(1.95), Inches(12.15), Inches(3.9), rows,
      widths=[1.15, 2.0, 1.25, 1.4, 1.5], fs=10, hs=11)
view_bar(s, Inches(0.6), Inches(6.15), Inches(12.15),
         "全线多数节点是「风景点」,只有丹东能同时提供:出发仪式+物资补给+文化体验+舒适过夜——「首站+首夜」是丹东在G331价值链中的天然分工。")

s = new_slide()
header(s, "叁 · 节点比较", "丹东的「首站+首夜」方程式", "把每一辆从零公里出发的车,变成一晚以上的停留", accent=PINE)
steps = [
    ("仪式", "零公里发车礼 · 起点护照第一枚章 · 完驾证书预登记", VERMI),
    ("补给", "自驾服务中心:车检/物资/攻略 · 房车营地整备", GOLD),
    ("体验", "红色文旅城半日 · 断桥+江船 · 安东老街之夜", PINE),
    ("过夜", "主题酒店/营地首夜 · 次日晨发,正式北上G331", RIVER),
]
x = Inches(0.62)
for i, (t, d, c) in enumerate(steps):
    w = Inches(2.85)
    card(s, x, Inches(2.1), w, Inches(2.3), c)
    shp(s, MSO_SHAPE.OVAL, x + Inches(0.2), Inches(2.32), Inches(0.62), Inches(0.62), c)
    txt(s, x + Inches(0.2), Inches(2.32), Inches(0.62), Inches(0.62), t, size=13, color=CARD,
        bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + Inches(0.2), Inches(3.15), w - Inches(0.4), Inches(1.1), d, size=11, color=INK, ls=1.3)
    if i < 3:
        shp(s, MSO_SHAPE.RIGHT_ARROW, x + w + Inches(0.02), Inches(3.0), Inches(0.24), Inches(0.4), GOLD)
    x += w + Inches(0.28)
bullets(s, Inches(0.62), Inches(4.75), Inches(12.1), Inches(1.5), [
    ("联盟策略:", "发起「G331起点城市联盟」(丹东—集安—长白山—延吉),互认起点护照与通票,共推「一程多站」;丹东争取秘书处/发布权,固化「始发港」话语权。"),
    ("数据目标:", "自驾客首夜留丹率从目前的低位提升至50%以上;每留一夜,人均消费预计增加300–500元(住宿+餐饮+演艺)。"),
], size=11.5, gap=7)
view_bar(s, Inches(0.62), Inches(6.35), Inches(12.1),
         "红色文旅城正是「体验+过夜」两环的核心载体——没有它,「首站」只是一张照片;有了它,「首站」才是一晚生意。")

# ============================================================
# 第肆章 红色文旅小镇可行性
# ============================================================
divider("肆", "红色文旅小镇可行性研判",
        ["对标已验证:延安红街月200万 · 遵义1935月120万",
         "选址确认:鸭绿江上游 虎山长城—叆河片区新开发",
         "八大内容模块 · 免大门票 · 投资分级滚动"], accent=VERMI)

# 对标案例
s = new_slide()
header(s, "肆 · 可行性", "对标:红色小镇模式已被市场验证")
cases = [
    ("延安红街", "万达投资 · 市场化运营", "61公顷、1.5公里街区;互动体验业态超60%;开业首月200万人次,80/90/00后占比过半", VERMI),
    ("遵义1935街区", "免门票 · 纪念馆生态圈", "与遵义会议纪念馆一街之隔;红军街+广场+公园整合;单月120万人次;「敬仰在馆内、消费在街区」", GOLD),
    ("红安影视幻城", "剧情+场景+互动", "「大别山抗战」等剧目线上售票旺盛;礼包宠客+票根经济;县域红色流量转化样本", PINE),
    ("万岁山(方法论)", "低价高频 · NPC玩家化", "百元票三日无限次;NPC全域互动+高频内容更新;前三季度1550万人次、收入9.5亿", RIVER),
]
x, y0 = Inches(0.62), Inches(1.85)
for i, (t, sub, d, c) in enumerate(cases):
    cx = x + (i % 2) * Inches(6.2)
    cy = y0 + (i // 2) * Inches(2.15)
    card(s, cx, cy, Inches(5.95), Inches(1.98), c)
    txt(s, cx + Inches(0.22), cy + Inches(0.14), Inches(3.4), Inches(0.4), t, size=14.5, color=c, bold=True)
    txt(s, cx + Inches(3.0), cy + Inches(0.18), Inches(2.8), Inches(0.35), sub, size=10, color=SOFT, align=PP_ALIGN.RIGHT)
    txt(s, cx + Inches(0.22), cy + Inches(0.62), Inches(5.5), Inches(1.3), d, size=10.5, color=INK, ls=1.25)
view_bar(s, Inches(0.62), Inches(6.25), Inches(12.1),
         "四个样本共同回答了可行性三问:红色内容能吸引年轻人(延安)、免门票街区能盈利(遵义)、沉浸运营能长红(万岁山)。丹东的题材烈度(渡江出征)高于以上任何一家。")

# 选址论证
s = new_slide()
header(s, "肆 · 可行性", "选址论证:鸭绿江上游 · 虎山长城—叆河片区", "已确认方向;五大理由+两项风险对策")
reasons = [
    ("① 历史原址", "九连城马市渡口一带为1950年志愿军渡江浮桥区域之一——「渡江」演艺发生在真实历史空间,叙事无可替代", VERMI),
    ("② 水域自由", "叆河为内河支流,不属界河管控水域;「抢渡过江/攻打据点」水上实景演艺的合规性与调度自由度远高于鸭绿江主航道", RIVER),
    ("③ 动线枢纽", "地处城区(断桥/老街)与虎山长城/零公里之间,把全链路自然缝合;与国门湾营地形成「营地+小镇」组团", GOLD),
    ("④ 双叙事叠加", "与虎山长城(长城东端起点)和G331零公里共享客流:「长城起点+出征起点」双重仪式感", PINE),
    ("⑤ 土地成本", "城郊结合部新开发,存量用地充裕、拆迁量小,建设成本与用地弹性显著优于城区改造", SOFT),
]
y = Inches(1.9)
for t, d, c in reasons:
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.62), y, Inches(7.7), Inches(0.85), CARD, CARDLINE, 1)
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.62), y, Inches(0.09), Inches(0.85), c)
    txt(s, Inches(0.88), y + Inches(0.07), Inches(1.6), Inches(0.7), t, size=11.5, color=c, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(2.45), y + Inches(0.07), Inches(5.75), Inches(0.72), d, size=9.8, color=INK, ls=1.12, anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.95)
card(s, Inches(8.55), Inches(1.9), Inches(4.2), Inches(4.6), VERMI)
txt(s, Inches(8.8), Inches(2.08), Inches(3.7), Inches(0.4), "两项风险 · 对策", size=13.5, color=VERMI, bold=True)
bullets(s, Inches(8.8), Inches(2.55), Inches(3.75), Inches(3.8), [
    ("距城区约15公里:", "接驳专线(断桥—老街—小镇—虎山循环巴士);自驾/房车客群本就在此动线上;通票含接驳。"),
    ("冬季运营压力:", "小剧场群/演艺厅全部室内化;酒店配温泉业态;冬季主打「1950年的冬天」主题(长津湖季),把季节劣势转为叙事资产。"),
], size=10.5, gap=9)

# 内容模块
s = new_slide()
header(s, "肆 · 可行性", "内容规划:「鸭绿江·1950」八大模块", "按确认方向:战争年代情景整体还原,渡江+后勤两大主线")
mods = [
    ("① 抢渡实景演艺", "叆河水岸「抢渡过江/攻打据点」大型情景演艺,烟火/灯光/水效,日场+旺季加演", VERMI),
    ("② 后勤支前街区", "支前市井还原:军需缝纫、担架队、炒面坊、火车站台;NPC常态化互动", GOLD),
    ("③ 主题小剧场群", "6–8个室内小剧场轮演(15–30分钟):坑道、战地医院、一封家书、凯旋", PINE),
    ("④ 夜景大型歌舞演艺", "驻场晚会(约60分钟):从出征到凯旋的史诗歌舞,夜间留客核心引擎", RIVER),
    ("⑤ NPC角色化游园", "入伍登记/通行证/军功章集章任务线,游客成为「剧中人」", VERMI),
    ("⑥ 配套商街", "安东1950风貌商街:丹东美食(黄蚬子/朝鲜族风味)+军旅文创+老字号", GOLD),
    ("⑦ 配套酒店+营地", "主题酒店(温泉)+营地木屋,联动国门湾房车营地,承接「首夜」", PINE),
    ("⑧ 研学营地", "课程化产品:行军/旗语/战地炊事/家书课堂,对接学校与机关团建", RIVER),
]
x, y0 = Inches(0.62), Inches(1.9)
for i, (t, d, c) in enumerate(mods):
    cx = x + (i % 4) * Inches(3.11)
    cy = y0 + (i // 4) * Inches(2.15)
    card(s, cx, cy, Inches(2.96), Inches(1.98), c)
    txt(s, cx + Inches(0.16), cy + Inches(0.13), Inches(2.65), Inches(0.6), t, size=12, color=c, bold=True, ls=1.05)
    txt(s, cx + Inches(0.16), cy + Inches(0.72), Inches(2.65), Inches(1.2), d, size=9.5, color=INK, ls=1.18)
view_bar(s, Inches(0.62), Inches(6.3), Inches(12.1),
         "庄重底线:战斗与牺牲场景只在演艺与研学中呈现,商业娱乐业态严格限定在「支前市井」层面;开园即建立内容审查与讲解词规范。")

# 空间布局
s = new_slide()
header(s, "肆 · 可行性", "空间布局概念(示意)", "沿叆河展开「一轴四区」,与虎山长城/零公里/国门湾组团联动")
# 概念图
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), Inches(1.95), Inches(8.0), Inches(4.3), RGBColor(0xF4, 0xEE, 0xE0), CARDLINE, 1)
freeline(s, [(0.9, 5.6), (2.4, 5.15), (4.2, 5.05), (6.2, 4.75), (8.5, 4.55)], RIVER, 4.0)
txt(s, Inches(6.9), Inches(4.85), Inches(1.6), Inches(0.3), "叆河水岸(演艺水域)", size=9.5, color=RIVER, bold=True)
zones = [
    (1.0, 2.3, 1.75, 1.25, "入口广场\n入伍登记·仪式", VERMI),
    (2.95, 2.2, 2.0, 1.5, "支前老街\n商街+NPC市井", GOLD),
    (5.15, 2.3, 1.8, 1.3, "小剧场群\n室内轮演", PINE),
    (7.05, 2.45, 1.5, 1.15, "夜演大剧场", VERMI),
    (2.6, 4.0, 1.9, 1.0, "研学营地", PINE),
    (5.0, 3.85, 1.9, 0.95, "渡江实景区\n(水岸看台)", RIVER),
]
for zx, zy, zw, zh, zt, zc in zones:
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(zx), Inches(zy), Inches(zw), Inches(zh), CARD, zc, 1.5)
    txt(s, Inches(zx), Inches(zy), Inches(zw), Inches(zh), zt, size=10, color=zc, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ls=1.15)
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(5.75), Inches(2.6), Inches(0.42), CARD, SOFT, 1.25)
txt(s, Inches(0.95), Inches(5.75), Inches(2.6), Inches(0.42), "酒店+温泉+营地木屋区", size=9.5, color=SOFT,
    bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(6.3), Inches(2.0), Inches(2.3), Inches(0.35),
    [([("→ 虎山长城 · 零公里(3km)", {"bold": True, "color": PINE})], {})], size=9.5)
bullets(s, Inches(8.95), Inches(2.0), Inches(3.8), Inches(4.2), [
    ("一轴:", "叆河水岸景观演艺轴,白天市井、傍晚抢渡、夜晚大秀。"),
    ("动区与静区分离:", "演艺/研学在水岸侧,酒店温泉在背水侧,互不干扰。"),
    ("全室内小剧场:", "冬季主力产品,保障四季运营。"),
    ("组团联动:", "与虎山长城、零公里地标、国门湾房车营地构成「起点组团」,共享停车与接驳。"),
], size=11, gap=8)

# 商业模式
s = new_slide()
header(s, "肆 · 可行性", "商业模式:免大门票,分级投资,滚动开发")
col_chart(s, Inches(0.6), Inches(1.9), Inches(5.7), Inches(4.2),
          ["门票", "演艺票", "餐饮商街", "住宿温泉", "研学/文创"],
          [("传统景区模式(%)", (60, 5, 15, 12, 8)),
           ("鸭绿江·1950目标(%)", (0, 30, 25, 28, 17))],
          title="收入结构对比(示意)", colors=[SOFT, VERMI], fmt='0"%"', lsize=9)
bullets(s, Inches(6.6), Inches(1.95), Inches(6.2), Inches(2.9), [
    ("免大门票:", "街区开放进入,聚客优先(遵义模式);演艺、剧场、研学按项目收费,通票可含1场小剧场。"),
    ("投资分级:", "一期「轻」——支前老街+小剧场2个+水岸日场演艺,快速开业验证;二期「中」——夜演大剧场+酒店;三期「重」——视数据加码扩容。"),
    ("运营主体:", "政府平台公司持有资产+专业演艺运营团队(市场化选聘)+商户生态招商,「延安红街」股权与运营分离模式。"),
], size=11.5, gap=8)
view_bar(s, Inches(6.6), Inches(5.05), Inches(6.15),
         "原则:一次性投资严控,先内容后砖头——演艺内容是资产,建筑只是容器。", size=10.5, h=Inches(0.72))
txt(s, Inches(6.6), Inches(5.95), Inches(6.15), Inches(0.9),
    [([("可行性结论:", {"bold": True, "color": VERMI}),
       ("  有条件可行。题材独占、模式已验证、选址成立;约束条件是投资节奏与内容品质——「内容先行、分期滚动、免票聚客」。", {})], {"ls": 1.3})],
    size=12, color=INK)

# ============================================================
# 第伍章 全链路动线
# ============================================================
divider("伍", "全链路动线与门票重构",
        ["两日三夜:美食—老街—纪念馆—红色文旅城—断桥—江船—沿江自驾—虎山长城",
         "免票聚客 · 低票通行 · 付费体验三层结构",
         "门票收入占比目标降至30%以下"], accent=GOLD)

# 动线图
s = new_slide()
header(s, "伍 · 全链路", "「两日三夜」全链路动线", "每个节点都有明确分工:引流、体验、消费、过夜", accent=GOLD)
rows_flow = [
    ("抵达夜", GOLD, [("美食暖场", "夜市/黄蚬子/朝鲜族风味", "免票·引流"),
                      ("安东老街夜游", "市井烟火+首枚护照章", "免票·引流")]),
    ("第一日", VERMI, [("抗美援朝纪念馆", "敬仰·精神原点(上午)", "免费·分发"),
                       ("红色文旅城", "小剧场+支前街+午餐(午后)", "体验付费"),
                       ("断桥+江船日落航班", "凭吊+两岸观景(傍晚)", "通票+船票"),
                       ("夜演「鸭绿江·1950」", "大型歌舞演艺(夜)", "演艺票·留客")]),
    ("第二日", PINE, [("沿江自驾G331段", "江海线/河口方向(上午)", "免费·串联"),
                      ("虎山长城", "长城东端起点登临(午后)", "通票"),
                      ("零公里发车仪式", "完驾证书/北上启程(离城)", "免费·仪式")]),
]
y = Inches(1.95)
for day, c, nodes in rows_flow:
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.62), y, Inches(1.15), Inches(1.28), c)
    txt(s, Inches(0.62), y, Inches(1.15), Inches(1.28), day, size=13, color=CARD, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    x = Inches(1.95)
    n = len(nodes)
    for i, (t, d, tag) in enumerate(nodes):
        w = Inches(2.52) if n == 4 else Inches(3.4)
        card(s, x, y, w, Inches(1.28))
        txt(s, x + Inches(0.14), y + Inches(0.08), w - Inches(0.28), Inches(0.35), t, size=11, color=c, bold=True)
        txt(s, x + Inches(0.14), y + Inches(0.44), w - Inches(0.28), Inches(0.45), d, size=9, color=INK, ls=1.1)
        txt(s, x + Inches(0.14), y + Inches(0.95), w - Inches(0.28), Inches(0.28), tag, size=8.5, color=SOFT, bold=True)
        if i < n - 1:
            shp(s, MSO_SHAPE.RIGHT_ARROW, x + w + Inches(0.015), y + Inches(0.48), Inches(0.16), Inches(0.3), GOLD)
        x += w + Inches(0.19)
    y += Inches(1.48)
view_bar(s, Inches(0.62), Inches(6.45), Inches(12.1),
         "动线闭环的关键在两个「夜」:老街之夜负责第一晚,1950夜演负责第二晚——夜产品每留住一晚,人均消费提升300元以上。", size=10.5)

# 三层票务
s = new_slide()
header(s, "伍 · 全链路", "门票依赖重构:三层收入结构", "免票聚客、低票通行、付费体验——收入跟着停留走", accent=GOLD)
layers = [
    ("免票引流层", "安东老街 · 红色文旅城街区 · 沿江岸线 · 零公里地标 · 纪念馆(公益)", "作用:把人聚进来,制造「随时可来」的低门槛", PINE),
    ("低票通行层", "City Pass通票:断桥+虎山长城+游船基础航班+接驳巴士(3日有效)", "作用:一次付费全城通行,消灭「逐个买票」的摩擦", GOLD),
    ("付费体验层", "1950夜演 · 小剧场 · 江船日落/主题航班 · 研学课程 · 温泉酒店", "作用:为「值得的体验」付费,承担主要收入", VERMI),
]
y = Inches(1.95)
for t, d, role, c in layers:
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.62), y, Inches(12.1), Inches(1.15), CARD, CARDLINE, 1)
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.62), y, Inches(1.7), Inches(1.15), c)
    txt(s, Inches(0.62), y, Inches(1.7), Inches(1.15), t, size=12.5, color=CARD, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(2.55), y + Inches(0.12), Inches(10.0), Inches(0.5), d, size=11.5, color=INK, bold=True)
    txt(s, Inches(2.55), y + Inches(0.62), Inches(10.0), Inches(0.42), role, size=10, color=SOFT)
    y += Inches(1.3)
bullets(s, Inches(0.62), Inches(5.95), Inches(12.1), Inches(1.1), [
    ("指标体系:", "平均停留时长(目标2晚3天)、过夜率、人均二消、非门票收入占比(>70%)、旗舰锚定率(>15%)、复游率。"),
], size=11.5)

# ============================================================
# 第陆章 实施与结论
# ============================================================
divider("陆", "实施路径与结论",
        ["三步走:动线先行 → 小镇一期 → 旗舰扩容",
         "结论:有条件可行,内容先行、分期滚动"], accent=PINE)

s = new_slide()
header(s, "陆 · 实施", "三步走路线图", None, accent=PINE)
phases = [
    ("第一步 · 动线先行", "0–12个月 · 轻投入", [
        "City Pass通票+接驳环线开通",
        "老街夜与江船日落航班上线",
        "零公里仪式+起点护照运营",
        "小镇一期开工(支前老街+2个小剧场+日场演艺)",
    ], GOLD),
    ("第二步 · 小镇成势", "1–3年 · 中投入", [
        "「鸭绿江·1950」一期开业(免大门票)",
        "夜演大剧场+主题酒店二期",
        "研学课程对接学校/机关规模化",
        "G331起点城市联盟与通票互认",
    ], VERMI),
    ("第三步 · 旗舰扩容", "3–5年 · 视数据决策", [
        "演艺扩容/水岸夜游二期",
        "争创国家级旅游度假区/5A",
        "入境边境游产品(政策窗口)",
        "「旅居+研学+自驾」三客群体系成熟",
    ], PINE),
]
x = Inches(0.62)
for t, tm, its, c in phases:
    w = Inches(3.95)
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.95), w, Inches(0.85), c)
    txt(s, x + Inches(0.2), Inches(2.03), w - Inches(0.4), Inches(0.4), t, size=13.5, color=CARD, bold=True)
    txt(s, x + Inches(0.2), Inches(2.4), w - Inches(0.4), Inches(0.32), tm, size=10, color=RGBColor(0xF6, 0xF0, 0xE4))
    card(s, x, Inches(2.95), w, Inches(3.15))
    txt(s, x + Inches(0.2), Inches(3.12), w - Inches(0.4), Inches(2.85),
        [([("· ", {"color": c, "bold": True}), (it, {})], {"sa": 8, "ls": 1.18}) for it in its],
        size=10.5, color=INK)
    x += w + Inches(0.12)
view_bar(s, Inches(0.62), Inches(6.35), Inches(12.1),
         "第一步不等小镇建成:动线与夜产品先跑起来,既提前兑现停留与二消,也为小镇开业积累客流与口碑。")

# 结论页
s = new_slide()
header(s, "陆 · 结论", "可行性结论与下一步工作", None, accent=PINE)
concl = [
    ("题材可行", "抗美援朝渡江叙事全国独占,烈度高于延安/遵义已验证题材;年轻客群接受度已被市场证明", VERMI),
    ("选址可行", "虎山—叆河:渡江历史原址+内河水域演艺自由+起点组团联动+新开发用地弹性", GOLD),
    ("模式可行", "免大门票开放街区+三层收入结构,门票依赖降至30%以下;投资分级滚动,风险可控", PINE),
    ("体系可行", "两日三夜全链路把美食、老街、纪念馆、断桥、江船、自驾、小镇、虎山串成闭环,IP维度从「打卡」升维到「入戏」", RIVER),
]
x, y0 = Inches(0.62), Inches(1.9)
for i, (t, d, c) in enumerate(concl):
    cx = x + (i % 2) * Inches(6.2)
    cy = y0 + (i // 2) * Inches(1.7)
    card(s, cx, cy, Inches(5.95), Inches(1.55), c)
    txt(s, cx + Inches(0.22), cy + Inches(0.13), Inches(5.5), Inches(0.4), t, size=13.5, color=c, bold=True)
    txt(s, cx + Inches(0.22), cy + Inches(0.55), Inches(5.5), Inches(0.9), d, size=10.5, color=INK, ls=1.22)
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.62), Inches(5.45), Inches(12.1), Inches(1.35), RGBColor(0xF3, 0xEB, 0xDB), GOLD, 1.25)
txt(s, Inches(0.92), Inches(5.62), Inches(11.6), Inches(1.05),
    [([("下一步工作(确认后展开):", {"bold": True, "color": VERMI})], {"sa": 4}),
     ("① 小镇一期概念方案与投资估算  ② 客流与收入测算模型  ③ 演艺内容大纲(渡江/支前/夜演)  ④ 通票定价与联盟谈判方案", {})],
    size=12, color=INK, ls=1.3)

# 封底
s = new_slide(RGBColor(0xF3, 0xEB, 0xDB))
PAGE[0] += 1
shp(s, MSO_SHAPE.OVAL, Inches(9.6), Inches(-2.0), Inches(6.5), Inches(6.5), None, GOLD, 1.5)
shp(s, MSO_SHAPE.OVAL, Inches(-1.8), Inches(5.0), Inches(4.2), Inches(4.2), None, RIVER, 1.25)
txt(s, Inches(0.95), Inches(2.5), Inches(11.4), Inches(1.0),
    "让游客从「打卡起点」,到「走进1950」", size=32, color=INK, bold=True)
txt(s, Inches(0.98), Inches(3.6), Inches(11.2), Inches(1.2),
    [("红色文旅城不是又一个景区,而是丹东全链路的「留量心脏」——", {"sa": 5}),
     ("它让纪念馆的敬仰有了去处,让零公里的仪式有了下文,让每一晚停留都有理由。", {})],
    size=15, color=SOFT, ls=1.4)
txt(s, Inches(0.98), Inches(5.4), Inches(11), Inches(0.5),
    "鸭绿江畔 · 丹东真好", size=13, color=GOLD, bold=True)

OUT = "丹东红色文旅小镇可行性与全链路旅游体系.pptx"
prs.save(OUT)
print(f"saved: {OUT}, pages: {len(prs.slides._sldIdLst)}")
