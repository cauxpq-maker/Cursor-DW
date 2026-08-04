# -*- coding: utf-8 -*-
"""
「鸭绿江·1950」一期客流与收入测算模型(Excel,公式联动可编辑)
运行: python3 build_phase1_model.py
"""
import xlsxwriter

OUT = "鸭绿江1950一期测算模型.xlsx"
wb = xlsxwriter.Workbook(OUT)

# ---------- 格式 ----------
F_TITLE = wb.add_format({"font_name": "微软雅黑", "font_size": 16, "bold": True, "font_color": "#C4533C"})
F_H = wb.add_format({"font_name": "微软雅黑", "font_size": 11, "bold": True, "font_color": "#FFFFFF",
                     "bg_color": "#C4533C", "border": 1, "align": "center", "valign": "vcenter"})
F_SUB = wb.add_format({"font_name": "微软雅黑", "font_size": 11, "bold": True, "bg_color": "#F3EBDB",
                       "border": 1, "valign": "vcenter"})
F_TXT = wb.add_format({"font_name": "微软雅黑", "font_size": 10.5, "border": 1, "valign": "vcenter"})
F_TXTW = wb.add_format({"font_name": "微软雅黑", "font_size": 10.5, "border": 1, "valign": "vcenter", "text_wrap": True})
F_IN = wb.add_format({"font_name": "微软雅黑", "font_size": 10.5, "bg_color": "#FFF3C4", "border": 1,
                      "align": "center", "valign": "vcenter", "num_format": "#,##0"})
F_INP = wb.add_format({"font_name": "微软雅黑", "font_size": 10.5, "bg_color": "#FFF3C4", "border": 1,
                       "align": "center", "valign": "vcenter", "num_format": "0.0%"})
F_INY = wb.add_format({"font_name": "微软雅黑", "font_size": 10.5, "bg_color": "#FFF3C4", "border": 1,
                       "align": "center", "valign": "vcenter", "num_format": "#,##0.0"})
F_NUM = wb.add_format({"font_name": "微软雅黑", "font_size": 10.5, "border": 1, "align": "center",
                       "valign": "vcenter", "num_format": "#,##0"})
F_NUM1 = wb.add_format({"font_name": "微软雅黑", "font_size": 10.5, "border": 1, "align": "center",
                        "valign": "vcenter", "num_format": "#,##0.0"})
F_PCT = wb.add_format({"font_name": "微软雅黑", "font_size": 10.5, "border": 1, "align": "center",
                       "valign": "vcenter", "num_format": "0.0%"})
F_RES = wb.add_format({"font_name": "微软雅黑", "font_size": 11, "bold": True, "bg_color": "#E9F0EE",
                       "border": 1, "align": "center", "valign": "vcenter", "num_format": "#,##0"})
F_RES1 = wb.add_format({"font_name": "微软雅黑", "font_size": 11, "bold": True, "bg_color": "#E9F0EE",
                        "border": 1, "align": "center", "valign": "vcenter", "num_format": "#,##0.0"})
F_NOTE = wb.add_format({"font_name": "微软雅黑", "font_size": 9.5, "font_color": "#8A8276", "text_wrap": True})

# ============ 00 使用说明 ============
ws = wb.add_worksheet("00_使用说明")
ws.set_column("A:A", 100)
ws.write("A1", "「鸭绿江·1950」红色文旅城一期 —— 客流与收入测算模型", F_TITLE)
notes = [
    "",
    "■ 使用方法",
    "1. 只需修改「01_假设」中黄色底色的单元格(客流、票价、转化率、人均消费、成本、投资等参数);",
    "2. 「02_收入测算」「03_成本与利润」「04_月度客流」「05_敏感性」全部由公式联动,自动重算;",
    "3. 三列并行呈现保守/基准/乐观三个客流情景,便于对比;",
    "",
    "■ 模型口径",
    "· 测算年份口径为「稳定运营年」(开业第3年);开业首年建议按基准情景×70%爬坡系数理解;",
    "· 本模型为概念阶段测算(精度±30%),用于投资决策的方向性判断,非施工图预算;",
    "· 收入按一期业态口径(日场演艺/小剧场/餐饮商业/文创/研学/其他),夜演大剧场与酒店属二期,未计入;",
    "· 餐饮商业收入指小镇获得的租金+流水抽成口径,非商户流水;",
    "",
    "■ 关键锚点(外部参照)",
    "· 遵义1935街区(免门票):单月客流120万人次(2025年7月);",
    "· 延安红街:开业首月200万人次;",
    "· 丹东2025年春节假期全市客流424万人次,断桥景区2026年元旦客流同比+102%。",
]
for i, t in enumerate(notes, start=2):
    ws.write(i, 0, t, F_NOTE if not t.startswith("■") else F_SUB)

