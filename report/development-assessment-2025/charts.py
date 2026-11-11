# -*- coding: utf-8 -*-
"""生成《中国近二十年发展评估与国际比较报告》全部图表。

数据输入（均在 data/ 目录）：
- china_annual.csv            国家统计局公报/统计年鉴/财政部（build_china_annual.py 生成）
- worldbank_wdi.csv           世界银行 WDI（fetch_worldbank.py）
- imf_weo_oct2026.csv         IMF WEO 2026 年 10 月版（fetch_imf_weo.py）
- un_wpp2024_six_countries.csv 联合国 WPP2024 中方案（fetch_un_wpp.py）
- elderly_care_beds.csv       民政部历年统计公报/国家老龄事业发展公报
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "charts")
os.makedirs(OUT, exist_ok=True)

for p in [os.path.expanduser("~/.fonts/NotoSansCJKsc-Regular.otf"),
          os.path.expanduser("~/.fonts/NotoSansCJKsc-Bold.otf"),
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
          "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"]:
    if os.path.exists(p):
        font_manager.fontManager.addfont(p)
plt.rcParams["font.family"] = ["Noto Sans CJK SC", "WenQuanYi Micro Hei", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

C = ["CHN", "JPN", "KOR", "VNM", "MYS", "IND"]
NAME = {"CHN": "中国", "JPN": "日本", "KOR": "韩国", "VNM": "越南", "MYS": "马来西亚", "IND": "印度"}
COL = {"CHN": "#c0392b", "JPN": "#1f4e79", "KOR": "#2e86c1", "VNM": "#27ae60", "MYS": "#f39c12", "IND": "#8e44ad"}
BLUE, RED, GRAY, AMBER, GREEN = "#2563eb", "#dc2626", "#64748b", "#d97706", "#059669"

cn = pd.read_csv(os.path.join(DATA, "china_annual.csv")).set_index("year")
wb = pd.read_csv(os.path.join(DATA, "worldbank_wdi.csv"))
imf = pd.read_csv(os.path.join(DATA, "imf_weo_oct2026.csv"))
un = pd.read_csv(os.path.join(DATA, "un_wpp2024_six_countries.csv"))
beds = pd.read_csv(os.path.join(DATA, "elderly_care_beds.csv"))


def piv(df, ind):
    return df[df.indicator == ind].pivot(index="year", columns="country", values="value").reindex(columns=C)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=170)
    plt.close(fig)


def src(ax, text):
    ax.text(0, -0.16, text, transform=ax.transAxes, fontsize=8, color=GRAY, va="top")


# ---------- 图1 中国 GDP、社零、CPI ----------
def fig01():
    d = cn.loc[2005:2025]
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.bar(d.index, d.retail_growth_pct, color="#bfdbfe", width=0.7, label="社会消费品零售总额名义增速")
    ax.plot(d.index, d.gdp_growth_pct, color=RED, lw=2.2, marker="o", ms=4, label="GDP 实际增速")
    ax.plot(d.index, d.cpi_pct, color=GRAY, lw=1.8, marker="s", ms=3.5, label="CPI 涨幅")
    ax.axhline(0, color="#0f172a", lw=0.8)
    ax.scatter([2026], [1.1], color=BLUE, marker="D", zorder=5)
    ax.annotate("2026年1-9月\n社零 +1.1%，GDP +4.6%，CPI +0.9%", xy=(2026, 1.1), xytext=(2021.3, 17.5),
                fontsize=8.5, color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
    for x, y in zip(d.index, d.gdp_growth_pct):
        ax.text(x, y + 0.6, f"{y:g}", ha="center", fontsize=7.5, color=RED)
    ax.set_xticks(list(range(2005, 2027)))
    ax.set_xticklabels([str(y) for y in range(2005, 2026)] + ["26Q1-3"], rotation=45, fontsize=8.5)
    ax.set_ylabel("同比增长（%）")
    ax.set_ylim(-5, 24)
    ax.set_title("图1  中国 2005—2025 年 GDP 实际增速、社会消费品零售总额名义增速与 CPI", fontsize=12, pad=10)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    src(ax, "数据来源：国家统计局历年《国民经济和社会发展统计公报》；2026 年为前三季度数据。")
    save(fig, "fig01_china_gdp_retail_cpi.png")


# ---------- 图2 消费占比 ----------
def fig02():
    d = cn.loc[2005:2025]
    hh = piv(wb, "hh_consumption_pct_gdp")["CHN"].loc[2005:2024]
    fig, ax = plt.subplots(figsize=(10, 4.4))
    ax.plot(d.index, d.retail_to_gdp_pct, color=BLUE, lw=2.2, marker="o", ms=4, label="社会消费品零售总额 / GDP（国家统计局口径）")
    ax.plot(hh.index, hh.values, color=AMBER, lw=2.2, marker="s", ms=4, label="居民最终消费支出 / GDP（世界银行口径）")
    ax.fill_between(d.index, d.retail_to_gdp_pct, hh.reindex(d.index).ffill(), color="#f1f5f9")
    ax.set_ylim(25, 50)
    ax.set_ylabel("占 GDP 比重（%）")
    ax.set_xticks(range(2005, 2026, 2))
    ax.set_title("图2  中国消费占 GDP 比重：社零口径 vs 居民最终消费口径（2005—2025）", fontsize=12, pad=10)
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    ax.annotate("2015-2017 年社零/GDP 见顶（约 43%）\n此后回落至 36% 左右", xy=(2016, 43.7), xytext=(2007.5, 46.5),
                fontsize=8.5, arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))
    src(ax, "数据来源：国家统计局（社零为公报当年初步数，GDP 为年鉴修订数）；世界银行 WDI（NE.CON.PRVT.ZS）。")
    save(fig, "fig02_china_consumption_share.png")


# ---------- 图3 出口 ----------
def fig03():
    d = cn.loc[2005:2025]
    fig, ax = plt.subplots(figsize=(10, 4.6))
    colors = [BLUE if v >= 0 else RED for v in d.exports_growth_pct]
    ax.bar(d.index, d.exports_growth_pct, color=colors, width=0.7, label="货物出口同比增速（左轴）")
    ax.axhline(0, color="#0f172a", lw=0.8)
    ax.set_ylabel("出口同比增速（%）")
    ax.set_ylim(-20, 40)
    ax2 = ax.twinx()
    ax2.plot(d.index, d.exports_to_gdp_pct, color=AMBER, lw=2.4, marker="o", ms=4, label="货物出口 / GDP（右轴）")
    ax2.set_ylabel("货物出口 / GDP（%）", color=AMBER)
    ax2.set_ylim(10, 40)
    ax2.spines["right"].set_visible(True)
    ax.scatter([2026], [16.4], color=GREEN, marker="D", zorder=5)
    ax.annotate("2026年1-9月出口 +16.4%", xy=(2026, 16.4), xytext=(2020.5, 30), fontsize=8.5, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.8))
    ax.set_xticks(list(range(2005, 2027)))
    ax.set_xticklabels([str(y) for y in range(2005, 2026)] + ["26Q1-3"], rotation=45, fontsize=8.5)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=9, loc="upper right")
    ax.set_title("图3  中国货物出口：增速与出口依存度（2005—2025）", fontsize=12, pad=10)
    src(ax, "数据来源：国家统计局公报（2005-2013 年增速按美元计价，2014 年起按人民币计价）；出口额按海关人民币口径 / 年鉴修订 GDP。")
    save(fig, "fig03_china_exports.png")


# ---------- 图4 宏观税负 ----------
def fig04():
    d = cn.loc[2005:2025]
    gg = piv(imf, "gen_gov_revenue_pct_gdp")["CHN"].loc[2005:2025]
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(d.index, d.tax_to_gdp_pct, color=RED, lw=2.4, marker="o", ms=4, label="税收收入 / GDP（小口径）")
    ax.plot(d.index, d.fiscal_revenue_to_gdp_pct, color=BLUE, lw=2.2, marker="s", ms=4, label="一般公共预算收入 / GDP（中口径）")
    b = d.broad_revenue_to_gdp_pct.dropna()
    ax.plot(b.index, b.values, color=AMBER, lw=2.2, marker="^", ms=4.5,
            label="一般公共预算+土地出让+社保基金收入 / GDP（宽口径，含财政补贴重复计算）")
    ax.plot(gg.index, gg.values, color=GRAY, lw=1.6, ls="--", label="IMF 广义政府收入 / GDP（国际可比口径）")
    for x in [2012, 2025]:
        ax.annotate(f"{d.loc[x, 'tax_to_gdp_pct']:.1f}%", xy=(x, d.loc[x, "tax_to_gdp_pct"]),
                    xytext=(0, -14), textcoords="offset points", ha="center", fontsize=8.5, color=RED)
    ax.annotate(f"{b.max():.1f}%（2018）", xy=(2018, b.max()), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8.5, color=AMBER)
    ax.annotate(f"{b.loc[2025]:.1f}%", xy=(2025, b.loc[2025]), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8.5, color=AMBER)
    ax.set_ylim(8, 40)
    ax.set_ylabel("占 GDP 比重（%）")
    ax.set_xticks(range(2005, 2026, 2))
    ax.set_title("图4  中国宏观税负的三种口径（2005—2025）", fontsize=12, pad=10)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    src(ax, "数据来源：《中国统计年鉴 2025》表 3-1/7-1/7-4/24-24，财政部历年财政决算与《2025 年财政收支情况》，IMF WEO（2026 年 10 月）。")
    save(fig, "fig04_china_tax_burden.png")


# ---------- 图5 2025 税收结构 ----------
def fig05():
    items = [
        ("国内增值税", 68947), ("企业所得税", 41304), ("土地和房地产相关税收*", 17725), ("进口环节增值税与消费税", 18268),
        ("国内消费税", 16857), ("个人所得税", 16187), ("城市维护建设税", 5170), ("印花税", 4270), ("资源税", 2949),
        ("关税", 2370), ("车辆购置税", 1972), ("其他税种", 1848), ("出口退税（冲减）", -21337),
    ]
    items_sorted = sorted(items, key=lambda x: x[1])
    labels = [i[0] for i in items_sorted]; vals = [i[1] for i in items_sorted]
    total = 176369
    fig, ax = plt.subplots(figsize=(10, 5.2))
    colors = [RED if v < 0 else (AMBER if "土地" in l else BLUE) for l, v in zip(labels, vals)]
    ax.barh(labels, vals, color=colors, height=0.65)
    for i, v in enumerate(vals):
        ax.text(v + (800 if v > 0 else -800), i, f"{v:,.0f}亿元（{v / total * 100:.1f}%）", va="center",
                ha="left" if v > 0 else "right", fontsize=8.5)
    ax.axvline(0, color="#0f172a", lw=0.8)
    ax.set_xlim(-32000, 95000)
    ax.set_xlabel("亿元（占税收收入合计 176,369 亿元的比重）")
    ax.set_title("图5  2025 年中国税收收入结构：以增值税和企业所得税为主的间接税体系", fontsize=12, pad=10)
    src(ax, "数据来源：财政部《2025 年全国一般公共预算收入决算表》。*土地和房地产相关税收 = 房产税+契税+土地增值税+城镇土地使用税+耕地占用税。")
    save(fig, "fig05_china_tax_structure_2025.png")


# ---------- 图6 六国 GDP 增速分期 ----------
def fig06():
    g = piv(imf, "real_gdp_growth_pct")
    periods = [(2005, 2010), (2011, 2015), (2016, 2019), (2020, 2025)]
    fig, ax = plt.subplots(figsize=(10, 4.8))
    w = 0.13
    x = np.arange(len(periods))
    for i, c in enumerate(C):
        vals = [g.loc[a:b, c].mean() for a, b in periods]
        ax.bar(x + (i - 2.5) * w, vals, width=w, color=COL[c], label=NAME[c])
        for xi, v in zip(x + (i - 2.5) * w, vals):
            ax.text(xi, v + 0.15, f"{v:.1f}", ha="center", fontsize=7.5)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{a}—{b}" for a, b in periods], fontsize=10)
    ax.set_ylabel("年均实际 GDP 增速（%）")
    ax.set_title("图6  六国分阶段年均 GDP 实际增速对比（2005—2025）", fontsize=12, pad=10)
    ax.legend(frameon=False, fontsize=9, ncol=6, loc="upper right")
    ax.set_ylim(0, 13)
    src(ax, "数据来源：IMF World Economic Outlook（2026 年 10 月），NGDP_RPCH；2025 年为估计值。")
    save(fig, "fig06_six_gdp_growth_periods.png")


# ---------- 图7 人均 GDP ----------
def fig07():
    g = piv(imf, "gdp_per_capita_usd").loc[2005:2025]
    fig, ax = plt.subplots(figsize=(10, 4.8))
    for c in C:
        ax.plot(g.index, g[c], color=COL[c], lw=2.4 if c == "CHN" else 1.8, label=NAME[c])
        ax.text(2025.3, g.loc[2025, c], f"{NAME[c]} {g.loc[2025, c] / 1000:.1f}k", fontsize=8.5, va="center", color=COL[c])
    ax.set_yscale("log")
    ax.set_yticks([500, 1000, 2000, 5000, 10000, 20000, 40000])
    ax.set_yticklabels(["500", "1,000", "2,000", "5,000", "10,000", "20,000", "40,000"])
    ax.set_ylabel("人均 GDP（现价美元，对数坐标）")
    ax.set_xlim(2005, 2028.5)
    ax.set_title("图7  六国人均 GDP 轨迹（2005—2025，现价美元）", fontsize=12, pad=10)
    ax.legend(frameon=False, fontsize=9, loc="upper left", ncol=2)
    ax.annotate("中国 2005 年人均 GDP 为日本的 1/22，\n2025 年追至马来西亚水平、约为日韩的 38%",
                xy=(2025, 13970), xytext=(2011, 22000), fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))
    src(ax, "数据来源：IMF World Economic Outlook（2026 年 10 月），NGDPDPC。")
    save(fig, "fig07_six_gdp_per_capita.png")


# ---------- 图8 消费对比 ----------
def fig08():
    share = piv(wb, "hh_consumption_pct_gdp")
    growth = piv(wb, "hh_consumption_real_growth_pct")
    periods = [(2005, 2010), (2011, 2015), (2016, 2019), (2020, 2024)]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw=dict(width_ratios=[1, 1.35]))
    x = np.arange(len(C)); w = 0.38
    a1.bar(x - w / 2, [share.loc[2005, c] for c in C], width=w, color="#94a3b8", label="2005")
    a1.bar(x + w / 2, [share.loc[2024, c] for c in C], width=w, color=[COL[c] for c in C], label="2024")
    for i, c in enumerate(C):
        a1.text(i - w / 2, share.loc[2005, c] + 0.8, f"{share.loc[2005, c]:.0f}", ha="center", fontsize=8)
        a1.text(i + w / 2, share.loc[2024, c] + 0.8, f"{share.loc[2024, c]:.0f}", ha="center", fontsize=8)
    a1.set_xticks(x); a1.set_xticklabels([NAME[c] for c in C], fontsize=9)
    a1.set_ylabel("居民最终消费支出 / GDP（%）"); a1.set_ylim(0, 75)
    a1.set_title("(a) 居民消费率：2005 vs 2024", fontsize=10.5)
    a1.legend(frameon=False, fontsize=8.5)
    w2 = 0.13; x2 = np.arange(len(periods))
    for i, c in enumerate(C):
        vals = [growth.loc[a:b, c].mean() for a, b in periods]
        a2.bar(x2 + (i - 2.5) * w2, vals, width=w2, color=COL[c], label=NAME[c])
    a2.axhline(0, color="#0f172a", lw=0.8)
    a2.set_xticks(x2); a2.set_xticklabels([f"{a}—{b}" for a, b in periods], fontsize=9)
    a2.set_ylabel("居民消费实际增速年均（%）")
    a2.set_title("(b) 居民实际消费增速：分阶段年均", fontsize=10.5)
    a2.legend(frameon=False, fontsize=8, ncol=3, loc="upper right")
    fig.suptitle("图8  六国居民消费：消费率偏低但增速领先的“中国式消费结构”", fontsize=12)
    src(a1, "数据来源：世界银行 WDI，NE.CON.PRVT.ZS 与 NE.CON.PRVT.KD.ZG。")
    save(fig, "fig08_six_consumption.png")


# ---------- 图9 CPI ----------
def fig09():
    p = piv(imf, "inflation_avg_pct").loc[2005:2025]
    fig, ax = plt.subplots(figsize=(10, 4.6))
    for c in C:
        ax.plot(p.index, p[c], color=COL[c], lw=2.6 if c == "CHN" else 1.5, alpha=1 if c in ("CHN", "JPN") else 0.85, label=NAME[c])
    ax.axhline(0, color="#0f172a", lw=0.8)
    ax.axhspan(-1, 1, color="#fee2e2", alpha=0.5)
    ax.text(2005.2, 0.35, "低通胀/通缩区间（-1%~1%）", fontsize=8, color=RED)
    ax.set_ylabel("CPI 年均涨幅（%）")
    ax.set_ylim(-2, 24)
    ax.set_xticks(range(2005, 2026, 2))
    ax.set_title("图9  六国 CPI 走势：中国 2023—2025 年连续三年接近零通胀（2005—2025）", fontsize=12, pad=10)
    ax.legend(frameon=False, fontsize=9, ncol=6, loc="upper right")
    src(ax, "数据来源：IMF World Economic Outlook（2026 年 10 月），PCPIPCH（年均 CPI）。")
    save(fig, "fig09_six_cpi.png")


# ---------- 图10 出口对比 ----------
def fig10():
    m = piv(wb, "merch_exports_usd").loc[2005:2024]
    idx = m / m.loc[2005] * 100
    ex = piv(wb, "exports_pct_gdp")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw=dict(width_ratios=[1.4, 1]))
    for c in C:
        a1.plot(idx.index, idx[c], color=COL[c], lw=2.4 if c == "CHN" else 1.6, label=f"{NAME[c]}（2024={idx.loc[2024, c]:.0f}）")
    a1.set_ylabel("商品出口额指数（2005 年 = 100，美元计）")
    a1.set_title("(a) 商品出口规模扩张倍数", fontsize=10.5)
    a1.legend(frameon=False, fontsize=8.5, loc="upper left")
    a1.set_xticks(range(2005, 2025, 3))
    x = np.arange(len(C)); w = 0.38
    a2.bar(x - w / 2, [ex.loc[2005, c] for c in C], width=w, color="#94a3b8", label="2005")
    a2.bar(x + w / 2, [ex.loc[2024, c] for c in C], width=w, color=[COL[c] for c in C], label="2024")
    for i, c in enumerate(C):
        a2.text(i - w / 2, ex.loc[2005, c] + 1.5, f"{ex.loc[2005, c]:.0f}", ha="center", fontsize=8)
        a2.text(i + w / 2, ex.loc[2024, c] + 1.5, f"{ex.loc[2024, c]:.0f}", ha="center", fontsize=8)
    a2.set_xticks(x); a2.set_xticklabels([NAME[c] for c in C], fontsize=9)
    a2.set_ylabel("货物与服务出口 / GDP（%）"); a2.set_ylim(0, 125)
    a2.set_title("(b) 出口依存度：2005 vs 2024", fontsize=10.5)
    a2.legend(frameon=False, fontsize=8.5)
    fig.suptitle("图10  六国出口：中国“规模最大、依存度下降”，越南“规模增长最快、依存度最高”", fontsize=12)
    src(a1, "数据来源：世界银行 WDI，TX.VAL.MRCH.CD.WT 与 NE.EXP.GNFS.ZS。")
    save(fig, "fig10_six_exports.png")


# ---------- 图11 政府收入与债务 ----------
def fig11():
    r = piv(imf, "gen_gov_revenue_pct_gdp").loc[2005:2025]
    dbt = piv(imf, "gen_gov_gross_debt_pct_gdp")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw=dict(width_ratios=[1.5, 1]))
    for c in C:
        s = r[c].dropna()
        a1.plot(s.index, s.values, color=COL[c], lw=2.4 if c == "CHN" else 1.6, label=NAME[c])
    a1.set_ylabel("广义政府收入 / GDP（%）"); a1.set_ylim(10, 40)
    a1.set_title("(a) 广义政府收入占 GDP 比重（IMF 口径）", fontsize=10.5)
    a1.legend(frameon=False, fontsize=8.5, ncol=3, loc="upper left")
    a1.set_xticks(range(2005, 2026, 3))
    x = np.arange(len(C)); w = 0.38
    a2.bar(x - w / 2, [dbt.loc[2015, c] for c in C], width=w, color="#94a3b8", label="2015")
    a2.bar(x + w / 2, [dbt.loc[2025, c] for c in C], width=w, color=[COL[c] for c in C], label="2025")
    for i, c in enumerate(C):
        a2.text(i + w / 2, dbt.loc[2025, c] + 3, f"{dbt.loc[2025, c]:.0f}", ha="center", fontsize=8)
    a2.set_xticks(x); a2.set_xticklabels([NAME[c] for c in C], fontsize=9)
    a2.set_ylabel("广义政府总债务 / GDP（%）"); a2.set_ylim(0, 230)
    a2.set_title("(b) 政府债务率：2015 vs 2025", fontsize=10.5)
    a2.legend(frameon=False, fontsize=8.5)
    fig.suptitle("图11  六国财政：中国政府收入占比居中、债务率十年翻番", fontsize=12)
    src(a1, "数据来源：IMF World Economic Outlook（2026 年 10 月），GGR_NGDP、GGXWDG_NGDP；韩国 2012 年前缺数据。")
    save(fig, "fig11_six_gov_revenue_debt.png")


# ---------- 图12 六国老龄化曲线 ----------
def fig12():
    p = un.pivot(index="year", columns="country", values="pop65_pct").reindex(columns=C).loc[2000:2060]
    fig, ax = plt.subplots(figsize=(10, 5))
    for c in C:
        ax.plot(p.index, p[c], color=COL[c], lw=2.6 if c == "CHN" else 1.7, label=NAME[c])
        ax.text(2060.5, p.loc[2060, c], f"{p.loc[2060, c]:.0f}%", fontsize=8.5, va="center", color=COL[c])
    for lvl, lab in [(7, "老龄化社会 7%"), (14, "深度老龄化 14%"), (20, "超老龄化 20%")]:
        ax.axhline(lvl, color=GRAY, lw=0.8, ls=":")
        ax.text(2000.3, lvl + 0.5, lab, fontsize=8, color=GRAY)
    ax.axvspan(2025, 2060, color="#f8fafc")
    ax.text(2042, 2.5, "← 联合国中方案预测 →", fontsize=8.5, color=GRAY, ha="center")
    ax.set_ylabel("65 岁及以上人口占比（%）")
    ax.set_xlim(2000, 2063); ax.set_ylim(0, 45)
    ax.set_title("图12  六国 65 岁及以上人口占比：历史与预测（2000—2060）", fontsize=12, pad=10)
    ax.legend(frameon=False, fontsize=9, loc="upper left", ncol=2, bbox_to_anchor=(0.09, 1))
    src(ax, "数据来源：联合国《世界人口展望 2024》（中方案），按 5 岁组人口汇总计算。中国 2025 年官方口径为 15.9%（国家统计局）。")
    save(fig, "fig12_six_aging_curve.png")


def aging_milestones():
    """返回各国 65+ 占比首次突破 7%/14%/20% 的年份及当年人均 GDP（现价美元）。"""
    p = un.pivot(index="year", columns="country", values="pop65_pct")
    pc = piv(imf, "gdp_per_capita_usd")
    # 日本 1970 年即超过 7%，1994 年超过 14%；韩国 2000 年超过 7%（WPP 2000 年起数据覆盖）
    known = {"JPN": {7: 1970, 14: 1994}, "KOR": {7: 2000}, "CHN": {7: 2001}}
    out = {}
    for c in C:
        out[c] = {}
        for lvl in (7, 14, 20):
            if c in known and lvl in known[c]:
                y = known[c][lvl]
            else:
                s = p[c]; hit = s[s >= lvl]
                y = int(hit.index[0]) if len(hit) else None
            out[c][lvl] = y
        y14 = out[c][14]
        out[c]["gdppc_at_14"] = float(pc.loc[y14, c]) if y14 and y14 in pc.index else None
    out["JPN"]["gdppc_at_14"] = 39933.0  # 1994 年日本人均 GDP（IMF WEO）
    return out


# ---------- 图13 老龄化速度 ----------
def fig13():
    ms = aging_milestones()
    order = ["JPN", "KOR", "CHN", "VNM", "MYS", "IND"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw=dict(width_ratios=[1.4, 1]))
    y = np.arange(len(order))[::-1]
    for yi, c in zip(y, order):
        y7, y14, y20 = ms[c][7], ms[c][14], ms[c][20]
        if y7 and y14:
            a1.barh(yi, y14 - y7, left=y7, color=COL[c], alpha=0.55, height=0.55)
            a1.text(y7 + (y14 - y7) / 2, yi, f"7%→14%：{y14 - y7}年", ha="center", va="center", fontsize=8.5, color="#0f172a")
        if y14 and y20:
            a1.barh(yi, y20 - y14, left=y14, color=COL[c], height=0.55)
            a1.text(y14 + (y20 - y14) / 2, yi, f"14%→20%：{y20 - y14}年", ha="center", va="center", fontsize=8.5, color="white")
        a1.text(1966, yi, NAME[c], ha="right", va="center", fontsize=10)
        if y20:
            a1.text(y20 + 0.8, yi, f"{y7}/{y14}/{y20}", va="center", fontsize=8, color=GRAY)
    a1.axvline(2025, color=RED, lw=1, ls="--"); a1.text(2025.5, len(order) - 0.6, "2025", color=RED, fontsize=8.5)
    a1.set_yticks([]); a1.set_xlim(1962, 2066)
    a1.set_xlabel("年份（标注：突破 7% / 14% / 20% 的年份）")
    a1.set_title("(a) 老龄化进程所需年数：越晚进入，跑得越快", fontsize=10.5)
    vals = [ms[c]["gdppc_at_14"] for c in order]
    a2.barh([NAME[c] for c in order][::-1], [v if v else 0 for v in vals][::-1], color=[COL[c] for c in order][::-1], height=0.55)
    for i, (c, v) in enumerate(zip(order[::-1], vals[::-1])):
        y14 = ms[c][14]
        a2.text((v or 0) + 800, i, f"{y14}年：{v / 1000:.1f}k 美元" if v else "—", va="center", fontsize=8.5)
    a2.set_xlim(0, 52000)
    a2.set_xlabel("进入深度老龄化（65+ 达 14%）当年的人均 GDP（现价美元）")
    a2.set_title("(b) “未富先老”程度", fontsize=10.5)
    fig.suptitle("图13  老龄化速度与“未富先老”：中国用 20 年走完日本 24 年的路，人均收入只有日本当年的 1/3", fontsize=12)
    src(a1, "数据来源：联合国 WPP2024（日本 1970/1994、韩国 2000、中国 2001 年里程碑按各国官方统计）；人均 GDP 为 IMF WEO。")
    save(fig, "fig13_aging_speed.png")


# ---------- 图14 中国人口结构 ----------
def fig14():
    d = un[un.country == "CHN"].set_index("year")
    years = [2005, 2015, 2025, 2035, 2050]
    ch = [d.loc[y, "children_0_14_thousands"] / 1e4 for y in years]   # 亿人
    wa = [d.loc[y, "working_age_15_64_thousands"] / 1e4 for y in years]
    old = [d.loc[y, "pop65_thousands"] / 1e4 for y in years]
    fig, ax = plt.subplots(figsize=(10, 4.8))
    x = np.arange(len(years))
    ax.bar(x, ch, color="#93c5fd", width=0.6, label="0-14 岁")
    ax.bar(x, wa, bottom=ch, color="#2563eb", width=0.6, label="15-64 岁（劳动年龄）")
    ax.bar(x, old, bottom=np.array(ch) + np.array(wa), color=RED, width=0.6, label="65 岁及以上")
    for i, y in enumerate(years):
        tot = ch[i] + wa[i] + old[i]
        ax.text(i, tot + 0.2, f"总人口 {tot:.2f} 亿", ha="center", fontsize=8.5)
        ax.text(i, ch[i] + wa[i] + old[i] / 2, f"{old[i]:.2f}亿\n{d.loc[y, 'pop65_pct']:.1f}%", ha="center", va="center", fontsize=8, color="white")
        ax.text(i, ch[i] + wa[i] / 2, f"{wa[i]:.2f}亿\n{d.loc[y, 'working_age_pct']:.1f}%", ha="center", va="center", fontsize=8, color="white")
    ax.set_xticks(x); ax.set_xticklabels([f"{y}" + ("（预测）" if y > 2025 else "") for y in years])
    ax.set_ylabel("人口（亿人）"); ax.set_ylim(0, 16.5)
    ax2 = ax.twinx()
    ax2.plot(x, [d.loc[y, "old_age_dependency"] for y in years], color=AMBER, lw=2.2, marker="o", label="老年抚养比（65+/15-64，右轴）")
    for i, y in enumerate(years):
        ax2.text(i + 0.08, d.loc[y, "old_age_dependency"] + 1.5, f"{d.loc[y, 'old_age_dependency']:.0f}%", fontsize=8.5, color=AMBER)
    ax2.set_ylim(0, 70); ax2.set_ylabel("老年抚养比（%）", color=AMBER); ax2.spines["right"].set_visible(True)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8.5, loc="upper left")
    ax.set_title("图14  中国人口年龄结构演变：2005—2050（联合国中方案）", fontsize=12, pad=10)
    src(ax, "数据来源：联合国《世界人口展望 2024》中方案。官方口径 2025 年末 65+ 为 2.24 亿、占 15.9%。")
    save(fig, "fig14_china_age_structure.png")


# ---------- 图15 养老床位 ----------
def fig15():
    b = beds.set_index("year")
    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.bar(b.index, b.beds_total_10k, color="#bfdbfe", width=0.7, label="各类养老机构和设施床位合计（万张，左轴）")
    reg = b.registered_institution_beds_10k.dropna()
    ax.bar(reg.index, reg.values, color=BLUE, width=0.7, label="其中：注册登记养老机构床位（万张，左轴）")
    for x, v in zip(b.index, b.beds_total_10k):
        ax.text(x, v + 10, f"{v:.0f}", ha="center", fontsize=8)
    ax.set_ylabel("床位（万张）"); ax.set_ylim(0, 1000)
    ax2 = ax.twinx()
    ax2.plot(b.index, b.beds_per_1000_elderly, color=RED, lw=2.2, marker="o", label="每千名 60 岁及以上老人拥有床位（张，右轴）")
    for x, v in zip(b.index, b.beds_per_1000_elderly):
        ax2.text(x, v + 0.8, f"{v:.1f}", ha="center", fontsize=8, color=RED)
    ax2.set_ylim(0, 40); ax2.set_ylabel("每千老人床位（张）", color=RED); ax2.spines["right"].set_visible(True)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8.5, loc="upper left")
    ax.set_xticks(b.index)
    ax.set_title("图15  中国养老床位供给：总量 2020 年见顶回落，每千老人床位降至十年最低", fontsize=12, pad=10)
    src(ax, "数据来源：民政部历年《民政事业发展统计公报》、民政部/全国老龄办《国家老龄事业发展公报》；每千老人床位 = 床位合计 / 60 岁及以上人口。")
    save(fig, "fig15_elderly_care_beds.png")


# ---------- 图16 酒店改养老推演 ----------
def scenario_table():
    """机构护理床位供需与酒店改造情景（2025—2035）。假设见报告第六章。"""
    d = un[un.country == "CHN"].set_index("year")
    years = list(range(2025, 2036))
    pop60 = np.array([d.loc[y, "pop60_thousands"] / 1e4 for y in years])        # 亿人... thousands/1e4 = 万人*? -> 千人/1e4 = 千万人
    pop60_wan = pop60 * 1000                                                     # 万人
    # 2025 年官方 60+ 为 32338 万人，UN 口径略低；按官方基数、UN 增速外推
    pop60_wan = pop60_wan / pop60_wan[0] * 32338
    disabled_rate = 0.116                                                        # 第五次城乡老年人生活状况抽样调查：失能占 11.6%
    disabled = pop60_wan * disabled_rate
    inst_share = np.linspace(0.10, 0.15, len(years))                             # 失能老人机构照护比例 10%→15%
    occupancy = 0.85
    need_nursing_beds = disabled * inst_share / occupancy                        # 万张护理型床位需求
    base_nursing_2025 = 498.4 * 0.699                                            # 2025 年护理型床位 ≈348 万张
    organic = base_nursing_2025 * (1.03 ** np.arange(len(years)))                # 常规新建/改造年均 +3%
    hotel_rooms = 1700                                                           # 万间（2025 年存量酒店客房）
    beds_per_room = 1.3
    scen = {
        "受阻情景（累计改造 0.8% 客房）": 0.008,
        "基准情景（累计改造 2.5% 客房）": 0.025,
        "加速情景（累计改造 5% 客房）": 0.05,
    }
    rows = []
    for i, y in enumerate(years):
        prog = (i / (len(years) - 1)) ** 1.3                                     # 改造进度前慢后快
        row = dict(year=y, pop60_10k=round(pop60_wan[i]), disabled_10k=round(disabled[i]),
                   nursing_bed_need_10k=round(need_nursing_beds[i]), nursing_bed_organic_10k=round(organic[i]),
                   gap_before_hotels_10k=round(need_nursing_beds[i] - organic[i]))
        for k, v in scen.items():
            row[k] = round(hotel_rooms * v * prog * beds_per_room)
        rows.append(row)
    return pd.DataFrame(rows)


def fig16():
    t = scenario_table()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t.year, t.nursing_bed_need_10k, color=RED, lw=2.4, marker="o", label="机构护理型床位需求（万张）")
    ax.plot(t.year, t.nursing_bed_organic_10k, color=GRAY, lw=2, ls="--", label="常规供给：现有护理型床位按年均 +3% 增长")
    cols = ["受阻情景（累计改造 0.8% 客房）", "基准情景（累计改造 2.5% 客房）", "加速情景（累计改造 5% 客房）"]
    cc = ["#fdba74", AMBER, "#9a3412"]
    for c, col in zip(cols, cc):
        ax.plot(t.year, t.nursing_bed_organic_10k + t[c], color=col, lw=2, marker="s", ms=3.5, label=f"常规供给 + 酒店改造：{c}")
    ax.fill_between(t.year, t.nursing_bed_organic_10k, t.nursing_bed_need_10k, color="#fee2e2", alpha=0.6)
    gap = t.gap_before_hotels_10k.iloc[-1]
    ax.annotate(f"2035 年缺口约 {gap:.0f} 万张\n（加速情景下酒店改造可填补约 {t[cols[2]].iloc[-1] / gap * 100:.0f}%）",
                xy=(2035, t.nursing_bed_need_10k.iloc[-1]), xytext=(2027.3, t.nursing_bed_need_10k.iloc[-1] - 40),
                fontsize=9, arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))
    ax.set_ylabel("护理型床位（万张）")
    ax.set_xticks(t.year)
    ax.set_title("图16  2025—2035 年机构护理床位供需推演：酒店改造是“补充项”而非“解决方案”", fontsize=12, pad=10)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    src(ax, "测算假设：60+ 人口按官方 2025 基数、联合国中方案增速外推；失能率 11.6%；机构照护比例 10%→15%；目标入住率 85%；存量客房 1700 万间，每间改 1.3 床。")
    save(fig, "fig16_hotel_conversion_scenarios.png")
    t.to_csv(os.path.join(DATA, "scenario_nursing_beds_2025_2035.csv"), index=False)


# ---------- 图17 综合评分雷达 ----------
def radar_scores():
    """2020—2025 年五维度相对得分（0—10，组内 min-max 标准化）。方向：增长高、消费率高、通胀适度（距 2% 越近越好）、出口扩张快、财政空间大（收入占比高且债务低）为优。"""
    g = piv(imf, "real_gdp_growth_pct").loc[2020:2025].mean()
    cons = piv(wb, "hh_consumption_pct_gdp").loc[2020:2024].mean()
    infl = (piv(imf, "inflation_avg_pct").loc[2020:2025].mean() - 2).abs() * -1
    m = piv(wb, "merch_exports_usd"); exg = (m.loc[2024] / m.loc[2019]) ** (1 / 5) - 1
    rev = piv(imf, "gen_gov_revenue_pct_gdp").loc[2025]; debt = piv(imf, "gen_gov_gross_debt_pct_gdp").loc[2025]
    fiscal = rev - debt / 4
    aging = -piv(wb, "pop65_pct").loc[2024]

    def norm(s):
        return (s - s.min()) / (s.max() - s.min()) * 10
    df = pd.DataFrame({"经济增长": norm(g), "消费率": norm(cons), "物价稳定": norm(infl), "出口扩张": norm(exg),
                       "财政空间": norm(fiscal), "人口结构": norm(aging)})
    raw = pd.DataFrame({"GDP增速(20-25均)": g, "居民消费率(20-24均)": cons, "CPI(20-25均)": piv(imf, "inflation_avg_pct").loc[2020:2025].mean(),
                        "商品出口年均增速(19-24)": exg * 100, "政府收入/GDP 2025": rev, "政府债务/GDP 2025": debt, "65+占比 2024": -aging})
    return df, raw


def fig17():
    df, raw = radar_scores()
    raw.round(1).to_csv(os.path.join(DATA, "radar_inputs_2020_2025.csv"))
    labels = list(df.columns); n = len(labels)
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist(); ang += ang[:1]
    fig, axes = plt.subplots(2, 3, figsize=(11, 7.2), subplot_kw=dict(polar=True))
    for ax, c in zip(axes.flat, C):
        v = df.loc[c].tolist(); v += v[:1]
        ax.plot(ang, v, color=COL[c], lw=2); ax.fill(ang, v, color=COL[c], alpha=0.25)
        ax.set_xticks(ang[:-1]); ax.set_xticklabels(labels, fontsize=8.5)
        ax.set_ylim(0, 10); ax.set_yticks([2, 4, 6, 8, 10]); ax.set_yticklabels(["", "", "", "", ""])
        ax.set_title(f"{NAME[c]}  综合 {df.loc[c].mean():.1f}/10", fontsize=10.5, pad=12, color=COL[c])
    fig.suptitle("图17  六国 2020—2025 年六维度相对评分（组内标准化，10 分为六国最优）", fontsize=12)
    fig.text(0.02, 0.01, "评分方向：GDP 增速高、居民消费率高、CPI 接近 2%、商品出口 2019-2024 年均增速高、政府收入高且债务低、65+ 占比低为优。"
             "数据来源：IMF WEO、世界银行 WDI。", fontsize=8, color=GRAY)
    fig.tight_layout(rect=(0, 0.03, 1, 0.96))
    fig.savefig(os.path.join(OUT, "fig17_radar_scores.png"), dpi=170); plt.close(fig)


if __name__ == "__main__":
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15, fig16, fig17]:
        f(); print("ok", f.__name__)
    ms = aging_milestones()
    for c in C:
        print(NAME[c], ms[c])
    print(scenario_table().to_string())
    print(radar_scores()[0].round(1).to_string())
    print(radar_scores()[1].round(1).to_string())
