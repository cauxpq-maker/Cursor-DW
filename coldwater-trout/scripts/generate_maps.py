#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成东北三省虹鳟/冷水鱼适宜水域研究地图与图表。"""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, patheffects
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch
from shapely.geometry import MultiPolygon, Polygon, shape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")
GEO = os.path.join(DATA, "geo")
COUNTY_DIR = os.path.join(GEO, "county")
OUT = os.path.join(ROOT, "charts")
os.makedirs(OUT, exist_ok=True)

FONT = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
font_manager.fontManager.addfont(FONT)
plt.rcParams["font.family"] = "WenQuanYi Micro Hei"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["savefig.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "#f8fafc"

SUIT_COLOR = {
    "高度适宜": "#0f766e",
    "适宜": "#2dd4bf",
    "条件适宜": "#fbbf24",
    "限制主导": "#f97316",
    "不适宜": "#e2e8f0",
}
SUIT_ORDER = ["高度适宜", "适宜", "条件适宜", "限制主导", "不适宜"]
SITE_MARK = {
    "高度适宜": ("o", "#0f766e", 55),
    "适宜": ("o", "#0ea5e9", 48),
    "条件适宜": ("D", "#ca8a04", 42),
    "限制主导": ("X", "#c2410c", 50),
    "不适宜": ("s", "#94a3b8", 36),
}

RIVERS = {
    "黑龙江": [(121.5, 53.3), (123.5, 53.4), (126.0, 51.7), (127.5, 50.2), (129.5, 49.4),
              (131.0, 48.3), (132.5, 47.7), (134.0, 48.3), (135.0, 48.5)],
    "嫩江": [(124.7, 51.0), (125.2, 50.2), (125.0, 49.2), (124.6, 48.5), (124.2, 47.3),
            (123.9, 46.3), (124.5, 45.5), (125.2, 45.4)],
    "松花江": [(128.05, 42.00), (127.6, 42.4), (127.2, 42.7), (126.9, 43.2),
              (126.75, 43.7), (126.6, 44.8), (126.6, 45.8), (127.0, 46.3),
              (129.5, 46.8), (130.4, 47.2), (132.5, 47.65)],
    "牡丹江": [(128.23, 43.37), (128.9, 43.87), (129.1, 44.2), (129.4, 44.6),
              (129.5, 45.4), (129.6, 46.3)],
    "鸭绿江": [(128.1, 41.9), (127.4, 41.7), (126.9, 41.8), (126.2, 41.1),
              (125.5, 40.9), (124.8, 40.5), (124.4, 40.1)],
    "浑江": [(126.6, 41.9), (126.0, 41.7), (125.6, 41.5), (125.42, 41.28)],
    "太子河": [(124.4, 41.4), (124.1, 41.30), (123.85, 41.20), (123.3, 41.25)],
    "辽河": [(123.8, 42.8), (123.5, 42.2), (123.3, 41.7), (122.5, 41.2)],
    "图们江": [(128.3, 42.1), (129.2, 42.6), (129.8, 42.9), (130.4, 42.9)],
    "汤旺河": [(129.3, 48.5), (129.1, 48.0), (128.9, 47.7), (129.4, 47.0)],
}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_inventory():
    return load_json(os.path.join(DATA, "inventory.json"))


def iter_polygons(geom):
    g = shape(geom)
    if isinstance(g, Polygon):
        yield g
    elif isinstance(g, MultiPolygon):
        for p in g.geoms:
            yield p
    else:
        if hasattr(g, "geoms"):
            for p in g.geoms:
                if isinstance(p, (Polygon, MultiPolygon)):
                    yield from iter_polygons(p.__geo_interface__)


def draw_feature(ax, feature, facecolor, edgecolor="#64748b", lw=0.25, alpha=0.92, z=2):
    for poly in iter_polygons(feature["geometry"]):
        xs, ys = poly.exterior.xy
        ax.fill(xs, ys, facecolor=facecolor, edgecolor=edgecolor, linewidth=lw, alpha=alpha, zorder=z)
        for ring in poly.interiors:
            ax.fill(*ring.xy, facecolor="white", edgecolor=edgecolor, linewidth=0.2, zorder=z + 0.1)


def load_all_counties():
    features = []
    for fn in sorted(os.listdir(COUNTY_DIR)):
        if not fn.endswith(".json"):
            continue
        gj = load_json(os.path.join(COUNTY_DIR, fn))
        features.extend(gj["features"])
    return features


def county_lookup(inv):
    return {c["adcode"]: c for c in inv["counties"]}


def suit_of(feat, lookup):
    ad = feat["properties"]["adcode"]
    rec = lookup.get(ad)
    if rec:
        return rec["suit"]
    return "不适宜"


def halo(text_artist):
    text_artist.set_path_effects([patheffects.withStroke(linewidth=2.4, foreground="white")])


def add_legend_suit(ax, loc="lower left"):
    handles = [Patch(facecolor=SUIT_COLOR[k], edgecolor="#334155", lw=0.4, label=k) for k in SUIT_ORDER]
    ax.legend(handles=handles, loc=loc, frameon=True, fancybox=False, fontsize=8,
              title="县区适宜性", title_fontsize=8.5, edgecolor="#cbd5e1")


def add_north(ax, x=0.93, y=0.92):
    ax.annotate("N", xy=(x, y), xytext=(x, y - 0.07), xycoords="axes fraction",
                ha="center", va="center", fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="#0f172a", lw=1.2))


