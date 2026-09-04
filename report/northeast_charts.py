# -*- coding: utf-8 -*-
"""生成气候专篇·东北区域深度章节图表（雷达图+增速图）"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
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

DIMS = ["气候适宜度", "交通可达性", "住宿接待能力", "旅游IP/内容", "服务配套"]

# 分析性示意评分（1—10），依据文中列举的公开数据与案例综合研判
MATURE = {
    "哈尔滨": [8, 9, 9, 10, 8],
    "大连":   [8, 9, 9, 8, 8],
    "延吉(延边)": [8, 7, 7, 9, 6],
    "长春":   [8, 8, 8, 6, 7],
}
POTENTIAL = {
    "伊春":   [10, 5, 5, 6, 4],
    "阿尔山": [10, 4, 5, 6, 4],
    "本溪":   [9, 5, 4, 4, 4],
    "丹东":   [8, 6, 5, 5, 5],
}
COLORS = ["#16a34a", "#2563eb", "#f59e0b", "#8b5cf6"]


def radar(ax, data, title):
    n = len(DIMS)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]
    for (city, vals), c in zip(data.items(), COLORS):
        v = vals + vals[:1]
        ax.plot(angles, v, color=c, lw=1.8, label=city)
        ax.fill(angles, v, color=c, alpha=0.10)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(DIMS, fontsize=9)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], fontsize=7, color="#94a3b8")
    ax.set_title(title, fontsize=11.5, pad=16)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.22), ncol=4,
              frameon=False, fontsize=9)
    ax.grid(color="#e2e8f0")
    ax.spines["polar"].set_color("#cbd5e1")


def chart_ne_radar():
    """专篇图3：东北城市避暑竞争力雷达图（成熟热点 vs 潜力待补）"""
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.9),
                             subplot_kw={"projection": "polar"})
    radar(axes[0], MATURE, "图3a  成熟热点城市：气候+配套双高")
    radar(axes[1], POTENTIAL, "图3b  潜力城市：气候满分、配套与IP待补")
    fig.suptitle("图3  东北避暑城市竞争力雷达图（五维示意评分，1—10分）",
                 fontsize=12.5, y=1.0)
    fig.tight_layout(rect=[0, 0.02, 1, 0.96])
    fig.savefig(os.path.join(OUT, "chart_c3_ne_radar.png"), dpi=200,
                bbox_inches="tight")
    plt.close(fig)


def chart_ne_growth():
    """专篇图4：2026暑期东北避暑市场增速实证"""
    labels = [
        "哈尔滨包车游预订（同比）",
        "东三省7月景区订单人次（同比）",
        "东三省7月门票预订量（同比）",
        "黑龙江酒店预订量（同比）",
        "伊春/黑河/抚顺等酒店预订（同比）",
        "哈尔滨酒店预订量（同比）",
        "东北热门城市酒店预订（同比）",
        "哈尔滨文旅综合预订单量（同比）",
    ]
    values = [107, 94.7, 85.3, 70, 50, 50, 40, 32]
    fig, ax = plt.subplots(figsize=(9, 4.4))
    y = range(len(labels))[::-1]
    ax.barh(list(y), values, color="#16a34a", height=0.6)
    for yi, v in zip(y, values):
        ax.text(v + 1.5, yi, f"+{v:g}%", va="center", fontsize=10)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=9.5)
    ax.set_xlim(0, 125)
    ax.set_xlabel("同比增速（%）")
    ax.set_title("图4  2026年暑期东北避暑市场增速实证（飞猪/去哪儿/美团/新华社监测）",
                 fontsize=12, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart_c4_ne_growth.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    chart_ne_radar()
    chart_ne_growth()
    print("northeast charts generated")
