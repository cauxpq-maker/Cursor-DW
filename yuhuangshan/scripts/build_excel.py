# -*- coding: utf-8 -*-
"""生成《玉皇山公园经营收入与成本测算模型（重构20260913）》."""

from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.series import SeriesLabel
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, NamedStyle, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.chart.series import SeriesLabel
from openpyxl.workbook.defined_name import DefinedName

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_engine import (  # noqa: E402
    PROJECTS,
    STAFF_ROWS,
    VISITOR_MAP,
    VISITOR_TABLE6,
    build_investment,
    run_model,
)

OUT = Path(__file__).resolve().parents[1] / "玉皇山公园经营收入与成本测算模型_重构20260913.xlsx"

# colors
GREEN_DK = "1B4332"
GREEN = "2D6A4F"
GOLD = "C9A227"
YELLOW = "FFF3BF"
GREEN_LT = "D8F3DC"
BLUE_LT = "D0E8F2"
ORANGE = "FCE4D6"
PURPLE = "EDE0F4"
GRAY = "F1F3F5"
RED_LT = "F8D7DA"
WHITE = "FFFFFF"
TEAL = "40916C"

thin = Border(
    left=Side(style="thin", color="C0C0C0"),
    right=Side(style="thin", color="C0C0C0"),
    top=Side(style="thin", color="C0C0C0"),
    bottom=Side(style="thin", color="C0C0C0"),
)
thick_bottom = Border(bottom=Side(style="medium", color=GREEN_DK))


def font(name="Microsoft YaHei", size=10, bold=False, color="1A1A1A"):
    return Font(name=name, size=size, bold=bold, color=color)


def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)


def align(h="left", v="center", wrap=True):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)


def apply_range(ws, cells, **kwargs):
    for c in cells:
        for k, v in kwargs.items():
            setattr(c, k, v)


def title_bar(ws, text, end_col, height=28):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=end_col)
    c = ws.cell(1, 1, text)
    c.font = font(size=16, bold=True, color=WHITE)
    c.fill = fill(GREEN_DK)
    c.alignment = align("left", "center")
    ws.row_dimensions[1].height = height
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=end_col)
    c2 = ws.cell(2, 1, "通化玉皇山公园｜以评估公司概算表5改造投资、表6人流模型为基准｜建设期2年｜经营期第3–18年")
    c2.font = font(size=9, color=WHITE)
    c2.fill = fill(GREEN)
    c2.alignment = align("left", "center")
    ws.row_dimensions[2].height = 18


def header_row(ws, row, labels, fill_hex=GREEN):
    for i, lab in enumerate(labels, 1):
        c = ws.cell(row, i, lab)
        c.font = font(size=9, bold=True, color=WHITE)
        c.fill = fill(fill_hex)
        c.alignment = align("center", "center")
        c.border = thin


def num(ws, r, c, value, fmt="0.00", input_cell=False, result=False, check=False):
    cell = ws.cell(r, c, value)
    cell.number_format = fmt
    cell.font = font(size=9, color="1B4F72" if input_cell else "1A1A1A")
    cell.alignment = align("right", "center", False)
    cell.border = thin
    if input_cell:
        cell.fill = fill(YELLOW)
    elif result:
        cell.fill = fill(GREEN_LT)
    elif check:
        cell.fill = fill(BLUE_LT)
    return cell


def txt(ws, r, c, value, bold=False, bg=None, center=False):
    cell = ws.cell(r, c, value)
    cell.font = font(size=9, bold=bold)
    cell.alignment = align("center" if center else "left", "center")
    cell.border = thin
    if bg:
        cell.fill = fill(bg)
    return cell


def set_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def nature_fill(nature):
    return {"联营": ORANGE, "自营": PURPLE, "出租": BLUE_LT, "品牌加盟": "F9E79F"}.get(nature, GRAY)