def style_map(ax, title, subtitle=None):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#cbd5e1")
    ax.set_title(title, fontsize=13.5, pad=10, color="#0f172a", loc="left")
    if subtitle:
        ax.text(0.0, 1.0, subtitle, transform=ax.transAxes, fontsize=8,
                color="#475569", va="bottom", ha="left")


def plot_rivers(ax, clip=None):
    for name, pts in RIVERS.items():
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color="#2563eb", lw=1.05, alpha=0.55, zorder=4, solid_capstyle="round")


def plot_sites(ax, sites, labels=True, size_scale=1.0):
    for s in sites:
        mk, color, size = SITE_MARK[s["suit"]]
        ax.scatter(s["lon"], s["lat"], marker=mk, s=size * size_scale, c=color,
                   edgecolors="white", linewidths=0.6, zorder=6)
        if labels:
            t = ax.text(s["lon"] + 0.08, s["lat"] + 0.05, s["name"], fontsize=6.2,
                        color="#0f172a", zorder=7)
            halo(t)


def plot_reservoirs(ax, reservoirs, labels=True):
    for r in reservoirs:
        ax.scatter(r["lon"], r["lat"], marker="s", s=36, c="#7c3aed",
                   edgecolors="white", linewidths=0.5, zorder=5, alpha=0.9)
        if labels:
            t = ax.text(r["lon"] + 0.08, r["lat"] - 0.12, r["name"], fontsize=6,
                        color="#5b21b6", zorder=7)
            halo(t)


