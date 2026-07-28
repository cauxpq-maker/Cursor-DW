# -*- coding: utf-8 -*-
"""从世界银行API拉取中日韩美长期指标序列,缓存为JSON供图表脚本使用"""
import json
import os

import requests

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUT, exist_ok=True)

COUNTRIES = "CHN;JPN;KOR;USA"
INDICATORS = {
    "gdp_pc_usd": "NY.GDP.PCAP.CD",       # 人均GDP(现价美元)
    "pop65_share": "SP.POP.65UP.TO.ZS",    # 65岁以上人口占比
    "urban_share": "SP.URB.TOTL.IN.ZS",    # 城镇化率
    "services_share": "NV.SRV.TOTL.ZS",    # 服务业增加值占GDP比重
    "hh_consumption_share": "NE.CON.PRVT.ZS",  # 居民消费占GDP比重
    "fertility": "SP.DYN.TFRT.IN",         # 总和生育率
}


def fetch(indicator):
    url = (
        f"https://api.worldbank.org/v2/country/{COUNTRIES}/indicator/{indicator}"
        "?format=json&per_page=2000&date=1960:2025"
    )
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    payload = r.json()
    series = {}
    for row in payload[1]:
        iso = row["countryiso3code"]
        year = int(row["date"])
        val = row["value"]
        if val is not None:
            series.setdefault(iso, {})[year] = val
    return series


def main():
    for name, code in INDICATORS.items():
        path = os.path.join(OUT, f"{name}.json")
        series = fetch(code)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(series, f, ensure_ascii=False)
        counts = {k: len(v) for k, v in series.items()}
        print(name, counts)


if __name__ == "__main__":
    main()
