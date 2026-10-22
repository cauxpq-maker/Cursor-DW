# -*- coding: utf-8 -*-
"""生成《旅顺口区海产品养殖加工产业专题分析报告》图表。"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

FONT = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
font_manager.fontManager.addfont(FONT)
plt.rcParams["font.family"] = "WenQuanYi Micro Hei"
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(OUT, exist_ok=True)

NAVY = "#0b2a5b"
BLUE = "#2563eb"
TEAL = "#0f766e"
LIGHT = "#93c5fd"
RED = "#dc2626"
GRAY = "#64748b"
GREEN = "#059669"
AMBER = "#d97706"
ORANGE = "#ea580c"


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=200, bbox_inches="tight")
    plt.close(fig)


def chart1_two_veg_scale():
    """图1：旅顺口区“两菜”养殖面积与鲜品产量"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.4))

    names = ["海带", "裙带菜"]
    area = [3.4, 0.6]
    bars = ax1.bar(names, area, color=[NAVY, TEAL], width=0.52)
    for b, v in zip(bars, area):
        ax1.text(b.get_x() + b.get_width() / 2, v + 0.08, f"{v}万亩", ha="center", fontsize=11)
    ax1.set_ylim(0, 4.2)
    ax1.set_ylabel("万亩")
    ax1.set_title("养殖面积（当前生产口径）", fontsize=11)
    ax1.spines[["top", "right"]].set_visible(False)

    vol = [30, 6]
    bars2 = ax2.bar(names, vol, color=[BLUE, GREEN], width=0.52)
    for b, v in zip(bars2, vol):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.5, f"近{v}万吨" if v == 30 else f"约{v}万吨",
                 ha="center", fontsize=11)
    ax2.set_ylim(0, 38)
    ax2.set_ylabel("万吨（鲜品）")
    ax2.set_title("鲜品年产量", fontsize=11)
    ax2.spines[["top", "right"]].set_visible(False)

    fig.suptitle("图1  旅顺口区海带、裙带菜养殖规模（2025—2026年公开口径）", fontsize=12, y=1.02)
    _save(fig, "chart1_two_veg_scale.png")