# ============ 01 假设 ============
ws = wb.add_worksheet("01_假设")
ws.set_column("A:A", 30)
ws.set_column("B:D", 14)
ws.set_column("E:E", 46)
ws.write("A1", "01 假设参数(黄色单元格可修改)", F_TITLE)

ws.write_row("A3", ["A. 年客流情景(人次/年)", "保守", "基准", "乐观"], F_H)
ws.write("E3", "说明", F_H)
ws.write("A4", "稳定年入园客流", F_TXT)
ws.write("B4", 600000, F_IN); ws.write("C4", 1000000, F_IN); ws.write("D4", 1500000, F_IN)
ws.write("E4", "基准=城市旗舰锚定率约15%口径;对标遵义1935单月120万的1/14强度", F_TXTW)

ws.write_row("A6", ["B. 转化率与价格", "数值", "", ""], F_H)
ws.write("E6", "说明", F_H)
params_b = [
    ("日场《抢渡鸭绿江》观演转化率", 0.35, F_INP, "入园客流中购票观演比例"),
    ("日场票价(元/人)", 80, F_IN, "对标同类实景演艺80–128元区间下沿"),
    ("小剧场观演转化率", 0.25, F_INP, "多剧场轮演,通票含1场后加购"),
    ("小剧场平均票价(元/人)", 40, F_IN, "单场30–50元"),
    ("研学客群占比", 0.06, F_INP, "研学人次占总客流比例"),
    ("研学课程客单价(元/人)", 150, F_IN, "半日课程口径"),
    ("餐饮商业人均贡献(元/人)", 18, F_IN, "小镇租金+流水抽成口径(约合商户流水的20%)"),
    ("文创零售人均贡献(元/人)", 8, F_IN, "自营+联营毛贡献"),
    ("停车交通及其他人均(元/人)", 4, F_IN, ""),
]
r = 6
for name, val, fmt, note in params_b:
    ws.write(r, 0, name, F_TXT)
    ws.write(r, 1, val, fmt)
    ws.write(r, 4, note, F_TXTW)
    r += 1

ws.write_row(f"A{r+2}", ["C. 成本参数", "数值", "", ""], F_H)
ws.write(f"E{r+2}", "说明", F_H)
row_c0 = r + 2
cost_params = [
    ("年固定成本(万元)", 4400, F_IN, "演职员+运营团队薪酬、物业能耗基础值、管理费用"),
    ("变动成本率(占收入)", 0.15, F_INP, "随客流变动的耗材、能耗增量、佣金渠道费等"),
]
r = row_c0
for name, val, fmt, note in cost_params:
    ws.write(r, 0, name, F_TXT)
    ws.write(r, 1, val, fmt)
    ws.write(r, 4, note, F_TXTW)
    r += 1

ws.write_row(f"A{r+2}", ["D. 投资参数", "数值", "", ""], F_H)
ws.write(f"E{r+2}", "说明", F_H)
row_d0 = r + 2
ws.write(row_d0, 0, "一期总投资(万元)", F_TXT)
ws.write(row_d0, 1, 31000, F_IN)
ws.write(row_d0, 4, "详见报告投资估算表;概念级估算±30%", F_TXTW)

# 命名引用(便于公式可读):使用绝对地址
A = {
    "flow_c": "'01_假设'!$B$4", "flow_b": "'01_假设'!$C$4", "flow_o": "'01_假设'!$D$4",
    "conv_day": "'01_假设'!$B$7", "p_day": "'01_假设'!$B$8",
    "conv_thr": "'01_假设'!$B$9", "p_thr": "'01_假设'!$B$10",
    "conv_edu": "'01_假设'!$B$11", "p_edu": "'01_假设'!$B$12",
    "pp_food": "'01_假设'!$B$13", "pp_retail": "'01_假设'!$B$14", "pp_other": "'01_假设'!$B$15",
    "fixed": f"'01_假设'!$B${row_c0+1}", "varr": f"'01_假设'!$B${row_c0+2}",
    "capex": f"'01_假设'!$B${row_d0+1}",
}

# python 侧同步计算缓存值
V = {"flow": [600000, 1000000, 1500000], "conv_day": 0.35, "p_day": 80, "conv_thr": 0.25,
     "p_thr": 40, "conv_edu": 0.06, "p_edu": 150, "pp_food": 18, "pp_retail": 8, "pp_other": 4,
     "fixed": 4400, "varr": 0.15, "capex": 31000}

