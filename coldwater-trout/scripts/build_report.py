#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将研究报告写成可打印 HTML，并由 Chrome 导出 PDF。"""
from __future__ import annotations

import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data", "inventory.json")
HTML = os.path.join(ROOT, "report.html")
PDF = os.path.join(ROOT, "东北三省虹鳟冷水鱼适宜水域研究报告.pdf")


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def rows_sites(inv, province=None):
    items = inv["sites"]
    if province:
        items = [s for s in items if s["province"] == province]
    out = []
    for s in items:
        loc = f"{s['province']}{s['city']}{s['county']}"
        out.append(
            f"<tr><td>{s['id']}</td><td>{s['name']}</td><td>{loc}</td>"
            f"<td>{s['water']}</td><td>{s['t_summer']}</td>"
            f"<td>{s['suit']}</td><td>{s['mode']}；{s['protect']}</td></tr>"
        )
    return "\n".join(out)


def rows_counties(inv, province):
    items = [c for c in inv["counties"] if c["province"] == province]
    order = {"高度适宜": 0, "适宜": 1, "条件适宜": 2, "限制主导": 3, "不适宜": 4}
    items = sorted(items, key=lambda c: (order.get(c["suit"], 9), c["city"], c["name"]))
    out = []
    for c in items:
        cls = {
            "高度适宜": "lv-high",
            "适宜": "lv-ok",
            "条件适宜": "lv-cond",
            "限制主导": "lv-ban",
            "不适宜": "lv-no",
        }.get(c["suit"], "")
        out.append(
            f"<tr><td>{c['city']}</td><td>{c['name']}</td>"
            f"<td class='{cls}'>{c['suit']}</td><td>{c['reason']}</td></tr>"
        )
    return "\n".join(out)


def count_suit(inv, province, level):
    return sum(1 for c in inv["counties"] if c["province"] == province and c["suit"] == level)


