"""IMF WEO (Oct 2026 vintage) via api.imf.org SDMX 3.0."""
import json, urllib.request, csv, sys, time

COUNTRIES = ["CHN", "JPN", "KOR", "VNM", "MYS", "IND"]
INDS = {
    "GGR_NGDP": "gen_gov_revenue_pct_gdp",
    "GGX_NGDP": "gen_gov_expenditure_pct_gdp",
    "GGXWDG_NGDP": "gen_gov_gross_debt_pct_gdp",
    "NGDP_RPCH": "real_gdp_growth_pct",
    "PCPIPCH": "inflation_avg_pct",
    "NGDPDPC": "gdp_per_capita_usd",
    "NGDPD": "gdp_usd_bn",
}
rows = []
for ind, name in INDS.items():
    for c in COUNTRIES:
        url = f"https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.RES/WEO/+/{c}.{ind}.A"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    d = json.load(r)
                break
            except Exception as e:
                print("retry", c, ind, e, file=sys.stderr); time.sleep(3)
        else:
            continue
        ds = d["data"]["dataSets"][0]
        series = list(ds["series"].values())
        if not series:
            print("empty", c, ind, file=sys.stderr); continue
        obs = series[0]["observations"]
        struct = d["data"]["structures"][0]
        tdim = [x for x in struct["dimensions"]["observation"] if x["id"] == "TIME_PERIOD"][0]
        periods = [v.get("id") or v["value"] for v in tdim["values"]]
        # observations after the "latest actual" year are IMF projections
        attrs = series[0].get("attributes", [])
        sattrs = struct["attributes"].get("series", [])
        lad = None
        for a, val in zip(sattrs, attrs):
            if a["id"] in ("LATEST_ACTUAL_ANNUAL_DATA", "LAST_ACTUAL_DATE") and val not in (None, 0):
                vals = a.get("values")
                lad = vals[val]["id"] if vals and isinstance(val, int) else val
        print("  latest actual:", lad, file=sys.stderr)
        # observation-level attributes (estimate flag etc.)
        for k, v in obs.items():
            year = int(periods[int(k)])
            if v[0] is None:
                continue
            rows.append({"country": c, "indicator": name, "imf_code": ind, "year": year, "value": float(v[0])})
        print(c, ind, len(obs), "obs", periods[0], "-", periods[-1])
with open("/tmp/imf_data.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["country", "indicator", "imf_code", "year", "value"])
    w.writeheader(); w.writerows(rows)
print("total rows", len(rows))