def chart2_seed_share():
    """图2：三类苗种市场占有率对比"""
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    labels = ["海带苗", "裙带菜苗", "海胆苗"]
    share = [2, 23, 30]
    colors = [AMBER, TEAL, NAVY]
    bars = ax.barh(labels[::-1], share[::-1], color=colors[::-1], height=0.55)
    for b, v in zip(bars, share[::-1]):
        ax.text(v + 0.6, b.get_y() + b.get_height() / 2, f"{v}%", va="center", fontsize=12)
    ax.set_xlim(0, 40)
    ax.set_xlabel("在相应细分市场中的占有率（%）")
    ax.set_title("图2  旅顺口区水产苗种市场占有率：裙带菜、海胆强，海带种业偏弱", fontsize=12, pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.annotate("种业短板", xy=(2, 2), xytext=(10, 2.35),
                arrowprops=dict(arrowstyle="->", color=AMBER), color=AMBER, fontsize=10)
    _save(fig, "chart2_seed_share.png")


def chart3_value_chain():
    """图3：从鲜菜到活性提取的价值跃升对照"""
    fig, ax = plt.subplots(figsize=(10.2, 4.6))
    stages = [
        "鲜海带\n（旅顺2026）",
        "干海带粗加工\n（盐渍对应）",
        "荣成精深提取\n（1吨干海带）",
        "功能食品/\n海洋药物（示意）",
    ]
    # 统一到“每吨干海带当量”的数量级：鲜菜约750元/吨，约6吨鲜菜晒1吨干海带 → 约4500元
    values = [0.45, 4, 43, 430]
    colors = [GRAY, BLUE, TEAL, NAVY]
    bars = ax.bar(stages, values, color=colors, width=0.58)
    labels = ["约0.45万元\n（6吨鲜菜≈1吨干品）", "约4万元", "超过43万元", "再提升约10倍"]
    for b, lab in zip(bars, labels):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() * 1.05, lab,
                ha="center", va="bottom", fontsize=9)
    ax.set_yscale("log")
    ax.set_ylabel("市场价值（万元 / 吨干海带当量，对数）")
    ax.set_title("图3  海带价值链跃升：旅顺优势在原料品质，升值空间在精深加工", fontsize=12, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    _save(fig, "chart3_value_ladder.png")


def chart4_wakame_share():
    """图4：全国裙带菜产量区域格局"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.5))

    labels = ["辽宁", "山东", "其他"]
    sizes = [74.35, 25.26, 0.39]
    colors = [NAVY, BLUE, LIGHT]
    explode = (0.03, 0, 0)
    ax1.pie(sizes, labels=labels, colors=colors, explode=explode, autopct="%1.1f%%",
            startangle=90, textprops={"fontsize": 10})
    ax1.set_title("2022年全国裙带菜产量分布", fontsize=11)

    names = ["全国", "辽宁", "旅顺口（公开口径）"]
    tons = [20.61, 15.33, 6.0]
    bars = ax2.bar(names, tons, color=[GRAY, BLUE, TEAL], width=0.55)
    for b, v, t in zip(bars, tons, ["20.6万吨", "15.3万吨", "鲜品约6万吨"]):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.35, t, ha="center", fontsize=9.5)
    ax2.set_ylim(0, 25)
    ax2.set_ylabel("万吨")
    ax2.set_title("产量对照（2022年鉴 + 旅顺近年公开数）", fontsize=11)
    ax2.spines[["top", "right"]].set_visible(False)

    fig.suptitle("图4  裙带菜：辽宁占全国七成以上，旅顺是核心产区与种业高地", fontsize=12, y=1.02)
    _save(fig, "chart4_wakame_share.png")


def chart5_industry_structure():
    """图5：旅顺口区海产品产业主体结构"""
    fig, ax = plt.subplots(figsize=(9.4, 4.8))
    cats = ["海水养殖\n企业", "两菜养殖\n企业（户）", "水产加工\n企业", "其中藻类\n加工", "海带加工", "裙带菜加工", "育苗企业"]
    vals = [70, 50, 110, 60, 55, 20, 20]
    colors = [NAVY, TEAL, BLUE, GREEN, AMBER, ORANGE, GRAY]
    bars = ax.bar(cats, vals, color=colors, width=0.62)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v}余家" if v != 55 else "50—60家",
                ha="center", fontsize=9)
    ax.set_ylim(0, 135)
    ax.set_ylabel("家（公开口径，约数）")
    ax.set_title("图5  旅顺口区海产品养殖加工产业主体结构", fontsize=12, pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    _save(fig, "chart5_entities.png")


def chart6_benchmark():
    """图6：旅顺口与连江、荣成的海带产业定位对照"""
    fig, ax = plt.subplots(figsize=(10.2, 4.6))
    metrics = ["养殖规模", "原料品质", "种业能力", "初加工集群", "精深提取", "预制菜/品牌"]
    lushun = [55, 88, 70, 75, 35, 80]
    lianjiang = [95, 70, 85, 80, 45, 60]
    rongcheng = [90, 75, 70, 85, 92, 55]
    x = range(len(metrics))
    w = 0.25
    ax.bar([i - w for i in x], lushun, width=w, label="旅顺口（品质+裙带菜+预制菜）", color=TEAL)
    ax.bar(list(x), lianjiang, width=w, label="福建连江（规模+鲍鱼联动）", color=BLUE)
    ax.bar([i + w for i in x], rongcheng, width=w, label="山东荣成（精深提取）", color=NAVY)
    ax.set_xticks(list(x))
    ax.set_xticklabels(metrics, fontsize=10)
    ax.set_ylim(0, 110)
    ax.set_ylabel("相对评分（课题组综合研判，0—100）")
    ax.set_title("图6  海带主产区定位对照：旅顺应以品质溢价和精深加工补规模差距", fontsize=12, pad=10)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    _save(fig, "chart6_benchmark.png")


def chart7_output_mix():
    """图7：渔业产量与加工产值结构"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.5))

    ax1.pie(
        [70, 30],
        labels=["两菜（烫煮后）\n约15.9万吨", "其他海水养殖"],
        colors=[TEAL, LIGHT],
        autopct="%1.0f%%",
        startangle=90,
        textprops={"fontsize": 10},
    )
    ax1.set_title("2023年海水养殖产量结构", fontsize=11)

    names = ["水产品加工\n总产值", "其中藻类加工", "裙带菜加工\n营业收入", "其中出口"]
    vals = [20, 10, 5, 3.6]
    bars = ax2.bar(names, vals, color=[NAVY, TEAL, BLUE, GREEN], width=0.55)
    for b, v in zip(bars, vals):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.35, f"{v}亿元", ha="center", fontsize=10)
    ax2.set_ylim(0, 24)
    ax2.set_ylabel("亿元")
    ax2.set_title("加工环节产值（近年公开口径）", fontsize=11)
    ax2.spines[["top", "right"]].set_visible(False)

    fig.suptitle("图7  两菜占海水养殖产量七成以上，加工产值仍以藻类初加工为主", fontsize=12, y=1.02)
    _save(fig, "chart7_output_mix.png")


def chart8_calendar():
    """图8：两菜生产加工年历"""
    fig, ax = plt.subplots(figsize=(10.4, 4.2))
    months = list(range(1, 13))
    labels = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

    # 0=无 1=育苗/夹苗 2=生长期 3=收获加工高峰
    kelp = [2, 2, 2, 2, 3, 3, 2, 0, 0, 0, 1, 1]
    wakame = [2, 3, 3, 3, 2, 0, 0, 0, 0, 1, 1, 2]
    colors = {0: "#e2e8f0", 1: "#93c5fd", 2: "#38bdf8", 3: "#0f766e"}

    for i, row in enumerate([kelp, wakame]):
        for j, v in enumerate(row):
            ax.add_patch(FancyBboxPatch(
                (j + 0.08, 1 - i + 0.18), 0.84, 0.64,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                linewidth=0, facecolor=colors[v],
            ))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 2)
    ax.set_xticks([i + 0.5 for i in range(12)])
    ax.set_xticklabels(labels)
    ax.set_yticks([0.5, 1.5])
    ax.set_yticklabels(["裙带菜", "海带"])
    ax.set_title("图8  旅顺口区“两菜”生产年历：收获窗口短、加工峰值高度集中", fontsize=12, pad=10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)
    legend = [
        plt.Rectangle((0, 0), 1, 1, color="#93c5fd", label="夹苗/育苗"),
        plt.Rectangle((0, 0), 1, 1, color="#38bdf8", label="海上生长期"),
        plt.Rectangle((0, 0), 1, 1, color="#0f766e", label="收获与加工高峰"),
        plt.Rectangle((0, 0), 1, 1, color="#e2e8f0", label="海上空窗/休整"),
    ]
    ax.legend(handles=legend, frameon=False, ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.28))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart8_calendar.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    chart1_two_veg_scale()
    chart2_seed_share()
    chart3_value_chain()
    chart4_wakame_share()
    chart5_industry_structure()
    chart6_benchmark()
    chart7_output_mix()
    chart8_calendar()
    print("charts generated:", sorted(os.listdir(OUT)))