def html_doc(inv):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>辽宁、吉林、黑龙江虹鳟及冷水鱼适宜水域研究报告</title>
<style>
@page {{
  size: A4;
  margin: 18mm 16mm 18mm 16mm;
  @bottom-center {{
    content: "东北三省虹鳟冷水鱼适宜水域研究 · 第 " counter(page) " 页";
    font-size: 8.5pt; color: #94a3b8;
    font-family: "WenQuanYi Micro Hei", "Noto Sans CJK SC", sans-serif;
  }}
}}
@page cover {{ margin: 0; @bottom-center {{ content: none; }} }}
* {{ box-sizing: border-box; }}
body {{
  font-family: "WenQuanYi Micro Hei", "Noto Sans CJK SC", "Source Han Sans SC", sans-serif;
  font-size: 10.4pt; line-height: 1.78; color: #1e293b; margin: 0;
}}
.cover {{
  page: cover; width: 210mm; height: 296mm;
  background: linear-gradient(155deg, #042f2e 0%, #0f766e 48%, #134e4a 100%);
  color: #fff; position: relative; padding: 34mm 20mm;
}}
.cover .tag {{
  display: inline-block; border: 1px solid rgba(255,255,255,.45);
  padding: 2mm 5.5mm; font-size: 10pt; letter-spacing: 2px; border-radius: 2mm;
}}
.cover h1 {{ font-size: 24pt; margin: 16mm 0 4mm; line-height: 1.45; }}
.cover h2 {{ font-size: 12.5pt; font-weight: 400; color: #99f6e4; margin: 0 0 10mm; }}
.cover .line {{ width: 40mm; height: 1.1mm; background: #5eead4; margin-bottom: 10mm; }}
.cover .points {{ font-size: 10.3pt; color: #ccfbf1; line-height: 2.05; }}
.cover .points span {{ color: #5eead4; margin-right: 3mm; }}
.cover .meta {{
  position: absolute; bottom: 20mm; left: 20mm; right: 20mm;
  border-top: 1px solid rgba(255,255,255,.28); padding-top: 5mm;
  font-size: 9.2pt; color: #ccfbf1; line-height: 1.85;
}}
h1.sec {{
  font-size: 14.5pt; color: #115e59;
  border-left: 3.6mm solid #0f766e; padding-left: 3.6mm;
  margin: 7mm 0 3.5mm; page-break-after: avoid;
}}
h2.sub {{ font-size: 12pt; color: #0f766e; margin: 5.5mm 0 2mm; page-break-after: avoid; }}
p {{ margin: 2mm 0; text-align: justify; }}
.newpage {{ page-break-before: always; }}
.summary-box, .keybox, .warnbox {{
  border-radius: 2mm; padding: 3.4mm 5mm; margin: 3.2mm 0; font-size: 10pt;
}}
.summary-box {{ background: #f0fdfa; border: 1px solid #99f6e4; }}
.keybox {{ background: #f8fafc; border-left: 2.4mm solid #0ea5e9; }}
.warnbox {{ background: #fff7ed; border-left: 2.4mm solid #ea580c; }}
.summary-box li {{ margin: 1.3mm 0; }}
table {{
  width: 100%; border-collapse: collapse; margin: 3mm 0; font-size: 8.7pt;
  page-break-inside: auto;
}}
th {{ background: #115e59; color: #fff; padding: 1.6mm 2.2mm; text-align: left; font-weight: 500; }}
td {{ border-bottom: 0.25mm solid #e2e8f0; padding: 1.5mm 2.2mm; vertical-align: top;
      word-break: keep-all; overflow-wrap: break-word; }}
tr:nth-child(even) td {{ background: #f8fafc; }}
table.compact td, table.compact th {{ font-size: 8pt; padding: 1.2mm 1.6mm; }}
.lv-high {{ color: #0f766e; font-weight: 700; }}
.lv-ok {{ color: #0d9488; font-weight: 700; }}
.lv-cond {{ color: #b45309; font-weight: 700; }}
.lv-ban {{ color: #c2410c; font-weight: 700; }}
.lv-no {{ color: #64748b; }}
figure {{ margin: 3.5mm 0; text-align: center; page-break-inside: avoid; }}
figure img {{ max-width: 100%; }}
figcaption {{ font-size: 8.4pt; color: #64748b; margin-top: 1mm; }}
.refs {{ font-size: 8.6pt; color: #475569; line-height: 1.75; }}
.refs li {{ margin: 1mm 0; word-break: break-all; }}
.note {{ font-size: 8.8pt; color: #64748b; }}
.toc a {{ color: #115e59; text-decoration: none; }}
.toc li {{ margin: 1.2mm 0; }}
ul {{ margin: 1.5mm 0 2mm 5mm; }}
</style>
</head>
<body>

<div class="cover">
  <div class="tag">资源区划 · 冷水渔业专题</div>
  <h1>辽宁、吉林、黑龙江<br>虹鳟及冷水鱼适宜水域研究报告</h1>
  <h2>—— 结合河流水温、上下游水库与水源保护区的县区尺度区划与地图标注</h2>
  <div class="line"></div>
  <div class="points">
    <div><span>◆</span>虹鳟最适生长水温 12–18℃，周年不宜超过 24℃，溶氧宜 ≥6 mg/L</div>
    <div><span>◆</span>高度适宜区集中在长白山—张广才岭—小兴安岭山泉溪流带</div>
    <div><span>◆</span>大伙房—桓仁—凤鸣、松花湖、碧流河、兴凯湖等水源/保护地限制投饲养殖</div>
    <div><span>◆</span>推荐“库区退出、山泉转入、坝下利用、设施闭环”的空间策略</div>
    <div><span>◆</span>报告附三省县区分级表、代表性水域清单与可下载专题地图</div>
  </div>
  <div class="meta">
    <div>研究范围：辽宁省、吉林省、黑龙江省（县/市/区尺度）</div>
    <div>编制日期：2026年9月</div>
    <div>资料来源：国家与地方标准、养殖水域滩涂规划、水源保护区批复、公开科研与政务报道（详见文末）</div>
    <div>性质说明：本研究为综合研判图，不替代各市县法定养殖水域滩涂规划与环评许可</div>
  </div>
</div>

<h1 class="sec">目录</h1>
<ol class="toc">
<li>摘要与核心结论</li>
<li>研究对象、方法与分级标准</li>
<li>虹鳟对水温与水质的刚性约束</li>
<li>东北河流水温资源格局</li>
<li>上下游水库、水源地与保护区约束</li>
<li>辽宁省适宜水域及所属县区</li>
<li>吉林省适宜水域及所属县区</li>
<li>黑龙江省适宜水域及所属县区</li>
<li>专题地图与图表</li>
<li>比较、布局建议与风险</li>
<li>参考资料</li>
<li>附录：代表性水域与县区全表</li>
</ol>

<h1 class="sec">一、摘要与核心结论</h1>
<p>虹鳟（<i>Oncorhynchus mykiss</i>）是东北三省最具代表性的引进冷水性养殖鱼类。1959年发眼卵落户黑龙江宁安渤海后，产业沿长白山—张广才岭—辽东山地扩展，形成“山泉流水为主、水库坝下为辅、大水面网箱审慎试点”的格局。本报告把<b>水温资源</b>与<b>水库/水源保护区空间管制</b>叠置到县区尺度，回答三个问题：哪些河段与山溪真正适合养虹鳟；哪些库区虽然冷、但不能养；适宜水体分别隶属哪些县（市、区）。</p>
<div class="summary-box">
<b>核心结论</b>
<ul>
<li><b>高度适宜区呈“东山带”分布</b>：辽宁本溪南芬区、本溪满族自治县、宽甸满族自治县；吉林江源、抚松、靖宇、长白、临江、安图；黑龙江宁安、海林及伊春友好、汤旺、丰林、乌翠、伊美。共同特征是山泉/上游溪流周年最高水温多不超过 20℃，溶氧充足，且主体不在饮用水源一级保护区。</li>
<li><b>水温适宜 ≠ 可以养殖</b>。桓仁水库、凤鸣输水河道、大伙房水库、松花湖（丰满）、碧流河、兴凯湖等水域夏季底层或坝下可能很冷，但因饮用水源、风景名胜或自然保护区，<b>禁止或严格限制投饲网箱</b>。2019年松花湖 115 处拦网已全部拆除。</li>
<li><b>平原河段基本不适宜</b>。辽河、嫩江下游、松嫩平原池塘夏季表层常达 24–28℃，超过虹鳟停食阈值，即使政策口径的“冷水渔业振兴”也不等于虹鳟适养。</li>
<li><b>最优技术路径</b>不是重开库区网箱，而是：保护地外山泉流水池塘 + 发电水库<b>坝下/底层低温水</b> + 尾水循环的设施渔业；大水面仅可在非水源、非核心保护地做低密度生态或严格环评的深水网箱。</li>
<li>三省已形成差异化产业锚点：辽宁“南芬虹鳟”地理标志与本溪全市约 860 亩冷水水面；吉林东部流水池塘约 14 万平方米、年商品鱼 700 余吨；黑龙江宁安种源地 + 海林莲花湖网箱示范 + 伊春、五大连池新兴基地。</li>
</ul>
</div>
<div class="keybox"><b>县区数量（本研究分级，不含未列入的平原不适宜县）</b>　辽宁：高度适宜 {count_suit(inv,'辽宁','高度适宜')}、适宜 {count_suit(inv,'辽宁','适宜')}、条件适宜 {count_suit(inv,'辽宁','条件适宜')}、限制主导 {count_suit(inv,'辽宁','限制主导')}。吉林：高度适宜 {count_suit(inv,'吉林','高度适宜')}、适宜 {count_suit(inv,'吉林','适宜')}、条件适宜 {count_suit(inv,'吉林','条件适宜')}、限制主导 {count_suit(inv,'吉林','限制主导')}。黑龙江：高度适宜 {count_suit(inv,'黑龙江','高度适宜')}、适宜 {count_suit(inv,'黑龙江','适宜')}、条件适宜 {count_suit(inv,'黑龙江','条件适宜')}。</div>

<h1 class="sec newpage">二、研究对象、方法与分级标准</h1>
<h2 class="sub">2.1 对象与尺度</h2>
<p>对象以虹鳟为主，兼顾金鳟、三倍体虹鳟（市场常称“淡水三文鱼”）及细鳞、哲罗等土著冷水鱼的空间重叠。空间单元为<b>县（市、区）</b>，并点状标注代表性水体。时间基准为 2018—2026 年公开资料，水温采用文献实测与水文气候综合区间，而非逐日监测序列。</p>
<h2 class="sub">2.2 资料与方法</h2>
<p>研究叠置四类信息：①虹鳟养殖技术规范与地方标准中的水温、溶氧、流速阈值；②东北山区流水养殖试验（白山江源、长白十五道沟等）的实测水温；③各省养殖水域滩涂规划中的禁养区、限养区；④大伙房、桓仁—凤鸣、丰满水库、碧流河、兴凯湖、镜泊湖等水源地/保护地批复与整改案例。底图采用阿里云 DataV 县区界，在 GCS_WGS_1984 下制图。</p>
<h2 class="sub">2.3 五级适宜性定义</h2>
<table>
<tr><th style="width:16%">等级</th><th>判定要点</th><th>典型空间含义</th></tr>
<tr><td class="lv-high">高度适宜</td><td>山泉或上游溪流为主，生长季水温大体落在 8–18℃，周年峰值多 ≤20℃；已有稳定产业或明确试验数据；不在水源一级保护区。</td><td>可优先布局苗种场与流水商品鱼</td></tr>
<tr><td class="lv-ok">适宜</td><td>冷水资源明确，但规模、盛夏升温或局部保护地切割使其略逊于第一档。</td><td>宜在支流山溪发展，慎入干流敞水</td></tr>
<tr><td class="lv-cond">条件适宜</td><td>水温基本可养，但位于水源汇水区、生长季过短、或必须设施化才能达标。</td><td>循环水、尾水治理、避让一级区</td></tr>
<tr><td class="lv-ban">限制主导</td><td>饮用水源一级区、已拆除网箱/拦网的湖库、国家级自然保护区核心水体。</td><td>禁止投饲养殖，只允许净水增殖</td></tr>
<tr><td class="lv-no">不适宜</td><td>松嫩—辽河平原夏季高温河段、城市建成区污染河道。</td><td>不建议发展虹鳟</td></tr>
</table>
<div class="warnbox">未列入分级表的县区，默认按“不适宜或缺乏冷水资源”处理（主要为沈阳、长春、哈尔滨平原区，齐齐哈尔、大庆、松原、白城，辽西锦阜朝大部分等）。地图灰色即此含义。</div>

<h1 class="sec">三、虹鳟对水温与水质的刚性约束</h1>
<p>虹鳟是鲑科中相对耐温的种类，但远不能按鲤科温水鱼方式进大湖、进平原塘。综合 NY/T 5161、SC/T 1030.6、DB2105/T 009—2023《地理标志产品 南芬虹鳟鱼》及吉林省水产科学研究院试验：</p>
<table>
<tr><th>指标</th><th>阈值 / 要求</th><th>对东北选址的含义</th></tr>
<tr><td>生存极限</td><td>约 0–30℃（实践中 26℃已极危险）</td><td>不能用“冬天冷”证明夏天也能养</td></tr>
<tr><td>适宜 / 最适生长</td><td>7–20℃ / <b>12–18℃（峰值 16–18℃）</b></td><td>山泉与坝下低温水最匹配</td></tr>
<tr><td>胁迫阈值</td><td>&lt;7℃ 或 &gt;20℃ 食欲下降；<b>&gt;24℃ 停食</b></td><td>松花湖、桓仁库表、辽河平原夏季出局</td></tr>
<tr><td>溶氧</td><td>健壮生长 ≥6.0–6.4 mg/L，南芬苗种要求 ≥6 mg/L</td><td>必须流水或底层冷水，静水塘不适合</td></tr>
<tr><td>水质</td><td>符合 GB 11607；pH 约 6.5–8.5；低氨氮</td><td>城市下游、尾矿汇水、稻田退水需谨慎</td></tr>
<tr><td>流水池塘</td><td>水温宜 &lt;20℃；注水量常见 ≥50 L/s；池塘宜长条形</td><td>适合沟谷山泉，不适合平原大塘</td></tr>
<tr><td>网箱</td><td>适宜 7–20℃；流速约 0.3–0.5 m/s；吉林要求水深宜 20 m 以上、覆盖率 ≤0.2%，20–25℃ 持续时间不宜超过 1 个月</td><td>仅少数深水非水源水库可试点</td></tr>
<tr><td>水源类型</td><td>山泉、溪流、井水、水库底层/坝下渗水、洁净河水</td><td>发电水库下游是被标准明确写入的冷水区</td></tr>
</table>
<p>2018 年 8–10 月，江源森源良种场山泉水温 9.2–13.8℃、溶氧 7.55–10.16 mg/L；长白十五道沟 7.7–12.4℃、溶氧 7.83–11.33 mg/L。两处均证明长白山区山泉可支撑三倍体虹鳟幼鱼规模化培育，且水温略高（仍低于 14℃）的一组生长更快——说明“越冷越好”并不成立，<b>12℃ 左右比 8℃ 更利于生长</b>。</p>

<h1 class="sec newpage">四、东北河流水温资源格局</h1>
<p>东北冷水并不是均匀铺在三省，而是被地貌切成三条“冷廊”和两大“热盆”：</p>
<h2 class="sub">4.1 三条冷廊</h2>
<ul>
<li><b>长白山—鸭绿江—图们江源区</b>（吉林白山、延边，辽宁宽甸、桓仁山溪）：火山岩与玄武岩裂隙泉、高森林覆盖，山泉水温常年 1–17℃。这是虹鳟生长稳定性最好的区域。</li>
<li><b>张广才岭—老爷岭—牡丹江上游</b>（吉林敦化，黑龙江宁安、海林、穆棱、东宁，哈尔滨尚志、五常东部）：涌泉与山溪并存。宁安钻心湖以矿泉水质著称，严寒气温下仍不冻，是全国虹鳟种源地。</li>
<li><b>小兴安岭—汤旺河—沾河</b>（伊春各区县、逊克、孙吴、五大连池山口湖、绥棱、庆安）：夏季凉爽，溶氧高，但北部生长季短，更适合与细鳞、哲罗等土著冷水鱼混配布局。</li>
</ul>
<h2 class="sub">4.2 两大热盆与干流升温</h2>
<ul>
<li><b>辽河—浑河中下游平原</b>：夏季河温常 24–28℃，完全不适合虹鳟。</li>
<li><b>松嫩平原</b>：嫩江中下游、松花江哈尔滨以下干流夏季表层多超过 20℃，政策上的“冷水渔业”更多指向寒地大宗鱼、稻渔和土著鱼，而不是虹鳟敞水养殖。</li>
</ul>
<p>水库使温度结构复杂化：夏季表层可升至 20–25℃，底层和发电尾水常保持 8–16℃。因此，<b>同一座水库可以同时是“表层不宜、底层/坝下可利用、水源区又不能投饲”</b>。这是本报告把“水温资源”和“保护区”分开评价的原因。</p>
<figure>
<img src="charts/chart6_temperature.png" alt="水温对照">
<figcaption>图6 代表性水域水温区间与虹鳟 12–18℃ 最适窗口、20℃ / 24℃ 胁迫线对照</figcaption>
</figure>

<h1 class="sec">五、上下游水库、水源地与保护区约束</h1>
<p>农业农村部养殖水域滩涂规划规范要求与饮用水源、自然保护地、防洪区衔接。吉林全省规划禁养区约占规划水域 30.4%，限养区 21.5%。对虹鳟而言，真正“一票否决”的是<b>投饲型网箱进入水源一级区和保护地核心水体</b>。</p>
<table>
<tr><th>水体</th><th>所属</th><th>保护属性</th><th>对虹鳟的含义</th></tr>
<tr><td>大伙房水库</td><td>抚顺顺城/东洲等</td><td>辽宁中部城市群饮用水源</td><td>禁止投饲养殖；汇水区清原、新宾严控</td></tr>
<tr><td>桓仁水库</td><td>桓仁满族自治县（跨吉林汇水）</td><td>大伙房水源一级区，县规划库区约 8075 公顷禁养</td><td>库内退出；山泉支流可养</td></tr>
<tr><td>凤鸣水库及输水河道</td><td>桓仁</td><td>桓仁坝下至凤鸣约 20.5 km 一级保护区</td><td>禁止养殖</td></tr>
<tr><td>观音阁、清河、碧流河</td><td>本溪县 / 清河区 / 庄河</td><td>城市供水</td><td>库区限养；坝下冷水或汇水区外山溪可论证</td></tr>
<tr><td>松花湖（丰满）</td><td>丰满区、永吉、蛟河</td><td>中部城市引松供水，2025 年批复水源保护区</td><td>115 处拦网已拆；只做鲢鳙净水渔业</td></tr>
<tr><td>白山湖、红石湖</td><td>桦甸、抚松等</td><td>松花江梯级 + 三湖保护</td><td>限制投饲网箱，支流山溪更优</td></tr>
<tr><td>镜泊湖</td><td>宁安</td><td>风景名胜 / 保护地</td><td>增殖与观光；虹鳟主战场在钻心湖山泉</td></tr>
<tr><td>莲花水库</td><td>海林</td><td>水电为主，非城市主水源</td><td>已试点虹鳟深水网箱，须控密度与残饵</td></tr>
<tr><td>兴凯湖</td><td>密山、虎林</td><td>国家级自然保护区</td><td>禁止养殖开发</td></tr>
<tr><td>长白山国家公园 / 龙湾</td><td>抚松、安图、辉南</td><td>自然保护地</td><td>核心区禁止；外围山溪特许或避让</td></tr>
<tr><td>三江保护区</td><td>抚远、同江等</td><td>湿地与跨境河流</td><td>虹鳟不是优先品种</td></tr>
</table>
<div class="keybox"><b>上下游逻辑</b>：上游县的投饲尾水会进入下游水源地。通化、集安、新宾、清原的山溪即使水温适宜，也必须按“汇水区设施化、尾水不入一级区”管理。辽吉已建立浑江协同共治机制，虹鳟项目环评应把下游桓仁供水安全写进约束。</div>
<figure>
<img src="charts/map5_protection.png" alt="保护区约束图">
<figcaption>图5 上下游水库水源地与保护地的空间约束（虚线圆为研究示意影响圈，不是法定边界）</figcaption>
</figure>

<h1 class="sec newpage">六、辽宁省：适宜水域及所属县区</h1>
<p>辽宁冷水鱼的产业重心在辽东山地，不在辽河平原。南芬区山泉被称作“冷泉水”，地理标志“南芬虹鳟鱼”保护范围覆盖思山岭、南芬、铁山、郭家、下马塘 5 个街道；地方标准要求水源以山泉为宜、全年水温不超过 20℃，苗种阶段 8–18℃。本溪市已把模式推广到本溪县、桓仁县，全市可利用冷水养殖面积约 860 亩、养殖户 121 户、品种 20 余个，并转向设施大棚循环水，以节省山泉、控制尾水。</p>
<h2 class="sub">6.1 空间判断</h2>
<ul>
<li><b>第一梯队</b>：南芬区、本溪满族自治县、宽甸满族自治县。太子河上游、蒲石河、半拉江山溪是虹鳟主体水源。</li>
<li><b>第二梯队</b>：桓仁（山泉而非库区）、凤城叆河上游、岫岩大洋河上游、西丰清河源、本溪市区河谷山泉。</li>
<li><b>水源冲突带</b>：清原、新宾、抚顺大伙房周边、桓仁库区与凤鸣河道、庄河碧流河、铁岭清河水库——水温或坝下冷水有利用价值，但<b>不能做投饲大水面</b>。</li>
<li><b>不适宜</b>：沈阳、盘锦、锦州、阜新及辽河、浑河中下游县城。</li>
</ul>
<figure>
<img src="charts/map2_liaoning.png" alt="辽宁地图">
<figcaption>图2 辽宁省虹鳟适宜水域与所属县区</figcaption>
</figure>
<h2 class="sub">6.2 县区分级表</h2>
<table>
<tr><th>所属市</th><th>县（市、区）</th><th>等级</th><th>主要依据</th></tr>
{rows_counties(inv, "辽宁")}
</table>

<h1 class="sec newpage">七、吉林省：适宜水域及所属县区</h1>
<p>吉林东部山区是松花江、图们江、鸭绿江源区。省政府渔业格局把金鳟、虹鳟流水池塘放在白山、延边，面积约 14 万平方米、年产商品鱼 700 余吨，山泉水三倍体虹鳟已进入京沪市场。与此同时，中部松花湖走的是完全相反的路：拆除拦网、改净水渔业、划定丰满水库饮用水水源保护区。</p>
<h2 class="sub">7.1 空间判断</h2>
<ul>
<li><b>第一梯队</b>：江源、抚松、靖宇、长白、临江、安图。江源湾沟山泉 1–17℃；十五道沟 8–10 月仅 7.7–12.4℃；二道白河需避开长白山国家公园核心区。</li>
<li><b>第二梯队</b>：敦化、和龙、汪清、龙井、通化县、柳河、辉南、集安、桦甸、蛟河。辉南龙湾、通化浑江分别受保护地和桓仁上游汇水约束。</li>
<li><b>限制带</b>：丰满区、永吉及松花湖水体——禁止投饲网箱/拦网。</li>
<li><b>不适宜</b>：长春、四平、辽源大部、松原、白城等中西部平原。</li>
</ul>
<figure>
<img src="charts/map3_jilin.png" alt="吉林地图">
<figcaption>图3 吉林省虹鳟适宜水域与所属县区</figcaption>
</figure>
<h2 class="sub">7.2 县区分级表</h2>
<table>
<tr><th>所属市（州）</th><th>县（市、区）</th><th>等级</th><th>主要依据</th></tr>
{rows_counties(inv, "吉林")}
</table>

<h1 class="sec newpage">八、黑龙江省：适宜水域及所属县区</h1>
<p>黑龙江是中国虹鳟养殖的原点，也是当前省级“冷水渔业振兴”（2022–2026）的主战场。需要区分两个概念：政策文件中的“冷水渔业”包含稻渔、大白鱼、鲟鳇、银鲫等寒地品种；<b>虹鳟只适合其中山溪、涌泉和少数深水湖库</b>。</p>
<p>宁安渤海镇钻心湖（镜心湖）承接 1959 年朝鲜赠送发眼卵，后建成虹鳟良种场，2013 年“宁安虹鳟鱼”获农产品地理标志，保护范围约 10468 公顷，包括镜泊湖、钻心湖一带，主养区在钻心湖。海林依托莲花湖 6.2 万亩水面，2025 年首次开展虹鳟网箱，宣称生长周期可缩短约 50%。伊春友好区已建千亩级冷水鱼基地；五大连池规划以山口湖为核心养殖虹鳟、细鳞、黑斑狗鱼。</p>
<h2 class="sub">8.1 空间判断</h2>
<ul>
<li><b>第一梯队</b>：宁安（钻心湖山泉系统）、海林（山溪 + 有条件的莲花湖）、伊春友好 / 汤旺 / 丰林 / 乌翠 / 伊美。</li>
<li><b>第二梯队</b>：穆棱、东宁、林口、尚志、五常东部、延寿、方正、通河、木兰、南岔、大箐山、金林、嘉荫、五大连池（山口湖而非风景区天池）、逊克、孙吴、绥棱、庆安、萝北、铁力。</li>
<li><b>限制带</b>：镜泊湖保护地、兴凯湖保护区、三江湿地；莲花湖可试点但必须密度与残饵双控。</li>
<li><b>条件带</b>：大兴安岭漠河、塔河、呼玛——太冷、生长季太短；黑龙江干流同江—抚远——政策热、虹鳟不是最优种。</li>
<li><b>不适宜</b>：齐齐哈尔、大庆、绥化平原县、哈尔滨主城。</li>
</ul>
<figure>
<img src="charts/map4_heilongjiang.png" alt="黑龙江地图">
<figcaption>图4 黑龙江省虹鳟适宜水域与所属县区</figcaption>
</figure>
<h2 class="sub">8.2 县区分级表</h2>
<table>
<tr><th>所属市（地）</th><th>县（市、区）</th><th>等级</th><th>主要依据</th></tr>
{rows_counties(inv, "黑龙江")}
</table>

<h1 class="sec newpage">九、专题地图与结构图表</h1>
<figure>
<img src="charts/map1_northeast_overview.png" alt="总图">
<figcaption>图1 东北三省虹鳟及冷水鱼适宜水域县区区划总图</figcaption>
</figure>
<p>总图把“东山冷、西原热”和“库区红叉、山泉绿点”同时画出来：绿色县区沿长白山—张广才岭—小兴安岭连成一条东北—西南向的冷水产业带；灰色覆盖松嫩平原与辽河平原；紫色方块标出必须优先服从供水与保护地管制的水库。</p>
<figure>
<img src="charts/chart7_county_structure.png" alt="县区结构">
<figcaption>图7 三省已分级县区的适宜性结构</figcaption>
</figure>
<figure>
<img src="charts/chart8_modes.png" alt="养殖方式">
<figcaption>图8 代表性水域推荐养殖方式结构</figcaption>
</figure>

<h1 class="sec">十、比较、布局建议与风险</h1>
<h2 class="sub">10.1 三省比较</h2>
<table>
<tr><th></th><th>辽宁</th><th>吉林</th><th>黑龙江</th></tr>
<tr><td>资源禀赋</td><td>辽东山地山泉，纬度偏低、生长季较长</td><td>长白山源区水质最优、温度最稳</td><td>种源地 + 山溪带宽，北部积温偏低</td></tr>
<tr><td>产业锚点</td><td>南芬地理标志、本溪设施化</td><td>白山—延边流水池塘 14 万㎡</td><td>宁安良种、海林网箱、伊春/五大连池新兴</td></tr>
<tr><td>最大约束</td><td>大伙房—桓仁供水安全</td><td>松花湖水源与三湖保护</td><td>保护地切割、北部生长季短、政策口径过宽</td></tr>
<tr><td>推荐主模式</td><td>山泉流水 + 大棚循环水</td><td>山泉流水苗种/商品鱼</td><td>山泉流水为主，莲花湖审慎网箱</td></tr>
</table>
<h2 class="sub">10.2 可落地的空间策略</h2>
<ul>
<li><b>优先带（可扩大）</b>：南芬—本溪县—宽甸；江源—抚松—靖宇—长白—临江—安图；宁安钻心湖—海林山溪—敦化；伊春汤旺河沿岸。</li>
<li><b>转换带（库退泉进）</b>：桓仁、清原、新宾、丰满、永吉、宁安镜泊湖周边——把产能从一级水源和风景湖面转到保护区外的山泉与循环水车间。</li>
<li><b>坝下带（工程利用）</b>：观音阁、红石、白山、莲花等发电水库下游，用低温尾水做流水池，避免进入库面投饲。</li>
<li><b>不建议带</b>：辽河/嫩江平原敞水、水源一级区、自然保护区核心、兴凯湖、松花湖。</li>
</ul>
<h2 class="sub">10.3 主要风险</h2>
<div class="warnbox">
<b>环境风险</b>：投饲残饵与药物是水源地最敏感的压力，也是中央环保督察反复点名湖库网箱的原因。<br>
<b>气候风险</b>：辽东、延边低海拔河谷在极端高温年可能短暂超过 20℃，需有遮阴、加大流量或循环降温预案。<br>
<b>生物风险</b>：虹鳟逃逸可能影响细鳞、哲罗、茴鱼等土著冷水鱼，鸭绿江、图们江、牡丹江上游应设置防逃。<br>
<b>政策风险</b>：县级养殖水域滩涂规划若调整禁养区，已建项目可能退出；选址必须以现行规划为准。<br>
<b>市场风险</b>：国内虹鳟/三文鱼供给仍远低于进口，但品质与药残决定溢价，不能走“高密度换产量”。
</div>
<p>综上，东北三省虹鳟的真正资源不在大湖大库的“水面数字”，而在<b>东部长白—张广才岭—小兴安岭的山泉与发电尾水</b>；真正的红线不在技术能不能养，而在<b>下游数千万人口的饮水安全和保护地法律</b>。县区尺度上把二者分开标注，是本报告地图的核心用途。</p>

<h1 class="sec newpage">十一、参考资料</h1>
<ol class="refs">
<li>SC/T 1030.6—1999《虹鳟养殖技术规范 网箱饲养食用鱼技术》；SC/T 1030.5 池塘饲养技术。农业部。</li>
<li>NY/T 5161—2002《无公害食品 虹鳟养殖技术规范》。</li>
<li>DB2105/T 009—2023《地理标志产品 南芬虹鳟鱼》，本溪市地方标准。保护范围：南芬区现辖行政区域；水源以山泉为宜，全年水温不超过 20℃。</li>
<li>柳鹏, 高春山, 杜晓燕, 等. 中国东北山区虹鳟三倍体幼鱼生长特性研究. 大连海洋大学学报, 2020. 试验点：白山森源良种场、长白十五道沟。</li>
<li>吉林省水产科学研究院. 三倍体虹鳟养殖技术（吉林城乡网转载, 2022）。流水池塘适宜 12–20℃，网箱水域水温应低于 25℃ 且 20–25℃ 不超过 1 个月。</li>
<li>吉林省农业农村厅. 《吉林省养殖水域滩涂规划（2019—2030年）》(2020). 禁养区 24.83 万公顷（30.43%），限养区 17.55 万公顷（21.51%）。</li>
<li>吉林省人民政府. 《关于吉林市丰满水库饮用水水源保护区划定方案的批复》（吉政函〔2025〕63号）。</li>
<li>国际在线 / 中新网. 吉林松花湖 115 处拦网全部拆除（2019）。</li>
<li>人民网吉林频道. 依托白山松水禀赋 做强吉林生态特色渔业（2026-08-24）。白山、延边金鳟虹鳟流水池塘约 14 万平方米。</li>
<li>吉林城乡网. 泉水清清凭鱼跃（2020）。江源湾沟山泉水温常年 1–17℃。</li>
<li>辽宁省人民政府 / 本溪市农业农村局. 本溪：冷水鱼游出“热”产业（2024-07）。全市冷水养殖约 860 亩、121 户。</li>
<li>辽宁省生态环境厅. 对省人大《关于成立辽宁省水源地桓仁水库监管机构的建议》的答复。大伙房水源保护区含抚顺大伙房、桓仁水库及汇水、两条输水河道。</li>
<li>桓仁满族自治县人民政府. 养殖水域滩涂规划文本：禁止养殖区 8792.33 公顷，含桓仁水库一级区 8075.26 公顷、凤鸣及输水河道 715.37 公顷。</li>
<li>辽宁省人民政府关于划定大伙房饮用水水源保护区的批复（辽政〔2009〕172号）。</li>
<li>中国水产科学研究院黑龙江水产研究所. 虹鳟鱼——一个冷水性鱼引进种在我国的发展史。1959 年宁安东京城（渤海）落户。</li>
<li>宁安市人民政府 / 农产品地理标志相关公开材料. 宁安虹鳟鱼；钻心湖虹鳟鱼养殖基地（2024）。</li>
<li>牡丹江市农业农村局 / 黑龙江省人民政府网站. 牡丹江冷水鱼产业观察（2025）。海林莲花湖虹鳟网箱示范。</li>
<li>黑龙江省农业农村厅. 《黑龙江省加快冷水渔业振兴发展若干政策措施（2024—2026年）》；《黑龙江省冷水渔业振兴行动方案（2022—2026年）》。</li>
<li>中国食品安全报. 黑龙江伊春市：让特色养殖创造热经济（友好区冷水鱼基地）。</li>
<li>五大连池市公开报道. 山口湖冷水鱼规划（虹鳟、细鳞、黑斑狗鱼）。</li>
<li>GB 11607—1989《渔业水质标准》；《中华人民共和国水污染防治法》关于饮用水水源保护区的禁止性规定。</li>
<li>行政区划底图：阿里云 DataV GeoAtlas 省/市/县界（areas_v3）。</li>
</ol>
<p class="note">水温数值来自文献实测、地方标准与区域水文气候综合，用于区划判断，不能替代场址逐月监测。项目落地须以所在县养殖水域滩涂规划、水源保护区划、自然保护地准入和环评为准。</p>

<h1 class="sec newpage">十二、附录　代表性水域清单</h1>
<p class="note">下表对应地图点位。完整县区表见各章；机器可读文件见 data/sites.csv、data/counties.csv。</p>
<table class="compact">
<tr>
<th>编号</th><th>水域</th><th>所属县区</th><th>类型</th>
<th>生长期水温℃</th><th>等级</th><th>推荐方式与保护约束</th>
</tr>
{rows_sites(inv)}
</table>
<p class="note">报告全文、专题地图 PNG 与本 PDF 同目录发布，可直接下载打印。</p>

</body>
</html>
"""


def write_html(inv):
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html_doc(inv))
    print("html:", HTML)


def write_pdf():
    cmd = [
        "timeout", "50",
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF}",
        "--print-to-pdf-no-header",
        "--virtual-time-budget=8000",
        f"file://{HTML}",
    ]
    print("chrome:", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(PDF) or os.path.getsize(PDF) < 10000:
        print(r.stdout)
        print(r.stderr)
        raise SystemExit(r.returncode or 1)
    print("pdf:", PDF, "bytes", os.path.getsize(PDF), "chrome_rc", r.returncode)


def main():
    inv = load()
    write_html(inv)
    if "--no-pdf" in sys.argv:
        return
    write_pdf()


if __name__ == "__main__":
    main()
