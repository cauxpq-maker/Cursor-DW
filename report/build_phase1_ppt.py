# -*- coding: utf-8 -*-
"""
「鸭绿江·1950」一期概念方案·投资估算·测算模型·演艺大纲 PPT(文旅风模板)
运行: python3 build_phase1_ppt.py
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.oxml.ns import qn

CREAM = RGBColor(0xFA, 0xF5, 0xEC)
INK = RGBColor(0x3F, 0x3A, 0x34)
VERMI = RGBColor(0xC4, 0x53, 0x3C)
GOLD = RGBColor(0xDE, 0xA4, 0x4E)
PINE = RGBColor(0x4C, 0x85, 0x77)
RIVER = RGBColor(0x4A, 0x7F, 0xA5)
SOFT = RGBColor(0x8A, 0x82, 0x76)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
CARDLINE = RGBColor(0xE7, 0xDD, 0xCC)

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


def shp(slide, shape, x, y, w, h, fill=None, line=None, lw=0.75, dash=None):
    o = slide.shapes.add_shape(shape, x, y, w, h)
    if fill is None:
        o.fill.background()
    else:
        o.fill.solid(); o.fill.fore_color.rgb = fill
    if line is None:
        o.line.fill.background()
    else:
        o.line.color.rgb = line; o.line.width = Pt(lw)
        if dash:
            d = o.line._get_or_add_ln()
            d.append(d.makeelement(qn('a:prstDash'), {'val': dash}))
    o.shadow.inherit = False
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
            r = p.add_run(); r.text = st
            f = r.font
            f.name = FONT
            f.size = Pt(so.get("size", ov.get("size", size)))
            f.bold = so.get("bold", ov.get("bold", bold))
            f.color.rgb = so.get("color", ov.get("color", color))
    return tb


def deco(slide):
    shp(slide, MSO_SHAPE.OVAL, Inches(12.55), Inches(-0.55), Inches(1.5), Inches(1.5), None, GOLD, 1.5)
    shp(slide, MSO_SHAPE.OVAL, Inches(12.9), Inches(-0.2), Inches(0.5), Inches(0.5), GOLD)
    shp(slide, MSO_SHAPE.OVAL, Inches(-0.6), Inches(6.7), Inches(1.3), Inches(1.3), None, RIVER, 1.25)


def header(slide, part, title, subtitle=None, accent=VERMI):
    PAGE[0] += 1
    deco(slide)
    shp(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(0.35), Inches(2.2), Inches(0.42), accent)
    txt(slide, Inches(0.55), Inches(0.35), Inches(2.2), Inches(0.42), part,
        size=11, color=CARD, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(slide, Inches(0.58), Inches(0.85), Inches(11.6), Inches(0.6), title, size=25, color=INK, bold=True)
    shp(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.5), Inches(0.9), Inches(0.06), accent)
    if subtitle:
        txt(slide, Inches(0.6), Inches(1.62), Inches(11.9), Inches(0.35), subtitle, size=12, color=SOFT)
    txt(slide, Inches(0.55), Inches(7.15), Inches(7), Inches(0.3),
        "「鸭绿江·1950」一期方案·测算·演艺大纲", size=9, color=CARDLINE)
    txt(slide, Inches(12.35), Inches(7.15), Inches(0.55), Inches(0.3),
        str(PAGE[0] + 1), size=9, color=SOFT, align=PP_ALIGN.RIGHT)


def card(slide, x, y, w, h, top_color=None):
    c = shp(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, CARD, CARDLINE, 1)
    if top_color:
        shp(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.18), y - Inches(0.09),
            Inches(0.85), Inches(0.18), top_color)
    return c


def bullets(slide, x, y, w, h, items, size=12.5, gap=7, ls=1.16):
    paras = []
    for lead, body in items:
        segs = [("✦ ", {"color": GOLD, "size": size - 2})]
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


def col_chart(slide, x, y, w, h, cats, series, title=None, colors=None,
              fmt='#,##0', legend=None, lsize=9, ctype=XL_CHART_TYPE.COLUMN_CLUSTERED):
    data = CategoryChartData()
    data.categories = cats
    for n, v in series:
        data.add_series(n, v)
    ch = slide.shapes.add_chart(ctype, x, y, w, h, data).chart
    ch.font.name = FONT; ch.font.size = Pt(10); ch.font.color.rgb = INK
    if legend is None:
        legend = len(series) > 1
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(10)
    for plot in ch.plots:
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.font.size = Pt(lsize); dl.font.bold = True; dl.font.color.rgb = INK
        dl.number_format = fmt; dl.number_format_is_linked = False
        try:
            dl.position = XL_LABEL_POSITION.OUTSIDE_END
        except Exception:
            pass
    if title:
        ch.has_title = True
        ch.chart_title.text_frame.text = title
        tp = ch.chart_title.text_frame.paragraphs[0]
        tp.font.size = Pt(12); tp.font.bold = True; tp.font.name = FONT; tp.font.color.rgb = INK
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


def pie_chart(slide, x, y, w, h, cats, vals, title=None, colors=None, fmt='0"%"'):
    data = CategoryChartData()
    data.categories = cats
    data.add_series("占比", vals)
    ch = slide.shapes.add_chart(XL_CHART_TYPE.PIE, x, y, w, h, data).chart
    ch.font.name = FONT; ch.font.size = Pt(10)
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(9.5)
    plot = ch.plots[0]
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format = fmt; dl.number_format_is_linked = False
    dl.font.size = Pt(10); dl.font.bold = True; dl.font.color.rgb = CARD
    if title:
        ch.has_title = True
        ch.chart_title.text_frame.text = title
        tp = ch.chart_title.text_frame.paragraphs[0]
        tp.font.size = Pt(12); tp.font.bold = True; tp.font.name = FONT; tp.font.color.rgb = INK
    else:
        ch.has_title = False
    pal = colors or [VERMI, GOLD, PINE, RIVER, SOFT]
    for i, pt_ in enumerate(ch.series[0].points):
        pt_.format.fill.solid()
        pt_.format.fill.fore_color.rgb = pal[i % len(pal)]
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


# ============ 封面 ============
s = new_slide()
shp(s, MSO_SHAPE.OVAL, Inches(9.4), Inches(-2.4), Inches(7.5), Inches(7.5), RGBColor(0xF3, 0xE7, 0xD2))
shp(s, MSO_SHAPE.OVAL, Inches(10.6), Inches(-1.2), Inches(5.1), Inches(5.1), None, GOLD, 1.5)
shp(s, MSO_SHAPE.OVAL, Inches(-2.2), Inches(4.9), Inches(5.4), Inches(5.4), RGBColor(0xE9, 0xF0, 0xEE))
shp(s, MSO_SHAPE.OVAL, Inches(-1.2), Inches(5.9), Inches(3.4), Inches(3.4), None, RIVER, 1.25)
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(1.1), Inches(3.2), Inches(0.5), VERMI)
txt(s, Inches(0.95), Inches(1.1), Inches(3.2), Inches(0.5), "一期深化 · 三合一交付",
    size=13, color=CARD, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0.92), Inches(1.85), Inches(11.6), Inches(1.0),
    "「鸭绿江 · 1950」一期", size=44, color=VERMI, bold=True)
txt(s, Inches(0.95), Inches(2.95), Inches(11.6), Inches(0.7),
    "概念方案与投资估算 · 客流与收入测算模型 · 演艺内容大纲", size=22, color=INK, bold=True)
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.75), Inches(1.6), Inches(0.07), GOLD)
txt(s, Inches(0.98), Inches(4.05), Inches(11.4), Inches(0.9),
    [("选址:虎山长城—叆河片区 · 免大门票开放街区 · 一期投资约3.1亿元(概念级±30%)", {"sa": 5}),
     ("附:可编辑Excel测算模型(参数联动,黄色单元格即改即算)", {"color": SOFT})],
    size=13.5, color=INK, ls=1.5)
tags = [("一期约200亩 · 12个月建成", VERMI), ("基准年客流100万 · 收入7,700万", GOLD), ("日场抢渡 + 4小剧场 + NPC街区", PINE)]
tx = Inches(0.98)
for t, c in tags:
    w = Inches(3.7)
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, tx, Inches(5.35), w, Inches(0.55), CARD, c, 1.25)
    txt(s, tx, Inches(5.35), w, Inches(0.55), t, size=11.5, color=c, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tx += w + Inches(0.25)
txt(s, Inches(0.98), Inches(6.45), Inches(10), Inches(0.4),
    "2026年8月 · 概念深化稿(V1) · 前序:《丹东红色文旅小镇可行性与全链路旅游体系》", size=11.5, color=SOFT)

# ============ 目录 ============
s = new_slide()
header(s, "CONTENTS", "目录")
toc = [
    ("壹", "一期概念方案", "定位与开发原则 · 一轴四区分区 · 业态面积清单 · 12个月建设时序", VERMI),
    ("贰", "投资估算", "分项估算表(概念级±30%) · 投资结构 · 二三期预留与决策门槛 · 资金组织", GOLD),
    ("叁", "客流与收入测算模型", "测算逻辑与假设 · 三情景客流 · 收入/成本/盈亏平衡 · 敏感性 · Excel模型使用", PINE),
    ("肆", "演艺内容大纲", "总叙事 · 日场《抢渡鸭绿江》 · NPC任务线 · 小剧场群剧目 · 夜演分幕(二期) · 更新机制", RIVER),
]
y = Inches(2.0)
for no, t, d, c in toc:
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.75), y, Inches(11.8), Inches(1.0), CARD, CARDLINE, 1)
    shp(s, MSO_SHAPE.OVAL, Inches(1.0), y + Inches(0.25), Inches(0.5), Inches(0.5), c)
    txt(s, Inches(1.0), y + Inches(0.25), Inches(0.5), Inches(0.5), no, size=14, color=CARD,
        bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(1.75), y + Inches(0.16), Inches(5.2), Inches(0.4), t, size=16, color=INK, bold=True)
    txt(s, Inches(1.75), y + Inches(0.58), Inches(10.5), Inches(0.32), d, size=10.5, color=SOFT)
    y += Inches(1.15)

# ============ 第壹章 概念方案 ============
divider("壹", "一期概念方案",
        ["定位:全链路的「留量心脏」,免大门票开放街区",
         "一期约200亩,一轴四区,建筑面积约1.9万㎡",
         "12个月建成开业,先内容后砖头"])

# 定位与开发原则
s = new_slide()
header(s, "壹 · 概念方案", "一期定位与六条开发原则", "小步快跑:用最小可行产品验证「渡江叙事+免票街区」模型")
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.62), Inches(1.85), Inches(12.1), Inches(1.05), RGBColor(0xF3, 0xEB, 0xDB), GOLD, 1.25)
txt(s, Inches(0.9), Inches(2.0), Inches(11.6), Inches(0.8),
    [([("一期定位:", {"bold": True, "color": VERMI}),
       ("「鸭绿江·1950」支前老街与日场演艺核心区 —— 白天有市井、午后有抢渡、四季有剧场,先把「值得专程」立起来。", {})], {"ls": 1.3})],
    size=14, color=INK)
prins = [
    ("① 内容先行", "演艺与NPC剧目先于建筑定稿;建筑为内容服务,不做无内容的仿古空壳"),
    ("② 免票聚客", "街区开放进入;收入靠演艺票+餐饮+文创+研学,开业即执行三层收入结构"),
    ("③ 最小可行", "一期只建支撑「半日体验」的必要体量,拒绝一次铺满;预留二期用地"),
    ("④ 四季可用", "小剧场全室内;冬季「1950年的冬天」主题接续,不做纯季节性资产"),
    ("⑤ 庄重底线", "战斗与牺牲只在演艺/研学呈现;商业业态限定于支前市井层面"),
    ("⑥ 组团联动", "与虎山长城、零公里、国门湾营地共享停车/接驳/客流,不自建孤岛"),
]
x, y0 = Inches(0.62), Inches(3.2)
for i, (t, d) in enumerate(prins):
    cx = x + (i % 3) * Inches(4.13)
    cy = y0 + (i // 3) * Inches(1.62)
    card(s, cx, cy, Inches(3.95), Inches(1.45))
    txt(s, cx + Inches(0.18), cy + Inches(0.12), Inches(3.6), Inches(0.38), t, size=12.5, color=VERMI, bold=True)
    txt(s, cx + Inches(0.18), cy + Inches(0.52), Inches(3.6), Inches(0.85), d, size=10, color=INK, ls=1.2)
view_bar(s, Inches(0.62), Inches(6.55), Inches(12.1),
         "一期的成功标准不是「建了多少」,而是:开业首年客流70万+、复游与口碑数据达标——达标才解锁二期夜演大剧场与酒店。", size=10.5)

# 分区方案
s = new_slide()
header(s, "壹 · 概念方案", "一期「一轴四区」分区方案(约200亩)", "沿叆河水岸展开;酒店与夜演大剧场为二期预留")
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), Inches(1.95), Inches(7.9), Inches(4.35), RGBColor(0xF4, 0xEE, 0xE0), CARDLINE, 1)
# 叆河
from pptx.util import Inches as I
def fl(slide, pts, color, width=2.0, dash=None):
    x0, y0 = pts[0]
    fb = slide.shapes.build_freeform(Emu(int(Inches(x0))), Emu(int(Inches(y0))), scale=1.0)
    fb.add_line_segments([(Emu(int(Inches(px))), Emu(int(Inches(py)))) for px, py in pts[1:]], close=False)
    o = fb.convert_to_shape()
    o.fill.background()
    o.line.color.rgb = color; o.line.width = Pt(width)
    if dash:
        ln = o.line._get_or_add_ln()
        ln.append(ln.makeelement(qn('a:prstDash'), {'val': dash}))
    o.shadow.inherit = False
    return o
fl(s, [(0.9, 5.75), (2.6, 5.35), (4.6, 5.2), (6.6, 4.9), (8.45, 4.7)], RIVER, 4.5)
txt(s, Inches(6.9), Inches(5.0), Inches(1.7), Inches(0.3), "叆河水岸(演艺水域)", size=9.5, color=RIVER, bold=True)
zones = [
    (0.95, 2.25, 1.7, 1.2, "A 入口广场区\n约15亩", "入伍登记·游客中心\n仪式广场", VERMI),
    (2.85, 2.15, 2.3, 1.55, "B 支前老街区\n约45亩", "商街12,000㎡\nNPC市井+美食+文创", GOLD),
    (5.35, 2.25, 1.9, 1.35, "C 小剧场群区\n约25亩", "室内小剧场×4\n(一期先开2个)", PINE),
    (2.7, 4.05, 1.9, 0.95, "D 研学营地区\n约30亩", "", PINE),
    (5.0, 3.9, 2.3, 0.95, "E 抢渡实景区 约40亩\n看台1,500座+水域舞台", "", RIVER),
]
for zx, zy, zw, zh, zt, zd, zc in zones:
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(zx), Inches(zy), Inches(zw), Inches(zh), CARD, zc, 1.5)
    txt(s, Inches(zx + 0.08), Inches(zy + 0.06), Inches(zw - 0.16), Inches(zh - 0.1),
        [(zt, {"bold": True, "color": zc, "sa": 2}), (zd, {"size": 8.5, "color": INK})] if zd else
        [(zt, {"bold": True, "color": zc})],
        size=9.5, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ls=1.1)
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(5.95), Inches(3.4), Inches(0.42), CARD, SOFT, 1.25, dash="dash")
txt(s, Inches(0.95), Inches(5.95), Inches(3.4), Inches(0.42), "二期预留:夜演大剧场+主题酒店+温泉(约45亩)",
    size=8.5, color=SOFT, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(6.6), Inches(2.05), Inches(1.9), Inches(0.35),
    [([("→ 虎山长城·零公里 3km", {"bold": True, "color": PINE})], {})], size=9)
bullets(s, Inches(8.85), Inches(2.0), Inches(3.9), Inches(4.4), [
    ("动静分离:", "演艺/研学沿水岸(动区),二期酒店在背水侧(静区)。"),
    ("动线闭环:", "入口→老街(逛吃)→小剧场(看)→水岸(抢渡日场)→返程老街(带走文创),半日闭环约4小时。"),
    ("容量:", "瞬时承载约8,000人,日最大约2.5万人次;停车位一期800个+房车位联动国门湾。"),
    ("市政:", "接驳专线站点设于入口广场;水电气讯与防洪按二期总规模一次敷设,避免二次开挖。"),
], size=11, gap=8)

# 业态清单
s = new_slide()
header(s, "壹 · 概念方案", "一期业态与建筑面积清单", "总建筑面积约19,000㎡;改造与轻建造优先")
rows = [
    ["分区", "建设内容", "规模", "功能/业态"],
    ["A 入口广场", "游客中心+仪式广场", "3,000㎡建筑+广场", "入伍登记NPC、寄存、护照发放、集散"],
    ["B 支前老街", "商街建筑(两层为主)", "12,000㎡", "美食档口40+、文创店8、老字号6、NPC剧目点位10"],
    ["C 小剧场群", "室内小剧场×2(一期)", "2×750㎡·各约250座", "《坑道》《战地医院》轮演;预留2个剧场基础"],
    ["E 抢渡实景区", "看台+水域舞台+设备库", "看台1,500座", "日场《抢渡鸭绿江》;旺季日2–4场"],
    ["D 研学营地", "营房+多功能教室", "1,200㎡+场地", "半日/一日课程;淡季承接团建"],
    ["配套", "停车/市政/景观", "车位800个", "接驳站、亮化、防洪与水岸整治"],
]
table(s, Inches(0.6), Inches(1.95), Inches(12.15), Inches(3.9), rows,
      widths=[1.0, 1.5, 1.2, 2.4], fs=10.5, hs=11)
view_bar(s, Inches(0.6), Inches(6.15), Inches(12.15),
         "对比参照:延安红街61公顷/1.5公里街区为成熟态;一期13公顷(200亩)约为其1/5,匹配丹东客流基数,避免「大而空」。")

# 建设时序
s = new_slide()
header(s, "壹 · 概念方案", "12个月建设与开业时序", "内容与工程双线并行;第13个月「五一」开业")
lanes = [
    ("工程线", GOLD, [("M1–M3", "土地整理·市政·防洪水岸"), ("M3–M8", "老街与游客中心主体"),
                      ("M6–M10", "小剧场×2·看台与水域舞台"), ("M9–M12", "装修·景观·亮化·联调")]),
    ("内容线", VERMI, [("M1–M4", "剧本创作·导演团队组建"), ("M4–M8", "选角培训·服装道具·音乐制作"),
                       ("M8–M11", "排练·设备进场·合成"), ("M11–M12", "带妆彩排·压力测试·试运营")]),
    ("运营线", PINE, [("M3–M6", "招商(美食/文创/老字号)"), ("M6–M9", "商户进场装修·研学课程开发"),
                      ("M9–M12", "预热营销·通票系统上线"), ("M13", "「五一」正式开业")]),
]
y = Inches(2.0)
for name, c, steps in lanes:
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.62), y, Inches(1.3), Inches(1.15), c)
    txt(s, Inches(0.62), y, Inches(1.3), Inches(1.15), name, size=13, color=CARD, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    x = Inches(2.1)
    for i, (tm, d) in enumerate(steps):
        w = Inches(2.55)
        card(s, x, y, w, Inches(1.15))
        txt(s, x + Inches(0.14), y + Inches(0.1), w - Inches(0.28), Inches(0.32), tm, size=10.5, color=c, bold=True)
        txt(s, x + Inches(0.14), y + Inches(0.44), w - Inches(0.28), Inches(0.65), d, size=9.5, color=INK, ls=1.12)
        if i < 3:
            shp(s, MSO_SHAPE.RIGHT_ARROW, x + w + Inches(0.015), y + Inches(0.42), Inches(0.14), Inches(0.28), GOLD)
        x += w + Inches(0.17)
    y += Inches(1.35)
view_bar(s, Inches(0.62), Inches(6.25), Inches(12.1),
         "关键路径是内容线:剧本与导演团队必须在M1启动——工程可以压缩,内容打磨不能;宁可延期开业,不可带着平庸的戏开业。")

# ============ 第贰章 投资估算 ============
divider("贰", "投资估算",
        ["一期总投资约3.1亿元(概念级估算,精度±30%)",
         "内容与演艺设备占约33%,「先内容后砖头」落在钱上",
         "二期约3.2亿元,以一期数据达标为决策门槛"], accent=GOLD)

s = new_slide()
header(s, "贰 · 投资估算", "一期投资估算表(概念级 ±30%)", "单位:万元;取费按辽宁地区2026年造价水平估", accent=GOLD)
rows = [
    ["科目", "内容", "估算(万元)", "占比"],
    ["1 场地与基础设施", "土地整理、市政管网、防洪水岸、停车与接驳", "4,000", "12.9%"],
    ["2 建筑工程", "支前老街12,000㎡、小剧场×2、游客中心、研学营地", "9,700", "31.3%"],
    ["3 演艺工程", "水岸看台与舞台土建、水效/烟火/声光电设备、小剧场舞美", "6,600", "21.3%"],
    ["4 内容制作", "日场演艺创排、小剧场剧目×4、NPC体系与服装道具", "3,500", "11.3%"],
    ["5 景观环境", "景观绿化、街区亮化、标识系统", "2,500", "8.1%"],
    ["6 其他费用", "设计咨询、开办培训、不可预见费(8%)、流动资金", "4,700", "15.2%"],
    ["合计", "", "31,000", "100%"],
]
table(s, Inches(0.6), Inches(1.95), Inches(7.6), Inches(4.3), rows,
      widths=[1.5, 3.0, 1.1, 0.8], fs=10.5, hs=11)
pie_chart(s, Inches(8.45), Inches(1.95), Inches(4.3), Inches(3.7),
          ["场地基础", "建筑工程", "演艺工程", "内容制作", "景观环境", "其他"],
          [12.9, 31.3, 21.3, 11.3, 8.1, 15.2],
          title="投资结构", colors=[SOFT, GOLD, VERMI, RGBColor(0x9E, 0x3B, 0x2B), PINE, CARDLINE])
view_bar(s, Inches(0.6), Inches(6.45), Inches(12.15),
         "演艺工程+内容制作合计约1.01亿(占33%)——这是与「仿古街区」项目最大的区别:钱花在内容上,内容才是复游理由。", size=10.5)

s = new_slide()
header(s, "贰 · 投资估算", "二三期预留与投资决策门槛", "一期数据说话,达标解锁,不达标止损", accent=GOLD)
rows = [
    ["期次", "建设内容", "估算投资", "启动条件(决策门槛)"],
    ["一期(本案)", "支前老街+小剧场×2+日场抢渡+研学营地", "约3.1亿元", "即刻启动"],
    ["二期", "夜演大剧场(1,200座)+主题酒店(150间)+温泉", "约3.2亿元", "一期开业首年:客流≥70万、演艺转化≥30%、商户存活率≥80%"],
    ["三期(弹性)", "小剧场扩至4–6个、水岸夜游、营地扩容", "约1–1.5亿元", "二期开业后:过夜率≥25%、全年EBITDA≥5,000万"],
]
table(s, Inches(0.6), Inches(1.95), Inches(12.15), Inches(2.6), rows,
      widths=[1.1, 2.4, 1.0, 2.6], fs=10.5, hs=11)
bullets(s, Inches(0.62), Inches(4.85), Inches(12.1), Inches(1.6), [
    ("资金组织建议:", "政府平台公司资本金约40%(含土地作价)+ 政策性贷款/专项债约40%(文旅基础设施方向)+ 社会资本约20%(演艺运营方跟投、商户联营保证金)。"),
    ("风险控制:", "演艺设备与内容制作合同与票房对赌条款挂钩;商街采用「低保底+高抽成」租约,与商户共担爬坡期。"),
], size=11.5, gap=8)
view_bar(s, Inches(0.62), Inches(6.55), Inches(12.1),
         "总盘子约6.3–6.8亿分三期滚动,任何一期数据不达标即暂停加码——把「重资产沉没」风险锁在单期3亿的可承受范围内。", size=10.5)

# ============ 第叁章 测算模型 ============
divider("叁", "客流与收入测算模型",
        ["三情景:保守60万 / 基准100万 / 乐观150万人次",
         "基准年收入约7,700万、EBITDA约2,145万、盈亏平衡约67万人次",
         "附Excel联动模型:改黄色参数即自动重算"], accent=PINE)

s = new_slide()
header(s, "叁 · 测算模型", "测算逻辑与关键假设", "口径:稳定运营年(开业第3年);首年按基准×70%爬坡理解", accent=PINE)
rows = [
    ["假设项", "取值", "依据"],
    ["年客流(保守/基准/乐观)", "60 / 100 / 150万人次", "基准=城市旗舰锚定率约15%;≈遵义1935单月120万的1/14强度"],
    ["日场演艺转化率×票价", "35% × 80元", "免票入街聚客后的观演转化;票价取同类实景演艺区间下沿"],
    ["小剧场转化率×均价", "25% × 40元", "多剧场轮演+通票含1场的加购逻辑"],
    ["餐饮商业人均贡献", "18元(租金+抽成口径)", "约合商户流水20%抽成,商户人均流水约90元"],
    ["文创/研学/其他", "8元 + 研学6%×150元 + 4元", "研学对接学校/机关,淡季填舱"],
    ["成本", "固定4,400万 + 变动15%", "演职员约120人+运营80人、能耗物业、营销"],
]
table(s, Inches(0.6), Inches(1.95), Inches(12.15), Inches(3.9), rows,
      widths=[1.6, 1.5, 3.1], fs=10.5, hs=11)
view_bar(s, Inches(0.6), Inches(6.15), Inches(12.15),
         "全部参数开放在Excel「01_假设」表黄色单元格,即改即算——本页数字是模型默认值,不是结论;决策请以敏感性区间看待。")

s = new_slide()
header(s, "叁 · 测算模型", "三情景测算结果", "单位:万元/年;一期业态口径(夜演与酒店在二期)", accent=PINE)
col_chart(s, Inches(0.55), Inches(1.95), Inches(6.2), Inches(4.15),
          ["保守(60万)", "基准(100万)", "乐观(150万)"],
          [("收入合计", (4620, 7700, 11550)), ("EBITDA", (-473, 2145, 5418))],
          title="收入与EBITDA(万元/年)", colors=[GOLD, PINE], fmt='#,##0', lsize=9.5)
rows = [
    ["指标", "保守", "基准", "乐观"],
    ["年客流(万人次)", "60", "100", "150"],
    ["收入合计(万元)", "4,620", "7,700", "11,550"],
    ["EBITDA(万元)", "-473", "2,145", "5,418"],
    ["EBITDA率", "—", "27.9%", "46.9%"],
    ["一期回收期(年)", "—", "14.5", "5.7"],
]
table(s, Inches(7.0), Inches(1.95), Inches(5.75), Inches(3.3), rows,
      widths=[1.5, 0.9, 0.9, 0.9], fs=10.5, hs=11)
txt(s, Inches(7.0), Inches(5.4), Inches(5.75), Inches(0.9),
    [([("盈亏平衡:", {"bold": True, "color": VERMI}),
       ("约67万人次/年(按基准人均77元口径)——即保守情景略低于平衡点,基准情景有约33万人次安全垫。", {})], {"ls": 1.25})],
    size=11, color=INK)
view_bar(s, Inches(0.55), Inches(6.4), Inches(12.2),
         "回收期14.5年是「纯一期票据口径」;叠加二期夜演+酒店(过夜消费)与土地增值后,整体回收预计缩短至8–10年——一期的使命是验证,不是回本。", size=10.5)

s = new_slide()
header(s, "叁 · 测算模型", "月度客流与敏感性", "冬季占比20%靠室内剧场与主题season支撑", accent=PINE)
col_chart(s, Inches(0.55), Inches(1.95), Inches(6.4), Inches(3.9),
          [f"{i}月" for i in range(1, 13)],
          [("月客流(万人次,基准)", (4, 6, 5, 7, 10, 10, 14, 14, 10, 10, 5, 5))],
          title="月度客流分布(基准100万)", colors=[PINE], fmt='0"万"', legend=False, lsize=8.5)
rows = [
    ["EBITDA(万元)", "人均60元", "人均77元", "人均95元"],
    ["客流60万", "-1,340", "-473", "445"],
    ["客流80万", "-320", "836", "2,060"],
    ["客流100万", "700", "2,145", "3,675"],
    ["客流120万", "1,720", "3,454", "5,290"],
    ["客流150万", "3,250", "5,418", "7,713"],
]
table(s, Inches(7.2), Inches(1.95), Inches(5.55), Inches(3.4), rows,
      widths=[1.3, 1.0, 1.0, 1.0], fs=10.5, hs=10.5)
txt(s, Inches(7.2), Inches(5.5), Inches(5.55), Inches(0.85),
    [([("敏感性读法:", {"bold": True, "color": VERMI}),
       ("客流跌破70万且人均低于77元即亏损——运营重心应放在「人均提升」(演艺转化与二消),其弹性大于客流拉新。", {})], {"ls": 1.22})],
    size=10.5, color=INK)
view_bar(s, Inches(0.55), Inches(6.45), Inches(12.2),
         "Excel模型五张表:00使用说明 / 01假设(黄色可改) / 02收入 / 03成本利润 / 04月度 / 05敏感性,全公式联动,可直接用于向上汇报与银行尽调底稿。", size=10.5)

# ============ 第肆章 演艺大纲 ============
divider("肆", "演艺内容大纲",
        ["总叙事「出征之城·1950」:一条大江、一座城、最可爱的人",
         "日场抢渡 · NPC任务线 · 小剧场群 · 夜演(二期)四层内容",
         "季度上新机制对抗审美疲劳"], accent=RIVER)

s = new_slide()
header(s, "肆 · 演艺大纲", "总叙事与四层内容体系", "叙事母题:江的这一边是家,那一边是战场", accent=RIVER)
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.62), Inches(1.85), Inches(12.1), Inches(1.0), RGBColor(0xF3, 0xEB, 0xDB), GOLD, 1.25)
txt(s, Inches(0.9), Inches(2.0), Inches(11.6), Inches(0.75),
    [([("总叙事「出征之城·1950」:", {"bold": True, "color": VERMI}),
       ("以安东城1950年10月为时空切片——市井的烟火、集结的青春、渡江的决绝、后方的守望;不渲染仇恨,只讲「平凡人如何成为最可爱的人」。", {})], {"ls": 1.3})],
    size=13.5, color=INK)
layers = [
    ("第一层 · 街区NPC(常态)", "免费,人人可遇", "支前市井10个点位剧目,游客领任务成为「剧中人」", GOLD),
    ("第二层 · 小剧场群(轮演)", "40元/场,通票含1场", "15–30分钟强情感小戏,室内四季可演", PINE),
    ("第三层 · 日场《抢渡鸭绿江》", "80元,一期旗舰", "水岸实景战争场面,每日2场旺季4场", VERMI),
    ("第四层 · 夜演《鸭绿江·1950》", "120元,二期旗舰", "1,200座大剧场史诗歌舞,留客过夜引擎", RIVER),
]
x = Inches(0.62)
for t, price, d, c in layers:
    w = Inches(3.0)
    card(s, x, Inches(3.15), w, Inches(2.5), c)
    txt(s, x + Inches(0.18), Inches(3.38), w - Inches(0.36), Inches(0.7), t, size=12.5, color=c, bold=True, ls=1.1)
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.18), Inches(4.1), w - Inches(0.36), Inches(0.42), RGBColor(0xF6, 0xF0, 0xE4))
    txt(s, x + Inches(0.28), Inches(4.1), w - Inches(0.56), Inches(0.42), price, size=9.5, color=INK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + Inches(0.18), Inches(4.66), w - Inches(0.36), Inches(0.9), d, size=9.5, color=INK, ls=1.2)
    x += w + Inches(0.11)
view_bar(s, Inches(0.62), Inches(5.95), Inches(12.1),
         "四层内容对应四个消费深度:白逛(免费)→ 浅看(40元)→ 必看(80元)→ 过夜(120元+住宿)——层层向上转化,免票不等于免费。")

s = new_slide()
header(s, "肆 · 演艺大纲", "日场旗舰《抢渡鸭绿江》分幕大纲", "水岸实景 · 约30分钟 · 看台1,500座 · 每日2场(旺季4场)", accent=RIVER)
acts = [
    ("序幕《江城十月》", "3分钟", "1950年10月的安东:江风、汽笛、市井声;广播骤响,气氛陡转", "全场灯光渐暗,江面雾效"),
    ("第一幕《集结》", "7分钟", "码头集结:新兵告别、老兵沉默、母亲塞进怀里的一把炒面", "演员从观众席穿行入场,近距离告别戏"),
    ("第二幕《炮火封江》", "8分钟", "敌机轰炸浮桥,工兵冒火抢修;水爆、烟火、机械桥体断裂复位", "全剧技术高潮:水效+烟火+特技坠水"),
    ("第三幕《抢渡》", "9分钟", "夜色强渡:百人方阵踏桥过江,攻打对岸据点;火光映江", "观众席震动音效;据点爆破占位对岸"),
    ("尾声《回望》", "3分钟", "硝烟散去,江面恢复平静;画外音:「他们中的很多人,再也没有回来」", "全场肃立段落,禁止鼓掌提示——庄重收束"),
]
rows = [["幕次", "时长", "内容", "舞台手段"]] + [[a, b, c, d] for a, b, c, d in acts]
table(s, Inches(0.6), Inches(1.95), Inches(12.15), Inches(3.9), rows,
      widths=[1.3, 0.6, 2.6, 1.9], fs=10, hs=11)
view_bar(s, Inches(0.6), Inches(6.15), Inches(12.15),
         "创排要求:军事顾问+党史专家全程把关;尾声「静默段落」是全剧的精神落点,宁可牺牲「爽感」也要保住庄重。")

s = new_slide()
header(s, "肆 · 演艺大纲", "街区NPC任务线与小剧场群剧目", "常态内容:让「逛街」变成「入戏」", accent=RIVER)
txt(s, Inches(0.62), Inches(1.85), Inches(5.9), Inches(0.4), "NPC任务线「支前模范」(免费)", size=14, color=VERMI, bold=True)
npc = [
    ("① 入伍登记处", "领「支前通行证」,选择身份:民工/护士/文工团员"),
    ("② 炒面坊", "参与炒面打包任务,盖第一枚章"),
    ("③ 军邮所", "代写一封家书(可寄出/可带走),盖第二枚章"),
    ("④ 担架队集合点", "双人担架运送任务,盖第三枚章"),
    ("⑤ 车站送别", "参与整点「送别」群戏,授「支前模范」纪念章"),
]
y = Inches(2.35)
for t, d in npc:
    shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.62), y, Inches(5.9), Inches(0.68), CARD, CARDLINE, 1)
    txt(s, Inches(0.82), y + Inches(0.06), Inches(1.7), Inches(0.55), t, size=10.5, color=GOLD, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(2.6), y + Inches(0.06), Inches(3.8), Inches(0.55), d, size=9.5, color=INK, anchor=MSO_ANCHOR.MIDDLE, ls=1.1)
    y += Inches(0.78)
txt(s, Inches(6.85), Inches(1.85), Inches(5.9), Inches(0.4), "小剧场群剧目表(一期开2个厅,轮演4剧目)", size=14, color=PINE, bold=True)
rows = [
    ["剧目", "类型/时长", "一句话内容"],
    ["《坑道》", "沉浸声光·20分钟", "上甘岭坑道七天七夜,黑暗中的呼吸与歌声"],
    ["《战地医院》", "互动剧·25分钟", "观众成为担架员与护士,亲历一场抢救"],
    ["《一封家书》", "独角戏·15分钟", "军邮员读信,一封没有寄出的家书"],
    ["《凯旋1953》", "合家欢·20分钟", "停战日的安东车站,重逢与等待"],
    ["《1950年的冬天》", "季节限定(冬)", "长津湖主题:严寒、坚守与「冰雕连」的注目礼"],
]
table(s, Inches(6.85), Inches(2.35), Inches(5.9), Inches(3.6), rows,
      widths=[1.2, 1.1, 2.4], fs=9.5, hs=10.5)
view_bar(s, Inches(0.62), Inches(6.35), Inches(12.1),
         "NPC任务线的终点设计成「送别群戏」——它同时是游客的情感高潮与日场《抢渡》的天然导流口(送别的队伍正是即将渡江的人)。", size=10.5)

s = new_slide()
header(s, "肆 · 演艺大纲", "夜演《鸭绿江·1950》分幕大纲(二期旗舰)", "1,200座大剧场 · 约60分钟 · 史诗歌舞 · 过夜引擎", accent=RIVER)
acts2 = [
    ("序《江水安澜》", "江畔渔歌与婚礼,1950年秋安东的寻常幸福", "水袖群舞·江面纱幕投影"),
    ("一幕《烽火骤起》", "战火烧到江边,安东夜空的第一声警报", "机械升降+全息空袭场面"),
    ("二幕《雄赳赳》", "誓师与渡江:军歌大合唱推向第一高潮", "军歌交响改编·百人方阵"),
    ("三幕《战地之春》", "双线并行:前线坑道的歌声/后方支前的灯火", "双层舞台上下切换"),
    ("四幕《最可爱的人》", "牺牲与铭记:雪落长津湖,英名墙亮起", "全场星光·英名墙装置"),
    ("尾声《山河无恙》", "回到今天:断桥、银杏、江上晨光;和平即答案", "儿童合唱·观众烛光互动"),
]
x, y0 = Inches(0.62), Inches(1.95)
for i, (t, d, tech) in enumerate(acts2):
    cx = x + (i % 3) * Inches(4.13)
    cy = y0 + (i // 3) * Inches(1.95)
    card(s, cx, cy, Inches(3.95), Inches(1.78), RIVER if i % 2 else VERMI)
    txt(s, cx + Inches(0.18), cy + Inches(0.12), Inches(3.6), Inches(0.38), t, size=12.5,
        color=VERMI if i % 2 == 0 else RIVER, bold=True)
    txt(s, cx + Inches(0.18), cy + Inches(0.52), Inches(3.6), Inches(0.7), d, size=10, color=INK, ls=1.18)
    txt(s, cx + Inches(0.18), cy + Inches(1.28), Inches(3.6), Inches(0.4), tech, size=9, color=SOFT)
view_bar(s, Inches(0.62), Inches(6.05), Inches(12.1),
         "定位对标《长恨歌》《只有河南》的情感浓度而非体量;每年迭代一幕、重要纪念年推特别版,并常设「老兵专场」公益场次。")

s = new_slide()
header(s, "肆 · 演艺大纲", "内容更新与运营机制", "对抗审美疲劳:让常客永远有「没看过的丹东」", accent=RIVER)
mechs = [
    ("季度上新", "NPC剧目每季度轮换2个点位;小剧场每年新增1部剧目(三期扩至6厅)", GOLD),
    ("节令内容", "清明「英名墙祭扫」、7·27停战纪念、10·25出征纪念、冬季长津湖季", VERMI),
    ("共创机制", "面向高校戏剧社/退役军人艺术团征集短剧,优胜者进驻小剧场公益场", PINE),
    ("内容审查", "常设内容委员会(党史/军史顾问+文旅部门),剧本、讲解词、商业物料三审", RIVER),
]
x, y0 = Inches(0.62), Inches(1.95)
for i, (t, d, c) in enumerate(mechs):
    cx = x + (i % 2) * Inches(6.2)
    cy = y0 + (i // 2) * Inches(1.55)
    card(s, cx, cy, Inches(5.95), Inches(1.4), c)
    txt(s, cx + Inches(0.22), cy + Inches(0.12), Inches(5.5), Inches(0.38), t, size=13, color=c, bold=True)
    txt(s, cx + Inches(0.22), cy + Inches(0.52), Inches(5.5), Inches(0.8), d, size=10.5, color=INK, ls=1.22)
shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.62), Inches(5.3), Inches(12.1), Inches(1.35), RGBColor(0xF3, 0xEB, 0xDB), GOLD, 1.25)
txt(s, Inches(0.92), Inches(5.47), Inches(11.6), Inches(1.05),
    [([("三合一交付已完成,建议下一步:", {"bold": True, "color": VERMI})], {"sa": 4}),
     ("① 委托专业机构开展选址地块勘察与合规预审(用地/防洪/军事设施距离) ② 演艺导演团队遴选(邀标2–3家) ③ 用Excel模型做资金方案压力测试后启动立项", {})],
    size=12, color=INK, ls=1.3)

# 封底
s = new_slide(RGBColor(0xF3, 0xEB, 0xDB))
PAGE[0] += 1
shp(s, MSO_SHAPE.OVAL, Inches(9.6), Inches(-2.0), Inches(6.5), Inches(6.5), None, GOLD, 1.5)
shp(s, MSO_SHAPE.OVAL, Inches(-1.8), Inches(5.0), Inches(4.2), Inches(4.2), None, RIVER, 1.25)
txt(s, Inches(0.95), Inches(2.5), Inches(11.4), Inches(1.0),
    "先把戏排好,再把街开张", size=32, color=INK, bold=True)
txt(s, Inches(0.98), Inches(3.6), Inches(11.2), Inches(1.2),
    [("一期3.1亿、200亩、12个月——规模不大,但每一分钱都花在「让人专程而来」的理由上。", {"sa": 5}),
     ("数据达标,再谈二期;这是对丹东最负责任的建设方式。", {})],
    size=15, color=SOFT, ls=1.4)
txt(s, Inches(0.98), Inches(5.4), Inches(11), Inches(0.5),
    "鸭绿江畔 · 丹东真好", size=13, color=GOLD, bold=True)

OUT = "鸭绿江1950一期方案与测算.pptx"
prs.save(OUT)
print(f"saved: {OUT}, pages: {len(prs.slides._sldIdLst)}")