# ============ 02 收入测算 ============
ws = wb.add_worksheet("02_收入测算")
ws.set_column("A:A", 26)
ws.set_column("B:D", 15)
ws.set_column("E:E", 40)
ws.write("A1", "02 收入测算(万元/年,稳定年)", F_TITLE)
ws.write_row("A3", ["收入科目", "保守", "基准", "乐观"], F_H)
ws.write("E3", "公式口径", F_H)
flows = ["flow_c", "flow_b", "flow_o"]
rev_rows = [
    ("日场《抢渡鸭绿江》演艺", lambda f: f"={A[f]}*{A['conv_day']}*{A['p_day']}/10000",
     lambda fv: fv * V["conv_day"] * V["p_day"] / 10000, "客流×观演转化率×票价"),
    ("小剧场群", lambda f: f"={A[f]}*{A['conv_thr']}*{A['p_thr']}/10000",
     lambda fv: fv * V["conv_thr"] * V["p_thr"] / 10000, "客流×转化率×均价"),
    ("餐饮商业(租金+抽成)", lambda f: f"={A[f]}*{A['pp_food']}/10000",
     lambda fv: fv * V["pp_food"] / 10000, "客流×人均贡献"),
    ("文创零售", lambda f: f"={A[f]}*{A['pp_retail']}/10000",
     lambda fv: fv * V["pp_retail"] / 10000, "客流×人均贡献"),
    ("研学课程", lambda f: f"={A[f]}*{A['conv_edu']}*{A['p_edu']}/10000",
     lambda fv: fv * V["conv_edu"] * V["p_edu"] / 10000, "客流×研学占比×客单价"),
    ("停车交通及其他", lambda f: f"={A[f]}*{A['pp_other']}/10000",
     lambda fv: fv * V["pp_other"] / 10000, "客流×人均"),
]
r = 3
for name, fx, calc, note in rev_rows:
    ws.write(r, 0, name, F_TXT)
    for ci, f in enumerate(flows):
        ws.write_formula(r, 1 + ci, fx(f), F_NUM, calc(V["flow"][ci]))
    ws.write(r, 4, note, F_TXTW)
    r += 1
ws.write(r, 0, "收入合计", F_SUB)
for ci in range(3):
    col = chr(ord("B") + ci)
    total = sum(calc(V["flow"][ci]) for _, _, calc, _ in rev_rows)
    ws.write_formula(r, 1 + ci, f"=SUM({col}4:{col}{r})", F_RES, total)
ws.write(r, 4, "", F_TXT)
row_rev_total = r + 1  # 1-based
r += 1
ws.write(r, 0, "人均综合收入(元/人次)", F_TXT)
for ci, f in enumerate(flows):
    col = chr(ord("B") + ci)
    val = sum(calc(V["flow"][ci]) for _, _, calc, _ in rev_rows) * 10000 / V["flow"][ci]
    ws.write_formula(r, 1 + ci, f"={col}{row_rev_total}*10000/{A[f]}", F_NUM1, val)
ws.write(r, 4, "收入合计÷客流", F_TXTW)

# ============ 03 成本与利润 ============
ws = wb.add_worksheet("03_成本与利润")
ws.set_column("A:A", 26)
ws.set_column("B:D", 15)
ws.set_column("E:E", 44)
ws.write("A1", "03 成本与利润(万元/年,稳定年)", F_TITLE)
ws.write_row("A3", ["科目", "保守", "基准", "乐观"], F_H)
ws.write("E3", "公式口径", F_H)
rev_ref = [f"'02_收入测算'!{c}{row_rev_total}" for c in "BCD"]
rev_val = [sum(calc(V["flow"][ci]) for _, _, calc, _ in rev_rows) for ci in range(3)]
rows3 = [
    ("收入合计", [f"={rev_ref[i]}" for i in range(3)], rev_val, F_NUM, "引自02表"),
    ("变动成本", [f"={rev_ref[i]}*{A['varr']}" for i in range(3)],
     [v * V["varr"] for v in rev_val], F_NUM, "收入×变动成本率"),
    ("固定成本", [f"={A['fixed']}"] * 3, [V["fixed"]] * 3, F_NUM, "演职员/运营/物业/管理"),
    ("EBITDA", [f"=B4-B5-B6", f"=C4-C5-C6", f"=D4-D5-D6"],
     [rev_val[i] * (1 - V["varr"]) - V["fixed"] for i in range(3)], F_RES, "收入-变动-固定"),
    ("EBITDA率", [f"=B7/B4", f"=C7/C4", f"=D7/D4"],
     [(rev_val[i] * (1 - V["varr"]) - V["fixed"]) / rev_val[i] for i in range(3)], F_PCT, ""),
    ("一期投资回收期(年)", [f'=IF(B7<=0,"—",{A["capex"]}/B7)', f'=IF(C7<=0,"—",{A["capex"]}/C7)',
                            f'=IF(D7<=0,"—",{A["capex"]}/D7)'],
     [("—" if (rev_val[i] * (1 - V["varr"]) - V["fixed"]) <= 0
       else V["capex"] / (rev_val[i] * (1 - V["varr"]) - V["fixed"])) for i in range(3)], F_RES1,
     "总投资÷EBITDA(简单口径,未计二期与土地增值);EBITDA为负显示「—」"),
]
r = 3
for name, fxs, vals, fmt, note in rows3:
    ws.write(r, 0, name, F_TXT if fmt not in (F_RES, F_RES1) else F_SUB)
    for ci in range(3):
        v = vals[ci]
        ws.write_formula(r, 1 + ci, fxs[ci], fmt, round(v, 4) if isinstance(v, (int, float)) else v)
    ws.write(r, 4, note, F_TXTW)
    r += 1
