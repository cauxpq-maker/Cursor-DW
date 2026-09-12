# -*- coding: utf-8 -*-
"""生成《通化玉皇山公园升级改造专题研究报告》配套图表"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

FONT = "WenQuanYi Micro Hei"
plt.rcParams["font.sans-serif"] = [FONT]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 150

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(OUT, exist_ok=True)

C_MAIN = "#2E6E4E"   # 山林绿
C_SUB = "#C9A227"    # 玉皇金
C_BLUE = "#3A6EA5"   # 浑江蓝
C_RED = "#B04A3A"    # 砖红
C_GRAY = "#8A8F98"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


# 图1 通化市旅游总量增长（真实数据+官方目标）
fig, ax1 = plt.subplots(figsize=(7.6, 4.2))
years = ["2024年\n(雪季77万滑雪人次)", "2025年\n(实际)", "2026年\n(官方目标)"]
visitors = [2100, 2800, 3000]   # 万人次（2024为按官方增速回推的约值）
spend = [260, 350, 400]         # 亿元
x = np.arange(len(years))
b = ax1.bar(x - 0.18, visitors, width=0.36, color=C_MAIN, label="接待游客（万人次）")
ax1.set_ylabel("接待游客（万人次）", color=C_MAIN)
ax1.set_ylim(0, 3600)
for i, v in enumerate(visitors):
    ax1.text(x[i] - 0.18, v + 60, f"{v}", ha="center", fontsize=10, color=C_MAIN, fontweight="bold")
ax2 = ax1.twinx()
ax2.bar(x + 0.18, spend, width=0.36, color=C_SUB, label="旅游总花费（亿元）")
ax2.set_ylabel("旅游总花费（亿元）", color="#8a6d1a")
ax2.set_ylim(0, 520)
for i, v in enumerate(spend):
    ax2.text(x[i] + 0.18, v + 10, f"{v}", ha="center", fontsize=10, color="#8a6d1a", fontweight="bold")
ax1.set_xticks(x); ax1.set_xticklabels(years, fontsize=9.5)
ax1.set_title("通化市旅游接待量与旅游总花费快速攀升", fontsize=13, fontweight="bold")
h1, l1 = ax1.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=9)
ax1.text(0.99, -0.16, "数据来源：通化市政府工作报告（2025年2800万人次/350亿元；2026年目标3000万/400亿）；2024年为约值",
         transform=ax1.transAxes, ha="right", fontsize=7.5, color=C_GRAY)
save(fig, "01_tourism_growth.png")

# 图2 万峰雪场雪季跃升（冬季联动依据）
fig, ax = plt.subplots(figsize=(7.6, 4.2))
seasons = ["2024-25雪季", "2025-26雪季"]
wf_visitors = [77.0, 112.24]   # 全市滑雪场接待（万人次）
wf_rev = [0.9, 1.11]           # 亿元（24-25为约值）
x = np.arange(2)
ax.bar(x - 0.17, wf_visitors, width=0.34, color=C_BLUE, label="全市雪场接待（万人次）")
for i, v in enumerate(wf_visitors):
    ax.text(x[i] - 0.17, v + 2, f"{v:.1f}万", ha="center", fontsize=10, color=C_BLUE, fontweight="bold")
ax2 = ax.twinx()
ax2.bar(x + 0.17, wf_rev, width=0.34, color=C_SUB, label="雪场营收（亿元）")
for i, v in enumerate(wf_rev):
    ax2.text(x[i] + 0.17, v + 0.03, f"{v:.2f}亿", ha="center", fontsize=10, color="#8a6d1a", fontweight="bold")
ax2.set_ylim(0, 1.6)
ax.set_ylim(0, 150)
ax.set_xticks(x); ax.set_xticklabels(seasons, fontsize=11)
ax.set_ylabel("接待游客（万人次）", color=C_BLUE)
ax2.set_ylabel("营收（亿元）", color="#8a6d1a")
ax.set_title("万峰雪场跃升“百万级”：冬季客流即在城边，玉皇山承接近在咫尺", fontsize=12.5, fontweight="bold")
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=9)
ax.text(0.99, -0.13, "数据来源：通化市文旅局/中国吉林网：2025-26雪季全市雪场112.24万人次、营收1.11亿元，万峰首破百万人次、营收破亿",
        transform=ax.transAxes, ha="right", fontsize=7.5, color=C_GRAY)
save(fig, "02_wanfeng_growth.png")

# 图3 沈白高铁带来的客流
fig, ax = plt.subplots(figsize=(7.6, 4.2))
items = ["通化站日均发送\n（开通首月）", "通化站日均发送\n（2026春运）", "通化站春运峰值\n（单日）"]
vals = [3000, 4400, 7000]
bars = ax.bar(items, vals, color=[C_BLUE, C_MAIN, C_RED], width=0.5)
for b_, v in zip(bars, vals):
    ax.text(b_.get_x() + b_.get_width() / 2, v + 120, f"{v}人次", ha="center", fontsize=11, fontweight="bold")
ax.set_ylim(0, 8200)
ax.set_ylabel("旅客发送量（人次/日）")
ax.set_title("沈白高铁（2025.9.28开通）：通化站为全线新建站客流第一", fontsize=13, fontweight="bold")
ax.text(0.5, 0.92, "全线首月运送旅客超66万人次｜通化—长白山最快约1小时｜北京朝阳—长白山4小时33分",
        transform=ax.transAxes, ha="center", fontsize=9, color=C_BLUE,
        bbox=dict(boxstyle="round,pad=0.4", fc="#EAF1F8", ec=C_BLUE, lw=0.8))
ax.text(0.99, -0.13, "数据来源：国铁集团、吉林省政府网（2025.10—2026.3公开报道）",
        transform=ax.transAxes, ha="right", fontsize=7.5, color=C_GRAY)
save(fig, "03_hsr_flow.png")

# 图4 全国高温趋势（避暑需求）
fig, ax = plt.subplots(figsize=(7.6, 4.2))
yrs = [1990, 2000, 2010, 2013, 2017, 2022, 2024]
hot_days = [7.8, 9.0, 10.4, 13.0, 13.7, 16.4, 16.7]
ax.plot(yrs, hot_days, marker="o", color=C_RED, lw=2.2, label="全国平均高温日数（35°C以上，天）")
ax.fill_between(yrs, hot_days, color=C_RED, alpha=0.10)
for xi, yi in zip(yrs, hot_days):
    ax.text(xi, yi + 0.35, f"{yi}", ha="center", fontsize=9, color=C_RED)
ax.axhline(22, color=C_MAIN, ls="--", lw=1.6)
ax.text(1991, 20.3, "通化夏季平均气温约22°C（森林覆盖率66.64%）", fontsize=9.5, color=C_MAIN, fontweight="bold")
ax.set_ylim(5, 24)
ax.set_ylabel("高温日数（天）")
ax.set_title("全球变暖背景下高温日数持续增多，“22°C的夏天”成稀缺资源", fontsize=13, fontweight="bold")
ax.legend(loc="upper left", fontsize=9)
ax.text(0.99, -0.15, "数据来源：国家气候中心公开发布（约值示意）；通化气候数据来源：吉林省文旅厅",
        transform=ax.transAxes, ha="right", fontsize=7.5, color=C_GRAY)
save(fig, "04_heat_trend.png")

# 图5 新时代客群结构（目标市场，测算示意）
fig, (axl, axr) = plt.subplots(1, 2, figsize=(10.5, 4.4))
labels = ["家庭亲子客群", "年轻潮玩/研学客群", "康养银发客群", "滑雪度假联动客群", "高铁过境中转客群"]
sizes = [30, 25, 18, 15, 12]
colors = [C_MAIN, C_SUB, C_BLUE, "#6FA8DC", C_RED]
w, t, a = axl.pie(sizes, labels=labels, autopct="%1.0f%%", colors=colors, startangle=90,
                  textprops={"fontsize": 9}, pctdistance=0.72)
axl.set_title("改造后目标客群结构（测算示意）", fontsize=12, fontweight="bold")
needs = ["夜间消费/夜游", "沉浸体验/打卡", "亲子互动", "康养慢游", "轻户外/微度假", "文化认同/怀旧"]
score = [92, 88, 85, 78, 82, 75]
axr.barh(needs[::-1], score[::-1], color=C_MAIN, alpha=0.85)
for i, v in enumerate(score[::-1]):
    axr.text(v + 1, i, f"{v}", va="center", fontsize=9.5, fontweight="bold", color=C_MAIN)
axr.set_xlim(0, 105)
axr.set_xlabel("需求强度指数（100为最强，行业调研综合示意）")
axr.set_title("新时代客群六大核心需求", fontsize=12, fontweight="bold")
fig.text(0.99, 0.01, "说明：结构与指数为基于文旅行业公开调研的规划测算示意", ha="right", fontsize=7.5, color=C_GRAY)
save(fig, "05_customer_structure.png")

# 图6 四季运营互补（与万峰错峰互补）
fig, ax = plt.subplots(figsize=(8.2, 4.2))
months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
wanfeng = [95, 100, 55, 0, 0, 0, 0, 0, 0, 0, 45, 90]        # 万峰客流指数
park = [70, 78, 45, 40, 62, 78, 95, 100, 72, 68, 42, 65]     # 玉皇山改造后客流指数
x = np.arange(12)
ax.plot(x, wanfeng, marker="s", color=C_BLUE, lw=2, label="万峰雪场客流指数（雪季11月—次年3月）")
ax.plot(x, park, marker="o", color=C_MAIN, lw=2, label="玉皇山公园（改造后）客流指数")
ax.fill_between(x, park, color=C_MAIN, alpha=0.08)
ax.axvspan(5, 8, color=C_SUB, alpha=0.12)
ax.text(6.5, 8, "避暑旺季", ha="center", fontsize=9.5, color="#8a6d1a", fontweight="bold")
ax.axvspan(0, 2, color=C_BLUE, alpha=0.08); ax.axvspan(10, 11, color=C_BLUE, alpha=0.08)
ax.text(1, 8, "冰雪旺季", ha="center", fontsize=9.5, color=C_BLUE, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(months)
ax.set_ylabel("客流指数（100=峰值）")
ax.set_title("“白天滑雪在万峰、夜晚消费在城里”：玉皇山与万峰全年客流互补（规划示意）", fontsize=12, fontweight="bold")
ax.legend(fontsize=9, loc="upper center")
ax.set_ylim(0, 118)
save(fig, "06_season_synergy.png")

# 图7 市场空白：过境地 vs 目的地
fig, (axl, axr) = plt.subplots(1, 2, figsize=(10.5, 4.2))
cats = ["通化市区现状", "成熟旅游目的地城市"]
stay = [1.2, 2.5]
bars = axl.bar(cats, stay, color=[C_GRAY, C_MAIN], width=0.45)
for b_, v in zip(bars, stay):
    axl.text(b_.get_x() + b_.get_width() / 2, v + 0.05, f"{v}天", ha="center", fontsize=12, fontweight="bold")
axl.set_ylim(0, 3.2)
axl.set_ylabel("游客平均停留（天）")
axl.set_title("停留时间差距 = 消费流失（调研示意）", fontsize=12, fontweight="bold")
gaps = ["城区夜游夜演", "山地亲子乐园", "城市观景地标", "冬季戏雪(市区)", "文化沉浸体验", "康养休闲业态"]
gap_v = [85, 80, 90, 75, 70, 65]
axr.barh(gaps[::-1], gap_v[::-1], color=C_RED, alpha=0.8)
for i, v in enumerate(gap_v[::-1]):
    axr.text(v + 1, i, f"{v}%", va="center", fontsize=9.5, color=C_RED, fontweight="bold")
axr.set_xlim(0, 105)
axr.set_xlabel("市场空白度（100%=完全空白，规划评估示意）")
axr.set_title("通化市区文旅业态空白度评估", fontsize=12, fontweight="bold")
save(fig, "07_market_gap.png")

# 图8 营收提升50%瀑布图
fig, ax = plt.subplots(figsize=(9.2, 4.6))
labels8 = ["基准营收\n(工作表05/06)", "夜游经济\n+灯光秀二销", "冬季项目\n+万峰联动", "高铁客群\n套票渠道", "研学团建\n会员年卡", "文创餐饮\n二销升级", "动态定价\n+智慧转化", "提升后\n营收"]
inc = [100, 13, 11, 8, 7, 6, 5, 150]
starts = [0, 100, 113, 124, 132, 139, 145, 0]
colors8 = [C_GRAY, C_MAIN, C_BLUE, C_SUB, "#6FA8DC", "#A47C48", "#7E57C2", C_RED]
for i, (s, h, c) in enumerate(zip(starts, inc, colors8)):
    ax.bar(i, h, bottom=s, color=c, width=0.62)
    top = s + h
    txt = f"+{h}%" if 0 < i < 7 else f"{h}%"
    ax.text(i, top + 3, txt, ha="center", fontsize=10.5, fontweight="bold",
            color=c if i not in (0, 7) else "#333")
    if 0 < i < 7:
        ax.plot([i - 0.31, i + 0.69], [top, top], color="#bbb", lw=0.8, ls="--")
ax.set_xticks(range(8)); ax.set_xticklabels(labels8, fontsize=8.8)
ax.set_ylabel("营收指数（基准=100%）")
ax.set_ylim(0, 172)
ax.set_title("营业收入提升50%路径拆解（在工作表05/06基准之上）", fontsize=13, fontweight="bold")
save(fig, "08_revenue_uplift.png")

# 图9 各经营项目成本结构与毛利率
fig, ax = plt.subplots(figsize=(9.6, 4.8))
projects = ["架空观景\n(桁架栈道/塔)", "山地游乐\n(滑道/无动力)", "冬季戏雪\n冰灯夜游", "夜游光影秀", "餐饮茶咖", "文创零售", "研学团建\n营地活动", "演艺庙会\n活动"]
labor = [12, 18, 20, 15, 28, 12, 25, 30]
energy = [8, 6, 15, 18, 10, 3, 5, 8]
maint = [15, 14, 10, 12, 5, 2, 6, 7]
material = [0, 2, 5, 0, 32, 45, 12, 10]
mkt = [5, 5, 6, 6, 3, 4, 7, 10]
gross = [100 - (a + b + c + d + e) for a, b, c, d, e in zip(labor, energy, maint, material, mkt)]
x = np.arange(len(projects))
bot = np.zeros(len(projects))
for data, name, color in [(labor, "人工", C_BLUE), (energy, "能耗", C_RED), (maint, "维护折旧/租赁", C_GRAY),
                          (material, "物料/进货", "#A47C48"), (mkt, "营销渠道", "#7E57C2"), (gross, "毛利", C_MAIN)]:
    ax.bar(x, data, bottom=bot, label=name, color=color, width=0.62,
           alpha=0.92 if name == "毛利" else 0.85)
    bot += np.array(data, dtype=float)
for i, g in enumerate(gross):
    ax.text(x[i], 102, f"毛利率\n{g}%", ha="center", fontsize=8.6, color=C_MAIN, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(projects, fontsize=8.6)
ax.set_ylabel("占营收比例（%）")
ax.set_ylim(0, 118)
ax.set_title("各经营项目成本结构与毛利率测算（占营收比，行业参数估算）", fontsize=13, fontweight="bold")
ax.legend(ncol=6, fontsize=8.6, loc="lower center", bbox_to_anchor=(0.5, -0.24))
save(fig, "09_cost_structure.png")

print("all charts done")
