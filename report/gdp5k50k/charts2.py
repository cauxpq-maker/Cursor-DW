# -*- coding: utf-8 -*-
"""生成《城市分层视角下的发展阶段与文旅、银发经济深度研究》报告图表(N1-N7)"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "charts")
DATA = os.path.join(BASE, "data")

RED, BLUE, GREEN, GRAY, ORANGE = "#dc2626", "#2563eb", "#059669", "#64748b", "#f59e0b"


def n1_quadrant():
    # 31省区市:人均GDP(2025,万元,公报整理约数) × 65+占比(%,2023-24,统计年鉴/老龄报告整理约数)
    prov = [
        ("北京", 23.9, 14.8), ("上海", 22.9, 19.6), ("江苏", 16.5, 18.7), ("福建", 14.2, 12.1),
        ("浙江", 14.0, 14.7), ("天津", 13.1, 16.5), ("内蒙古", 11.7, 14.6), ("广东", 11.4, 10.0),
        ("湖北", 11.0, 16.3), ("山东", 10.5, 17.0), ("重庆", 10.4, 18.6), ("陕西", 9.2, 14.7),
        ("安徽", 8.3, 16.1), ("湖南", 8.0, 15.9), ("江西", 8.0, 12.7), ("辽宁", 8.0, 21.9),
        ("海南", 8.0, 11.6), ("山西", 7.5, 14.3), ("四川", 7.5, 17.7), ("新疆", 7.8, 8.3),
        ("宁夏", 7.8, 10.9), ("西藏", 7.3, 5.9), ("河南", 6.6, 14.7), ("吉林", 6.5, 18.2),
        ("青海", 6.5, 9.7), ("河北", 6.5, 15.4), ("云南", 6.4, 12.5), ("黑龙江", 6.2, 18.7),
        ("贵州", 6.0, 12.9), ("广西", 5.9, 13.4), ("甘肃", 5.6, 13.6),
    ]
    cities = [("深圳", 21.5, 4.0, "深圳型:富+年轻"), ("南通", 16.5, 26.6, "南通型:未富先老震中"),
              ("东莞", 12.0, 3.9, None)]
    x_mid, y_mid = 9.97, 15.6  # 全国人均GDP(万元)与65+占比(官方口径)

    fig, ax = plt.subplots(figsize=(9.6, 6.2))
    ax.axvline(x_mid, color="#cbd5e1", lw=1.0, ls="--")
    ax.axhline(y_mid, color="#cbd5e1", lw=1.0, ls="--")
    ax.text(23.5, 5.2, "富+年轻\n(准备期最长)", fontsize=10, color=GREEN, ha="right")
    ax.text(23.5, 25.8, "富+老\n(上海型:日本2020s当下)", fontsize=10, color=BLUE, ha="right")
    ax.text(4.7, 25.8, "未富先老\n(东北/川渝型:日韩无先例)", fontsize=10, color=RED)
    ax.text(4.7, 5.2, "欠发达+年轻\n(西部型:阶段Ⅰ)", fontsize=10, color=GRAY)

    for name, x, y in prov:
        c = RED if (x < x_mid and y > y_mid) else BLUE if (x >= x_mid and y > y_mid) \
            else GREEN if (x >= x_mid) else GRAY
        ax.scatter(x, y, s=46, color=c, zorder=3, alpha=0.85)
        ax.annotate(name, (x, y), textcoords="offset points", xytext=(4, 3), fontsize=8.2)
    for name, x, y, note in cities:
        ax.scatter(x, y, s=72, marker="D", color=ORANGE, zorder=4)
        ax.annotate(name, (x, y), textcoords="offset points", xytext=(4, 3), fontsize=8.6,
                    color="#b45309", fontweight="bold")
        if note:
            ax.annotate(note, (x, y), textcoords="offset points", xytext=(8, -13),
                        fontsize=8.2, color="#b45309")
    ax.text(10.15, 27.2, "全国:65+占比15.6%", fontsize=8.5, color="#64748b")
    ax.text(10.15, 4.6, "全国:人均GDP 9.97万元", fontsize=8.5, color="#64748b", rotation=90, va="bottom")
    ax.set_xlim(4, 25)
    ax.set_ylim(3, 28.5)
    ax.set_xlabel("人均GDP(2025年,万元)")
    ax.set_ylabel("65岁及以上人口占比(%,2023-24)")
    ax.set_title("图N1  收入×老龄化四象限:中国的老龄化与购买力在空间上错位(菱形为代表城市)", fontsize=12, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "n1_quadrant.png"), dpi=200)
    plt.close(fig)


def n2_elevator():
    tiers = [
        ("T1 超核心\n(京沪深+苏锡常宁)", 2.8, 3.3, "日本1988-92 / 韩国2014-18"),
        ("T2 都市圈骨干\n(杭甬穗青厦汉蓉)", 1.8, 2.6, "日本1984-88 / 韩国2006-12"),
        ("T3 普通地级市", 1.0, 1.7, "日本1978-83 / 韩国1996-2004"),
        ("T4 县域与收缩带", 0.5, 1.0, "日本1972-77 / 韩国1990-95"),
    ]
    fig, ax = plt.subplots(figsize=(9.4, 4.6))
    ys = range(len(tiers))[::-1]
    colors = [BLUE, GREEN, ORANGE, RED]
    for (label, lo, hi, note), y, c in zip(tiers, ys, colors):
        ax.barh(y, hi - lo, left=lo, height=0.52, color=c, alpha=0.85)
        ax.text(lo - 0.05, y, label, ha="right", va="center", fontsize=9.5)
        ax.text(hi + 0.06, y, note, va="center", fontsize=9.2, color="#475569")
    ax.axvline(1.39, color=RED, lw=1.1, ls="--")
    ax.text(1.41, 3.42, "全国平均$1.39万", fontsize=9, color=RED)
    ax.set_xlim(-1.1, 5.6)
    ax.set_yticks([])
    ax.set_xlabel("人均GDP(万美元,2025)")
    ax.set_title("图N2  四部电梯:中国四个层级的人均GDP区间与对应的日韩年代", fontsize=12, pad=12)
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "n2_elevator.png"), dpi=200)
    plt.close(fig)


def n3_flow_matrix():
    # 客源层级×目的地类型 客流强度(1-5,基于OTA公开数据与交通客流的量级研判)
    rows = ["T1客源", "T2客源", "T3客源", "T4客源"]
    cols = ["门户城市游\n(京沪蓉渝:演艺/首店)", "传统观光名城\n(西安桂林敦煌)", "度假带\n(三亚/环滇/崇礼)", "县域与微度假\n(县城/近郊/小城)"]
    m = np.array([
        [3, 3, 5, 4],
        [4, 4, 4, 3],
        [5, 4, 3, 2],
        [5, 3, 2, 2],
    ])
    notes = {(0, 3): "落差旅游↓", (2, 0): "仪式性上行↑", (3, 0): "首次远游↑", (0, 2): "度假常态化"}
    fig, ax = plt.subplots(figsize=(9.4, 4.9))
    im = ax.imshow(m, cmap="Blues", vmin=0, vmax=5.5)
    for i in range(4):
        for j in range(4):
            ax.text(j, i - 0.08, str(m[i, j]), ha="center", va="center", fontsize=13,
                    color="white" if m[i, j] >= 4 else "#0b2a5b", fontweight="bold")
            if (i, j) in notes:
                ax.text(j, i + 0.3, notes[(i, j)], ha="center", va="center", fontsize=8.4,
                        color="white" if m[i, j] >= 4 else "#b45309")
    ax.set_xticks(range(4)); ax.set_xticklabels(cols, fontsize=8.8)
    ax.set_yticks(range(4)); ax.set_yticklabels(rows, fontsize=10)
    ax.set_title("图N3  客源层级×目的地类型流量强度矩阵(1-5级,量级研判):“落差旅游”双向流动", fontsize=11.5, pad=12)
    fig.colorbar(im, ax=ax, shrink=0.75, label="流量强度(级)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "n3_flow_matrix.png"), dpi=200)
    plt.close(fig)


def n4_japan_dispersion():
    # 访日外国人延べ宿泊者数中"地方部"(三大都市圈以外)份额,观光厅宿泊旅行统计整理约数
    years = [2013, 2015, 2017, 2019, 2023, 2024]
    share = [33, 36, 39, 41, 32, 35]
    fig, ax = plt.subplots(figsize=(9.2, 4.5))
    ax.plot(years, share, "-o", color=BLUE, lw=2, ms=5)
    ax.axhspan(30, 33, color="#fef2f2", zorder=0)
    ax.annotate("2013-2019:免签扩围+地方机场开航\n地方部份额6年提升8个百分点", xy=(2017, 39),
                xytext=(2013.2, 42.5), fontsize=9, color=BLUE,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.9))
    ax.annotate("疫后回补期重新向都市圈集中\n(2023),之后再度扩散", xy=(2023, 32), xytext=(2019.5, 27.5),
                fontsize=9, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=0.9))
    ax.text(2013.2, 30.7, "中国2025年状态:入境外国人过夜高度集中于少数门户城市,扩散尚未开始", fontsize=9,
            color="#b45309")
    ax.set_ylim(25, 46)
    ax.set_ylabel("地方部占外国人过夜量份额(%)")
    ax.set_title("图N4  日本入境游的“地方扩散”:门户先行,地方部承接第二波增量", fontsize=12, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "n4_japan_dispersion.png"), dpi=200)
    plt.close(fig)


def n5_kaigo():
    # 日本介护保险:介护给付费用(万亿日元)与要介护认定者数(万人),厚生劳动省整理约数
    years = [2000, 2005, 2010, 2015, 2020, 2023]
    cost = [3.6, 5.7, 7.4, 9.5, 10.7, 11.5]
    certified = [256, 432, 506, 620, 682, 708]
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.plot(years, cost, "-o", color=RED, lw=2, ms=5, label="介护费用(万亿日元,左轴)")
    ax.set_ylabel("介护费用(万亿日元)", color=RED)
    ax.set_ylim(0, 13)
    ax2 = ax.twinx()
    ax2.plot(years, certified, "-s", color=BLUE, lw=2, ms=5, label="要介护/要支援认定者(万人,右轴)")
    ax2.set_ylabel("认定者数(万人)", color=BLUE)
    ax2.set_ylim(0, 800)
    ax.annotate("2000年介护保险开办:\n“支付制度先行,产业随支付而生”", xy=(2000, 3.6), xytext=(2001, 8.6),
                fontsize=9.5, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=0.9))
    ax.text(2012, 1.0, "23年间费用增3.2倍、认定者增2.8倍;介护就业超200万人", fontsize=9, color="#475569")
    lines = ax.get_lines() + ax2.get_lines()
    ax.legend(lines, [l.get_label() for l in lines], frameon=False, fontsize=9.5, loc="center right")
    ax.set_title("图N5  日本介护保险开办后的产业曲线(2000-2023):中国长护险的先行剧本", fontsize=12, pad=12)
    ax.spines[["top"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "n5_kaigo.png"), dpi=200)
    plt.close(fig)


def n6_dependency():
    with open(os.path.join(DATA, "oldage_dependency.json"), encoding="utf-8") as f:
        raw = json.load(f)
    d = {iso: {int(y): v for y, v in s.items()} for iso, s in raw.items()}
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    for iso, name, c in [("JPN", "日本", BLUE), ("KOR", "韩国", GREEN), ("CHN", "中国", RED)]:
        yrs = sorted(d[iso])
        ax.plot(yrs, [d[iso][y] for y in yrs], color=c, lw=2.0 if iso == "CHN" else 1.6, label=name)
    ax.annotate("中国2025:21.4\n≈日本1998年水平", xy=(2025, 21.4), xytext=(2002, 34), fontsize=9,
                color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=0.9))
    ax.annotate("日本2025:51.0\n(每2个劳动年龄人口抚养1位老人)", xy=(2025, 51.0), xytext=(1988, 52),
                fontsize=9, color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.9))
    ax.set_ylabel("老年抚养比(65+/15-64,%)")
    ax.set_xlim(1960, 2026)
    ax.set_title("图N6  中日韩老年抚养比(1960-2025):中国的斜率正在追上日本的历史斜率", fontsize=12, pad=12)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "n6_dependency.png"), dpi=200)
    plt.close(fig)


def n7_inbound_aligned():
    # 政策拐点对齐:日本t0=2012(签证放宽前夜)、中国t0=2023(重启+免签扩围起点)
    jp_t = list(range(0, 8))
    jp_v = [8.4, 10.4, 13.4, 19.7, 24.0, 28.7, 31.2, 31.9]  # 2012-2019 访日外国人(百万)
    cn_t = [0, 1, 2]
    cn_v = [13.8, 26.9, 35.2]  # 2023-2025 入境外国人(百万,文旅部/统计公报口径,2023为约数)
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.plot(jp_t, jp_v, "-o", color=BLUE, lw=1.8, ms=5, label="日本访日外国人(t0=2012)")
    ax.plot(cn_t, cn_v, "-o", color=RED, lw=2.2, ms=6, label="中国入境外国人(t0=2023)")
    for t, v, y in [(0, 8.4, 2012), (3, 19.7, 2015), (7, 31.9, 2019)]:
        ax.annotate(str(y), (t, v), textcoords="offset points", xytext=(4, -13), fontsize=8.5, color=BLUE)
    for t, v, y in [(0, 13.8, 2023), (2, 35.2, 2025)]:
        ax.annotate(str(y), (t, v), textcoords="offset points", xytext=(4, -13), fontsize=8.5, color=RED)
    ax.annotate("中国前两年斜率超过日本同段:\n免签政策弹性+基数中的商务/口岸客流", xy=(2, 35.2),
                xytext=(3.1, 22), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=0.9))
    ax.set_xlabel("政策拐点后的年数")
    ax.set_ylabel("入境外国人(百万人次)")
    ax.set_title("图N7  政策拐点对齐:中国入境游正走在日本2013-2015的起跳段上", fontsize=12, pad=12)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "n7_inbound_aligned.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    n1_quadrant()
    n2_elevator()
    n3_flow_matrix()
    n4_japan_dispersion()
    n5_kaigo()
    n6_dependency()
    n7_inbound_aligned()
    print("charts2 generated:", sorted(f for f in os.listdir(OUT) if f.startswith("n")))