r += 1
ws.write(r, 0, "盈亏平衡客流(万人次/年)", F_SUB)
pp_rev = rev_val[1] * 10000 / V["flow"][1]
be = V["fixed"] * 10000 / (pp_rev * (1 - V["varr"])) / 10000
ws.write_formula(r, 1, f"={A['fixed']}*10000/('02_收入测算'!C{row_rev_total+1}*(1-{A['varr']}))/10000",
                 F_RES1, round(be, 2))
ws.write(r, 4, "固定成本÷人均边际贡献(按基准情景人均收入)", F_TXTW)

# ============ 04 月度客流 ============
ws = wb.add_worksheet("04_月度客流")
ws.set_column("A:A", 14)
ws.set_column("B:N", 10)
ws.write("A1", "04 月度客流分布(基准情景)", F_TITLE)
months = [f"{i}月" for i in range(1, 13)]
share = [0.04, 0.06, 0.05, 0.07, 0.10, 0.10, 0.14, 0.14, 0.10, 0.10, 0.05, 0.05]
ws.write_row("A3", ["月份"] + months + ["合计"], F_H)
ws.write("A4", "占比(可改)", F_TXT)
for i, sv in enumerate(share):
    ws.write(3, 1 + i, sv, F_INP)
ws.write_formula(3, 13, "=SUM(B4:M4)", F_PCT, 1.0)
ws.write("A5", "客流(万人次)", F_TXT)
for i in range(12):
    col = chr(ord("B") + i)
    ws.write_formula(4, 1 + i, f"={A['flow_b']}*{col}4/10000", F_NUM1,
                     round(V["flow"][1] * share[i] / 10000, 1))
ws.write_formula(4, 13, "=SUM(B5:M5)", F_RES1, V["flow"][1] / 10000)
ws.write("A7", "日均(万人次/日)", F_TXT)
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
for i in range(12):
    col = chr(ord("B") + i)
    ws.write_formula(6, 1 + i, f"={col}5/{days[i]}", wb.add_format(
        {"font_name": "微软雅黑", "font_size": 10.5, "border": 1, "align": "center",
         "num_format": "0.00"}), round(V["flow"][1] * share[i] / 10000 / days[i], 2))
ws.write("A9", "说明:7–8月暑期与5/10月假期为高峰;冬季(11–2月)靠室内小剧场+温泉+「1950年的冬天」主题支撑,占比20%。", F_NOTE)

# ============ 05 敏感性 ============
ws = wb.add_worksheet("05_敏感性")
ws.set_column("A:A", 24)
ws.set_column("B:F", 13)
ws.write("A1", "05 敏感性分析:EBITDA(万元)", F_TITLE)
ws.write("A3", "客流(万人次)↓ / 人均综合收入(元)→", F_H)
pps = [60, 77, 95]
flows_s = [60, 80, 100, 120, 150]
for j, pp in enumerate(pps):
    ws.write(2, 1 + j, pp, F_IN)
for i, fl in enumerate(flows_s):
    ws.write(3 + i, 0, fl, F_IN)
    for j, pp in enumerate(pps):
        colL = chr(ord("B") + j)
        fx = f"=$A{4+i}*{colL}$3*(1-{A['varr']})-{A['fixed']}"
        val = fl * pp * (1 - V["varr"]) - V["fixed"]
        ws.write_formula(3 + i, 1 + j, fx, F_NUM, round(val, 0))
ws.write("A10", "读法:行=年客流,列=人均综合收入;绿色区间为正EBITDA。基准点(100万×77元)EBITDA约2,145万元。", F_NOTE)
ws.conditional_format(3, 1, 7, 3, {"type": "3_color_scale", "min_color": "#F4CCCC",
                                   "mid_color": "#FFF3C4", "max_color": "#D9EAD3"})

wb.close()
print("saved:", OUT)