def map_overview(inv, counties):
    lookup = county_lookup(inv)
    fig, ax = plt.subplots(figsize=(11.2, 13.2))
    for feat in counties:
        draw_feature(ax, feat, SUIT_COLOR[suit_of(feat, lookup)])
    for code in ("210000", "220000", "230000"):
        gj = load_json(os.path.join(GEO, f"{code}_full.json"))
        for feat in gj["features"]:
            draw_feature(ax, feat, "none", edgecolor="#1e293b", lw=0.55, alpha=1, z=3)
    plot_rivers(ax)
    plot_sites(ax, inv["sites"], labels=False, size_scale=0.85)
    plot_reservoirs(ax, inv["reservoirs"], labels=False)
    # 重点标注
    for s in inv["sites"]:
        if s["suit"] in ("高度适宜", "限制主导"):
            t = ax.text(s["lon"] + 0.12, s["lat"] + 0.06, s["name"], fontsize=6.4,
                        color="#0f172a", zorder=7)
            halo(t)
    ax.set_xlim(118.6, 135.6)
    ax.set_ylim(38.4, 53.8)
    style_map(ax, "图1  东北三省虹鳟及冷水鱼适宜水域县区区划总图",
              "底色为县区综合适宜性；圆点为代表性水域，紫色方块为关键水库/水源地")
    add_legend_suit(ax, "lower left")
    site_handles = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#0f766e", markersize=7, label="高度适宜水域"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#0ea5e9", markersize=7, label="适宜水域"),
        Line2D([0], [0], marker="D", color="w", markerfacecolor="#ca8a04", markersize=6, label="条件适宜水域"),
        Line2D([0], [0], marker="X", color="w", markerfacecolor="#c2410c", markersize=7, label="限制/禁养水域"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor="#7c3aed", markersize=6, label="重点水库/水源地"),
        Line2D([0], [0], color="#2563eb", lw=1.4, label="主要河流（示意）"),
    ]
    ax.legend(handles=[Patch(facecolor=SUIT_COLOR[k], edgecolor="#334155", lw=0.4, label=k) for k in SUIT_ORDER] + site_handles,
              loc="lower left", fontsize=7.4, frameon=True, ncol=1, edgecolor="#cbd5e1")
    add_north(ax)
    ax.text(0.01, 0.01, "坐标系：GCS_WGS_1984　边界：阿里云 DataV 行政区　区划为研究综合判断，非法定养殖规划图",
            transform=ax.transAxes, fontsize=6.5, color="#64748b")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "map1_northeast_overview.png"), dpi=220)
    plt.close(fig)


def map_province(inv, counties, province, xlim, ylim, fname, title, extra_labels=True):
    lookup = county_lookup(inv)
    fig, ax = plt.subplots(figsize=(11.0, 10.6))
    for feat in counties:
        name = feat["properties"]["name"]
        ad = feat["properties"]["adcode"]
        rec = lookup.get(ad)
        if rec and rec["province"] != province:
            continue
        # 用质心粗过滤，避免跨省碎片
        if rec is None:
            # 仅绘制本省：通过 adcode 前两位
            prefix = {"辽宁": "21", "吉林": "22", "黑龙江": "23"}[province]
            if not str(ad).startswith(prefix):
                continue
        draw_feature(ax, feat, SUIT_COLOR[suit_of(feat, lookup)], lw=0.35)
        if extra_labels and suit_of(feat, lookup) in ("高度适宜", "适宜", "限制主导"):
            g = shape(feat["geometry"])
            c = g.representative_point()
            if xlim[0] < c.x < xlim[1] and ylim[0] < c.y < ylim[1]:
                t = ax.text(c.x, c.y, name, fontsize=6.2, ha="center", va="center",
                            color="#0f172a", zorder=5, alpha=0.9)
                halo(t)
    plot_rivers(ax)
    sites = [s for s in inv["sites"] if s["province"] == province]
    plot_sites(ax, sites, labels=True, size_scale=1.05)
    res = [r for r in inv["reservoirs"] if xlim[0] - 0.3 <= r["lon"] <= xlim[1] + 0.3
           and ylim[0] - 0.3 <= r["lat"] <= ylim[1] + 0.3]
    plot_reservoirs(ax, res, labels=True)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    style_map(ax, title, "圆点=代表性水域　紫色方块=水库/水源地　县名仅标注较高等级或限制区")
    add_legend_suit(ax, "lower left")
    add_north(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=220)
    plt.close(fig)