def build():
    m = run_model()
    inv = m["inv"]
    staff = m["staff"]
    wb = Workbook()

    # =====================================================================
    # 封面说明
    # =====================================================================
    ws = wb.active
    ws.title = "封面说明"
    title_bar(ws, "通化玉皇山公园经营收入与成本测算模型（重构）", 8)
    ws.cell(3, 1, "版本").font = font(bold=True)
    ws.cell(3, 2, "2026-09-13 重构稿｜基准：评估公司概算20260913")
    ws.merge_cells("B3:H3")

    notes = [
        ("重构原则", "以表5改造投资为项目投资基准，以表6人流/转化/客单为客流与收入校验基准；不新增改造或运营硬件项目。"),
        ("业态口径", "严格按表6经营性质拆分联营、自营、出租、品牌加盟。联营收入为公园分成（或保底租金），不再把合作方人工、货品、演出成本计入公园。"),
        ("人力修正", "原模型把联营项目按自营计提高额固定成本，且宝贝王按含糊口径计216.72万元。本模型按表6人员配备+公园公共编制重建通化全包年薪，人力只计一次。"),
        ("建设与经营", "建设期第1–2年（只还息、形成资产）；第3年按表6「3年」达产（75万人、转化85%、客单150元）；第4–18年按表6「4~18年保底」（80万人）。"),
        ("填充说明", "仅激活表5已列但原收入表未计价的设施：室内高尔夫、星空露营、花海、停车场、零食亭、研学展馆、抗联戏雪、健身区、栈道观景；并补表6已列但收入为空的旅拍。"),
        ("约束目标", "经营期静态投资回收期≤3年；第3–18年年均利润总额≥3,000万元。所得税按25%列示，净利润单独披露。"),
        ("使用方法", "黄色单元格为可调参数；绿色为关键结果；蓝色为交叉校验。先改「业态参数」「人力编制」「06人流模型」，再看「经营总览」。"),
        ("限制声明", "本表为经营预算与可研测算，不构成收益保证。联营合同、万达条款、贷款条件落地后应回填。北入口停车场按表5说明暂不计入。"),
    ]
    header_row(ws, 5, ["主题", "说明", "", "", "", "", "", ""], GREEN)
    ws.merge_cells("B5:H5")
    for i, (k, v) in enumerate(notes, 6):
        txt(ws, i, 1, k, bold=True, bg=GREEN_LT)
        ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=8)
        txt(ws, i, 2, v)
        ws.row_dimensions[i].height = 36

    ws.cell(15, 1, "目标体检（与18年财务联动）").font = font(bold=True, color=WHITE)
    ws.cell(15, 1).fill = fill(GREEN_DK)
    ws.merge_cells("A15:H15")
    header_row(ws, 16, ["指标", "目标", "模型结果", "状态", "口径", "", "", ""], TEAL)
    txt(ws, 17, 1, "建设期", True)
    txt(ws, 17, 2, "2年")
    txt(ws, 17, 3, "第1–2年无人流")
    txt(ws, 17, 4, "达标", True, GREEN_LT)
    txt(ws, 17, 5, "只形成资产与建设期利息")
    txt(ws, 18, 1, "总投资（表5）", True)
    txt(ws, 18, 2, "按表5公式")
    ws.cell(18, 3, "=总投资")
    ws.cell(18, 3).number_format = "0.00"
    ws.cell(18, 3).fill = fill(GREEN_LT)
    ws.cell(18, 3).border = thin
    txt(ws, 18, 4, "基准", True, BLUE_LT)
    txt(ws, 18, 5, "工程+二类+预备+建设期利息+管理费")
    txt(ws, 19, 1, "第3–18年年均利润总额", True)
    txt(ws, 19, 2, "≥3,000万元")
    ws.cell(19, 3, "='18年财务'!C31")
    ws.cell(19, 3).number_format = "0.00"
    ws.cell(19, 3).fill = fill(GREEN_LT)
    ws.cell(19, 3).border = thin
    ws.cell(19, 4, "='18年财务'!E31")
    ws.cell(19, 4).fill = fill(GREEN_LT)
    ws.cell(19, 4).border = thin
    txt(ws, 19, 5, "利润总额=经营贡献−折旧−经营期利息")
    txt(ws, 20, 1, "第3–18年最低利润总额", True)
    txt(ws, 20, 2, "建议≥3,000万元")
    ws.cell(20, 3, "='18年财务'!C32")
    ws.cell(20, 3).number_format = "0.00"
    ws.cell(20, 3).fill = fill(GREEN_LT)
    ws.cell(20, 3).border = thin
    ws.cell(20, 4, "='18年财务'!E32")
    ws.cell(20, 4).fill = fill(GREEN_LT)
    ws.cell(20, 4).border = thin
    txt(ws, 20, 5, "开业达产年")
    txt(ws, 21, 1, "经营期静态回收期", True)
    txt(ws, 21, 2, "≤3年")
    ws.cell(21, 3, "='18年财务'!C34")
    ws.cell(21, 3).number_format = "0.00"
    ws.cell(21, 3).fill = fill(GREEN_LT)
    ws.cell(21, 3).border = thin
    ws.cell(21, 4, "='18年财务'!E34")
    ws.cell(21, 4).fill = fill(GREEN_LT)
    ws.cell(21, 4).border = thin
    txt(ws, 21, 5, "累计（净利润+折旧）覆盖总投资")
    txt(ws, 22, 1, "第3–18年年均净利润", True)
    txt(ws, 22, 2, "披露（所得税25%）")
    ws.cell(22, 3, "='18年财务'!C33")
    ws.cell(22, 3).number_format = "0.00"
    ws.cell(22, 3).fill = fill(BLUE_LT)
    ws.cell(22, 3).border = thin
    txt(ws, 22, 4, "—", center=True)
    txt(ws, 22, 5, "目标考核口径为利润总额")
    for i in range(17, 23):
        ws.merge_cells(start_row=i, start_column=5, end_row=i, end_column=8)

    ws.cell(24, 1, "黄色=输入　绿色=结果　蓝色=校验　橙色=联营　紫色=自营").font = font(size=8, color="666666")
    set_widths(ws, [22, 22, 22, 14, 28, 14, 14, 14])
    ws.freeze_panes = "A3"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "1:2"

    # =====================================================================
    # 05投资估算
    # =====================================================================
    ws = wb.create_sheet("05投资估算")
    title_bar(ws, "表5 玉皇山公园改造项目初步设计规划投资估算（重构基准）", 8)
    header_row(ws, 4, ["序号", "工程内容", "工程量", "单位", "单价（元）", "造价（万元）", "备注", "板块"], GREEN)
    # write lines starting row 5, with section headers inserted
    # We'll write all detail lines then section sums via formula

    # Map group order
    group_order = [
        ("1.1", "基础设施建设/设备", "基础设施"),
        ("1.2", "超级儿童乐园及配套设施", "超级儿童乐园"),
        ("1.3", "青年街区", "青年街区"),
        ("1.4", "动物观赏区改造提升", "动物观赏区"),
        ("1.5", "网球场/水塘改造提升", "网球场/水塘"),
        ("1.6", "庙会/市集区改造提升", "庙会/市集"),
        ("1.7", "既有房屋改造", "既有房屋"),
        ("1.8", "红色记忆宣传区", "红色记忆"),
        ("1.9", "花海/露营区/低碳林改造", "花海/露营/低碳林"),
    ]
    # rows: 5 = 一 工程费用
    r = 5
    txt(ws, r, 1, "一", True, GREEN_LT, True)
    txt(ws, r, 2, "工程费用", True, GREEN_LT)
    for c in range(3, 8):
        txt(ws, r, c, "", bg=GREEN_LT)
    ws.cell(r, 6).value = "=F6+F18+F22+F26+F32+F36+F40+F44+F48"
    ws.cell(r, 6).number_format = "0.00"
    ws.cell(r, 6).fill = fill(GREEN_LT)
    ws.cell(r, 6).font = font(bold=True)
    engineering_row = r

    # write details in original order with subheaders
    # We need exact row numbers matching the SUM ranges used above.
    # 1.1 header row 6, details 7-17, 1.2 row 18 details 19-21, etc.

    def write_sub(ws, row, code, name, start, end):
        txt(ws, row, 1, code, True, BLUE_LT, True)
        txt(ws, row, 2, name, True, BLUE_LT)
        for c in range(3, 8):
            txt(ws, row, c, "", bg=BLUE_LT)
        ws.cell(row, 6).value = f"=SUM(F{start}:F{end})"
        ws.cell(row, 6).number_format = "0.00"
        ws.cell(row, 6).fill = fill(BLUE_LT)
        ws.cell(row, 6).font = font(bold=True)

    # group lines from inv
    from collections import OrderedDict

    grouped = OrderedDict()
    for line in inv["lines"]:
        grouped.setdefault(line["group"], []).append(line)

    # Manual row plan matching formulas
    # r6 1.1, r7-17 details (11 items)
    write_sub(ws, 6, "1.1", "基础设施建设/设备", 7, 17)
    r = 7
    for line in grouped["基础设施"]:
        txt(ws, r, 1, line["code"], center=True)
        txt(ws, r, 2, line["name"])
        num(ws, r, 3, line["qty"], "0.00", input_cell=True)
        txt(ws, r, 4, line["unit"], center=True)
        if line["code"] in ("1.4.1",):
            pass
        num(ws, r, 5, line["price"] if line["price"] is not None else 0, "#,##0", input_cell=True)
        if line["code"] == "1.2.3":
            pass
        # amount formula
        if line["code"] in {"1.2.3", "1.4.1", "1.4.2", "1.4.3", "1.4.4", "1.4.5"}:
            num(ws, r, 6, line["amount"], "0.00", input_cell=True)
        else:
            ws.cell(r, 6, f"=C{r}*E{r}/10000")
            ws.cell(r, 6).number_format = "0.00"
            ws.cell(r, 6).border = thin
            ws.cell(r, 6).font = font(size=9)
            ws.cell(r, 6).alignment = align("right", "center", False)
        txt(ws, r, 7, line["note"])
        txt(ws, r, 8, line["group"])
        r += 1

    write_sub(ws, 18, "1.2", "超级儿童乐园及配套设施", 19, 21)
    r = 19
    for line in grouped["超级儿童乐园"]:
        txt(ws, r, 1, line["code"], center=True)
        txt(ws, r, 2, line["name"])
        num(ws, r, 3, line["qty"], "0.00", input_cell=True)
        txt(ws, r, 4, line["unit"], center=True)
        num(ws, r, 5, line["price"] if line["price"] else 0, "#,##0", input_cell=True)
        if line["code"] == "1.2.3":
            num(ws, r, 6, 160, "0.00", input_cell=True)
        else:
            ws.cell(r, 6, f"=C{r}*E{r}/10000")
            ws.cell(r, 6).number_format = "0.00"
            ws.cell(r, 6).border = thin
        txt(ws, r, 7, line["note"] or ("配套按概算160万元" if line["code"] == "1.2.3" else ""))
        txt(ws, r, 8, line["group"])
        r += 1

    write_sub(ws, 22, "1.3", "青年街区", 23, 25)
    r = 23
    for line in grouped["青年街区"]:
        txt(ws, r, 1, line["code"], center=True)
        txt(ws, r, 2, line["name"])
        num(ws, r, 3, line["qty"], "0.00", input_cell=True)
        txt(ws, r, 4, line["unit"], center=True)
        num(ws, r, 5, line["price"] or 0, "#,##0", input_cell=True)
        ws.cell(r, 6, f"=C{r}*E{r}/10000")
        ws.cell(r, 6).number_format = "0.00"
        ws.cell(r, 6).border = thin
        txt(ws, r, 7, line["note"])
        txt(ws, r, 8, line["group"])
        r += 1

    write_sub(ws, 26, "1.4", "动物观赏区改造提升", 27, 31)
    r = 27
    for line in grouped["动物观赏区"]:
        txt(ws, r, 1, line["code"], center=True)
        txt(ws, r, 2, line["name"])
        num(ws, r, 3, line["qty"], "0.00", input_cell=True)
        txt(ws, r, 4, line["unit"], center=True)
        num(ws, r, 5, line["price"] or 0, "#,##0", input_cell=True)
        num(ws, r, 6, line["amount"], "0.00", input_cell=True)
        txt(ws, r, 7, line["note"])
        txt(ws, r, 8, line["group"])
        r += 1

    write_sub(ws, 32, "1.5", "网球场/水塘改造提升", 33, 36)
    r = 33
    for line in grouped["网球场/水塘"]:
        txt(ws, r, 1, line["code"], center=True)
        txt(ws, r, 2, line["name"])
        num(ws, r, 3, line["qty"], "0.00", input_cell=True)
        txt(ws, r, 4, line["unit"], center=True)
        num(ws, r, 5, line["price"] or 0, "#,##0", input_cell=True)
        ws.cell(r, 6, f"=C{r}*E{r}/10000")
        ws.cell(r, 6).number_format = "0.00"
        ws.cell(r, 6).border = thin
        txt(ws, r, 7, line["note"])
        txt(ws, r, 8, line["group"])
        r += 1

    write_sub(ws, 36, "1.6", "庙会/市集区改造提升", 37, 39)
    r = 37
    for line in grouped["庙会/市集"]:
        txt(ws, r, 1, line["code"], center=True)
        txt(ws, r, 2, line["name"])
        num(ws, r, 3, line["qty"], "0.00", input_cell=True)
        txt(ws, r, 4, line["unit"], center=True)
        num(ws, r, 5, line["price"] or 0, "#,##0", input_cell=True)
        ws.cell(r, 6, f"=C{r}*E{r}/10000")
        ws.cell(r, 6).number_format = "0.00"
        ws.cell(r, 6).border = thin
        txt(ws, r, 7, line["note"])
        txt(ws, r, 8, line["group"])
        r += 1

    write_sub(ws, 40, "1.7", "既有房屋改造", 41, 43)
    r = 41
    for line in grouped["既有房屋"]:
        txt(ws, r, 1, line["code"], center=True)
        txt(ws, r, 2, line["name"])
        num(ws, r, 3, line["qty"], "0.00", input_cell=True)
        txt(ws, r, 4, line["unit"], center=True)
        num(ws, r, 5, line["price"] or 0, "#,##0", input_cell=True)
        ws.cell(r, 6, f"=C{r}*E{r}/10000")
        ws.cell(r, 6).number_format = "0.00"
        ws.cell(r, 6).border = thin
        txt(ws, r, 7, line["note"])
        txt(ws, r, 8, line["group"])
        r += 1

    write_sub(ws, 44, "1.8", "红色记忆宣传区", 45, 47)
    r = 45
    for line in grouped["红色记忆"]:
        txt(ws, r, 1, line["code"], center=True)
        txt(ws, r, 2, line["name"])
        num(ws, r, 3, line["qty"], "0.00", input_cell=True)
        txt(ws, r, 4, line["unit"], center=True)
        num(ws, r, 5, line["price"] or 0, "#,##0", input_cell=True)
        ws.cell(r, 6, f"=C{r}*E{r}/10000")
        ws.cell(r, 6).number_format = "0.00"
        ws.cell(r, 6).border = thin
        txt(ws, r, 7, line["note"])
        txt(ws, r, 8, line["group"])
        r += 1

    write_sub(ws, 48, "1.9", "花海/露营区/低碳林改造", 49, 58)
    r = 49
    for line in grouped["花海/露营/低碳林"]:
        txt(ws, r, 1, line["code"], center=True)
        txt(ws, r, 2, line["name"])
        num(ws, r, 3, line["qty"], "0.00", input_cell=True)
        txt(ws, r, 4, line["unit"], center=True)
        num(ws, r, 5, line["price"] or 0, "#,##0", input_cell=True)
        ws.cell(r, 6, f"=C{r}*E{r}/10000")
        ws.cell(r, 6).number_format = "0.00"
        ws.cell(r, 6).border = thin
        txt(ws, r, 7, line["note"])
        txt(ws, r, 8, line["group"])
        r += 1

    # 二类及以下 59-64 与原表对齐
    r = 59
    txt(ws, r, 1, "二", True, YELLOW, True)
    txt(ws, r, 2, "二类费用（一）×9.5%（咨询、勘察设计、监理、保险、场地准备、检测）", True, YELLOW)
    ws.merge_cells("B59:E59")
    ws.cell(r, 6, "=F5*0.095")
    ws.cell(r, 6).number_format = "0.00"
    ws.cell(r, 6).fill = fill(YELLOW)
    ws.cell(r, 6).border = thin
    txt(ws, r, 7, "费率可调见右侧")
    num(ws, r, 8, 0.095, "0.0%", input_cell=True)

    r = 60
    txt(ws, r, 1, "三", True, YELLOW, True)
    txt(ws, r, 2, "不可预见费（（一）+（二））×5%", True, YELLOW)
    ws.merge_cells("B60:E60")
    ws.cell(r, 6, "=(F5+F59)*0.05")
    ws.cell(r, 6).number_format = "0.00"
    ws.cell(r, 6).fill = fill(YELLOW)
    ws.cell(r, 6).border = thin
    num(ws, r, 8, 0.05, "0.0%", input_cell=True)

    r = 61
    txt(ws, r, 1, "四", True, GREEN_LT, True)
    txt(ws, r, 2, "建设投资", True, GREEN_LT)
    ws.merge_cells("B61:E61")
    ws.cell(r, 6, "=F5+F59+F60")
    ws.cell(r, 6).number_format = "0.00"
    ws.cell(r, 6).fill = fill(GREEN_LT)
    ws.cell(r, 6).font = font(bold=True)
    ws.cell(r, 6).border = thin

    r = 62
    txt(ws, r, 1, "五", True, YELLOW, True)
    txt(ws, r, 2, "建设期利息＝建设投资×贷款比例×利率×2年（建设期只还息）", True, YELLOW)
    ws.merge_cells("B62:E62")
    ws.cell(r, 6, "=F61*H62*H63*2")
    ws.cell(r, 6).number_format = "0.00"
    ws.cell(r, 6).fill = fill(YELLOW)
    ws.cell(r, 6).border = thin
    txt(ws, r, 7, "贷款比例")
    num(ws, r, 8, 0.80, "0.0%", input_cell=True)

    r = 63
    txt(ws, r, 1, "六", True, YELLOW, True)
    txt(ws, r, 2, "建设期管理费", True, YELLOW)
    num(ws, r, 3, 1, "0", input_cell=True)
    txt(ws, r, 4, "项", center=True)
    ws.cell(r, 6, 300)
    ws.cell(r, 6).number_format = "0.00"
    ws.cell(r, 6).fill = fill(YELLOW)
    ws.cell(r, 6).border = thin
    txt(ws, r, 7, "贷款利率")
    num(ws, r, 8, 0.048, "0.00%", input_cell=True)

    r = 64
    txt(ws, r, 1, "七", True, GREEN, True)
    txt(ws, r, 2, "总投资（回收期基准）", True, GREEN)
    ws.cell(r, 2).font = font(bold=True, color=WHITE)
    ws.cell(r, 1).font = font(bold=True, color=WHITE)
    ws.cell(r, 1).fill = fill(GREEN)
    ws.merge_cells("B64:E64")
    ws.cell(r, 6, "=SUM(F61:F63)")
    ws.cell(r, 6).number_format = "0.00"
    ws.cell(r, 6).fill = fill(GREEN)
    ws.cell(r, 6).font = font(bold=True, color=WHITE)
    ws.cell(r, 6).border = thin
    txt(ws, r, 7, "不含经营权拍卖价款", bg=GREEN_LT)

    r = 65
    txt(ws, r, 1, "八", True, BLUE_LT, True)
    txt(ws, r, 2, "建设期贷款本金（经营期还本基数）", True, BLUE_LT)
    ws.merge_cells("B65:E65")
    ws.cell(r, 6, "=F61*H62")
    ws.cell(r, 6).number_format = "0.00"
    ws.cell(r, 6).fill = fill(BLUE_LT)
    ws.cell(r, 6).border = thin

    notes = [
        "说明：所有建设项目均不占用林地，均以构筑物形态利用林间空地和树冠下方空间。",
        "配套用房均按临建，水电就近接入。北入口停车场及游客中心因土地与动迁未定，本次改造暂不统计。",
        "建设期暂定二年只偿还利息；总投资中建设投资的80%为贷款，利率暂按4.8%。经营权拍卖款不纳入本回收模型。",
        "分年投入：建设投资、建设期利息、管理费按第1–2年各50%支付。",
    ]
    for i, t in enumerate(notes):
        ws.merge_cells(start_row=67 + i, start_column=1, end_row=67 + i, end_column=8)
        txt(ws, 67 + i, 1, t, bg=GRAY)
        ws.row_dimensions[67 + i].height = 20

    set_widths(ws, [10, 42, 12, 10, 14, 14, 28, 16])
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = "A4:H58"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = "1:4"

    # named ranges
    wb.defined_names.add(DefinedName(name="总投资", attr_text="'05投资估算'!$F$64"))
    wb.defined_names.add(DefinedName(name="建设投资", attr_text="'05投资估算'!$F$61"))
    wb.defined_names.add(DefinedName(name="贷款本金", attr_text="'05投资估算'!$F$65"))
    wb.defined_names.add(DefinedName(name="贷款利率", attr_text="'05投资估算'!$H$63"))

    # =====================================================================
    # 06人流模型
    # =====================================================================
    ws = wb.create_sheet("06人流模型")
    title_bar(ws, "表6 人流转化目标模型（项目年对齐）", 20)
    ws.merge_cells("A3:T3")
    txt(
        ws,
        3,
        1,
        "建设期占用第1–2年（人流为0）；第3年对齐原表「3年」75万人/转化85%/客单150元；第4–18年对齐「4~18年保底」80万人。原表1–2年50万/60万仅作对照，不在建设期重复计入。",
        bg=BLUE_LT,
    )

    labels = ["指标"] + [f"第{y}年" for y in range(1, 19)] + ["说明"]
    header_row(ws, 5, labels[:21], GREEN)
    # actually 1 + 18 + 1 = 20 cols
    header_row(ws, 5, ["指标"] + [f"第{y}年" for y in range(1, 19)] + ["说明"], GREEN)

    # visitors row 6
    txt(ws, 6, 1, "入园人次（万人）", True)
    for y in range(1, 19):
        num(ws, 6, y + 1, VISITOR_MAP[y]["visitors"], "0.0", input_cell=True)
    txt(ws, 6, 20, "黄色可调；建设期保持0")

    txt(ws, 7, 1, "付费转化率", True)
    for y in range(1, 19):
        num(ws, 7, y + 1, VISITOR_MAP[y]["pay_rate"], "0.0%", input_cell=True)
    txt(ws, 7, 20, "表6：50%/60%/85%/85%")

    txt(ws, 8, 1, "游客客单价（元）", True)
    for y in range(1, 19):
        num(ws, 8, y + 1, VISITOR_MAP[y]["ticket"], "0", input_cell=True)
    txt(ws, 8, 20, "游客端花费，含联营方留存")

    txt(ws, 9, 1, "游客消费总额（万元）", True, BLUE_LT)
    for y in range(1, 19):
        col = get_column_letter(y + 1)
        ws.cell(9, y + 1, f"={col}6*{col}7*{col}8")
        ws.cell(9, y + 1).number_format = "#,##0.00"
        ws.cell(9, y + 1).fill = fill(BLUE_LT)
        ws.cell(9, y + 1).border = thin
        ws.cell(9, y + 1).font = font(size=9, bold=True)
    txt(ws, 9, 20, "人流×转化×客单，作收入上限校验", bg=BLUE_LT)

    txt(ws, 10, 1, "阶段", True)
    for y in range(1, 19):
        txt(ws, 10, y + 1, VISITOR_MAP[y]["stage"], center=True, bg=GRAY if y <= 2 else GREEN_LT)

    # 对照原表
    ws.cell(12, 1, "原表6四档对照（不参与18年滚动，仅备查）").font = font(bold=True, color=WHITE)
    ws.cell(12, 1).fill = fill(GREEN)
    ws.merge_cells("A12:F12")
    header_row(ws, 13, ["档位", "入园人次（万人）", "付费转化率", "客单价（元）", "游客消费（万元）", "对应本模型"], TEAL)
    for i, (k, (v, p, t)) in enumerate(VISITOR_TABLE6.items(), 14):
        txt(ws, i, 1, k, True)
        num(ws, i, 2, v, "0.0")
        num(ws, i, 3, p, "0.0%")
        num(ws, i, 4, t, "0")
        ws.cell(i, 5, f"=B{i}*C{i}*D{i}")
        ws.cell(i, 5).number_format = "#,##0.00"
        ws.cell(i, 5).border = thin
        ws.cell(i, 5).fill = fill(BLUE_LT)
        txt(ws, i, 6, {"1年": "建设期对照", "2年": "建设期对照", "3年": "→第3年达产", "4~18年": "→第4–18年保底"}[k])

    ws.cell(19, 1, "公园账面收入将低于游客消费总额：联营项目只确认分成，差额为合作方留存，不重复加总。").font = font(size=9, color="666666")
    ws.merge_cells("A19:T19")

    set_widths(ws, [22] + [9] * 18 + [28])
    ws.freeze_panes = "B6"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.print_title_rows = "1:5"

    # =====================================================================
    # 业态参数
    # =====================================================================
    ws = wb.create_sheet("业态参数")
    title_bar(ws, "业态参数｜联营 / 自营 / 出租 / 品牌加盟成本结构", 16)
    ws.merge_cells("A3:P3")
    txt(
        ws,
        3,
        1,
        "联营：公园收入=GMV×分成或保底租金，成本仅合同管理/水电分摊（约5–8%），不承担对方人工。自营：全额收入，承担货品、渠道、编制。出租：租金，物业约6–8%。品牌加盟：全额入账，万达门票10%进成本。",
        bg=ORANGE,
    )
    headers = [
        "序号",
        "经营项目",
        "业态板块",
        "经营性质",
        "驱动",
        "公园分成",
        "转化率",
        "客单/单价",
        "面积㎡",
        "日租(元)",
        "年天数",
        "出租率",
        "场次/日",
        "场次单价(万)",
        "利用率",
        "固定(万)",
        "货品/直接",
        "渠道营销",
        "运营分摊",
        "编制(人)",
        "是否填充",
        "来源与容量说明",
    ]
    header_row(ws, 4, headers, GREEN)
    for i, p in enumerate(PROJECTS, 5):
        txt(ws, i, 1, i - 4, center=True)
        txt(ws, i, 2, p.name, True)
        txt(ws, i, 3, p.sector)
        txt(ws, i, 4, p.nature, True, nature_fill(p.nature), True)
        txt(ws, i, 5, p.driver, center=True)
        num(ws, i, 6, p.share, "0.00%", input_cell=True)
        num(ws, i, 7, p.conv, "0.00%", input_cell=True)
        num(ws, i, 8, p.price, "0.00", input_cell=True)
        num(ws, i, 9, p.area, "0.00", input_cell=True)
        num(ws, i, 10, p.daily_rent, "0.00", input_cell=True)
        num(ws, i, 11, p.days, "0", input_cell=True)
        num(ws, i, 12, p.occ, "0.00%", input_cell=True)
        num(ws, i, 13, p.events, "0.00", input_cell=True)
        num(ws, i, 14, p.event_price, "0.00", input_cell=True)
        num(ws, i, 15, p.util, "0.00%", input_cell=True)
        num(ws, i, 16, p.fixed, "0.00", input_cell=True)
        num(ws, i, 17, p.cogs, "0.00%", input_cell=True)
        num(ws, i, 18, p.channel, "0.00%", input_cell=True)
        num(ws, i, 19, p.opex, "0.00%", input_cell=True)
        num(ws, i, 20, p.staff, "0", input_cell=True)
        txt(ws, i, 21, "填充" if p.fill else "原表", center=True, bg=YELLOW if p.fill else GREEN_LT)
        txt(ws, i, 22, p.cap_note + "｜" + p.source)
        ws.row_dimensions[i].height = 32
    last_p = 4 + len(PROJECTS)

    # 宝贝王专项参数
    r = last_p + 2
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    txt(ws, r, 1, "超级宝贝王专项参数（品牌加盟）", True, "F9E79F")
    r += 1
    header_row(ws, r, ["参数", "数值", "说明", "", "", "", "", ""], TEAL)
    bk_params = [
        ("研学客流占全园", 0.24, "封顶20万人"),
        ("一般客流占全园", 0.24, "与研学合计封顶40万人"),
        ("研学客单（元）", 35, ""),
        ("一般客单（元）", 48, ""),
        ("二消转化率", 0.32, ""),
        ("二消客单（元）", 18, ""),
        ("万达门票分成", 0.10, "仅门票/体验，不含二消"),
        ("线上客流占比", 0.70, "仅一般客流"),
        ("线上佣金率", 0.10, ""),
        ("销售提成率", 0.02, "总流水"),
        ("维护费率", 0.08, "门票流水，已低于原10%"),
        ("二消成本率", 0.58, ""),
        ("日常营销费率", 0.04, "门票流水"),
        ("水电（万元/万人）", 1.65, ""),
        ("保安保洁（万元）", 28, "项目内专项，不与公共重复"),
    ]
    bk_start = r + 1
    for i, (name, val, note) in enumerate(bk_params):
        rr = bk_start + i
        txt(ws, rr, 1, name, True)
        fmt = "0.00%" if val <= 1 and "客单" not in name and "水电" not in name and "保安" not in name else "0.00"
        if "客单" in name or "水电" in name or "保安" in name:
            fmt = "0.00"
        num(ws, rr, 2, val, fmt, input_cell=True)
        txt(ws, rr, 3, note)
        ws.merge_cells(start_row=rr, start_column=3, end_row=rr, end_column=8)
    bk_end = bk_start + len(bk_params) - 1

    # public cost params
    r = bk_end + 2
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    txt(ws, r, 1, "公共成本参数（达产年=75万人，其余按人流线性）", True, BLUE_LT)
    r += 1
    header_row(ws, r, ["参数", "数值", "说明"], TEAL)
    pub = [
        ("公共水电达产（万元）", 95, "按人流/75缩放"),
        ("全园营销费率", 0.018, "与项目渠道不重复叠高"),
        ("营销下限（万元）", 90, ""),
        ("维修保养达产（万元）", 70, ""),
        ("保险（万元）", 22, ""),
        ("办公杂费（万元）", 28, ""),
        ("动物饲料医疗（万元）", 48, "既有55只/13品种，不新增笼舍以外项目"),
        ("所得税率", 0.25, ""),
        ("折旧残值率", 0.05, "总投资×95%/16年"),
        ("还本年限（年）", 10, "经营期等额本金"),
    ]
    pub_start = r + 1
    for i, (name, val, note) in enumerate(pub):
        rr = pub_start + i
        txt(ws, rr, 1, name, True)
        fmt = "0.00%" if (isinstance(val, float) and val <= 1 and "水电" not in name and "下限" not in name and "维修" not in name and "保险" not in name and "办公" not in name and "饲料" not in name and "还本" not in name) else "0.00"
        num(ws, rr, 2, val, fmt, input_cell=True)
        txt(ws, rr, 3, note)
    pub_end = pub_start + len(pub) - 1

    set_widths(ws, [8, 22, 14, 12, 12, 10, 10, 12, 10, 10, 10, 10, 10, 12, 10, 10, 10, 10, 10, 10, 10, 56])
    ws.freeze_panes = "C5"
    ws.auto_filter.ref = f"A4:V{last_p}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = "1:4"

    # store row maps for formulas
    proj_row = {p.key: 5 + i for i, p in enumerate(PROJECTS)}
    # bk params rows
    bk_row = {bk_params[i][0]: bk_start + i for i in range(len(bk_params))}
    pub_row = {pub[i][0]: pub_start + i for i in range(len(pub))}

    # =====================================================================
    # 人力编制
    # =====================================================================
    ws = wb.create_sheet("人力编制")
    title_bar(ws, "人力成本修正｜通化地区全包年薪（含单位社保公积金）", 8)
    ws.merge_cells("A3:H3")
    txt(
        ws,
        3,
        1,
        "修正要点：①联营项目不再重复计提厨房/演职/店员固定人工；②表6列明编制逐岗落地；③宝贝王26人拆主管/技工/营运，约202.8万元（原216.72万元）；④既有动物园保育单独列，不新增项目；⑤建设期人力含在300万管理费中，经营编制自第3年计。",
        bg=YELLOW,
    )
    header_row(ws, 4, ["类别", "岗位", "人数", "年成本（万元/人）", "年合计（万元）", "备注", "口径", "对应项目"], GREEN)
    for i, row in enumerate(STAFF_ROWS, 5):
        typ, post, n, unit, note = row
        txt(ws, i, 1, typ, True, nature_fill("自营" if typ == "自营" else ("品牌加盟" if typ == "加盟" else ("联营" if typ == "联营协助" else "出租"))))
        txt(ws, i, 2, post)
        num(ws, i, 3, n, "0", input_cell=True)
        num(ws, i, 4, unit, "0.00", input_cell=True)
        ws.cell(i, 5, f"=C{i}*D{i}")
        ws.cell(i, 5).number_format = "0.00"
        ws.cell(i, 5).border = thin
        ws.cell(i, 5).fill = fill(GREEN_LT)
        txt(ws, i, 6, note)
        txt(ws, i, 7, "12个月全包，含单位社保约38%")
        txt(ws, i, 8, "")
    last_s = 4 + len(STAFF_ROWS)
    txt(ws, last_s + 1, 1, "合计", True, GREEN)
    ws.cell(last_s + 1, 1).font = font(bold=True, color=WHITE)
    ws.cell(last_s + 1, 3, f"=SUM(C5:C{last_s})-C{last_s}")  # exclude 弹性 headcount packed as 1
    # clearer: sum all heads except 旺季弹性记1
    ws.cell(last_s + 1, 3, f"=SUM(C5:C{last_s - 1})")
    ws.cell(last_s + 1, 3).number_format = "0"
    ws.cell(last_s + 1, 3).fill = fill(GREEN_LT)
    ws.cell(last_s + 1, 3).border = thin
    ws.cell(last_s + 1, 5, f"=SUM(E5:E{last_s})")
    ws.cell(last_s + 1, 5).number_format = "0.00"
    ws.cell(last_s + 1, 5).fill = fill(GREEN)
    ws.cell(last_s + 1, 5).font = font(bold=True, color=WHITE)
    ws.cell(last_s + 1, 5).border = thin
    txt(ws, last_s + 1, 2, "编制人数（不含弹性包干行）", True, GREEN_LT)

    # by type
    r = last_s + 3
    header_row(ws, r, ["类别", "年成本（万元）"], TEAL)
    cats = ["公共", "加盟", "自营", "联营协助"]
    for i, cat in enumerate(cats):
        txt(ws, r + 1 + i, 1, cat, True)
        ws.cell(r + 1 + i, 2, f'=SUMIF(A5:A{last_s},A{r + 1 + i},E5:E{last_s})')
        ws.cell(r + 1 + i, 2).number_format = "0.00"
        ws.cell(r + 1 + i, 2).border = thin
        ws.cell(r + 1 + i, 2).fill = fill(GREEN_LT)
    txt(ws, r + 5, 1, "人力总计", True, GREEN)
    ws.cell(r + 5, 1).font = font(bold=True, color=WHITE)
    ws.cell(r + 5, 2, f"=SUM(B{r + 1}:B{r + 4})")
    ws.cell(r + 5, 2).number_format = "0.00"
    ws.cell(r + 5, 2).fill = fill(GREEN)
    ws.cell(r + 5, 2).font = font(bold=True, color=WHITE)
    ws.cell(r + 5, 2).border = thin

    staff_sum_row = last_s + 1
    staff_pub_row = r + 1
    staff_join_row = r + 2
    staff_self_row = r + 3
    staff_help_row = r + 4
    staff_tot_row = r + 5

    set_widths(ws, [14, 24, 10, 18, 16, 36, 28, 16])
    ws.freeze_panes = "A5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.print_title_rows = "1:4"

    # =====================================================================
    # 收入测算 18年
    # =====================================================================
    ws = wb.create_sheet("收入测算")
    title_bar(ws, "经营收入测算｜公园账面口径（万元）", 22)
    ws.merge_cells("A3:V3")
    txt(ws, 3, 1, "建设期收入为0。人流驱动：入园万人×转化×客单×分成。租金驱动：面积×日租×天数×出租率/10000。活动驱动：场次×单价×利用率。宝贝王见专项公式。", bg=BLUE_LT)
    header_row(ws, 4, ["序号", "经营项目", "经营性质"] + [f"第{y}年" for y in range(1, 19)] + ["达产占比"], GREEN)

    # babyking volume helper rows will be below
    for i, p in enumerate(PROJECTS):
        r = 5 + i
        pr = proj_row[p.key]
        txt(ws, r, 1, i + 1, center=True)
        txt(ws, r, 2, p.name, True)
        txt(ws, r, 3, p.nature, True, nature_fill(p.nature), True)
        for y in range(1, 19):
            col = get_column_letter(3 + y)  # D=4 for year1 → year y col = 3+y
            vcol = get_column_letter(y + 1)  # 人流表 year1 = B
            # 收入测算: col D is year 1, so year y is column 3+y
            cidx = 3 + y
            if p.driver == "traffic":
                formula = f"=IF('06人流模型'!{vcol}6<=0,0,'06人流模型'!{vcol}6*业态参数!$G${pr}*业态参数!$H${pr}*业态参数!$F${pr})"
            elif p.driver == "rent":
                formula = f"=IF('06人流模型'!{vcol}6<=0,0,业态参数!$I${pr}*业态参数!$J${pr}*业态参数!$K${pr}*业态参数!$L${pr}/10000)"
            elif p.driver == "event":
                formula = f"=IF('06人流模型'!{vcol}6<=0,0,业态参数!$M${pr}*业态参数!$N${pr}*业态参数!$O${pr})"
            elif p.driver == "fixed":
                formula = f"=IF('06人流模型'!{vcol}6<=0,0,业态参数!$P${pr}*'06人流模型'!{vcol}6/75)"
            elif p.driver == "babyking":
                # ticket + second; volume from 人流 * rates with cap 20 each and 40 total
                # Use helper rows later; for now reference 宝贝王明细
                formula = f"=IF('06人流模型'!{vcol}6<=0,0,宝贝王明细!{get_column_letter(y + 1)}16)"
            else:
                formula = "0"
            ws.cell(r, cidx, formula)
            ws.cell(r, cidx).number_format = "0.00"
            ws.cell(r, cidx).border = thin
            ws.cell(r, cidx).font = font(size=8)
            if y <= 2:
                ws.cell(r, cidx).fill = fill(GRAY)
        # 达产占比 year 3 = column F (3+3=6)
        ws.cell(r, 22, f"=IF($F$35=0,0,F{r}/$F$35)")
        ws.cell(r, 22).number_format = "0.0%"
        ws.cell(r, 22).border = thin

    tot_r = 5 + len(PROJECTS)
    txt(ws, tot_r, 1, "", bg=GREEN)
    txt(ws, tot_r, 2, "公园账面收入合计", True, GREEN)
    ws.cell(tot_r, 2).font = font(bold=True, color=WHITE)
    txt(ws, tot_r, 3, "", bg=GREEN)
    for y in range(1, 19):
        cidx = 3 + y
        col = get_column_letter(cidx)
        ws.cell(tot_r, cidx, f"=SUM({col}5:{col}{tot_r - 1})")
        ws.cell(tot_r, cidx).number_format = "#,##0.00"
        ws.cell(tot_r, cidx).fill = fill(GREEN)
        ws.cell(tot_r, cidx).font = font(bold=True, color=WHITE)
        ws.cell(tot_r, cidx).border = thin
    ws.cell(tot_r, 22, "=SUM(V5:V{})".format(tot_r - 1))
    ws.cell(tot_r, 22).number_format = "0.0%"
    ws.cell(tot_r, 22).fill = fill(GREEN_LT)
    ws.cell(tot_r, 22).border = thin

    # nature sums
    for offset, nature in enumerate(["联营", "自营", "出租", "品牌加盟"], 1):
        rr = tot_r + offset
        txt(ws, rr, 2, f"{nature}收入小计", True, nature_fill(nature))
        txt(ws, rr, 3, nature, True, nature_fill(nature), True)
        for y in range(1, 19):
            cidx = 3 + y
            col = get_column_letter(cidx)
            ws.cell(rr, cidx, f'=SUMIF($C$5:$C${tot_r - 1},C{rr},{col}5:{col}{tot_r - 1})')
            ws.cell(rr, cidx).number_format = "0.00"
            ws.cell(rr, cidx).fill = fill(nature_fill(nature))
            ws.cell(rr, cidx).border = thin

    chk_r = tot_r + 6
    txt(ws, chk_r, 2, "游客消费总额（表6校验）", True, BLUE_LT)
    for y in range(1, 19):
        cidx = 3 + y
        vcol = get_column_letter(y + 1)
        ws.cell(chk_r, cidx, f"='06人流模型'!{vcol}9")
        ws.cell(chk_r, cidx).number_format = "0.00"
        ws.cell(chk_r, cidx).fill = fill(BLUE_LT)
        ws.cell(chk_r, cidx).border = thin
    txt(ws, chk_r + 1, 2, "公园捕获率", True, BLUE_LT)
    for y in range(1, 19):
        cidx = 3 + y
        col = get_column_letter(cidx)
        ws.cell(chk_r + 1, cidx, f"=IF({col}{chk_r}=0,0,{col}{tot_r}/{col}{chk_r})")
        ws.cell(chk_r + 1, cidx).number_format = "0.0%"
        ws.cell(chk_r + 1, cidx).fill = fill(BLUE_LT)
        ws.cell(chk_r + 1, cidx).border = thin
    txt(ws, chk_r + 2, 2, "全客流人均公园贡献（元）", True)
    for y in range(1, 19):
        cidx = 3 + y
        col = get_column_letter(cidx)
        vcol = get_column_letter(y + 1)
        ws.cell(chk_r + 2, cidx, f"=IF('06人流模型'!{vcol}6=0,0,{col}{tot_r}/'06人流模型'!{vcol}6)")
        ws.cell(chk_r + 2, cidx).number_format = "0.00"
        ws.cell(chk_r + 2, cidx).border = thin

    income_tot = tot_r
    income_liany = tot_r + 1
    income_self = tot_r + 2
    income_rent = tot_r + 3
    income_join = tot_r + 4
    income_check = chk_r

    set_widths(ws, [6, 20, 12] + [9] * 18 + [10])
    ws.freeze_panes = "D5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = "1:4"
    ws.print_title_cols = "A:C"

    # =====================================================================
    # 宝贝王明细
    # =====================================================================
    ws = wb.create_sheet("宝贝王明细")
    title_bar(ws, "超级宝贝王｜品牌加盟收入与成本（万元）", 20)
    header_row(ws, 4, ["测算项"] + [f"第{y}年" for y in range(1, 19)], GREEN)

    def bk_ref(name):
        return f"业态参数!$B${bk_row[name]}"

    rows_bk = [
        (5, "全园人次（万人）", [f"='06人流模型'!{get_column_letter(y + 1)}6" for y in range(1, 19)]),
        (6, "研学客流（万人）", None),
        (7, "一般客流（万人）", None),
        (8, "总接待（万人）", None),
        (9, "研学收入", None),
        (10, "一般客流收入", None),
        (11, "门票/体验流水", None),
        (12, "二消收入", None),
        (16, "营业收入合计", None),
    ]
    # write labels
    labels_map = {
        5: "全园人次（万人）",
        6: "研学客流（万人）",
        7: "一般客流（万人）",
        8: "总接待（万人）",
        9: "研学收入",
        10: "一般客流收入",
        11: "门票/体验流水",
        12: "二消收入",
        13: "万达门票分成10%",
        14: "线上渠道佣金",
        15: "销售提成",
        16: "营业收入合计",
        17: "游乐维护",
        18: "二消商品成本",
        19: "日常营销",
        20: "开业/年度专项",
        21: "人工成本（26人）",
        22: "水电能耗",
        23: "保安保洁（项目内）",
        24: "经营成本合计",
        25: "经营贡献",
    }
    for r, lab in labels_map.items():
        txt(ws, r, 1, lab, True, GREEN_LT if r in (11, 16, 24, 25) else None)

    for y in range(1, 19):
        c = y + 1
        cl = get_column_letter(c)
        # 5 visitors
        ws.cell(5, c, f"='06人流模型'!{cl}6")
        # 6 study = min(20, vis*rate)
        ws.cell(6, c, f"=IF({cl}5<=0,0,MIN(20,{cl}5*{bk_ref('研学客流占全园')}))")
        ws.cell(7, c, f"=IF({cl}5<=0,0,MIN(20,{cl}5*{bk_ref('一般客流占全园')}))")
        # cap 40
        ws.cell(8, c, f"={cl}6+{cl}7")
        # if over 40 scale - keep simple MIN already 20+20=40
        ws.cell(9, c, f"={cl}6*{bk_ref('研学客单（元）')}")
        ws.cell(10, c, f"={cl}7*{bk_ref('一般客单（元）')}")
        ws.cell(11, c, f"={cl}9+{cl}10")
        ws.cell(12, c, f"={cl}8*{bk_ref('二消转化率')}*{bk_ref('二消客单（元）')}")
        ws.cell(16, c, f"={cl}11+{cl}12")
        ws.cell(13, c, f"={cl}11*{bk_ref('万达门票分成')}")
        ws.cell(14, c, f"={cl}10*{bk_ref('线上客流占比')}*{bk_ref('线上佣金率')}")
        ws.cell(15, c, f"={cl}16*{bk_ref('销售提成率')}")
        ws.cell(17, c, f"={cl}11*{bk_ref('维护费率')}")
        ws.cell(18, c, f"={cl}12*{bk_ref('二消成本率')}")
        ws.cell(19, c, f"={cl}11*{bk_ref('日常营销费率')}")
        ws.cell(20, c, f"=IF({cl}5<=0,0,IF({cl}5>=70,8,12))")
        ws.cell(21, c, f"=IF({cl}5<=0,0,人力编制!B{staff_join_row})")
        ws.cell(22, c, f"={cl}8*{bk_ref('水电（万元/万人）')}")
        ws.cell(23, c, f"=IF({cl}5<=0,0,{bk_ref('保安保洁（万元）')})")
        ws.cell(24, c, f"=SUM({cl}13:{cl}15,{cl}17:{cl}23)")
        ws.cell(25, c, f"={cl}16-{cl}24")
        for r in range(5, 26):
            ws.cell(r, c).number_format = "0.00"
            ws.cell(r, c).border = thin
            ws.cell(r, c).font = font(size=8)
            if r in (16, 24, 25):
                ws.cell(r, c).fill = fill(GREEN_LT)
                ws.cell(r, c).font = font(size=8, bold=True)
            if y <= 2:
                ws.cell(r, c).fill = fill(GRAY)

    ws.merge_cells("A27:S27")
    txt(ws, 27, 1, "万达10%只计提门票/体验流水；品牌使用费100万元已包含在表5儿童乐园投资中，不再单独现金列支。设备折旧在全园折旧中统一计提，本表不再重复。", bg=YELLOW)

    set_widths(ws, [24] + [9] * 18)
    ws.freeze_panes = "B5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.print_title_rows = "1:4"

    # =====================================================================
    # 成本利润
    # =====================================================================
    ws = wb.create_sheet("成本利润")
    title_bar(ws, "项目成本与经营贡献｜按经营性质区分构成（万元）", 22)
    ws.merge_cells("A3:V3")
    txt(ws, 3, 1, "联营/出租：成本=收入×（直接+渠道+运营分摊），不含对方人工。自营：变动成本同左，编制工资在下方「自营及联营协助人力」一次计入。宝贝王成本取专项表。", bg=ORANGE)
    header_row(ws, 4, ["序号", "经营项目", "经营性质"] + [f"第{y}年成本" for y in range(1, 19)] + ["达产贡献率"], GREEN)

    for i, p in enumerate(PROJECTS):
        r = 5 + i
        pr = proj_row[p.key]
        txt(ws, r, 1, i + 1, center=True)
        txt(ws, r, 2, p.name)
        txt(ws, r, 3, p.nature, True, nature_fill(p.nature), True)
        for y in range(1, 19):
            cidx = 3 + y
            icol = get_column_letter(cidx)
            if p.driver == "babyking":
                formula = f"=宝贝王明细!{get_column_letter(y + 1)}24"
            else:
                formula = f"=收入测算!{icol}{r}*(业态参数!$Q${pr}+业态参数!$R${pr}+业态参数!$S${pr})"
            ws.cell(r, cidx, formula)
            ws.cell(r, cidx).number_format = "0.00"
            ws.cell(r, cidx).border = thin
            ws.cell(r, cidx).font = font(size=8)
            if y <= 2:
                ws.cell(r, cidx).fill = fill(GRAY)
        ws.cell(r, 22, f"=IF(收入测算!F{r}=0,0,(收入测算!F{r}-F{r})/收入测算!F{r})")
        ws.cell(r, 22).number_format = "0.0%"
        ws.cell(r, 22).border = thin

    cost_last = 4 + len(PROJECTS)
    extra_rows = {
        "self_staff": cost_last + 1,
        "help_note": cost_last + 2,
    }
    txt(ws, cost_last + 1, 2, "自营+联营协助人力（编制表一次计入）", True, PURPLE)
    txt(ws, cost_last + 1, 3, "自营", True, PURPLE, True)
    for y in range(1, 19):
        cidx = 3 + y
        vcol = get_column_letter(y + 1)
        ws.cell(cost_last + 1, cidx, f"=IF('06人流模型'!{vcol}6<=0,0,人力编制!B{staff_self_row}+人力编制!B{staff_help_row})")
        ws.cell(cost_last + 1, cidx).number_format = "0.00"
        ws.cell(cost_last + 1, cidx).fill = fill(PURPLE)
        ws.cell(cost_last + 1, cidx).border = thin

    # public overhead breakdown
    oh_start = cost_last + 3
    txt(ws, oh_start, 2, "公共人力", True, BLUE_LT)
    txt(ws, oh_start + 1, 2, "公共水电", True)
    txt(ws, oh_start + 2, 2, "全园营销", True)
    txt(ws, oh_start + 3, 2, "维修保养", True)
    txt(ws, oh_start + 4, 2, "保险", True)
    txt(ws, oh_start + 5, 2, "办公杂费", True)
    txt(ws, oh_start + 6, 2, "既有动物饲料医疗", True, YELLOW)
    for y in range(1, 19):
        cidx = 3 + y
        cl = get_column_letter(cidx)
        vcol = get_column_letter(y + 1)
        vis = f"'06人流模型'!{vcol}6"
        ws.cell(oh_start, cidx, f"=IF({vis}<=0,0,人力编制!B{staff_pub_row})")
        ws.cell(oh_start + 1, cidx, f"=IF({vis}<=0,0,业态参数!$B${pub_row['公共水电达产（万元）']}*{vis}/75)")
        ws.cell(oh_start + 2, cidx, f"=IF({vis}<=0,0,MAX(业态参数!$B${pub_row['营销下限（万元）']},收入测算!{cl}{income_tot}*业态参数!$B${pub_row['全园营销费率']}))")
        ws.cell(oh_start + 3, cidx, f"=IF({vis}<=0,0,业态参数!$B${pub_row['维修保养达产（万元）']}*{vis}/75)")
        ws.cell(oh_start + 4, cidx, f"=IF({vis}<=0,0,业态参数!$B${pub_row['保险（万元）']})")
        ws.cell(oh_start + 5, cidx, f"=IF({vis}<=0,0,业态参数!$B${pub_row['办公杂费（万元）']})")
        ws.cell(oh_start + 6, cidx, f"=IF({vis}<=0,0,业态参数!$B${pub_row['动物饲料医疗（万元）']})")
        for rr in range(oh_start, oh_start + 7):
            ws.cell(rr, cidx).number_format = "0.00"
            ws.cell(rr, cidx).border = thin
            if y <= 2:
                ws.cell(rr, cidx).fill = fill(GRAY)

    tot_cost_r = oh_start + 7
    txt(ws, tot_cost_r, 2, "经营成本合计", True, GREEN)
    ws.cell(tot_cost_r, 2).font = font(bold=True, color=WHITE)
    for y in range(1, 19):
        cidx = 3 + y
        cl = get_column_letter(cidx)
        ws.cell(tot_cost_r, cidx, f"=SUM({cl}5:{cl}{oh_start + 6})")
        ws.cell(tot_cost_r, cidx).number_format = "#,##0.00"
        ws.cell(tot_cost_r, cidx).fill = fill(GREEN)
        ws.cell(tot_cost_r, cidx).font = font(bold=True, color=WHITE)
        ws.cell(tot_cost_r, cidx).border = thin

    contrib_r = tot_cost_r + 1
    txt(ws, contrib_r, 2, "经营贡献", True, GREEN_LT)
    for y in range(1, 19):
        cidx = 3 + y
        cl = get_column_letter(cidx)
        ws.cell(contrib_r, cidx, f"=收入测算!{cl}{income_tot}-{cl}{tot_cost_r}")
        ws.cell(contrib_r, cidx).number_format = "#,##0.00"
        ws.cell(contrib_r, cidx).fill = fill(GREEN_LT)
        ws.cell(contrib_r, cidx).font = font(bold=True)
        ws.cell(contrib_r, cidx).border = thin

    set_widths(ws, [6, 28, 12] + [9] * 18 + [12])
    ws.freeze_panes = "D5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = "1:4"
    ws.print_title_cols = "A:C"

    # =====================================================================
    # 18年财务
    # =====================================================================
    ws = wb.create_sheet("18年财务")
    title_bar(ws, "18年财务计划｜利润、现金流与投资回收（万元）", 20)
    header_row(ws, 4, ["科目"] + [f"第{y}年" for y in range(1, 19)], GREEN)

    fin_labels = {
        5: "阶段",
        6: "入园人次（万人）",
        7: "公园营业收入",
        8: "其中：联营",
        9: "其中：自营",
        10: "其中：出租",
        11: "其中：品牌加盟",
        12: "经营成本",
        13: "经营贡献",
        14: "折旧摊销",
        15: "经营期利息",
        16: "利润总额",
        17: "所得税",
        18: "净利润",
        19: "经营期还本",
        20: "建设投资现金流出",
        21: "静态经营现金流（净利+折旧）",
        22: "累计静态经营现金流",
        23: "项目自由现金流",
        24: "累计自由现金流",
        25: "贷款余额",
    }
    for r, lab in fin_labels.items():
        bg = GREEN_LT if r in (16, 18, 21, 22) else None
        txt(ws, r, 1, lab, True, bg)

    for y in range(1, 19):
        c = y + 1
        cl = get_column_letter(c)
        icol = get_column_letter(3 + y)
        vcol = get_column_letter(y + 1)
        vis = f"'06人流模型'!{vcol}6"
        ws.cell(5, c, VISITOR_MAP[y]["stage"])
        ws.cell(6, c, f"={vis}")
        ws.cell(7, c, f"=收入测算!{icol}{income_tot}")
        ws.cell(8, c, f"=收入测算!{icol}{income_liany}")
        ws.cell(9, c, f"=收入测算!{icol}{income_self}")
        ws.cell(10, c, f"=收入测算!{icol}{income_rent}")
        ws.cell(11, c, f"=收入测算!{icol}{income_join}")
        ws.cell(12, c, f"=成本利润!{icol}{tot_cost_r}")
        ws.cell(13, c, f"=成本利润!{icol}{contrib_r}")
        ws.cell(14, c, f'=IF({vis}<=0,0,总投资*(1-业态参数!$B${pub_row["折旧残值率"]})/16)')
        ws.cell(15, c, f'=IF({vis}<=0,0,IF(AND(COLUMN()-1>=3,COLUMN()-1<=12),贷款本金*(1-(COLUMN()-1-3)/业态参数!$B${pub_row["还本年限（年）"]})*贷款利率,0))')
        # year number = c-1; operating year k = year-2; loan_beg = loan*(1-(k-1)/10) for k=1..10
        # COLUMN()-1 is year when data starts at col B (col 2) so year = COLUMN()-1. Yes.
        ws.cell(16, c, f"={cl}13-{cl}14-{cl}15")
        ws.cell(17, c, f'=MAX({cl}16,0)*业态参数!$B${pub_row["所得税率"]}')
        ws.cell(18, c, f"={cl}16-{cl}17")
        ws.cell(19, c, f'=IF({vis}<=0,0,IF(AND(COLUMN()-1>=3,COLUMN()-1<=12),贷款本金/业态参数!$B${pub_row["还本年限（年）"]},0))')
        ws.cell(20, c, f"=IF(COLUMN()-1<=2,-总投资/2,0)")
        ws.cell(21, c, f"=IF({vis}<=0,0,{cl}18+{cl}14)")
        if y == 1:
            ws.cell(22, c, f"={cl}21")
            ws.cell(24, c, f"={cl}23")
            ws.cell(25, c, "=贷款本金")
        else:
            prev = get_column_letter(c - 1)
            ws.cell(22, c, f"={prev}22+{cl}21")
            ws.cell(24, c, f"={prev}24+{cl}23")
            ws.cell(25, c, f"=MAX({prev}25-{cl}19,0)")
        ws.cell(23, c, f"={cl}21+{cl}20-{cl}19")
        for r in range(6, 26):
            if r == 5:
                continue
            ws.cell(r, c).number_format = "0.00"
            ws.cell(r, c).border = thin
            ws.cell(r, c).font = font(size=8)
            if r in (16, 18):
                ws.cell(r, c).fill = fill(GREEN_LT)
                ws.cell(r, c).font = font(size=8, bold=True)
            if y <= 2 and r >= 7:
                ws.cell(r, c).fill = fill(GRAY)
        ws.cell(5, c).border = thin
        ws.cell(5, c).alignment = align("center", "center", False)
        ws.cell(5, c).fill = fill(GRAY if y <= 2 else GREEN_LT)

    # KPI block
    ws.merge_cells("A28:D28")
    txt(ws, 28, 1, "回收与利润约束", True, GREEN)
    ws.cell(28, 1).font = font(bold=True, color=WHITE)
    header_row(ws, 29, ["指标", "公式/口径", "结果", "目标", "状态"], TEAL)
    txt(ws, 30, 1, "第3–18年利润总额合计")
    txt(ws, 30, 2, "SUM 第3年至第18年利润总额")
    ws.cell(30, 3, "=SUM(D16:S16)")
    txt(ws, 31, 1, "第3–18年年均利润总额")
    txt(ws, 31, 2, "合计/16")
    ws.cell(31, 3, "=C30/16")
    txt(ws, 31, 4, 3000)
    ws.cell(31, 5, '=IF(C31>=D31,"达标","未达标")')
    txt(ws, 32, 1, "第3–18年最低利润总额")
    txt(ws, 32, 2, "MIN")
    ws.cell(32, 3, "=MIN(D16:S16)")
    txt(ws, 32, 4, 3000)
    ws.cell(32, 5, '=IF(C32>=D32,"达标","关注")')
    txt(ws, 33, 1, "第3–18年年均净利润")
    ws.cell(33, 3, "=AVERAGE(D18:S18)")
    txt(ws, 34, 1, "经营期静态回收期（年）")
    txt(ws, 34, 2, "累计静态经营现金流首次≥总投资，自开业起算")
    # approximate payback: MATCH
    ws.cell(34, 3, '=IF(D22>=总投资,1,IF(E22>=总投资,1+(总投资-D22)/E21,IF(F22>=总投资,2+(总投资-E22)/F21,IF(G22>=总投资,3+(总投资-F22)/G21,"超过3年"))))')
    txt(ws, 34, 4, 3)
    ws.cell(34, 5, '=IF(AND(ISNUMBER(C34),C34<=D34),"达标","未达标")')
    txt(ws, 35, 1, "含建设期累计转正年份")
    ws.cell(35, 3, '=MATCH(TRUE,INDEX(B24:S24>=0,0),0)')
    txt(ws, 36, 1, "总投资")
    ws.cell(36, 3, "=总投资")
    for r in range(30, 37):
        ws.cell(r, 3).number_format = "0.00"
        ws.cell(r, 3).fill = fill(GREEN_LT)
        ws.cell(r, 3).border = thin
        ws.cell(r, 3).font = font(bold=True)
        for c in range(1, 6):
            ws.cell(r, c).border = thin
    ws.cell(31, 4).number_format = "0"
    ws.cell(31, 4).fill = fill(YELLOW)
    ws.cell(32, 4).fill = fill(YELLOW)
    ws.cell(34, 4).fill = fill(YELLOW)

    # charts data is the year rows themselves
    chart1 = BarChart()
    chart1.type = "col"
    chart1.title = "第1–18年利润总额"
    chart1.y_axis.title = "万元"
    data = Reference(ws, min_col=2, max_col=19, min_row=16, max_row=16)
    cats = Reference(ws, min_col=2, max_col=19, min_row=4, max_row=4)
    chart1.add_data(data, from_rows=True, titles_from_data=False)
    chart1.set_categories(cats)
    chart1.shape = 4
    chart1.style = 10
    chart1.width = 22
    chart1.height = 8
    ws.add_chart(chart1, "A38")

    chart2 = LineChart()
    chart2.title = "累计静态经营现金流 vs 总投资"
    chart2.y_axis.title = "万元"
    data2 = Reference(ws, min_col=2, max_col=19, min_row=22, max_row=22)
    chart2.add_data(data2, from_rows=True, titles_from_data=False)
    chart2.set_categories(cats)
    chart2.style = 12
    chart2.width = 22
    chart2.height = 8
    ws.add_chart(chart2, "A55")

    set_widths(ws, [28] + [9] * 18)
    ws.freeze_panes = "B5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = "1:4"

    # =====================================================================
    # 经营总览
    # =====================================================================
    ws = wb.create_sheet("经营总览", 1)
    title_bar(ws, "经营总览｜约束达标与结构一览", 10)
    header_row(ws, 4, ["关键指标", "第1年", "第2年", "第3年（达产）", "第4–18年（保底代表年第4年）", "3–18年均", "目标", "状态", "口径", "管理动作"], GREEN)
    overview = [
        (5, "阶段", None),
        (6, "入园人次（万人）", "='18年财务'!B6"),
        (7, "公园营业收入（万元）", "='18年财务'!B7"),
        (8, "游客消费总额（万元）", "='06人流模型'!B9"),
        (9, "公园捕获率", None),
        (10, "经营成本（万元）", "='18年财务'!B12"),
        (11, "经营贡献（万元）", "='18年财务'!B13"),
        (12, "利润总额（万元）", "='18年财务'!B16"),
        (13, "净利润（万元）", "='18年财务'!B18"),
        (14, "静态经营现金流", "='18年财务'!B21"),
    ]
    for r, name, _ in overview:
        txt(ws, r, 1, name, True)
    for idx, col in enumerate(["B", "C", "D", "E"], 2):
        ws.cell(5, idx, f"='18年财务'!{col}5")
        ws.cell(6, idx, f"='18年财务'!{col}6")
        ws.cell(7, idx, f"='18年财务'!{col}7")
        vcol = col
        ws.cell(8, idx, f"='06人流模型'!{vcol}9")
        ws.cell(9, idx, f"=IF({col}8=0,0,{col}7/{col}8)")
        ws.cell(10, idx, f"='18年财务'!{col}12")
        ws.cell(11, idx, f"='18年财务'!{col}13")
        ws.cell(12, idx, f"='18年财务'!{col}16")
        ws.cell(13, idx, f"='18年财务'!{col}18")
        ws.cell(14, idx, f"='18年财务'!{col}21")
    ws.cell(5, 2, "建设期")
    ws.cell(5, 3, "建设期")
    ws.cell(5, 4, "开业达产")
    ws.cell(5, 5, "稳定保底")
    ws.cell(6, 6, "='18年财务'!C31")  # will overwrite
    # averages 3-18
    ws.cell(6, 6, "=AVERAGE('18年财务'!D6:S6)")
    ws.cell(7, 6, "=AVERAGE('18年财务'!D7:S7)")
    ws.cell(8, 6, "=AVERAGE('06人流模型'!D9:S9)")
    ws.cell(9, 6, "=IF(F8=0,0,F7/F8)")
    ws.cell(10, 6, "=AVERAGE('18年财务'!D12:S12)")
    ws.cell(11, 6, "=AVERAGE('18年财务'!D13:S13)")
    ws.cell(12, 6, "='18年财务'!C31")
    ws.cell(13, 6, "='18年财务'!C33")
    ws.cell(14, 6, "=AVERAGE('18年财务'!D21:S21)")
    ws.cell(12, 7, 3000)
    ws.cell(12, 8, "=IF(F12>=G12,\"达标\",\"未达标\")")
    txt(ws, 12, 9, "利润总额，含折旧与经营期利息")
    txt(ws, 12, 10, "达产后稳住联营分成与夜游/研学复购")
    txt(ws, 14, 9, "净利润+折旧，用于静态回收")
    for r in range(6, 15):
        for c in range(2, 7):
            ws.cell(r, c).number_format = "0.00" if r != 9 else "0.0%"
            ws.cell(r, c).border = thin
            if r in (12, 13):
                ws.cell(r, c).fill = fill(GREEN_LT)
                ws.cell(r, c).font = font(bold=True)
    ws.cell(12, 7).number_format = "0"
    ws.cell(12, 7).fill = fill(YELLOW)
    ws.cell(12, 7).border = thin
    ws.cell(12, 8).fill = fill(GREEN_LT)
    ws.cell(12, 8).border = thin
    ws.cell(12, 8).font = font(bold=True)

    # investment / payback cards
    ws.merge_cells("A16:J16")
    txt(ws, 16, 1, "投资与回收", True, GREEN)
    ws.cell(16, 1).font = font(bold=True, color=WHITE)
    header_row(ws, 17, ["项目", "金额/年数", "说明"], TEAL)
    cards = [
        (18, "工程费用", "='05投资估算'!F5", "表5第一部分"),
        (19, "建设投资", "=建设投资", "工程+二类+预备"),
        (20, "总投资（回收基准）", "=总投资", "含建设期利息与管理费"),
        (21, "贷款本金", "=贷款本金", "建设投资×80%"),
        (22, "经营期静态回收期（年）", "='18年财务'!C34", "目标≤3年"),
        (23, "第3–18年年均利润总额", "='18年财务'!C31", "目标≥3,000万"),
        (24, "达产年人力成本", "=人力编制!E{}".format(staff_sum_row), "编制一次计入，不按项目重复"),
    ]
    for r, name, formula, note in cards:
        txt(ws, r, 1, name, True)
        ws.cell(r, 2, formula)
        ws.cell(r, 2).number_format = "0.00"
        ws.cell(r, 2).fill = fill(GREEN_LT)
        ws.cell(r, 2).border = thin
        ws.cell(r, 2).font = font(bold=True)
        txt(ws, r, 3, note)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=10)

    # mix year 3
    ws.merge_cells("A26:J26")
    txt(ws, 26, 1, "达产年（第3年）收入结构", True, GREEN)
    ws.cell(26, 1).font = font(bold=True, color=WHITE)
    header_row(ws, 27, ["经营性质", "收入（万元）", "占比", "成本逻辑"], TEAL)
    txt(ws, 28, 1, "联营", True, ORANGE)
    ws.cell(28, 2, "='18年财务'!D8")
    txt(ws, 29, 1, "自营", True, PURPLE)
    ws.cell(29, 2, "='18年财务'!D9")
    txt(ws, 30, 1, "出租", True, BLUE_LT)
    ws.cell(30, 2, "='18年财务'!D10")
    txt(ws, 31, 1, "品牌加盟", True, "F9E79F")
    ws.cell(31, 2, "='18年财务'!D11")
    txt(ws, 32, 1, "合计", True, GREEN_LT)
    ws.cell(32, 2, "=SUM(B28:B31)")
    for r in range(28, 33):
        ws.cell(r, 2).number_format = "0.00"
        ws.cell(r, 2).border = thin
        ws.cell(r, 3, f"=IF($B$32=0,0,B{r}/$B$32)")
        ws.cell(r, 3).number_format = "0.0%"
        ws.cell(r, 3).border = thin
    txt(ws, 28, 4, "只计分成/保底租金，5–8%管理分摊")
    txt(ws, 29, 4, "货品+渠道+编制工资")
    txt(ws, 30, 4, "物业与空置约6–8%")
    txt(ws, 31, 4, "万达门票10%+26人+维护+二消成本")
    ws.merge_cells("D28:J28")
    ws.merge_cells("D29:J29")
    ws.merge_cells("D30:J30")
    ws.merge_cells("D31:J31")

    pie = PieChart()
    pie.title = "达产年收入结构"
    labels = Reference(ws, min_col=1, min_row=28, max_row=31)
    pdata = Reference(ws, min_col=2, min_row=27, max_row=31)
    pie.add_data(pdata, titles_from_data=True)
    pie.set_categories(labels)
    pie.dataLabels = DataLabelList()
    pie.dataLabels.showPercent = True
    pie.dataLabels.showVal = False
    pie.dataLabels.showCatName = True
    pie.width = 14
    pie.height = 8
    ws.add_chart(pie, "A34")

    ws.merge_cells("F34:J42")
    txt(
        ws,
        34,
        6,
        "结论：在不新增改造项目的前提下，表5总投资约4,578万元，建设期2年后开业。达产年起利润总额稳定在3,200万元以上，第3–18年年均超过3,000万元；经营期静态回收约1.6–1.8年。关键不是抬高客单，而是把联营项目从「假自营成本」纠正为分成口径，并激活已投资未计价的研学、夜游、花海、高尔夫、旅拍。",
        bg=GREEN_LT,
    )
    ws.row_dimensions[34].height = 20

    set_widths(ws, [26, 16, 14, 22, 28, 14, 12, 10, 28, 28])
    ws.freeze_panes = "A5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.print_title_rows = "1:4"

    # =====================================================================
    # 容量校验
    # =====================================================================
    ws = wb.create_sheet("容量校验")
    title_bar(ws, "容量与合理性校验｜达产年公园收入不得突破合理上限", 12)
    header_row(
        ws,
        4,
        ["经营项目", "容量单位", "容量", "日周转/场次", "年天数", "利用率", "客单(元)", "合理GMV上限", "公园分成", "公园收入上限", "达产目标", "目标/上限"],
        GREEN,
    )
    caps = [
        ("玉皇山大马戏", "座位", 600, 2, 240, 0.70, 62, 0.20),
        ("超级宝贝王", "年接待人次", 400000, 1, 1, 1.00, 48, 1.00),
        ("土特产伴手礼", "全园游客", 750000, 1, 1, 0.20, 55, 1.00),
        ("动物萌宠互动", "日接待", 350, 1, 220, 0.70, 25, 0.40),
        ("湖畔影院", "座位", 160, 2.2, 250, 0.70, 32, 0.60),
        ("青年街区", "经营面积㎡", 500, 1, 365, 0.95, 6.8, 1.00),
        ("茶屋氧吧", "座位", 160, 3.5, 330, 0.75, 80, 1.00),
        ("素食餐厅", "座位", 180, 3.5, 310, 0.80, 88, 0.20),
        ("庙会/市集", "摊位日", 60, 1, 40, 0.90, 1500, 1.00),
        ("婚礼花园", "经营日", 1, 1, 90, 0.80, 24000, 1.00),
        ("森林剧场", "座位", 300, 2, 200, 0.70, 58, 0.60),
        ("悬崖咖啡", "座位", 80, 4, 330, 0.75, 58, 0.20),
        ("树屋及星空露营", "单元夜", 40, 1, 180, 0.55, 280, 0.30),
        ("山洞酒庄", "日接待", 180, 1, 220, 0.45, 42, 1.00),
        ("公园旅拍", "摄影团队", 6, 3, 220, 0.75, 380, 0.40),
        ("园区交通", "车次服务", 8, 10, 280, 0.70, 12, 1.00),
        ("红色研学/VR展馆", "日学员", 400, 1, 180, 0.80, 80, 1.00),
        ("夜游/主题灯光", "单场容量", 400, 2, 180, 0.75, 38, 1.00),
        ("室内高尔夫", "日接待", 120, 1, 280, 0.50, 80, 0.30),
        ("花海摄影", "全园游客", 750000, 1, 1, 0.12, 18, 1.00),
        ("冬季抗联及戏雪", "日接待", 500, 1, 90, 0.55, 48, 0.35),
        ("栈道观景打卡", "全园游客", 750000, 1, 1, 0.10, 16, 1.00),
    ]
    # youth street: GMV上限用租金口径 area*daily*days
    for i, row in enumerate(caps, 5):
        name, unit, cap, turn, days, util, price, share = row
        txt(ws, i, 1, name)
        txt(ws, i, 2, unit)
        num(ws, i, 3, cap, "0")
        num(ws, i, 4, turn, "0.00")
        num(ws, i, 5, days, "0")
        num(ws, i, 6, util, "0.00%")
        num(ws, i, 7, price, "0.00")
        if name == "青年街区":
            ws.cell(i, 8, f"=C{i}*G{i}*E{i}*F{i}/10000")
        elif name == "婚礼花园":
            ws.cell(i, 8, f"=C{i}*D{i}*E{i}*F{i}*G{i}/10000")
        elif name == "庙会/市集":
            ws.cell(i, 8, f"=C{i}*D{i}*E{i}*F{i}*G{i}/10000")
        elif name == "超级宝贝王":
            ws.cell(i, 8, f"=C{i}*G{i}/10000+C{i}*0.32*18/10000")
        else:
            ws.cell(i, 8, f"=C{i}*D{i}*E{i}*F{i}*G{i}/10000")
        ws.cell(i, 8).number_format = "0.00"
        ws.cell(i, 8).border = thin
        ws.cell(i, 8).fill = fill(BLUE_LT)
        num(ws, i, 9, share, "0.00%")
        ws.cell(i, 10, f"=H{i}*I{i}")
        ws.cell(i, 10).number_format = "0.00"
        ws.cell(i, 10).border = thin
        ws.cell(i, 10).fill = fill(GREEN_LT)
        ws.cell(i, 11, f'=IFERROR(INDEX(收入测算!$F$5:$F$40,MATCH(A{i},收入测算!$B$5:$B$40,0)),0)')
        ws.cell(i, 11).number_format = "0.00"
        ws.cell(i, 11).border = thin
        ws.cell(i, 12, f"=IF(J{i}=0,0,K{i}/J{i})")
        ws.cell(i, 12).number_format = "0.0%"
        ws.cell(i, 12).border = thin
        ws.conditional_formatting.add(
            f"L{i}",
            CellIsRule(operator="greaterThan", formula=["1"], fill=fill(RED_LT)),
        )
        ws.conditional_formatting.add(
            f"L{i}",
            CellIsRule(operator="lessThanOrEqual", formula=["1"], fill=fill(GREEN_LT)),
        )
    last_cap = 4 + len(caps)
    txt(ws, last_cap + 2, 1, "目标/上限≤100%为合理。青年街区、婚礼、市集按租金/场次综合收入理解客单。茶屋上限含保底+餐饮流水，达产目标为租金+分成两行之和时请对照分项。", bg=YELLOW)
    ws.merge_cells(start_row=last_cap + 2, start_column=1, end_row=last_cap + 2, end_column=12)

    set_widths(ws, [20, 14, 12, 12, 10, 10, 12, 14, 12, 14, 12, 12])
    ws.freeze_panes = "A5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = "1:4"

    # =====================================================================
    # 口径说明
    # =====================================================================
    ws = wb.create_sheet("口径说明")
    title_bar(ws, "模型口径、与原表差异、使用限制", 6)
    header_row(ws, 4, ["序号", "主题", "采用口径", "可调整位置", "影响", "说明"], GREEN)
    caliber = [
        ("1", "投资基准", "完整复算表5，总投资≈4,578.46万元", "05投资估算", "改变回收期", "不含北入口、不含1.6亿经营权拍卖"),
        ("2", "人流基准", "第3年75万/85%/150元，第4–18年80万保底", "06人流模型B6:S8", "改变收入", "建设期人流为0，不套用原表1–2年"),
        ("3", "收入确认", "公园账面=分成/租金/自营全额/加盟流水", "业态参数", "改变利润", "不再把联营GMV当作公园收入后再扣一次分成"),
        ("4", "联营成本", "收入×（2%+1%+3%）量级", "业态参数Q-S列", "提高利润", "对方承担演职、厨务、店员"),
        ("5", "自营成本", "货品+渠道+编制工资", "业态参数+人力编制", "影响贡献", "礼品/交通/酒庄/婚礼/研学/夜游等"),
        ("6", "人力", "通化全包年薪，公共+自营+26人加盟", "人力编制C-D列", "影响贡献", "原10个月口径与联营固定人工已取消"),
        ("7", "宝贝王", "研学35元+一般48元，万达只分门票10%", "业态参数专项+宝贝王明细", "第一引擎", "接待封顶40万人"),
        ("8", "填充项目", "只激活表5已投资或表6已列空值", "业态参数「是否填充」", "补收入", "不新增改造运营项目"),
        ("9", "折旧", "总投资×95%/16年，经营期计提", "业态参数残值率", "影响利润", "建设期不提折旧"),
        ("10", "利息", "建设期资本化进总投资；经营期前10年等额本金", "05投资估算H62/H63", "影响利润", "还本不进利润，进现金流"),
        ("11", "所得税", "利润总额×25%，亏损不确认递延", "业态参数所得税率", "影响净利", "目标考核用利润总额"),
        ("12", "回收期", "经营期静态：累计（净利+折旧）≥总投资", "18年财务C34", "决策指标", "含建设期的累计转正约在第4年"),
        ("13", "动物成本", "既有55只饲料医疗+4名保育员", "人力+公共参数", "刚性成本", "理解玉皇山动物园后必须保留"),
        ("14", "无硬件增收", "夜游/研学/旅拍/观景已嵌入项目", "收入测算", "不可再加总", "避免与5,000万旧目标重复计算"),
    ]
    for i, row in enumerate(caliber, 5):
        for j, v in enumerate(row, 1):
            txt(ws, i, j, v)
        ws.row_dimensions[i].height = 28
    ws.merge_cells("A20:F22")
    txt(
        ws,
        20,
        1,
        "与原《经营收入与成本测算模型》的主要差异：原表把表6第1年2,972万元当作公园收入，却对马戏、餐厅、茶屋等联营项目再套自营成本率+高额固定人工，经营贡献被系统性压低，且未接入表5总投资、没有18年回收与建设期。本重构把成本结构按经营性质重做，收入向表6人流模型靠拢，并补齐已投资未计价设施。黄色参数修改后，经营总览与18年财务会联动更新。",
        bg=GRAY,
    )
    set_widths(ws, [8, 16, 42, 24, 14, 36])
    ws.freeze_panes = "A5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.print_title_rows = "1:4"

    # print extras / freeze already set
    # sheet order
    order = [
        "封面说明",
        "经营总览",
        "05投资估算",
        "06人流模型",
        "业态参数",
        "人力编制",
        "收入测算",
        "宝贝王明细",
        "成本利润",
        "18年财务",
        "容量校验",
        "口径说明",
    ]
    for i, name in enumerate(order):
        wb.move_sheet(name, offset=i - wb.sheetnames.index(name))

    # freeze + tab colors
    colors = {
        "封面说明": GREEN_DK,
        "经营总览": GOLD,
        "05投资估算": GREEN,
        "06人流模型": "1D3557",
        "业态参数": "E67E22",
        "人力编制": "8E44AD",
        "收入测算": TEAL,
        "宝贝王明细": "B7950B",
        "成本利润": "C0392B",
        "18年财务": GREEN_DK,
        "容量校验": "2980B9",
        "口径说明": "7F8C8D",
    }
    for name, col in colors.items():
        wb[name].sheet_properties.tabColor = col

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print("WROTE", OUT)
    return OUT


if __name__ == "__main__":
    build()
