# 东北三省虹鳟冷水鱼适宜水域研究

结合河流水温、上下游水库与水源保护区，对辽宁、吉林、黑龙江适合养殖虹鳟等冷水鱼的水域及其所属县区进行区划，并输出专题地图与可下载 PDF。

## 下载

- 研究报告 PDF：[`东北三省虹鳟冷水鱼适宜水域研究报告.pdf`](东北三省虹鳟冷水鱼适宜水域研究报告.pdf)
- 网页版：[`report.html`](report.html)
- 专题地图：[`charts/`](charts/)
- 水域/县区表：[`data/sites.csv`](data/sites.csv)、[`data/counties.csv`](data/counties.csv)

## 复现

```bash
python3 scripts/generate_maps.py
python3 scripts/build_report.py
```

底图来自阿里云 DataV 行政区界；区划为综合研判，不替代法定养殖水域滩涂规划。
