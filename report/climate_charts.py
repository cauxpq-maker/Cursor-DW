# -*- coding: utf-8 -*-
"""生成《气候变暖趋势下的暑期目的地与未来热点城市预测》专篇图表"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

for fp in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
           "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"):
    if os.path.exists(fp):
        font_manager.fontManager.addfont(fp)
        prop = font_manager.FontProperties(fname=fp)
        plt.rcParams["font.family"] = prop.get_name()
        break
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(OUT, exist_ok=True)

BLUE = "#2563eb"
RED = "#dc2626"
ORANGE = "#f59e0b"


def chart_heat_trend():
    """专篇图1：全国夏季高温日数——常态化上移"""
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.0))

    ax = axes[0]
    labels = ["常年同期均值", "2026年夏季实况"]
    vals = [8.0, 11.5]
    bars = ax.bar(labels, vals, width=0.5, color=["#94a3b8", RED])
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.15, f"{v}天", ha="center", fontsize=11)
    ax.set_ylim(0, 13.5)
    ax.set_ylabel("全国平均高温日数（天）")
    ax.set_title("图1a  2026年夏季高温日数较常年偏多3.5天", fontsize=11, pad=10)
    ax.spines[["top", "right"]].set_visible(False)

    ax = axes[1]
    labels = ["较1990年代", "较此前20年"]
    vals = [5, 2]
    bars = ax.bar(labels, vals, width=0.5, color=[ORANGE, ORANGE])
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.08, f"+{v}天", ha="center", fontsize=11)
    ax.set_ylim(0, 6)
    ax.set_ylabel("近10年高温日数增量（天）")
    ax.set_title("图1b  近10年高温日数系统性上移（气象部门监测）", fontsize=11, pad=10)
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart_c1_heat_trend.png"), dpi=200)
    plt.close(fig)


def chart_cool_premium():
    """专篇图2：2026暑期"清凉溢价"实证"""
    labels = [
        "“避暑/纳凉/夜游”搜索量（7月，环比）",
        "室内避暑场所搜索量（7月，环比）",
        "入境游机票订单（暑期，同比）",
        "“20℃清凉圈”城市机票订单（同比）",
        "洞穴主题产品预订（7月，环比）",
        "避暑黑马目的地平均增速（同比）",
        "三线及以下小机场旅客量（同比）",
    ]
    values = [270, 210, 197, 80, 72, 70, 26]
    fig, ax = plt.subplots(figsize=(9, 4.3))
    y = range(len(labels))[::-1]
    ax.barh(list(y), values, color=BLUE, height=0.6)
    for yi, v in zip(y, values):
        ax.text(v + 4, yi, f"+{v}%", va="center", fontsize=10)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=9.5)
    ax.set_xlim(0, 310)
    ax.set_xlabel("增速（%），口径见标注")
    ax.set_title("图2  2026年暑期“清凉溢价”实证：避暑与清凉资源类指标全面领涨", fontsize=12, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart_c2_cool_premium.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    chart_heat_trend()
    chart_cool_premium()
    print("climate charts generated")