def map_protection(inv, counties):
    """水源地/保护区约束专题图。"""
    lookup = county_lookup(inv)
    fig, ax = plt.subplots(figsize=(11.2, 12.4))
    restrict_counties = {c["adcode"] for c in inv["counties"] if c["suit"] in ("限制主导", "条件适宜")}
    for feat in counties:
        ad = feat["properties"]["adcode"]
        rec = lookup.get(ad)
        if rec and rec["suit"] == "限制主导":
            fc = "#fdba74"
        elif rec and rec["suit"] == "条件适宜":
            fc = "#fde68a"
        elif rec and rec["suit"] in ("高度适宜", "适宜"):
            fc = "#d1fae5"
        else:
            fc = "#f1f5f9"
        draw_feature(ax, feat, fc, edgecolor="#94a3b8", lw=0.2)
    plot_rivers(ax)
    plot_reservoirs(ax, inv["reservoirs"], labels=True)
    # 水源地影响圈（示意）
    rings = [
        (124.08, 41.88, 0.55, "大伙房水源影响圈"),
        (125.42, 41.28, 0.42, "桓仁—凤鸣水源圈"),
        (126.75, 43.70, 0.48, "松花湖水源圈"),
        (128.93, 43.87, 0.32, "镜泊湖保护地"),
        (132.40, 45.30, 0.38, "兴凯湖保护区"),
    ]
    for x, y, r, lab in rings:
        circ = plt.Circle((x, y), r, fill=False, ls="--", lw=1.3, color="#7c3aed", zorder=6)
        ax.add_patch(circ)
        ax.text(x, y + r + 0.08, lab, fontsize=7, ha="center", color="#5b21b6", zorder=7)
    ax.set_xlim(118.6, 135.6)
    ax.set_ylim(38.4, 53.8)
    style_map(ax, "图5  上下游水库水源地与保护地对虹鳟养殖的空间约束",
              "虚线圆为研究示意影响圈，不代表法定保护区精确边界；橙色系县区受水源/保护地约束更强")
    handles = [
        Patch(facecolor="#fdba74", label="限制主导县区（禁养/拆网箱）"),
        Patch(facecolor="#fde68a", label="条件适宜（汇水区或保护地切割）"),
        Patch(facecolor="#d1fae5", label="高度适宜/适宜（山泉为主）"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor="#7c3aed", markersize=7, label="重点水库/水源地"),
        Line2D([0], [0], color="#7c3aed", ls="--", lw=1.3, label="水源/保护地影响圈（示意）"),
    ]
    ax.legend(handles=handles, loc="lower left", fontsize=8, edgecolor="#cbd5e1")
    add_north(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "map5_protection.png"), dpi=220)
    plt.close(fig)


def chart_temp():
    labels = [
        "长白山山泉（江源/抚松）",
        "十五道沟山泉（长白）",
        "南芬山泉（本溪）",
        "钻心湖涌泉（宁安）",
        "汤旺河上游（伊春）",
        "太子河上游",
        "莲花湖底层/坝下",
        "鸭绿江上游",
        "牡丹江中游",
        "松花湖表层（夏）",
        "桓仁库区表层（夏）",
        "辽河平原河段（夏）",
    ]
    low = [1, 7.7, 8, 8, 7, 12, 8, 10, 14, 20, 18, 24]
    high = [17, 12.4, 20, 14, 15, 18, 14, 16, 20, 25, 24, 28]
    fig, ax = plt.subplots(figsize=(10.6, 6.4))
    y = range(len(labels))[::-1]
    ax.axvspan(12, 18, color="#99f6e4", alpha=0.45, label="虹鳟最适生长 12–18℃")
    ax.axvline(20, color="#f59e0b", ls="--", lw=1, label="食欲下降阈值 20℃")
    ax.axvline(24, color="#dc2626", ls="--", lw=1, label="停食/危险阈值 24℃")
    for yi, lo, hi in zip(y, low, high):
        ax.plot([lo, hi], [yi, yi], color="#0f766e", lw=6, solid_capstyle="round", alpha=0.85)
        ax.plot([lo], [yi], "o", color="#0f766e", ms=5)
        ax.plot([hi], [yi], "o", color="#134e4a", ms=5)
        ax.text(hi + 0.35, yi, f"{lo}–{hi}℃", va="center", fontsize=8, color="#334155")
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("水温（℃）")
    ax.set_xlim(0, 32)
    ax.set_title("图6  代表性水域水温区间与虹鳟适温窗口对照", fontsize=13, pad=10, loc="left")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart6_temperature.png"), dpi=200)
    plt.close(fig)


