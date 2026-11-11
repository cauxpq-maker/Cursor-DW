# -*- coding: utf-8 -*-
"""汇总中国 2005-2025 年度核心指标 -> data/china_annual.csv

来源：
- 历年《国民经济和社会发展统计公报》（data/nbs_bulletins_raw.json，由 parse_nbs_bulletins.py 解析）：
  GDP 增速、CPI、社零及增速、出口及增速、60+/65+ 人口、城镇化率
- 《中国统计年鉴 2025》表 3-1 / 7-1 / 7-4 / 24-24：修订后现价 GDP、一般公共预算收入、税收、社保基金收入
- 财政部历年《全国财政决算》《财政收支情况》：国有土地使用权出让收入、2025 年财政数据
- 人口普查：2010、2020 年年龄结构（公报未列）
"""
import json, csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

raw = {r["year"]: r for r in json.load(open(os.path.join(DATA, "nbs_bulletins_raw.json"), encoding="utf-8"))}

# 统计年鉴 2025 表 3-1：国内生产总值（现价，亿元，最终核实数；2025 为公报初步核算数）
GDP_REVISED = {
    2004: 161840.2, 2005: 187318.9, 2006: 222578.4, 2007: 274179.7, 2008: 324317.8, 2009: 354521.6,
    2010: 419253.3, 2011: 495707.6, 2012: 547510.6, 2013: 603660.4, 2014: 655782.9, 2015: 702511.5,
    2016: 761193.0, 2017: 847382.9, 2018: 936010.1, 2019: 1005872.4, 2020: 1034867.6, 2021: 1173823.0,
    2022: 1234029.4, 2023: 1294271.7, 2024: 1349083.5, 2025: 1401879.0,
}
# 统计年鉴 2025 表 7-1：一般公共预算收入（亿元）；2025 为财政部执行数
FISCAL_REVENUE = {
    2004: 26396.47, 2005: 31649.29, 2006: 38760.20, 2007: 51321.78, 2008: 61330.35, 2009: 68518.30,
    2010: 83101.51, 2011: 103874.43, 2012: 117253.52, 2013: 129209.64, 2014: 140370.03, 2015: 152269.23,
    2016: 159604.97, 2017: 172592.77, 2018: 183359.84, 2019: 190390.08, 2020: 182913.88, 2021: 202554.64,
    2022: 203649.29, 2023: 216795.43, 2024: 219734.30, 2025: 216045.0,
}
# 统计年鉴 2025 表 7-4：各项税收合计（亿元）；2025 为财政部执行数
TAX_REVENUE = {
    2004: 24165.68, 2005: 28778.54, 2006: 34804.35, 2007: 45621.97, 2008: 54223.79, 2009: 59521.59,
    2010: 73210.79, 2011: 89738.39, 2012: 100614.28, 2013: 110530.70, 2014: 119175.31, 2015: 124922.20,
    2016: 130360.73, 2017: 144369.87, 2018: 156402.86, 2019: 158000.46, 2020: 154312.29, 2021: 172735.67,
    2022: 166620.10, 2023: 181136.25, 2024: 175006.88, 2025: 176363.0,
}
# 统计年鉴 2025 表 24-24：社会保险基金收入合计（亿元，含财政补贴）；2025 为财政部决算
SOCIAL_INS_INCOME = {
    2005: 6975.2, 2010: 19276.1, 2011: 25153.3, 2012: 30738.8, 2013: 35252.9, 2014: 39827.7, 2015: 46012.1,
    2016: 53562.7, 2017: 67154.5, 2018: 79254.8, 2019: 83550.4, 2020: 75512.5, 2021: 96936.8,
    2022: 102504.8, 2023: 113214.9, 2024: 120227.0, 2025: 127849.5,
}
# 财政部历年决算/财政收支情况：国有土地使用权出让收入（亿元）
LAND_SALE_REVENUE = {
    2010: 30108.9, 2011: 33477.2, 2012: 28886.3, 2013: 41249.5, 2014: 42940.3, 2015: 32547.0,
    2016: 37456.6, 2017: 52059.0, 2018: 65095.9, 2019: 72584.4, 2020: 84142.0, 2021: 87051.0,
    2022: 66854.0, 2023: 57996.0, 2024: 48699.0, 2025: 41518.0,
}
# 公报未列年龄结构的普查年份（第六次、第七次全国人口普查）
CENSUS_AGE = {
    2010: dict(pop60_10k=17765, pop60_pct=13.26, pop65_10k=11883, pop65_pct=8.87),
    2020: dict(pop60_10k=26402, pop60_pct=18.70, pop65_10k=19064, pop65_pct=13.50),
}
# 公报正文中表述方式特殊、正则未命中的个别值（已人工核对公报原文）
MANUAL = {
    2010: dict(cpi=3.3),                         # “全年平均比上年上涨3.3%”
    2025: dict(cpi=0.0),                         # “居民消费价格与上年持平”
    2013: dict(exports_value=22096, exports_unit="亿美元", exports_growth=7.9),
    2009: dict(retail_real_growth=16.9),
    2004: dict(gdp_growth=9.5),
}
# 2005-2013 公报出口以美元计价，2014 年起改为人民币计价；为保持可比，补充人民币计价出口额（海关总署，亿元）
EXPORTS_CNY = {
    2004: 49103, 2005: 62648, 2006: 77597, 2007: 93627, 2008: 100395, 2009: 82030, 2010: 107023,
    2011: 123241, 2012: 129359, 2013: 137131,
}

