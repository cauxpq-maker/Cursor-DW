# -*- coding: utf-8 -*-
"""生成《中国电影市场深度分析报告》配套图表。

配色、字体与图表风格对齐《2026年中国暑期旅游市场分析报告》:
Noto Sans CJK SC / 蓝 #2563eb / 红 #dc2626 / 琥珀 #f59e0b / 灰 #64748b / 藏青 #0b2a5b
"""
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

BLUE = "#2563eb"
RED = "#dc2626"
AMBER = "#f59e0b"
GRAY = "#64748b"
NAVY = "#0b2a5b"
LIGHTBLUE = "#93c5fd"


def chart1():
    """图1:2015-2025 中国电影票房与观影人次趋势。"""
    years = list(range(2015, 2026))
    box = [440.7, 457.1, 559.1, 609.8, 642.7, 204.2, 472.6, 300.7, 549.2, 425.0, 518.3]
    adm = [12.6, 13.7, 16.2, 17.2, 17.3, 5.5, 11.7, 7.1, 13.0, 10.1, 12.4]

    fig, ax1 = plt.subplots(figsize=(9, 4.6))
    ax1.bar(years, box, color=BLUE, width=0.62, label="票房（亿元）")
    ax1.set_ylabel("票房（亿元）", color=NAVY)
    for x, y in zip(years, box):
        ax1.text(x, y + 10, f"{y:.0f}", ha="center", fontsize=9, color=NAVY)
    ax1.set_ylim(0, 730)

    ax2 = ax1.twinx()
    ax2.plot(years, adm, color=AMBER, marker="o", linewidth=2, label="观影人次（亿）")
    ax2.set_ylabel("观影人次（亿）", color=AMBER)
    ax2.tick_params(axis="y", labelcolor=AMBER)
    ax2.set_ylim(0, 21)
    ax2.spines[["top"]].set_visible(False)

    ax1.set_title("图1  中国电影票房与观影人次（2015—2025）：大盘由供给驱动，峰值仍停留在2019年",
                  fontsize=12, pad=12)
    ax1.set_xticks(years)
    ax1.spines[["top"]].set_visible(False)
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, frameon=False, fontsize=10, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart1_china_boxoffice_trend.png"), dpi=200)
    plt.close(fig)


def chart2():
    """图2:2025 中国电影市场类型结构。"""
    labels = ["动画（哪吒2带动）", "战争题材", "喜剧", "动作", "爱情", "其他"]
    shares = [50.0, 12.7, 12.4, 10.9, 1.5, 12.5]
    colors = [BLUE, RED, AMBER, NAVY, LIGHTBLUE, GRAY]

    fig, ax = plt.subplots(figsize=(8, 4.9))
    wedges, _, autotexts = ax.pie(
        shares, labels=labels, colors=colors, autopct="%.1f%%",
        startangle=90, counterclock=False,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        textprops={"fontsize": 10, "color": "#1e293b"},
    )
    for t in autotexts:
        t.set_color("white")
        t.set_fontsize(9)
    ax.set_title("图2  2025年中国电影票房类型结构：动画占近半大盘，爱情片份额萎缩至1.5%",
                 fontsize=12, pad=12)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart2_2025_genre_structure.png"), dpi=200)
    plt.close(fig)


def chart3():
    """图3:2025 全球票房TOP10。"""
    films = ["哪吒之魔童闹海（中）", "疯狂动物城2", "阿凡达：火与烬", "星际宝贝史迪奇",
             "我的世界大电影", "侏罗纪世界：重生", "鬼灭之刃：无限城篇（日）",
             "驯龙高手（真人版）", "F1：狂飙飞车", "超人"]
    gross = [22.7, 18.7, 14.9, 10.4, 9.6, 8.7, 7.9, 6.4, 6.3, 6.2]
    colors = [RED] + [BLUE] * 5 + [AMBER] + [BLUE] * 3

    fig, ax = plt.subplots(figsize=(9, 5.2))
    y = range(len(films))[::-1]
    ax.barh(list(y), gross, color=colors, height=0.62)
    ax.set_yticks(list(y))
    ax.set_yticklabels(films, fontsize=10)
    ax.set_xlabel("全球票房（亿美元）")
    for yi, g in zip(y, gross):
        ax.text(g + 0.2, yi, f"${g}亿", va="center", fontsize=9, color="#1e293b")
    ax.set_title("图3  2025年全球票房TOP10：影史首次由非好莱坞影片（红）夺得年冠，日本动画（琥珀）进入前十",
                 fontsize=11.5, pad=12)
    ax.set_xlim(0, 26)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart3_global_top10_2025.png"), dpi=200)
    plt.close(fig)


def chart4():
    """图4:微短剧产值 vs 电影票房。"""
    years = [2021, 2022, 2023, 2024, 2025]
    duanju = [36.8, 101.7, 373.9, 505.0, 1000.0]
    film = [472.6, 300.7, 549.2, 425.0, 518.3]

    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    w = 0.34
    x = range(len(years))
    ax.bar([i - w / 2 for i in x], film, w, color=BLUE, label="电影票房（亿元）")
    ax.bar([i + w / 2 for i in x], duanju, w, color=RED, label="微短剧（含漫剧）产值（亿元）")
    for i, (f, d) in enumerate(zip(film, duanju)):
        ax.text(i - w / 2, f + 14, f"{f:.0f}", ha="center", fontsize=9.5, color=NAVY)
        ax.text(i + w / 2, d + 14, f"{d:.0f}", ha="center", fontsize=9.5, color=RED)
    ax.set_xticks(list(x))
    ax.set_xticklabels(years)
    ax.set_ylabel("规模（亿元）")
    ax.set_ylim(0, 1120)
    ax.set_title("图4  微短剧产值 vs 电影票房（2021—2025）：2025年微短剧产值约1000亿元，接近电影票房的两倍",
                 fontsize=11.5, pad=12)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart4_duanju_vs_film.png"), dpi=200)
    plt.close(fig)


def chart5():
    """图5:韩国电影市场观影人次与本土片份额。"""
    years = list(range(2019, 2026))
    adm = [2.267, 0.595, 0.610, 1.128, 1.251, 1.231, 1.061]
    local_share = [51.0, 68.0, 30.1, 55.7, 48.5, 57.8, 40.0]

    fig, ax1 = plt.subplots(figsize=(8.2, 4.4))
    ax1.bar(years, adm, color=GRAY, width=0.6, label="观影人次（亿）")
    ax1.set_ylabel("观影人次（亿）", color=GRAY)
    for x, y in zip(years, adm):
        ax1.text(x, y + 0.05, f"{y:.2f}", ha="center", fontsize=9.5, color="#334155")
    ax1.set_ylim(0, 2.7)
    ax1.spines[["top"]].set_visible(False)

    ax2 = ax1.twinx()
    ax2.plot(years, local_share, color=RED, marker="s", linewidth=2, label="本土片票房份额（%）")
    ax2.set_ylabel("本土片份额（%）", color=RED)
    ax2.tick_params(axis="y", labelcolor=RED)
    ax2.set_ylim(0, 85)
    ax2.spines[["top"]].set_visible(False)

    ax1.set_title("图5  韩国电影市场（2019—2025）：观影人次仅为2019年的47%，本土片份额跌至40%被外片反超",
                  fontsize=11.5, pad=12)
    ax1.set_xticks(years)
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, frameon=False, fontsize=10, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart5_korea_market_decline.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    chart1()
    chart2()
    chart3()
    chart4()
    chart5()
    print("charts saved to", OUT)