def chart_counts(inv):
    by_p = defaultdict(Counter)
    for c in inv["counties"]:
        by_p[c["province"]][c["suit"]] += 1
    provinces = ["辽宁", "吉林", "黑龙江"]
    fig, ax = plt.subplots(figsize=(10.2, 5.2))
    x = range(len(provinces))
    bottom = [0] * 3
    palette = [SUIT_COLOR[k] for k in SUIT_ORDER if k != "不适宜"]
    keys = [k for k in SUIT_ORDER if k != "不适宜"]
    for k, col in zip(keys, palette):
        vals = [by_p[p][k] for p in provinces]
        ax.bar(list(x), vals, bottom=bottom, color=col, width=0.55, label=k, edgecolor="white")
        bottom = [b + v for b, v in zip(bottom, vals)]
    for i, p in enumerate(provinces):
        ax.text(i, bottom[i] + 0.4, f"n={sum(by_p[p].values())}", ha="center", fontsize=8, color="#475569")
    ax.set_xticks(list(x))
    ax.set_xticklabels(provinces, fontsize=11)
    ax.set_ylabel("纳入分级的县（市、区）数量")
    ax.set_title("图7  三省已分级县区的虹鳟适宜性结构（不含明确不适宜的平原县）", fontsize=12, pad=10, loc="left")
    ax.legend(frameon=False, ncol=4, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart7_county_structure.png"), dpi=200)
    plt.close(fig)


def chart_modes(inv):
    modes = Counter()
    for s in inv["sites"]:
        m = s["mode"].split("；")[0].split("/")[0]
        if "禁止" in s["mode"] or s["suit"] == "限制主导":
            modes["限制/禁养"] += 1
        elif "网箱" in s["mode"]:
            modes["深水网箱（有条件）"] += 1
        elif "设施" in s["mode"] or "循环" in s["mode"]:
            modes["设施/循环水"] += 1
        elif "流水" in s["mode"]:
            modes["山泉流水池塘"] += 1
        else:
            modes["其他/增殖"] += 1
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    labels = list(modes.keys())
    vals = [modes[k] for k in labels]
    colors = ["#0f766e", "#0ea5e9", "#8b5cf6", "#f97316", "#94a3b8"][:len(labels)]
    ax.barh(labels[::-1], vals[::-1], color=colors[::-1], height=0.55)
    for y, v in enumerate(vals[::-1]):
        ax.text(v + 0.15, y, str(v), va="center", fontsize=10)
    ax.set_xlabel("代表性水域样本数")
    ax.set_title("图8  推荐养殖方式结构（基于代表性水域样本）", fontsize=12, pad=10, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "chart8_modes.png"), dpi=200)
    plt.close(fig)


def write_tables(inv):
    # CSV 便于附录与复核
    import csv
    path = os.path.join(DATA, "sites.csv")
    keys = ["id", "name", "province", "city", "county", "lon", "lat", "water",
            "t_summer", "t_winter", "suit", "mode", "protect", "note"]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for s in inv["sites"]:
            w.writerow({k: s.get(k, "") for k in keys})
    path2 = os.path.join(DATA, "counties.csv")
    keys2 = ["adcode", "province", "city", "name", "suit", "reason"]
    with open(path2, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=keys2)
        w.writeheader()
        for c in inv["counties"]:
            w.writerow({k: c.get(k, "") for k in keys2})


def main():
    inv = load_inventory()
    counties = load_all_counties()
    write_tables(inv)
    map_overview(inv, counties)
    map_province(inv, counties, "辽宁", (118.8, 126.2), (38.6, 43.7),
                 "map2_liaoning.png",
                 "图2  辽宁省虹鳟适宜水域与所属县区")
    map_province(inv, counties, "吉林", (121.4, 131.6), (40.7, 46.4),
                 "map3_jilin.png",
                 "图3  吉林省虹鳟适宜水域与所属县区")
    map_province(inv, counties, "黑龙江", (121.0, 135.4), (43.2, 53.7),
                 "map4_heilongjiang.png",
                 "图4  黑龙江省虹鳟适宜水域与所属县区")
    map_protection(inv, counties)
    chart_temp()
    chart_counts(inv)
    chart_modes(inv)
    print("generated:", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
