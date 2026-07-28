# -*- coding: utf-8 -*-
"""生成《人均GDP从5000到50000美元:发达经济体社会变迁与中国阶段研判》报告图表"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter

font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "charts")
DATA = os.path.join(BASE, "data")
os.makedirs(OUT, exist_ok=True)

C = {"CHN": "#dc2626", "JPN": "#2563eb", "KOR": "#059669", "USA": "#64748b"}
NAME = {"CHN": "中国", "JPN": "日本", "KOR": "韩国", "USA": "美国"}
T5K = {"USA": 1969, "JPN": 1976, "KOR": 1989, "CHN": 2011}  # 名义人均GDP首次≥5000美元


def load(name):
    with open(os.path.join(DATA, f"{name}.json"), encoding="utf-8") as f:
        raw = json.load(f)
    return {iso: {int(y): v for y, v in s.items()} for iso, s in raw.items()}


def kfmt(x, _):
    return f"{x/1000:g}万" if x >= 10000 else f"{x:g}"


def chart1_trajectory():
    gdp = load("gdp_pc_usd")
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    for iso in ["USA", "JPN", "KOR", "CHN"]:
        s = gdp[iso]
        yrs = sorted(s)
        ax.plot(yrs, [s[y] for y in yrs], color=C[iso], lw=2.2 if iso == "CHN" else 1.7,
                label=NAME[iso])
    for th, lab in [(5000, "$5,000"), (10000, "$1万"), (20000, "$2万"), (30000, "$3万"), (50000, "$5万")]:
        ax.axhline(th, color="#cbd5e1", lw=0.7, ls="--")
        ax.text(1960.5, th * 1.05, lab, fontsize=8.5, color="#64748b")
    ax.annotate("1985广场协议→日元升值", xy=(1985, 11577), xytext=(1968, 26000), fontsize=9,
                color="#2563eb", arrowprops=dict(arrowstyle="->", color="#2563eb", lw=0.9))
    ax.annotate("1991日本泡沫破裂", xy=(1991, 30000), xytext=(1994, 68000), fontsize=9,
                color="#2563eb", arrowprops=dict(arrowstyle="->", color="#2563eb", lw=0.9))
    ax.annotate("1998韩国金融危机", xy=(1998, 8281), xytext=(1994, 4300), fontsize=9,
                color="#059669", arrowprops=dict(arrowstyle="->", color="#059669", lw=0.9))
    ax.annotate("中国2025:$13,953\n(≈日本1984-85 / 韩国2002-03)", xy=(2025, 13862),
                xytext=(2006, 1000), fontsize=9, color="#dc2626",
                arrowprops=dict(arrowstyle="->", color="#dc2626", lw=0.9))
    ax.set_yscale("log")
    ax.set_ylim(150, 130000)
    ax.set_xlim(1960, 2026)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_ylabel("人均GDP(现价美元,对数轴)")
    ax.set_title("图1  中日韩美名义人均GDP轨迹(1960-2025):只有美国名义走完5千→5万美元全程", fontsize=12, pad=12)
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart1_trajectory.png"), dpi=200)
    plt.close(fig)


def chart2_aligned():
    gdp = load("gdp_pc_usd")
    fig, ax = plt.subplots(figsize=(9.2, 5.0))
    for iso in ["USA", "JPN", "KOR", "CHN"]:
        s, t0 = gdp[iso], T5K[iso]
        xs = [y - t0 for y in sorted(s) if 0 <= y - t0 <= 36]
        ax.plot(xs, [s[t0 + x] for x in xs], color=C[iso], lw=2.2 if iso == "CHN" else 1.7,
                label=f"{NAME[iso]}(t0={t0})")
    for th in [10000, 20000, 30000, 50000]:
        ax.axhline(th, color="#cbd5e1", lw=0.7, ls="--")
    ax.axvline(14, color="#fca5a5", lw=1.0, ls=":")
    ax.text(14.3, 62000, "中国当前位置\n(过$5千后第14年)", fontsize=9, color="#dc2626")
    ax.set_yscale("log")
    ax.set_ylim(4000, 110000)
    ax.set_xlim(0, 36)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_xlabel("跨越5,000美元后的年数(t0=各国名义人均GDP首次达到5,000美元的年份)")
    ax.set_ylabel("人均GDP(现价美元,对数轴)")
    ax.set_title("图2  发展阶段对齐:以跨越$5,000美元为起点的名义人均GDP路径", fontsize=12, pad=12)
    ax.legend(frameon=False, loc="lower right", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart2_aligned.png"), dpi=200)
    plt.close(fig)


def chart3_aging():
    gdp, pop = load("gdp_pc_usd"), load("pop65_share")
    fig, ax = plt.subplots(figsize=(9.2, 5.0))
    for iso in ["USA", "JPN", "KOR", "CHN"]:
        yrs = sorted(set(gdp[iso]) & set(pop[iso]))
        ax.plot([gdp[iso][y] for y in yrs], [pop[iso][y] for y in yrs],
                color=C[iso], lw=2.2 if iso == "CHN" else 1.7, label=NAME[iso])
    marks = [("CHN", 2025, "中国2025:$1.39万时65+已达15%\n(官方口径15.6%,2024年末)", (2400, 19.5)),
             ("JPN", 1985, "日本$1.2万时65+仅10.4%(1985)", (900, 12.6)),
             ("KOR", 2002, "韩国$1.4万时65+仅7.8%(2002)", (5200, 3.2)),
             ("JPN", 2008, "日本人口见顶(2008):$4.0万/65+达22.3%", (5000, 24.6))]
    for iso, y, txt, xy_t in marks:
        ax.annotate(txt, xy=(gdp[iso][y], pop[iso][y]), xytext=xy_t, fontsize=8.8,
                    color=C[iso], arrowprops=dict(arrowstyle="->", color=C[iso], lw=0.9))
    ax.set_xscale("log")
    ax.set_xlim(500, 110000)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_xlabel("人均GDP(现价美元,对数轴)")
    ax.set_ylabel("65岁及以上人口占比(%)")
    ax.set_title("图3  “未富先老”:同等收入水平下,中国的老龄化程度远高于日韩同期", fontsize=12, pad=12)
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart3_aging.png"), dpi=200)
    plt.close(fig)


def chart4_structure():
    urb, hhc = load("urban_share"), load("hh_consumption_share")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.4))
    for iso in ["USA", "JPN", "KOR", "CHN"]:
        t0 = T5K[iso]
        for ax, data in [(ax1, urb[iso]), (ax2, hhc[iso])]:
            xs = [y - t0 for y in sorted(data) if -8 <= y - t0 <= 36]
            ax.plot(xs, [data[t0 + x] for x in xs], color=C[iso],
                    lw=2.2 if iso == "CHN" else 1.6, label=NAME[iso])
    for ax, title, ylab in [(ax1, "城镇化率", "城镇人口占比(%)"),
                            (ax2, "居民消费占GDP比重", "居民最终消费/GDP(%)")]:
        ax.axvline(0, color="#cbd5e1", lw=0.8, ls="--")
        ax.axvline(14, color="#fca5a5", lw=0.8, ls=":")
        ax.set_xlabel("跨越$5,000后的年数")
        ax.set_ylabel(ylab)
        ax.set_title(title, fontsize=11)
        ax.spines[["top", "right"]].set_visible(False)
    ax1.legend(frameon=False, fontsize=9, loc="lower right")
    ax2.text(14.5, 66, "中国当前", fontsize=8.5, color="#dc2626")
    fig.suptitle("图4  阶段对齐下的结构指标:中国城镇化偏低、居民消费占比显著偏低", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(os.path.join(OUT, "chart4_structure.png"), dpi=200)
    plt.close(fig)


def chart5_cars():
    # 千人汽车保有量(全口径机动车辆,约数)。来源:日本自动车检查登录情报协会、
    # 韩国国土交通部、中国公安部、美国FHWA,经整理取整。
    data = {
        "JPN": [(1970, 170), (1980, 324), (1990, 456), (2000, 572), (2010, 592), (2023, 615)],
        "KOR": [(1985, 24), (1990, 79), (1995, 188), (2000, 238), (2010, 360), (2023, 500)],
        "CHN": [(2005, 24), (2010, 58), (2015, 118), (2020, 199), (2024, 247)],
        "USA": [(1970, 545), (1990, 758), (2010, 797), (2022, 850)],
    }
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    for iso in ["USA", "JPN", "KOR", "CHN"]:
        xs = [p[0] for p in data[iso]]
        ys = [p[1] for p in data[iso]]
        ax.plot(xs, ys, "-o", color=C[iso], lw=2.0 if iso == "CHN" else 1.6, ms=4, label=NAME[iso])
    ax.axhspan(400, 650, color="#eff6ff", zorder=0)
    ax.text(1971, 610, "东亚饱和区间:400-650辆/千人\n(土地约束下低于美国的800+)", fontsize=9, color="#2563eb")
    ax.annotate("中国2024:约247辆/千人\n≈日本1970年代中后期", xy=(2024, 247), xytext=(2003, 330),
                fontsize=9, color="#dc2626", arrowprops=dict(arrowstyle="->", color="#dc2626", lw=0.9))
    ax.set_ylabel("千人汽车保有量(辆)")
    ax.set_xlim(1968, 2027)
    ax.set_title("图5  千人汽车保有量:中国总量仍有空间,但增速已进入减档期", fontsize=12, pad=12)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart5_cars.png"), dpi=200)
    plt.close(fig)


def chart6_japan_retail():
    # 日本零售业态销售额(万亿日元,约数)。来源:日本百货店协会、日本连锁加盟协会(JFA)、
    # 经济产业省商业动态统计,经整理取整。
    years = [1980, 1985, 1991, 1997, 2000, 2005, 2008, 2013, 2019, 2024]
    dept = [5.7, 7.2, 9.7, 9.1, 8.8, 7.8, 7.4, 6.2, 6.3, 5.9]
    cvs = [0.2, 0.9, 3.1, 5.6, 6.7, 7.4, 8.0, 9.7, 11.2, 11.8]
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    ax.plot(years, dept, "-o", color="#7c3aed", lw=1.8, ms=4, label="百货店销售额")
    ax.plot(years, cvs, "-o", color="#059669", lw=1.8, ms=4, label="便利店销售额")
    ax.axvline(1991, color="#cbd5e1", lw=0.9, ls="--")
    ax.text(1985.5, 11.0, "1991泡沫破裂\n百货销售额见顶9.7万亿日元", fontsize=9, color="#7c3aed")
    ax.annotate("2008年前后便利店反超百货", xy=(2008, 8.0), xytext=(2001, 10.4), fontsize=9,
                color="#059669", arrowprops=dict(arrowstyle="->", color="#059669", lw=0.9))
    ax.set_ylim(0, 13)
    ax.set_ylabel("销售额(万亿日元,约数)")
    ax.set_title("图6  日本零售业态兴替:泡沫后百货腰斩,便利店与折扣业态穿越低增长30年", fontsize=12, pad=12)
    ax.legend(frameon=False, fontsize=10, loc="center left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart6_japan_retail.png"), dpi=200)
    plt.close(fig)


def chart7_japan_tourism():
    # 日本出入境人次(百万,约数)。来源:JNTO、日本法务省出入国管理统计,经整理。
    years_out = [1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2012, 2019, 2024]
    outbound = [0.7, 2.5, 3.9, 4.9, 11.0, 15.3, 17.8, 17.4, 18.5, 20.1, 13.0]
    years_in = [1970, 1980, 1990, 1995, 2000, 2003, 2007, 2013, 2015, 2019, 2024]
    inbound = [0.9, 1.3, 3.2, 3.3, 4.8, 5.2, 8.3, 10.4, 19.7, 31.9, 36.9]
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    ax.plot(years_out, outbound, "-o", color="#2563eb", lw=1.8, ms=4, label="日本人出境游人次")
    ax.plot(years_in, inbound, "-o", color="#dc2626", lw=1.8, ms=4, label="访日入境游人次")
    ax.annotate("1985广场协议后\n出境游5年翻倍(“爆买全球”)", xy=(1990, 11.0), xytext=(1971, 16.5),
                fontsize=9, color="#2563eb", arrowprops=dict(arrowstyle="->", color="#2563eb", lw=0.9))
    ax.annotate("2003“观光立国”宣言", xy=(2003, 5.2), xytext=(1993, 25.5), fontsize=9,
                color="#dc2626", arrowprops=dict(arrowstyle="->", color="#dc2626", lw=0.9))
    ax.annotate("2013起放宽签证+日元贬值\n入境游6年增3倍", xy=(2015, 19.7), xytext=(2000, 32.5),
                fontsize=9, color="#dc2626", arrowprops=dict(arrowstyle="->", color="#dc2626", lw=0.9))
    ax.set_ylabel("人次(百万)")
    ax.set_title("图7  日本文旅的两次浪潮:收入上行期出境游爆发→停滞期转向“入境游立国”", fontsize=12, pad=12)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart7_japan_tourism.png"), dpi=200)
    plt.close(fig)


def chart8_china_clock():
    # 中国2025年各维度所处状态对应“日本的哪一年”(基于公开数据的研判,详见正文)
    dims = [
        ("名义人均GDP($13,953)", 1984.5, "日本1984-85(≈$1.1-1.4万)"),
        ("千人汽车保有量(约247辆)", 1977, "日本1977年前后(约250辆)"),
        ("城镇化率(67%)", 1988, "接近日本1988年水平(约77%尚有差距)"),
        ("65+人口占比(15.6%)", 1998, "日本1998年(16.3%)"),
        ("总和生育率(约1.0)", 2024, "低于日本任何时期(日本最低1.15,2024)"),
        ("人口总量拐点(2022)", 2008, "日本2008-10年人口见顶"),
        ("房地产新开工见顶(2021)", 1991, "日本1991年地产泡沫见顶"),
        ("电商/移动支付渗透率", 2020, "超过日本任何时期(全球最高)"),
    ]
    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    ys = range(len(dims))[::-1]
    xs = [d[1] for d in dims]
    ax.hlines(list(ys), 1975, xs, color="#e2e8f0", lw=5)
    ax.scatter(xs, list(ys), s=110, color="#dc2626", zorder=3)
    for y, (label, x, note) in zip(ys, dims):
        ax.text(1974.2, y, label, ha="right", va="center", fontsize=10)
        ax.text(x + 0.8, y, note, va="center", fontsize=8.8, color="#475569")
    ax.axvline(1984.5, color="#fca5a5", lw=1.0, ls="--")
    ax.text(1984.5, -0.75, "收入维度基准线(日本1984-85)", fontsize=9, color="#dc2626", ha="center")
    ax.set_ylim(-1.1, 7.6)
    ax.set_xlim(1961, 2035)
    ax.set_yticks([])
    ax.set_xlabel("对应日本的年份")
    ax.set_title("图8  “多维时钟”:中国2025年各维度分别对应日本的不同年代——压缩式发展的证据", fontsize=12, pad=12)
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart8_china_clock.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    chart1_trajectory()
    chart2_aligned()
    chart3_aging()
    chart4_structure()
    chart5_cars()
    chart6_japan_retail()
    chart7_japan_tourism()
    chart8_china_clock()
    print("charts generated:", sorted(os.listdir(OUT)))
