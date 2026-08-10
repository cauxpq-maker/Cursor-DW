# -*- coding: utf-8 -*-
"""生成《2026年中国暑期旅游市场分析报告》所需图表"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(OUT, exist_ok=True)

BLUE = "#2563eb"
RED = "#dc2626"
GRAY = "#64748b"


def chart_volume_vs_price():
    """图1：量增价跌——2026暑期核心量价指标同比变化（含7月实绩）"""
    labels = [
        "免签入境外国人（上半年）",
        "境内游预订出游人次",
        "跨省游热度",
        "亲子游预订量",
        "8月机票预订量（截至7/29）",
        "7月民航旅客量（单月纪录）",
        "7月国内经济舱均价（实绩）",
        "7月全国酒店RevPAR",
        "7月全国酒店ADR",
        "经济型酒店RevPAR(暑期首周)",
        "三亚酒店平均支付价",
    ]
    values = [30.6, 30, 22.4, 31, 7, 3.7, -0.7, -2.8, -3.7, -8.2, -20]
    colors = [BLUE if v > 0 else RED for v in values]

    fig, ax = plt.subplots(figsize=(9, 4.8))
    y = range(len(labels))[::-1]
    ax.barh(list(y), values, color=colors, height=0.62)
    for yi, v in zip(y, values):
        ax.text(v + (0.8 if v > 0 else -0.8), yi, f"{v:+g}%",
                va="center", ha="left" if v > 0 else "right", fontsize=10)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=10)
    ax.axvline(0, color="#0f172a", lw=0.8)
    ax.set_xlim(-32, 42)
    ax.set_xlabel("同比变化（%）")
    ax.set_title("图1  2026年暑期旅游市场“量增价跌”：客流指标与价格指标同比变化（8月上旬更新）", fontsize=12, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart1_volume_price.png"), dpi=200)
    plt.close(fig)


def chart_visits_spend():
    """图2：出游人次与花费增速剪刀差（一季度对比）"""
    years = ["2024Q1", "2025Q1", "2026Q1"]
    visits_growth = [16.7, 26.4, 6.0]
    spend_growth = [17.0, 18.6, 2.9]

    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    x = range(len(years))
    w = 0.32
    ax.bar([i - w / 2 for i in x], visits_growth, width=w, label="国内出游人次同比增速", color=BLUE)
    ax.bar([i + w / 2 for i in x], spend_growth, width=w, label="国内出游总花费同比增速", color="#f59e0b")
    for i, (v1, v2) in enumerate(zip(visits_growth, spend_growth)):
        ax.text(i - w / 2, v1 + 0.5, f"{v1}%", ha="center", fontsize=10)
        ax.text(i + w / 2, v2 + 0.5, f"{v2}%", ha="center", fontsize=10)
    ax.set_xticks(list(x))
    ax.set_xticklabels(years)
    ax.set_ylabel("同比增速（%）")
    ax.set_title("图2  “旺丁不旺财”：出游人次与总花费增速的剪刀差（一季度）", fontsize=12, pad=12)
    ax.legend(frameon=False, fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart2_visits_spend.png"), dpi=200)
    plt.close(fig)


def chart_hotel_revpar():
    """图3：2026年暑期首周（6.29-7.5）各档次酒店经营指标同比变化"""
    cats = ["经济型", "中档型"]
    revpar = [-8.2, -7.8]
    occ = [-4.7, -3.9]
    adr = [-3.7, -4.1]

    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    x = range(len(cats))
    w = 0.24
    ax.bar([i - w for i in x], revpar, width=w, label="RevPAR（每房收入）", color=RED)
    ax.bar(list(x), occ, width=w, label="OCC（入住率）", color=GRAY)
    ax.bar([i + w for i in x], adr, width=w, label="ADR（平均房价）", color="#f59e0b")
    for i in x:
        ax.text(i - w, revpar[i] - 0.35, f"{revpar[i]}%", ha="center", fontsize=10)
        ax.text(i, occ[i] - 0.35, f"{occ[i]}%", ha="center", fontsize=10)
        ax.text(i + w, adr[i] - 0.35, f"{adr[i]}%", ha="center", fontsize=10)
    ax.set_xticks(list(x))
    ax.set_xticklabels(cats, fontsize=11)
    ax.axhline(0, color="#0f172a", lw=0.8)
    ax.set_ylim(-10.5, 1.5)
    ax.set_ylabel("同比变化（%）")
    ax.set_title("图3  2026年暑期首周全国酒店核心经营指标同比变化（国金证券监测）", fontsize=12, pad=12)
    ax.legend(frameon=False, fontsize=10, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart3_hotel_revpar.png"), dpi=200)
    plt.close(fig)


def chart_catering():
    """图4：餐饮收入增速收窄与场景分层"""
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.0))
    ax = axes[0]
    months = ["1-2月", "一季度", "1-4月", "1-5月", "上半年"]
    growth = [4.8, 4.2, 3.8, 3.1, 2.8]
    ax.plot(months, growth, color=BLUE, marker="o", lw=2.2, markersize=7)
    for x, y in zip(months, growth):
        ax.text(x, y + 0.12, f"{y}%", ha="center", fontsize=9)
    ax.set_ylim(2.0, 5.5)
    ax.set_ylabel("累计同比增速（%）")
    ax.set_title("图4a  全国餐饮收入累计增速逐月收窄", fontsize=11, pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e2e8f0", lw=0.6)

    ax = axes[1]
    labels = ["工作餐/\n一人食", "外卖/\n即时零售", "小吃/\n快餐", "正餐/\n宴会", "夜经济/\n烧烤宵夜"]
    weekday = [9, 8, 8, 3, 5]
    holiday = [4, 5, 6, 9, 8]
    x = range(len(labels))
    w = 0.35
    ax.bar([i - w/2 for i in x], weekday, width=w, label="平日刚需强度", color=GRAY)
    ax.bar([i + w/2 for i in x], holiday, width=w, label="假期改善强度", color="#f59e0b")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0, 11)
    ax.set_ylabel("场景强度（示意评分）")
    ax.set_title("图4b  平日刚需 vs 假期改善：场景分层", fontsize=11, pad=10)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart4_catering.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    chart_volume_vs_price()
    chart_visits_spend()
    chart_hotel_revpar()
    chart_catering()
    print("charts generated:", os.listdir(OUT))
