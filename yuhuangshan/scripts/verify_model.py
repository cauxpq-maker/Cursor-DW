# -*- coding: utf-8 -*-
"""校验重构模型约束，并输出图表与日志。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_engine import PROJECTS, run_model

ROOT = Path(__file__).resolve().parents[1]
ART = Path("/opt/cursor/artifacts")
OUT = ROOT / "output"
ART.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)


def pick_font():
    candidates = [
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/arphic/uming.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return p
    for p in font_manager.findSystemFonts():
        low = p.lower()
        if "wqy" in low or "microhei" in low or "droid" in low and "fallback" in low:
            return p
    return None


def style_plots():
    fp = pick_font()
    if fp:
        try:
            font_manager.fontManager.addfont(fp)
        except Exception:
            pass
        font_manager._load_fontmanager(try_read_cache=False)
    plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "Droid Sans Fallback", "DejaVu Sans"]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "white"
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.25


def assert_constraints(m):
    errors = []
    inv = m["inv"]
    if abs(inv["engineering"] - 3455.8) > 0.05:
        errors.append(f"工程费用偏离表5: {inv['engineering']}")
    if abs(inv["total"] - 4578.46) > 0.1:
        errors.append(f"总投资偏离: {inv['total']}")
    if m["years"][0]["rev"]["合计"] != 0 or m["years"][1]["rev"]["合计"] != 0:
        errors.append("建设期收入应为0")
    if m["avg_ebt_3_18"] < 3000:
        errors.append(f"年均利润总额不足: {m['avg_ebt_3_18']:.2f}")
    if m["min_ebt_3_18"] < 3000:
        errors.append(f"最低利润总额不足: {m['min_ebt_3_18']:.2f}")
    if m["payback_ops"] is None or m["payback_ops"] > 3:
        errors.append(f"回收期超3年: {m['payback_ops']}")
    y3 = m["years"][2]
    # 联营项目直接成本率应显著低于自营
    liany_rev = y3["rev"]["联营"]
    liany_cost = y3["cost_direct"]["联营"]
    if liany_rev > 0 and liany_cost / liany_rev > 0.12:
        errors.append(f"联营成本率过高: {liany_cost / liany_rev:.2%}")
    # 不新增改造项目：填充项必须标记 fill
    if y3["visitor_check"] <= y3["rev"]["合计"]:
        # 公园收入不应高于游客消费总额
        errors.append("公园收入超过游客消费总额，存在重复计算风险")
    # 人力一次
    if m["staff"]["cost"] <= 0 or m["staff"]["headcount"] > 120:
        errors.append(f"人力异常: {m['staff']}")
    return errors


def main():
    style_plots()
    m = run_model()
    errors = assert_constraints(m)
    y3 = m["years"][2]
    lines = []
    lines.append("玉皇山公园经营模型重构｜自动校验")
    lines.append("=" * 56)
    lines.append(f"总投资 {m['inv']['total']:.2f} 万元（工程 {m['inv']['engineering']:.2f}）")
    lines.append(f"贷款本金 {m['inv']['loan']:.2f} 万元，利率 4.8%")
    lines.append(f"人力 {m['staff']['headcount']} 人，年成本 {m['staff']['cost']:.2f} 万元 {m['staff']['by_type']}")
    lines.append(f"第3年收入 {y3['rev']['合计']:.2f} / 游客消费校验 {y3['visitor_check']:.2f} / 捕获率 {y3['rev']['合计']/y3['visitor_check']:.1%}")
    lines.append(f"第3年利润总额 {y3['ebt']:.2f} 净利润 {y3['net']:.2f}")
    lines.append(f"3–18年年均利润总额 {m['avg_ebt_3_18']:.2f} （目标≥3000）")
    lines.append(f"3–18年最低利润总额 {m['min_ebt_3_18']:.2f}")
    lines.append(f"3–18年年均净利润 {m['avg_net_3_18']:.2f}")
    lines.append(f"经营期静态回收期 {m['payback_ops']:.2f} 年（目标≤3）")
    lines.append(f"达产年结构 联营{y3['rev']['联营']:.1f} 自营{y3['rev']['自营']:.1f} 出租{y3['rev']['出租']:.1f} 加盟{y3['rev']['加盟']:.1f}")
    lines.append("")
    lines.append("达产年项目（收入/成本）")
    for v in y3["projects"].values():
        lines.append(f"  {v['nature']:4s} {v['name']:12s} {v['rev']:8.1f} / {v['cost']:7.1f}")
    lines.append("")
    if errors:
        lines.append("校验失败：")
        lines.extend(f"  - {e}" for e in errors)
        status = "FAIL"
    else:
        lines.append("校验通过：建设期2年、回收期≤3年、3–18年年均及最低利润总额均≥3000万元。")
        status = "PASS"
    text = "\n".join(lines)
    (OUT / "verify_model.log").write_text(text, encoding="utf-8")
    (ART / "verify_model.log").write_text(text, encoding="utf-8")
    print(text)

    summary = {
        "status": status,
        "total_investment": round(m["inv"]["total"], 2),
        "avg_ebt_3_18": round(m["avg_ebt_3_18"], 2),
        "min_ebt_3_18": round(m["min_ebt_3_18"], 2),
        "avg_net_3_18": round(m["avg_net_3_18"], 2),
        "payback_ops": round(m["payback_ops"], 2),
        "year3_revenue": round(y3["rev"]["合计"], 2),
        "year3_ebt": round(y3["ebt"], 2),
        "errors": errors,
    }
    (OUT / "verify_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (ART / "verify_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    years = [r["year"] for r in m["years"]]
    ebt = [r["ebt"] for r in m["years"]]
    rev = [r["rev"]["合计"] for r in m["years"]]
    cum = [r.get("cum_ops", 0) for r in m["years"]]
    inv_line = [m["inv"]["total"]] * 18

    # chart 1 profit
    fig, ax = plt.subplots(figsize=(11, 5.2))
    colors = ["#ADB5BD" if y <= 2 else ("#2D6A4F" if e >= 3000 else "#C92A2A") for y, e in zip(years, ebt)]
    ax.bar(years, ebt, color=colors, width=0.72)
    ax.axhline(3000, color="#C9A227", lw=1.6, ls="--", label="目标 3,000万元")
    ax.set_title("玉皇山公园第1–18年利润总额")
    ax.set_xlabel("项目年（1–2年建设期）")
    ax.set_ylabel("利润总额（万元）")
    ax.set_xticks(years)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ART / "profit_18y.png", dpi=140)
    fig.savefig(OUT / "profit_18y.png", dpi=140)
    plt.close()

    # chart 2 cash vs investment
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.plot(years, cum, color="#1B4332", lw=2.2, marker="o", ms=3.5, label="累计静态经营现金流")
    ax.plot(years, inv_line, color="#C92A2A", lw=1.6, ls="--", label=f"总投资 {m['inv']['total']:.0f}万元")
    ax.fill_between(years, cum, inv_line, where=[c >= i for c, i in zip(cum, inv_line)], color="#D8F3DC", alpha=0.8)
    ax.set_title("经营期静态回收：累计（净利+折旧）覆盖表5总投资")
    ax.set_xlabel("项目年")
    ax.set_ylabel("万元")
    ax.set_xticks(years)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ART / "payback_curve.png", dpi=140)
    fig.savefig(OUT / "payback_curve.png", dpi=140)
    plt.close()

    # chart 3 mix
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    labels = ["联营", "自营", "出租", "加盟"]
    sizes = [y3["rev"][k] for k in labels]
    ax.pie(
        sizes,
        labels=[f"{a.replace('加盟','品牌加盟')}\n{b:.0f}万" for a, b in zip(labels, sizes)],
        colors=["#F4A261", "#9B5DE5", "#4EA8DE", "#E9C46A"],
        startangle=90,
        wedgeprops=dict(width=0.45, edgecolor="white"),
    )
    ax.set_title("达产年（第3年）公园账面收入结构")
    fig.tight_layout()
    fig.savefig(ART / "revenue_mix_y3.png", dpi=140)
    fig.savefig(OUT / "revenue_mix_y3.png", dpi=140)
    plt.close()

    # chart 4 revenue vs visitor check
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.bar([y - 0.18 for y in years], rev, width=0.36, color="#2D6A4F", label="公园账面收入")
    ax.bar([y + 0.18 for y in years], [r["visitor_check"] for r in m["years"]], width=0.36, color="#74C69D", label="表6人流校验（游客消费总额）")
    ax.set_title("公园收入 vs 表6人流模型游客消费总额")
    ax.set_xlabel("项目年")
    ax.set_ylabel("万元")
    ax.set_xticks(years)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ART / "revenue_vs_visitor_model.png", dpi=140)
    fig.savefig(OUT / "revenue_vs_visitor_model.png", dpi=140)
    plt.close()

    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
