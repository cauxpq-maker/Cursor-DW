# -*- coding: utf-8 -*-
"""生成《"十五五"六张网战略系统研究报告》所需图表"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(OUT, exist_ok=True)

NAVY = "#0b2a5b"
BLUE = "#2563eb"
LIGHT = "#93c5fd"
RED = "#dc2626"
GRAY = "#64748b"
GREEN = "#059669"
AMBER = "#d97706"


def chart_investment_scale():
    """图1：“十五五”六张网重点领域官方披露投资规模与电网投资跨周期对比"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.4), gridspec_kw={"width_ratios": [1.25, 1]})

    nets = ["国家水网", "新型电网", "城市地下管网"]
    vals = [6, 5, 5]
    bars = ax1.bar(nets, vals, color=[BLUE, NAVY, GRAY], width=0.55)
    for b, v, lab in zip(bars, vals, ["超6万亿", "超5万亿\n(带动上下游超10万亿)", "约5万亿\n(改造约77万公里)"]):
        ax1.text(b.get_x() + b.get_width() / 2, v + 0.12, lab, ha="center", va="bottom", fontsize=9.5)
    ax1.set_ylim(0, 7.6)
    ax1.set_ylabel("万亿元")
    ax1.set_title("“十五五”时期官方披露投资规模（部分网）", fontsize=11)
    ax1.spines[["top", "right"]].set_visible(False)

    periods = ["“十三五”", "“十四五”", "“十五五”(预计)"]
    grid = [2.64, 2.85, 5.0]
    bars2 = ax2.bar(periods, grid, color=[LIGHT, BLUE, NAVY], width=0.55)
    for b, v, lab in zip(bars2, grid, ["2.64", "2.85", "5.0+"]):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.08, lab, ha="center", va="bottom", fontsize=10)
    ax2.set_ylim(0, 6)
    ax2.set_ylabel("万亿元")
    ax2.set_title("全国电网固定资产投资：三个五年对比", fontsize=11)
    ax2.spines[["top", "right"]].set_visible(False)

    fig.suptitle("图1  “六张网”投资体量：2026年当年超7万亿元，电网投资较“十四五”增长超80%", fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart1_investment.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def chart_funding_tools():
    """图2：2026年支持六张网的主要中央资金/政策性金融工具规模"""
    tools = [
        "超长期特别国债（全年）",
        "新型政策性金融工具",
        "中央预算内投资",
        "其中：超长期国债支持地下管网",
        "“两新”设备更新资金",
    ]
    vals = [10000, 8000, 7550, 1600, 2000]
    colors = [NAVY, BLUE, BLUE, GRAY, LIGHT]
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    y = list(range(len(tools)))[::-1]
    ax.barh(y, vals, color=colors, height=0.6)
    for yi, v in zip(y, vals):
        ax.text(v + 120, yi, f"{v:,} 亿元", va="center", fontsize=10)
    ax.set_yticks(y)
    ax.set_yticklabels(tools, fontsize=10)
    ax.set_xlim(0, 12500)
    ax.set_xlabel("亿元")
    ax.set_title("图2  2026年“六张网”相关中央资金与政策性金融工具规模（新型政策性金融工具预计撬动约10万亿元项目投资）", fontsize=11.5, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart2_funding.png"), dpi=200)
    plt.close(fig)


def chart_dc_capacity():
    """图3：全球数据中心容量区域分布（SemiAnalysis，2026年9月）"""
    regions = ["美国", "中国", "亚太（除中国）", "欧洲/中东/非洲", "拉美"]
    gw = [56, 24, 15, 14, 2]
    colors = [RED, BLUE, GRAY, GRAY, GRAY]
    fig, ax = plt.subplots(figsize=(9, 4))
    y = list(range(len(regions)))[::-1]
    ax.barh(y, gw, color=colors, height=0.6)
    for yi, v, r in zip(y, gw, regions):
        suffix = "（2026年底）" if r == "美国" else ("（在运，另有约50GW储备/规划）" if r == "中国" else "")
        ax.text(v + 0.8, yi, f"{v} GW{suffix}", va="center", fontsize=10)
    ax.set_yticks(y)
    ax.set_yticklabels(regions, fontsize=10.5)
    ax.set_xlim(0, 80)
    ax.set_xlabel("数据中心在运容量（GW，IT负载）")
    ax.set_title("图3  全球数据中心容量区域分布：美国约为中国2.3倍，但中国储备规模庞大", fontsize=12, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart3_dc_capacity.png"), dpi=200)
    plt.close(fig)


def chart_token_vs_compute():
    """图4：算力需求侧（日均Token调用量）与供给侧（智算规模）的爆发式增长"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))

    t_labels = ["2024年初", "2025年底", "2026年3月"]
    t_vals = [0.1, 100, 140]  # 万亿 Token/日
    ax1.bar(t_labels, t_vals, color=[LIGHT, BLUE, NAVY], width=0.55)
    ax1.set_yscale("log")
    ax1.set_ylim(0.05, 600)
    for i, v in enumerate(t_vals):
        ax1.text(i, v * 1.25, f"{v:g} 万亿", ha="center", fontsize=10)
    ax1.set_ylabel("日均Token调用量（万亿，对数轴）")
    ax1.set_title("需求侧：两年增长超1000倍", fontsize=11)
    ax1.spines[["top", "right"]].set_visible(False)

    c_labels = ["2025年3月底", "2026年3月底"]
    c_vals = [188.2 / 2.5, 188.2]
    ax2.bar(c_labels, c_vals, color=[LIGHT, NAVY], width=0.5)
    for i, v in enumerate(c_vals):
        ax2.text(i, v + 4, f"{v:.1f} 万P" if i else f"约{v:.0f} 万P", ha="center", fontsize=10)
    ax2.set_ylim(0, 230)
    ax2.set_ylabel("已建成智能算力规模（万P）")
    ax2.set_title("供给侧：一年增长至2.5倍", fontsize=11)
    ax2.spines[["top", "right"]].set_visible(False)

    fig.suptitle("图4  算力网供需两端同步爆发，矛盾从“总量不足”转向“结构错配与调度不畅”", fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart4_token_compute.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def chart_telecom_capex():
    """图5：三大运营商资本开支结构迁移"""
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"width_ratios": [1.3, 1]})
    cats = ["2025年资本开支", "2026年计划资本开支"]
    # 2626/0.92 ≈ 2854
    vals = [2854, 2626]
    ax.bar(cats, vals, color=[LIGHT, NAVY], width=0.5)
    ax.text(0, 2854 + 40, "约2854亿元", ha="center", fontsize=10)
    ax.text(1, 2626 + 40, "约2626亿元（-8%）", ha="center", fontsize=10)
    ax.set_ylim(0, 3400)
    ax.set_ylabel("亿元")
    ax.set_title("三大运营商资本开支总额：连续收缩", fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)

    ax2.pie([34, 66], colors=[BLUE, "#e2e8f0"], startangle=90,
            wedgeprops=dict(width=0.38, edgecolor="white"))
    ax2.text(0, 0, "算力网\n≈34%", ha="center", va="center", fontsize=11, color=NAVY)
    ax2.set_title("2026年上半年资本开支投向\n（算力网投资约399亿元，同比+80%以上）", fontsize=10.5)

    fig.suptitle("图5  运营商资本开支“总量收缩、结构向算力迁移”：传统通信网预算收、算力网预算放", fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart5_telecom_capex.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def chart_market_space():
    """图6：六张网市场化成熟度与“十五五”可经营空间"""
    nets = ["物流网", "新一代通信网", "算力网", "新型电网", "国家水网", "城市地下管网"]
    mature = [4.5, 4.5, 3.5, 3.0, 2.0, 1.5]
    space = [4.5, 3.5, 5.0, 4.0, 3.0, 2.5]
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    y = list(range(len(nets)))[::-1]
    ax.barh([i + 0.18 for i in y], mature, height=0.32, color=GRAY, label="当前可经营现金流成熟度")
    ax.barh([i - 0.18 for i in y], space, height=0.32, color=BLUE, label="“十五五”市场化拓展空间")
    ax.set_yticks(y)
    ax.set_yticklabels(nets, fontsize=11)
    ax.set_xlim(0, 6)
    ax.set_xlabel("评估分（1–5，本报告结构化判断，非官方评级）")
    ax.set_title("图6  六张网市场化：物流和通信已经能收费，算力和电网的增量空间更大", fontsize=12, pad=10)
    ax.legend(frameon=False, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart6_market_space.png"), dpi=200)
    plt.close(fig)


def chart_five_cities():
    """图7：五城六网结构化评估"""
    import numpy as np

    dims = ["水网", "新型电网", "算力网", "通信网", "地下管网", "物流网"]
    cities = ["深圳\n东南", "成都\n西南", "天津\n华北", "西安\n西北", "沈阳\n东北"]
    data = {
        "深圳\n东南": [4, 5, 5, 5, 4, 4],
        "成都\n西南": [4, 5, 5, 4, 4, 5],
        "天津\n华北": [4, 4, 3, 3, 3, 5],
        "西安\n西北": [4, 3, 4, 3, 3, 4],
        "沈阳\n东北": [3, 3, 3, 3, 3, 4],
    }
    colors = [NAVY, BLUE, GREEN, AMBER, RED]
    x = np.arange(len(dims))
    width = 0.15
    fig, ax = plt.subplots(figsize=(10, 4.6))
    for i, (city, color) in enumerate(zip(cities, colors)):
        ax.bar(x + (i - 2) * width, data[city], width, label=city.replace("\n", "·"), color=color)
    ax.set_xticks(x)
    ax.set_xticklabels(dims)
    ax.set_ylim(0, 6)
    ax.set_ylabel("评估分（1–5）")
    ax.set_title("图7  五城六网评估：东南、西南领先，东北、西北的差距集中在算力和通信", fontsize=12, pad=10)
    ax.legend(ncol=5, frameon=False, fontsize=9, loc="upper center", bbox_to_anchor=(0.5, -0.14))
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart7_five_cities.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def chart_tier_county():
    """图9：一线城市与县城能力指数"""
    dims = ["算力可及", "通信能力", "供电质量", "供水保障", "管网智治", "物流能级"]
    tier = [100, 100, 100, 100, 100, 100]
    county = [30, 62, 88, 74, 35, 48]
    import numpy as np
    x = np.arange(len(dims))
    width = 0.36
    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    ax.bar(x - width / 2, tier, width, color=NAVY, label="一线城市（指数=100）")
    ax.bar(x + width / 2, county, width, color=AMBER, label="县城/县域综合水平")
    for i, v in enumerate(county):
        ax.text(i + width / 2, v + 2, str(v), ha="center", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(dims)
    ax.set_ylim(0, 120)
    ax.set_ylabel("相对指数（一线城市=100）")
    ax.set_title("图8  一线城市与县城：通达差距已缩小，算力和管网智治差距仍然很大", fontsize=12, pad=10)
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart8_tier_county.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    chart_investment_scale()
    chart_funding_tools()
    chart_dc_capacity()
    chart_token_vs_compute()
    chart_telecom_capex()
    chart_market_space()
    chart_five_cities()
    chart_tier_county()
    print("charts generated ->", OUT)