fields = ["year", "gdp_100m_cny_revised", "gdp_growth_pct", "cpi_pct", "retail_100m_cny", "retail_growth_pct",
          "retail_real_growth_pct", "retail_to_gdp_pct", "exports_100m_cny", "exports_growth_pct",
          "exports_to_gdp_pct", "fiscal_revenue_100m_cny", "tax_revenue_100m_cny", "tax_to_gdp_pct",
          "fiscal_revenue_to_gdp_pct", "land_sale_revenue_100m_cny", "social_insurance_income_100m_cny",
          "broad_revenue_to_gdp_pct", "pop_10k", "pop60_10k", "pop60_pct", "pop65_10k", "pop65_pct", "urban_pct"]
rows = []
for y in range(2004, 2026):
    r = dict(raw.get(y, {}))
    r.update(MANUAL.get(y, {}))
    r.update(CENSUS_AGE.get(y, {}))
    gdp = GDP_REVISED[y]
    exp_cny = r.get("exports_value") if r.get("exports_unit") == "亿元" else EXPORTS_CNY.get(y)
    fisc = FISCAL_REVENUE[y]; tax = TAX_REVENUE[y]
    land = LAND_SALE_REVENUE.get(y); soc = SOCIAL_INS_INCOME.get(y)
    broad = (fisc + land + soc) / gdp * 100 if land and soc else None
    rows.append({
        "year": y, "gdp_100m_cny_revised": gdp, "gdp_growth_pct": r.get("gdp_growth"), "cpi_pct": r.get("cpi"),
        "retail_100m_cny": r.get("retail_100m_cny"), "retail_growth_pct": r.get("retail_growth"),
        "retail_real_growth_pct": r.get("retail_real_growth"),
        "retail_to_gdp_pct": round(r["retail_100m_cny"] / gdp * 100, 2) if r.get("retail_100m_cny") else None,
        "exports_100m_cny": exp_cny, "exports_growth_pct": r.get("exports_growth"),
        "exports_to_gdp_pct": round(exp_cny / gdp * 100, 2) if exp_cny else None,
        "fiscal_revenue_100m_cny": fisc, "tax_revenue_100m_cny": tax,
        "tax_to_gdp_pct": round(tax / gdp * 100, 2), "fiscal_revenue_to_gdp_pct": round(fisc / gdp * 100, 2),
        "land_sale_revenue_100m_cny": land, "social_insurance_income_100m_cny": soc,
        "broad_revenue_to_gdp_pct": round(broad, 2) if broad else None,
        "pop_10k": r.get("pop_10k"), "pop60_10k": r.get("pop60_10k"), "pop60_pct": r.get("pop60_pct"),
        "pop65_10k": r.get("pop65_10k"), "pop65_pct": r.get("pop65_pct"), "urban_pct": r.get("urban_pct"),
    })

with open(os.path.join(DATA, "china_annual.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r["year"], "GDP%", r["gdp_growth_pct"], "CPI", r["cpi_pct"], "社零%", r["retail_growth_pct"],
          "社零/GDP", r["retail_to_gdp_pct"], "出口/GDP", r["exports_to_gdp_pct"], "税/GDP", r["tax_to_gdp_pct"],
          "宽口径", r["broad_revenue_to_gdp_pct"], "65+%", r["pop65_pct"])
