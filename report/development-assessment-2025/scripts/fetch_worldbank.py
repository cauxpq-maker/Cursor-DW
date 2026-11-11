import json, urllib.request, csv, sys, time

COUNTRIES = ["CHN", "JPN", "KOR", "VNM", "MYS", "IND"]
INDICATORS = {
    "NY.GDP.MKTP.KD.ZG": "gdp_growth_pct",
    "NY.GDP.PCAP.CD": "gdp_pc_usd",
    "NY.GDP.MKTP.CD": "gdp_usd",
    "FP.CPI.TOTL.ZG": "cpi_pct",
    "NE.EXP.GNFS.ZS": "exports_pct_gdp",
    "NE.EXP.GNFS.KD.ZG": "exports_real_growth_pct",
    "TX.VAL.MRCH.CD.WT": "merch_exports_usd",
    "NE.CON.PRVT.ZS": "hh_consumption_pct_gdp",
    "NE.CON.PRVT.KD.ZG": "hh_consumption_real_growth_pct",
    "GC.TAX.TOTL.GD.ZS": "tax_revenue_pct_gdp",
    "GC.REV.XGRT.GD.ZS": "gov_revenue_pct_gdp",
    "SP.POP.65UP.TO.ZS": "pop65_pct",
    "SP.POP.DPND.OL": "old_age_dependency",
    "SP.DYN.TFRT.IN": "fertility",
    "SP.DYN.LE00.IN": "life_expectancy",
    "SP.POP.TOTL": "population",
    "SP.URB.TOTL.IN.ZS": "urban_pct",
}

rows = []
for code, name in INDICATORS.items():
    url = (f"https://api.worldbank.org/v2/country/{';'.join(COUNTRIES)}/indicator/{code}"
           f"?format=json&date=2000:2025&per_page=500")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                d = json.load(r)
            break
        except Exception as e:
            print("retry", code, e, file=sys.stderr); time.sleep(3)
    else:
        continue
    if len(d) < 2 or not d[1]:
        print("no data", code, file=sys.stderr); continue
    for rec in d[1]:
        if rec["value"] is None:
            continue
        rows.append({"country": rec["countryiso3code"], "indicator": name, "wb_code": code,
                     "year": int(rec["date"]), "value": rec["value"]})
    print(code, name, len([r for r in rows if r["indicator"] == name]), "obs")

with open("/tmp/wb_data.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["country", "indicator", "wb_code", "year", "value"])
    w.writeheader(); w.writerows(rows)
print("total rows", len(rows))
