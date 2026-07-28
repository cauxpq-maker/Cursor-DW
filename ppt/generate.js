const pptxgen = require("pptxgenjs");
const path = require("path");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "丹东城市旅游战略研究";
pptx.subject = "政府研讨版战略规划";
pptx.title = "丹东城市旅游战略提升与鸭绿江沿江文旅发展规划";
pptx.company = "城市文旅战略研究";
pptx.lang = "zh-CN";
pptx.theme = {
  headFontFace: "Microsoft YaHei",
  bodyFontFace: "Microsoft YaHei",
  lang: "zh-CN",
};
pptx.defineSlideMaster({
  title: "MASTER",
  background: { color: "F5F1E8" },
  objects: [
    { rect: { x: 0, y: 0, w: 13.333, h: 0.12, fill: { color: "D45035" }, line: { color: "D45035" } } },
    { text: { text: "DANDONG · BORDER CITY TOURISM STRATEGY", options: { x: 0.55, y: 7.08, w: 5.8, h: 0.18, fontFace: "Arial", fontSize: 5.5, color: "7B827B", charSpacing: 1.2, margin: 0 } } },
    { text: { text: "政府研讨版｜2026.07", options: { x: 10.9, y: 7.05, w: 1.85, h: 0.2, fontSize: 6, color: "7B827B", align: "right", margin: 0 } } },
  ],
  slideNumber: { x: 12.8, y: 7.05, w: 0.22, h: 0.2, fontFace: "Arial", fontSize: 6, color: "7B827B", align: "right", margin: 0 },
});

const C = {
  ink: "173A3A",
  ink2: "244E4E",
  red: "D45035",
  gold: "D9A441",
  cream: "F5F1E8",
  paper: "FFFCF5",
  blue: "2E6471",
  paleBlue: "DDE9E8",
  green: "4D725B",
  paleGreen: "E3EBDD",
  paleRed: "F2DDD5",
  gray: "667271",
  light: "E7E1D6",
  white: "FFFFFF",
};

const FONT = "Microsoft YaHei";
const OUT = path.join(__dirname, "丹东城市旅游战略规划_政府研讨版.pptx");

function addText(slide, text, x, y, w, h, opts = {}) {
  slide.addText(text, {
    x, y, w, h,
    fontFace: opts.fontFace || FONT,
    fontSize: opts.fontSize || 14,
    color: opts.color || C.ink,
    bold: opts.bold || false,
    margin: opts.margin === undefined ? 0 : opts.margin,
    valign: opts.valign || "mid",
    align: opts.align || "left",
    breakLine: false,
    fit: "shrink",
    paraSpaceAfterPt: opts.paraSpaceAfterPt || 0,
    charSpacing: opts.charSpacing,
    isTextBox: true,
    ...opts,
  });
}

function addTitle(slide, section, title, subtitle = "") {
  addText(slide, section, 0.58, 0.33, 1.65, 0.28, { fontFace: "Arial", fontSize: 7, color: C.red, bold: true, charSpacing: 1.6 });
  addText(slide, title, 0.58, 0.67, 11.95, 0.58, { fontSize: 24, color: C.ink, bold: true });
  if (subtitle) addText(slide, subtitle, 0.6, 1.27, 11.8, 0.35, { fontSize: 9.5, color: C.gray });
}

function addPill(slide, text, x, y, w, color = C.ink, fill = C.paleBlue) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h: 0.34, rectRadius: 0.08, fill: { color: fill }, line: { color: fill } });
  addText(slide, text, x + 0.08, y + 0.02, w - 0.16, 0.28, { fontSize: 7.5, color, bold: true, align: "center" });
}

function addCard(slide, x, y, w, h, title, body, opts = {}) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x, y, w, h,
    rectRadius: 0.06,
    fill: { color: opts.fill || C.paper, transparency: opts.transparency || 0 },
    line: { color: opts.line || C.light, width: opts.lineWidth || 1 },
    shadow: opts.shadow === false ? undefined : { type: "outer", color: "A49F94", blur: 1, angle: 45, distance: 0.8, opacity: 0.12 },
  });
  if (opts.number) {
    addText(slide, opts.number, x + 0.2, y + 0.15, 0.45, 0.32, { fontFace: "Arial", fontSize: 10, color: opts.accent || C.red, bold: true });
  }
  addText(slide, title, x + 0.22, y + (opts.number ? 0.54 : 0.2), w - 0.44, 0.38, { fontSize: opts.titleSize || 13, color: opts.titleColor || C.ink, bold: true });
  addText(slide, body, x + 0.22, y + (opts.number ? 0.97 : 0.68), w - 0.44, h - (opts.number ? 1.12 : 0.86), {
    fontSize: opts.bodySize || 9,
    color: opts.bodyColor || C.gray,
    valign: "top",
    breakLine: true,
    bullet: opts.bullet,
    margin: 0,
  });
}

function addPhotoPlaceholder(slide, x, y, w, h, label, accent = C.red) {
  slide.addShape(pptx.ShapeType.rect, {
    x, y, w, h,
    fill: { color: "E8E3D9" },
    line: { color: accent, width: 1.2, dash: "dash" },
  });
  slide.addShape(pptx.ShapeType.line, { x: x + 0.3, y: y + h - 0.45, w: w - 0.6, h: -(h - 0.9), line: { color: "B6B1A8", width: 0.8 } });
  slide.addShape(pptx.ShapeType.line, { x: x + 0.3, y: y + 0.45, w: w - 0.6, h: h - 0.9, line: { color: "B6B1A8", width: 0.8 } });
  slide.addShape(pptx.ShapeType.roundRect, { x: x + 0.22, y: y + h - 0.56, w: w - 0.44, h: 0.34, fill: { color: "FFFCF5", transparency: 7 }, line: { color: "FFFCF5", transparency: 100 } });
  addText(slide, `图片占位｜${label}`, x + 0.3, y + h - 0.51, w - 0.6, 0.22, { fontSize: 6.8, color: C.gray, align: "center" });
}

function addMetric(slide, x, y, w, value, label, tone = C.red) {
  addText(slide, value, x, y, w, 0.5, { fontFace: "Arial", fontSize: 25, color: tone, bold: true, align: "center" });
  addText(slide, label, x + 0.03, y + 0.55, w - 0.06, 0.55, { fontSize: 8.2, color: C.gray, align: "center", valign: "top" });
}

function addSectionBand(slide, n, title, subtitle, keywords) {
  slide.background = { color: C.ink };
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 0.18, h: 7.5, fill: { color: C.red }, line: { color: C.red } });
  addText(slide, n, 0.72, 0.65, 1.4, 1.1, { fontFace: "Arial", fontSize: 54, color: C.gold, bold: true });
  addText(slide, title, 0.78, 2.0, 8.4, 0.95, { fontSize: 31, color: C.white, bold: true });
  addText(slide, subtitle, 0.8, 3.02, 8.8, 0.55, { fontSize: 12, color: "CAD9D7" });
  let x = 0.8;
  keywords.forEach((k) => {
    const width = Math.max(1.1, k.length * 0.22 + 0.45);
    addPill(slide, k, x, 4.25, width, C.white, C.ink2);
    x += width + 0.18;
  });
  addPhotoPlaceholder(slide, 9.65, 0.55, 3.05, 5.95, "章节主视觉");
  addText(slide, "丹东城市旅游战略规划 · 政府研讨版", 0.8, 6.85, 5, 0.22, { fontSize: 6.5, color: "91A8A5" });
}

function addArrow(slide, x, y, w, color = C.red) {
  slide.addShape(pptx.ShapeType.chevron, { x, y, w, h: 0.38, fill: { color }, line: { color } });
}

function addTable(slide, rows, x, y, w, h, colWidths, opts = {}) {
  slide.addTable(rows, {
    x, y, w, h,
    colW: colWidths,
    border: { type: "solid", color: opts.border || C.light, pt: 0.7 },
    fill: C.paper,
    color: C.ink,
    fontFace: FONT,
    fontSize: opts.fontSize || 8,
    margin: 0.08,
    valign: "mid",
    breakLine: false,
    autoFit: false,
    rowH: opts.rowH,
  });
}

// 01 封面
{
  const s = pptx.addSlide();
  s.background = { color: C.ink };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 0.18, h: 7.5, fill: { color: C.red }, line: { color: C.red } });
  s.addShape(pptx.ShapeType.arc, { x: 8.55, y: -1.05, w: 5.5, h: 5.5, adjustPoint: 0.33, rotate: 8, fill: { color: C.ink, transparency: 100 }, line: { color: C.gold, width: 2.2, transparency: 18 } });
  s.addShape(pptx.ShapeType.arc, { x: 9.45, y: 0.15, w: 4.55, h: 4.55, rotate: 185, fill: { color: C.ink, transparency: 100 }, line: { color: C.red, width: 5.5, transparency: 10 } });
  addText(s, "DANDONG 2035", 0.78, 0.62, 3.3, 0.35, { fontFace: "Arial", fontSize: 9, color: C.gold, bold: true, charSpacing: 2.4 });
  addText(s, "丹东城市旅游战略提升与\n鸭绿江沿江文旅发展规划", 0.75, 1.35, 8.35, 1.75, { fontSize: 31, color: C.white, bold: true, breakLine: true, valign: "top" });
  addText(s, "从“边境观光”走向“边境生活方式目的地”", 0.78, 3.35, 7.1, 0.46, { fontSize: 15, color: "C8D9D6" });
  addPill(s, "虎山—断桥沿江廊道", 0.78, 4.25, 2.12, C.white, C.ink2);
  addPill(s, "夜游演艺", 3.04, 4.25, 1.18, C.white, C.ink2);
  addPill(s, "四季运营", 4.38, 4.25, 1.18, C.white, C.ink2);
  addPill(s, "人口回流", 5.72, 4.25, 1.18, C.white, C.ink2);
  addPill(s, "银发经济", 7.06, 4.25, 1.18, C.white, C.ink2);
  addPhotoPlaceholder(s, 9.18, 1.55, 3.52, 4.72, "鸭绿江/断桥城市形象主图");
  addText(s, "政府研讨版｜供下一阶段行动决策讨论", 0.78, 6.47, 5.8, 0.3, { fontSize: 9.5, color: "A9C0BD" });
  addText(s, "2026年7月", 0.78, 6.86, 1.6, 0.22, { fontSize: 7, color: "73918E" });
}

// 02 目录
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "CONTENTS", "今天需要形成的，不只是项目清单，而是行动共识", "建议以“战略判断—空间抓手—运营机制—近期行动”推进政府讨论");
  const items = [
    ["01", "趋势判断", "暑期市场变了，丹东的打法也要变"],
    ["02", "战略定位", "从过境观光走向边境生活方式目的地"],
    ["03", "核心廊道", "虎山—断桥成为全市文旅第一抓手"],
    ["04", "夜游四季", "把白天客流转化为夜晚消费、全年热度"],
    ["05", "产品客群", "组合票、研学、自驾、银发与人口回流"],
    ["06", "行动机制", "90天启动、三阶段推进、跨部门统筹"],
  ];
  items.forEach((it, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.65 + col * 6.15;
    const y = 1.88 + row * 1.55;
    addText(s, it[0], x, y, 0.58, 0.42, { fontFace: "Arial", fontSize: 15, color: C.red, bold: true });
    addText(s, it[1], x + 0.72, y, 1.35, 0.38, { fontSize: 14, color: C.ink, bold: true });
    addText(s, it[2], x + 0.72, y + 0.47, 4.8, 0.45, { fontSize: 8.6, color: C.gray, valign: "top" });
    s.addShape(pptx.ShapeType.line, { x, y: y + 1.16, w: 5.55, h: 0, line: { color: C.light, width: 1 } });
  });
}

// 03 决策摘要
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "EXECUTIVE SUMMARY", "五句话形成丹东旅游下一阶段行动共识", "核心不是再造一个孤立景区，而是重组城市空间、时间和消费");
  const cards = [
    ["01", "以江定城", "把虎山—断桥从交通沿线升级为丹东城市旅游主轴。"],
    ["02", "以夜留人", "用日落、游船、演艺、夜食延长游客停留6小时。"],
    ["03", "以季稳流", "用四季事件日历替代“一夏独热”，形成全年传播节奏。"],
    ["04", "以联增收", "景区、交通、酒店、演艺一票联动，告别单一门票经济。"],
    ["05", "以旅兴城", "把游客导入转化为消费、人才、旅居和人口回流。"],
  ];
  cards.forEach((c, i) => addCard(s, 0.58 + i * 2.5, 1.86, 2.25, 3.8, c[1], c[2], { number: c[0], fill: i === 0 ? C.ink : C.paper, line: i === 0 ? C.ink : C.light, titleColor: i === 0 ? C.white : C.ink, bodyColor: i === 0 ? "C7D8D5" : C.gray, accent: i === 0 ? C.gold : C.red, titleSize: 14, bodySize: 9.2 }));
  addText(s, "建议总抓手", 0.62, 6.05, 1.1, 0.26, { fontSize: 8, color: C.red, bold: true });
  addText(s, "“一条江、一条路、一个夜晚、四个季节”", 1.85, 5.95, 7.3, 0.45, { fontSize: 18, color: C.ink, bold: true });
}

// 04 暑期市场
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "01 · MARKET SHIFT", "暑期旅游进入“量增、价跌、选择碎片化”的新阶段", "客流仍旺，但目的地不能再用“人来了”代替“价值留下了”");
  addMetric(s, 0.65, 1.78, 2.15, "+30%", "境内游预订出游人次\n同比增长", C.red);
  addMetric(s, 3.12, 1.78, 2.15, "+22.4%", "跨省游热度\n同比增长", C.blue);
  addMetric(s, 5.59, 1.78, 2.15, "−20%", "7月上旬机票预订均价\n同比约降", C.green);
  addMetric(s, 8.06, 1.78, 2.15, "−8.2%", "经济型酒店暑期首周\nRevPAR同比", C.red);
  addMetric(s, 10.53, 1.78, 2.15, "60%+", "暑期亲子客群\n占比", C.gold);
  s.addShape(pptx.ShapeType.line, { x: 0.68, y: 3.28, w: 11.95, h: 0, line: { color: C.light, width: 1 } });
  const shifts = [
    ["从“抢流量”", "到“提停留、提转化”"],
    ["从“卖门票”", "到“卖时间、场景与组合”"],
    ["从“提前计划”", "到“临时决策、短视频种草”"],
    ["从“大团观光”", "到“小团、自驾、自由行”"],
  ];
  shifts.forEach((v, i) => {
    const x = 0.7 + i * 3.05;
    addText(s, v[0], x, 3.72, 2.45, 0.32, { fontSize: 10, color: C.gray });
    addText(s, v[1], x, 4.2, 2.45, 0.62, { fontSize: 14, color: C.ink, bold: true, valign: "top" });
    s.addShape(pptx.ShapeType.line, { x, y: 5.12, w: 2.52, h: 0, line: { color: i === 0 ? C.red : C.gold, width: 3 } });
  });
  addText(s, "资料口径：文化和旅游部、国铁集团及携程、同程、去哪儿等公开市场信息，2026年暑期；用于趋势研判，正式报审前建议由统计部门复核。", 0.7, 6.45, 11.9, 0.3, { fontSize: 6.4, color: C.gray });
}

// 05 丹东含义
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "01 · MARKET SHIFT", "对丹东的含义：暑期优势仍在，但“只看断桥”不再够用");
  const left = [
    ["有流量", "辽宁暑期热度提升，边境、自驾、避暑具备话题基础"],
    ["有辨识", "界江、国门、断桥、331起点形成独有认知"],
    ["有空间", "虎山至断桥兼具山水、历史、乡村与城市消费"],
  ];
  left.forEach((c, i) => addCard(s, 0.65, 1.66 + i * 1.52, 5.25, 1.22, c[0], c[1], { shadow: false, titleSize: 12, bodySize: 8.3, fill: C.paleGreen, line: C.paleGreen }));
  const right = [
    ["停得短", "核心景点完成后缺少连续体验，过夜理由不足"],
    ["夜不强", "夜景有基础，但夜游叙事、演艺、消费场景尚未成链"],
    ["季节单", "暑期集中，秋冬春的产品和传播节奏尚未系统化"],
  ];
  right.forEach((c, i) => addCard(s, 6.25, 1.66 + i * 1.52, 5.25, 1.22, c[0], c[1], { shadow: false, titleSize: 12, bodySize: 8.3, fill: C.paleRed, line: C.paleRed }));
  addArrow(s, 11.77, 3.34, 0.65, C.red);
  addText(s, "突破口", 11.65, 2.78, 0.85, 0.28, { fontSize: 8, color: C.red, bold: true, align: "center" });
  addText(s, "以沿江廊道\n重组消费链", 11.56, 3.85, 1.0, 0.85, { fontSize: 12, color: C.ink, bold: true, align: "center", breakLine: true });
}

// 06 战略章节页
{
  const s = pptx.addSlide();
  addSectionBand(s, "02", "战略定位：\n以边境生活方式重塑丹东", "不是“景点更多”，而是“城市更值得停留”", ["国家边境门户", "331起点", "鸭绿江生活", "和平叙事"]);
}

// 07 定位升级
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "02 · POSITIONING", "从“边境观光城市”升级为“国家级边境生活方式目的地”");
  addText(s, "过去的丹东", 0.7, 1.66, 2.0, 0.4, { fontSize: 12, color: C.gray, bold: true });
  addText(s, "未来的丹东", 7.2, 1.66, 2.0, 0.4, { fontSize: 12, color: C.red, bold: true });
  const old = ["看断桥", "拍国境", "吃一顿", "当天走"];
  const next = ["走一段江", "住一个夜", "过一种生活", "再来一季"];
  old.forEach((t, i) => {
    addCard(s, 0.7, 2.25 + i * 0.92, 4.15, 0.67, t, "", { shadow: false, titleSize: 11, fill: "ECE8DF", line: "ECE8DF" });
    addArrow(s, 5.28, 2.4 + i * 0.92, 0.8, i === 3 ? C.red : C.gold);
    addCard(s, 6.5, 2.25 + i * 0.92, 5.9, 0.67, next[i], "", { shadow: false, titleSize: 12, fill: i === 3 ? C.ink : C.paleBlue, line: i === 3 ? C.ink : C.paleBlue, titleColor: i === 3 ? C.white : C.ink });
  });
  addText(s, "城市品牌建议语（讨论稿）", 0.72, 6.1, 2.3, 0.28, { fontSize: 8, color: C.red, bold: true });
  addText(s, "江山起点 · 边境丹东", 3.02, 5.98, 4.4, 0.52, { fontSize: 21, color: C.ink, bold: true });
}

// 08 空间结构
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "02 · SPATIAL STRATEGY", "“一心、一廊、一起点、两翼、多节点”统筹全域资源");
  s.addShape(pptx.ShapeType.ellipse, { x: 5.02, y: 2.35, w: 3.1, h: 3.1, fill: { color: C.ink }, line: { color: C.gold, width: 2 } });
  addText(s, "一廊", 5.78, 2.88, 1.55, 0.48, { fontSize: 22, color: C.gold, bold: true, align: "center" });
  addText(s, "虎山—断桥\n鸭绿江核心廊道", 5.48, 3.55, 2.15, 0.9, { fontSize: 13, color: C.white, bold: true, align: "center", breakLine: true });
  const nodes = [
    [0.72, 1.78, "一心", "城市旅游消费中心", C.red],
    [9.7, 1.78, "一起点", "331国道国家级起点", C.gold],
    [0.72, 4.95, "西翼", "山地温泉康养", C.green],
    [9.7, 4.95, "南翼", "滨海海岛度假", C.blue],
  ];
  nodes.forEach((n) => {
    addCard(s, n[0], n[1], 2.75, 1.15, n[2], n[3], { shadow: false, fill: C.paper, line: n[4], lineWidth: 1.5, titleSize: 13, bodySize: 8 });
    s.addShape(pptx.ShapeType.line, { x: n[0] < 5 ? n[0] + 2.75 : 8.12, y: n[1] + 0.58, w: n[0] < 5 ? 1.55 : 1.58, h: n[1] < 3 ? 1.15 : -0.75, line: { color: n[4], width: 1.3, dash: "dash" } });
  });
  addText(s, "多节点：虎山｜河口｜沿江驿站｜断桥｜纪念馆｜码头｜老街｜银杏大道", 2.25, 6.25, 8.85, 0.38, { fontSize: 9, color: C.gray, align: "center" });
}

// 09 廊道章节页
{
  const s = pptx.addSlide();
  addSectionBand(s, "03", "核心抓手：\n虎山—断桥沿江廊道", "从“沿江交通线”升级为“城市旅游主轴”", ["世界级边境风景道", "水陆联动", "慢游系统", "品质管控"]);
}

// 10 廊道愿景
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "03 · CORRIDOR VISION", "虎山—断桥：丹东最需要统一规划、统一标准、统一运营的空间");
  addPhotoPlaceholder(s, 0.65, 1.68, 7.35, 4.74, "沿江航拍/廊道全景");
  const v = [
    ["城市形象面", "展示国家边境门户与鸭绿江城市天际线"],
    ["旅游主产品", "形成可游半日、可玩一日、可住一夜的完整体验"],
    ["产业集聚带", "串联景区、乡村、驿站、游船、演艺与夜间商业"],
    ["治理示范区", "统一风貌、安全、生态、交通和服务标准"],
  ];
  v.forEach((c, i) => addCard(s, 8.32, 1.68 + i * 1.18, 4.35, 0.98, c[0], c[1], { shadow: false, titleSize: 11, bodySize: 7.7, fill: i === 0 ? C.paleRed : C.paper, line: i === 0 ? C.paleRed : C.light }));
}

// 11 四段组织
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "03 · CORRIDOR STRUCTURE", "四段联动：自然递进、情绪递进、消费递进");
  const stages = [
    ["01", "虎山国境段", "长城 / 国门 / 徒步", "探索"],
    ["02", "河口乡野段", "铁路 / 村落 / 花果", "松弛"],
    ["03", "沿江慢游段", "自驾 / 骑行 / 驿站", "沉浸"],
    ["04", "断桥城市段", "历史 / 夜游 / 消费", "高潮"],
  ];
  stages.forEach((st, i) => {
    const x = 0.67 + i * 3.12;
    const fill = i === 3 ? C.ink : [C.paleGreen, C.paleBlue, "EEE5D4"][i];
    addCard(s, x, 1.8, 2.78, 3.25, st[1], st[2], { number: st[0], fill, line: fill, titleColor: i === 3 ? C.white : C.ink, bodyColor: i === 3 ? "C7D8D5" : C.gray, accent: i === 3 ? C.gold : C.red, titleSize: 14 });
    addPill(s, st[3], x + 0.75, 4.56, 1.28, i === 3 ? C.ink : C.ink, i === 3 ? C.gold : C.paper);
    if (i < 3) addArrow(s, x + 2.83, 3.16, 0.28, C.red);
  });
  addText(s, "时间结构", 0.7, 5.65, 0.9, 0.26, { fontSize: 8, color: C.red, bold: true });
  addText(s, "晨间登高 → 午后乡野 → 傍晚沿江 → 夜宿城市", 1.72, 5.53, 8.2, 0.46, { fontSize: 17, color: C.ink, bold: true });
}

// 12 分段产品
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "03 · SEGMENT PRODUCTS", "每一段有主体验，每一节点有停留理由，每一次停留有消费接口");
  const rows = [
    [
      { text: "分段", options: { bold: true, color: C.white, fill: C.ink, align: "center" } },
      { text: "主叙事", options: { bold: true, color: C.white, fill: C.ink, align: "center" } },
      { text: "重点产品", options: { bold: true, color: C.white, fill: C.ink } },
      { text: "近期抓手", options: { bold: true, color: C.white, fill: C.ink } },
    ],
    ["虎山国境段", "边境探索", "长城徒步、国境观察、研学课堂", "入口重塑、观景点、亲子任务线"],
    ["河口乡野段", "江畔乡愁", "铁路记忆、花果季、村落餐桌", "村景整治、物产市集、微度假"],
    ["沿江慢游段", "风景在路上", "骑行、自驾、摄影、轻露营", "驿站体系、补能、统一导视"],
    ["断桥城市段", "历史与今夜", "断桥、纪念馆、游船、演艺、夜食", "夜游示范区、码头更新、联票"],
  ];
  addTable(s, rows, 0.65, 1.75, 12.0, 3.65, [1.55, 1.45, 4.35, 4.65], { fontSize: 9, rowH: 0.72 });
  addCard(s, 0.65, 5.65, 12.0, 0.7, "底层原则", "不追求沿线处处开发；以视廊保护和小体量、低干扰、高品质为准入底线。", { shadow: false, titleSize: 10, bodySize: 9, fill: C.paleRed, line: C.paleRed });
}

// 13 交通慢游
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "03 · MOBILITY", "交通不是配套，而是沿江旅游产品本身");
  const lanes = [
    ["水上", "日落游船\n主题航线", C.blue],
    ["公交", "高铁站—断桥—虎山\n旅游快线", C.red],
    ["自驾", "331起点—沿江驿站\n补能与停车", C.gold],
    ["骑行", "分段绿道\n租还与救援", C.green],
    ["步行", "滨江漫步\n无障碍系统", C.ink2],
  ];
  lanes.forEach((l, i) => {
    const y = 1.66 + i * 0.9;
    addText(s, l[0], 0.72, y, 0.72, 0.36, { fontSize: 10, color: l[2], bold: true });
    s.addShape(pptx.ShapeType.line, { x: 1.55, y: y + 0.18, w: 6.2, h: 0, line: { color: l[2], width: 5, beginArrowType: "none", endArrowType: "triangle" } });
    addText(s, l[1], 8.05, y - 0.13, 3.55, 0.62, { fontSize: 10.5, color: C.ink, bold: true, breakLine: true });
  });
  addPhotoPlaceholder(s, 10.9, 1.65, 1.75, 4.75, "交通场景");
  addText(s, "政府动作", 0.72, 6.31, 0.8, 0.25, { fontSize: 8, color: C.red, bold: true });
  addText(s, "统一线路、统一班次、统一购票、统一标识、统一安全标准", 1.68, 6.2, 8.8, 0.42, { fontSize: 15, color: C.ink, bold: true });
}

// 14 品质导则
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "03 · QUALITY CONTROL", "沿江品质提升：先立标准，再上项目");
  const items = [
    ["01", "视廊", "岸线、眺望面与天际线优先保护"],
    ["02", "建筑", "控制体量、色彩、屋顶与临江界面"],
    ["03", "店招", "统一尺度与照度，杜绝视觉污染"],
    ["04", "灯光", "低照度、低干扰、叙事化，不做满江亮化"],
    ["05", "服务", "厕所、停车、休憩、适老与多语种标准"],
    ["06", "业态", "建立正负面清单，淘汰低质同质供给"],
  ];
  items.forEach((c, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    addCard(s, 0.65 + col * 4.12, 1.72 + row * 2.15, 3.75, 1.78, c[1], c[2], { number: c[0], shadow: false, fill: row === 0 ? C.paper : C.paleBlue, line: row === 0 ? C.light : C.paleBlue, titleSize: 12, bodySize: 8.4 });
  });
  addText(s, "建议形成成果", 0.7, 6.2, 1.15, 0.25, { fontSize: 8, color: C.red, bold: true });
  addText(s, "《虎山—断桥沿江风貌与业态准入导则》", 1.95, 6.08, 6.55, 0.42, { fontSize: 16, color: C.ink, bold: true });
}

// 15 夜游章节
{
  const s = pptx.addSlide();
  addSectionBand(s, "04", "夜游与四季：\n把流量变成时间价值", "白天看边境，晚上过生活；一季来一次，全年有理由", ["鸭绿江之夜", "三级演艺", "夜生活", "四季事件日历"]);
}

// 16 夜游逻辑
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "04 · NIGHT STRATEGY", "夜游的目标不是“更亮”，而是让游客多留6小时、多住1晚");
  const chain = [
    ["17:00", "日落", "沿江慢行 / 摄影"],
    ["18:30", "晚餐", "海鲜 / 烧烤 / 朝鲜族风味"],
    ["20:00", "演艺", "游船 / 实景 / 行进式表演"],
    ["21:30", "夜生活", "音乐 / 市集 / 小酒馆"],
    ["23:00", "住宿", "江景酒店 / 温泉 / 民宿"],
  ];
  chain.forEach((c, i) => {
    const x = 0.62 + i * 2.48;
    addText(s, c[0], x, 1.65, 1.2, 0.35, { fontFace: "Arial", fontSize: 12, color: i === 4 ? C.red : C.gold, bold: true });
    s.addShape(pptx.ShapeType.ellipse, { x, y: 2.15, w: 0.45, h: 0.45, fill: { color: i === 4 ? C.red : C.ink }, line: { color: i === 4 ? C.red : C.ink } });
    if (i < 4) s.addShape(pptx.ShapeType.line, { x: x + 0.45, y: 2.38, w: 2.02, h: 0, line: { color: C.gold, width: 2 } });
    addText(s, c[1], x, 2.9, 1.55, 0.35, { fontSize: 14, color: C.ink, bold: true });
    addText(s, c[2], x, 3.43, 1.9, 0.7, { fontSize: 8.3, color: C.gray, valign: "top" });
  });
  addCard(s, 0.65, 4.76, 3.72, 1.15, "夜景", "城市背景与空间氛围", { shadow: false, fill: C.paleBlue, line: C.paleBlue });
  addCard(s, 4.8, 4.76, 3.72, 1.15, "夜游", "有线路、有内容、有票务", { shadow: false, fill: C.paleRed, line: C.paleRed });
  addCard(s, 8.95, 4.76, 3.72, 1.15, "夜生活", "有社交、有消费、有复访", { shadow: false, fill: C.paleGreen, line: C.paleGreen });
}

// 17 夜景分级
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "04 · NIGHTSCAPE", "建立“一核、两带、多点”的夜景秩序");
  addPhotoPlaceholder(s, 0.65, 1.65, 5.3, 4.8, "断桥夜景/鸭绿江夜航");
  const layers = [
    ["一核", "断桥—码头夜游核心", "历史地标、城市仪式、夜航集散", C.red],
    ["两带", "滨江生活带 + 水上观览带", "步行消费与游船观景相互导流", C.gold],
    ["多点", "桥、塔、驿站、广场、建筑", "克制照明形成节奏，不做全线同亮", C.green],
  ];
  layers.forEach((l, i) => {
    const y = 1.7 + i * 1.48;
    addText(s, l[0], 6.35, y, 0.72, 0.38, { fontSize: 13, color: l[3], bold: true });
    addText(s, l[1], 7.25, y, 4.8, 0.38, { fontSize: 13, color: C.ink, bold: true });
    addText(s, l[2], 7.25, y + 0.53, 4.9, 0.48, { fontSize: 8.5, color: C.gray, valign: "top" });
    s.addShape(pptx.ShapeType.line, { x: 6.35, y: y + 1.18, w: 5.85, h: 0, line: { color: C.light, width: 1 } });
  });
  addText(s, "灯光底线", 6.35, 6.05, 0.85, 0.25, { fontSize: 8, color: C.red, bold: true });
  addText(s, "生态友好｜避免眩光｜控制色温｜重大节日动态切换", 7.25, 5.93, 5.0, 0.42, { fontSize: 11, color: C.ink, bold: true });
}

// 18 演艺体系
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "04 · PERFORMANCE", "不押注单一大剧场：构建“大、中、小”三级演艺生态");
  const perf = [
    ["城市级", "《鸭绿江之夜》\n沉浸式水岸演艺", "建立城市主叙事\n旺季定时、淡季节庆"],
    ["街区级", "码头音乐 / 行进巡游\n夜间快闪", "低门槛聚人\n与餐饮商业联动"],
    ["场所级", "餐厅驻演 / 故事会\n朝鲜族歌舞", "高频常态\n支持青年主理人"],
  ];
  perf.forEach((p, i) => {
    const x = 0.65 + i * 4.12;
    const h = 3.15 - i * 0.38;
    const y = 1.78 + i * 0.38;
    s.addShape(pptx.ShapeType.roundRect, { x, y, w: 3.72, h, fill: { color: [C.ink, C.blue, C.green][i] }, line: { color: [C.ink, C.blue, C.green][i] } });
    addText(s, p[0], x + 0.25, y + 0.22, 1.05, 0.34, { fontSize: 11, color: C.gold, bold: true });
    addText(s, p[1], x + 0.25, y + 0.72, 3.15, 0.85, { fontSize: 15, color: C.white, bold: true, breakLine: true, valign: "top" });
    addText(s, p[2], x + 0.25, y + 1.82, 3.1, 0.72, { fontSize: 8.5, color: "D8E4E2", breakLine: true, valign: "top" });
  });
  addCard(s, 0.65, 5.52, 12.0, 0.85, "运营原则", "先用可移动、可迭代、可季节调整的内容验证市场，再决定固定资产投入。", { shadow: false, titleSize: 10, bodySize: 9, fill: C.paleRed, line: C.paleRed });
}

// 19 夜生活
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "04 · NIGHTLIFE", "夜生活要覆盖年轻人，也要覆盖家庭与银发客群");
  const groups = [
    ["青年社交", "江畔音乐、精酿、小酒馆、夜骑", "21:00后"],
    ["家庭夜游", "游船、轻演艺、亲子市集、甜品", "18:30–21:30"],
    ["银发文化", "滨江散步、戏曲、故事会、茶叙", "18:00–20:30"],
    ["大众夜食", "海鲜、烧烤、朝鲜族风味、夜市", "18:00–24:00"],
  ];
  groups.forEach((g, i) => {
    const x = 0.65 + (i % 2) * 6.1;
    const y = 1.75 + Math.floor(i / 2) * 2.05;
    addCard(s, x, y, 5.7, 1.63, g[0], g[1], { shadow: false, fill: [C.paleBlue, C.paleRed, C.paleGreen, "EEE5D4"][i], line: [C.paleBlue, C.paleRed, C.paleGreen, "EEE5D4"][i], titleSize: 14, bodySize: 9 });
    addPill(s, g[2], x + 4.1, y + 0.24, 1.25, C.ink, C.paper);
  });
  addText(s, "治理同步", 0.7, 6.0, 0.9, 0.25, { fontSize: 8, color: C.red, bold: true });
  addText(s, "营业时间｜噪声边界｜交通疏散｜食品安全｜价格诚信", 1.72, 5.88, 8.9, 0.42, { fontSize: 15, color: C.ink, bold: true });
}

// 20 四季
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "04 · FOUR SEASONS", "四季不是四套口号，而是四种明确的来丹东理由");
  const seasons = [
    ["春", "江岸苏醒", "花季 / 草莓 / 乡村", "331开路季", C.green],
    ["夏", "江风不眠", "避暑 / 夜游 / 海岛", "鸭绿江之夜", C.blue],
    ["秋", "满城金色", "银杏 / 骑行 / 摄影", "银杏城市季", C.gold],
    ["冬", "暖泉静养", "温泉 / 雾凇 / 美食", "边境暖冬季", C.red],
  ];
  seasons.forEach((ss, i) => {
    const x = 0.65 + i * 3.08;
    s.addShape(pptx.ShapeType.roundRect, { x, y: 1.7, w: 2.72, h: 4.45, fill: { color: i === 1 ? C.ink : C.paper }, line: { color: ss[4], width: 1.5 } });
    addText(s, ss[0], x + 0.2, 1.98, 0.7, 0.55, { fontSize: 26, color: ss[4], bold: true });
    addText(s, ss[1], x + 0.2, 2.75, 2.15, 0.42, { fontSize: 15, color: i === 1 ? C.white : C.ink, bold: true });
    addText(s, ss[2], x + 0.2, 3.4, 2.15, 0.72, { fontSize: 9.3, color: i === 1 ? "C7D8D5" : C.gray, valign: "top" });
    addText(s, "年度事件", x + 0.2, 4.62, 1.0, 0.25, { fontSize: 7, color: ss[4], bold: true });
    addText(s, ss[3], x + 0.2, 5.02, 2.12, 0.48, { fontSize: 12, color: i === 1 ? C.white : C.ink, bold: true });
  });
}

// 21 热度日历
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "04 · HEAT MANAGEMENT", "“一季一主题、一月一事件、每周有内容”保持城市热度");
  const months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"];
  months.forEach((m, i) => {
    const x = 0.65 + i * 1.0;
    addText(s, m, x, 1.65, 0.82, 0.26, { fontSize: 7, color: C.gray, align: "center" });
    s.addShape(pptx.ShapeType.rect, { x, y: 2.1, w: 0.82, h: 2.5, fill: { color: i < 2 || i === 11 ? C.paleRed : i < 5 ? C.paleGreen : i < 8 ? C.paleBlue : "EEE5D4" }, line: { color: C.white, width: 1 } });
  });
  const events = [
    [0, 2, "边境暖冬季", C.red],
    [2, 3, "草莓花季", C.green],
    [5, 3, "鸭绿江之夜", C.blue],
    [8, 2, "331自驾节", C.gold],
    [9, 2, "银杏城市季", C.gold],
  ];
  events.forEach((e, idx) => {
    const y = 2.28 + (idx % 2) * 0.88;
    s.addShape(pptx.ShapeType.roundRect, { x: 0.68 + e[0] * 1.0, y, w: e[1] * 1.0 - 0.18, h: 0.62, fill: { color: e[3] }, line: { color: e[3] } });
    addText(s, e[2], 0.73 + e[0] * 1.0, y + 0.12, e[1] * 1.0 - 0.28, 0.34, { fontSize: 8, color: C.white, bold: true, align: "center" });
  });
  const mechanism = [
    ["每季", "形成一个全国传播主题"],
    ["每月", "至少一个可预订事件产品"],
    ["每周", "演艺、市集、社群活动常态更新"],
    ["每天", "官方账号发布实时玩法与服务信息"],
  ];
  mechanism.forEach((m, i) => addCard(s, 0.65 + i * 3.08, 5.08, 2.72, 1.08, m[0], m[1], { shadow: false, titleSize: 11, bodySize: 7.8, fill: C.paper, line: C.light }));
}

// 22 产品客群章节
{
  const s = pptx.addSlide();
  addSectionBand(s, "05", "产品与客群：\n从“到访”走向“复访”", "组合空间、票务与人群，重建丹东旅游收益模型", ["停留时长", "组合票", "自驾研学", "银发旅居"]);
}

// 23 时长产品
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "05 · PRODUCT LADDER", "以停留时长为主线，构建“半日—三日—旅居”产品阶梯");
  const ladder = [
    ["半日", "断桥 + 纪念馆", "城市初识"],
    ["1日", "虎山—沿江—断桥—夜游", "核心闭环"],
    ["2日", "沿江 + 凤凰山/温泉", "山水度假"],
    ["3日", "沿江 + 海岛/乡村", "全域体验"],
    ["7日+", "温泉康养 + 社群课程", "银发旅居"],
  ];
  ladder.forEach((l, i) => {
    const x = 0.65 + i * 2.45;
    const h = 1.2 + i * 0.58;
    const y = 5.65 - h;
    s.addShape(pptx.ShapeType.roundRect, { x, y, w: 2.12, h, fill: { color: i === 4 ? C.ink : [C.paleBlue, "D7E4E0", C.paleGreen, "EEE5D4"][Math.min(i, 3)] }, line: { color: i === 4 ? C.ink : C.white } });
    addText(s, l[0], x + 0.16, y + 0.18, 1.25, 0.36, { fontSize: 15, color: i === 4 ? C.gold : C.red, bold: true });
    addText(s, l[1], x + 0.16, y + 0.72, 1.76, Math.max(0.55, h - 1.2), { fontSize: 9.5, color: i === 4 ? C.white : C.ink, bold: true, valign: "top" });
    addText(s, l[2], x + 0.16, y + h - 0.42, 1.7, 0.25, { fontSize: 6.8, color: i === 4 ? "B9CDCA" : C.gray });
  });
  addText(s, "战略指标", 0.7, 6.26, 0.85, 0.25, { fontSize: 8, color: C.red, bold: true });
  addText(s, "优先提升过夜率与夜间消费，不以单纯客流量作为首要考核", 1.72, 6.15, 9.3, 0.38, { fontSize: 14, color: C.ink, bold: true });
}

// 24 票务
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "05 · TICKETING", "以“产品包”替代“景点票”：让游客更容易多玩、多住、多消费");
  const packs = [
    ["城市夜游包", "断桥 + 游船 + 演艺 + 夜食券", "年轻人 / 家庭"],
    ["沿江一日包", "虎山 + 快线 + 驿站权益 + 断桥", "高铁客 / 团队"],
    ["331出发包", "起点仪式 + 自驾路书 + 补能 + 住宿", "自驾 / 摩旅"],
    ["银发旅居包", "温泉 + 适老交通 + 课程 + 医疗协同", "银发 / 疗休养"],
  ];
  packs.forEach((p, i) => addCard(s, 0.65 + (i % 2) * 6.1, 1.68 + Math.floor(i / 2) * 2.05, 5.72, 1.63, p[0], p[1], { shadow: false, fill: i === 0 ? C.paleRed : C.paper, line: i === 0 ? C.paleRed : C.light, titleSize: 14, bodySize: 9 }));
  packs.forEach((p, i) => addPill(s, p[2], 4.55 + (i % 2) * 6.1, 1.94 + Math.floor(i / 2) * 2.05, 1.45, C.ink, C.paleBlue));
  addText(s, "实施关键", 0.7, 5.95, 0.85, 0.25, { fontSize: 8, color: C.red, bold: true });
  addText(s, "统一入口｜动态定价｜跨主体分账｜会员沉淀｜淡旺季调节", 1.72, 5.83, 8.8, 0.42, { fontSize: 15, color: C.ink, bold: true });
}

// 25 客群
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "05 · AUDIENCE", "客群导入：不同人群，不同理由、不同渠道、不同产品");
  const rows = [
    [
      { text: "核心客群", options: { bold: true, color: C.white, fill: C.ink } },
      { text: "来丹东理由", options: { bold: true, color: C.white, fill: C.ink } },
      { text: "首推产品", options: { bold: true, color: C.white, fill: C.ink } },
      { text: "主要渠道", options: { bold: true, color: C.white, fill: C.ink } },
    ],
    ["东北城市家庭", "避暑、亲子、周末", "沿江夜游 + 研学", "高铁、亲子社群"],
    ["全国自驾客", "331起点、边境探索", "起点仪式 + 路书", "自驾平台、车友会"],
    ["青年客群", "边境打卡、夜生活", "城市漫游 + 演艺", "小红书、抖音"],
    ["银发客群", "温泉、康养、慢节奏", "7—21日旅居", "协会、疗休养机构"],
    ["研学团队", "红色、国防、地理", "主题课程 + 任务线", "学校、研学机构"],
  ];
  addTable(s, rows, 0.65, 1.65, 12.0, 4.32, [2.0, 3.1, 3.6, 3.3], { fontSize: 8.7, rowH: 0.72 });
  addText(s, "近程做频次｜远程做主题｜年轻人做传播｜银发做停留｜研学做淡季", 0.72, 6.22, 11.8, 0.35, { fontSize: 14, color: C.red, bold: true, align: "center" });
}

// 26 银发与回流
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "05 · LONG-STAY ECONOMY", "更高维度：让旅游成为人口回流与城市更新的入口");
  const rings = [
    [4.42, 1.57, 4.5, 4.5, C.paleBlue, "旅游到访"],
    [5.08, 2.23, 3.18, 3.18, C.paleGreen, "旅居停留"],
    [5.73, 2.88, 1.88, 1.88, C.ink, "人口\n回流"],
  ];
  rings.forEach((r, i) => {
    s.addShape(pptx.ShapeType.ellipse, { x: r[0], y: r[1], w: r[2], h: r[2], fill: { color: r[4], transparency: i < 2 ? 8 : 0 }, line: { color: C.white, width: 1.5 } });
    if (i === 0) addText(s, r[5], 5.88, 1.88, 1.6, 0.35, { fontSize: 11, color: C.ink, bold: true, align: "center" });
    if (i === 1) addText(s, r[5], 5.8, 2.52, 1.7, 0.35, { fontSize: 11, color: C.ink, bold: true, align: "center" });
    if (i === 2) addText(s, r[5], 6.08, 3.48, 1.2, 0.78, { fontSize: 14, color: C.white, bold: true, align: "center", breakLine: true });
  });
  addCard(s, 0.65, 1.75, 3.3, 1.3, "银发旅居", "温泉、医疗协同、老年大学、社群活动、长期租住", { shadow: false, fill: C.paper, line: C.light });
  addCard(s, 0.65, 4.45, 3.3, 1.3, "返乡消费", "面向丹东籍外地人口设计探亲度假、节庆与置业服务", { shadow: false, fill: C.paper, line: C.light });
  addCard(s, 9.38, 1.75, 3.3, 1.3, "青年主理人", "用低成本空间、内容场景和创业支持吸引返乡创业", { shadow: false, fill: C.paper, line: C.light });
  addCard(s, 9.38, 4.45, 3.3, 1.3, "城市宜居", "文旅改善夜生活、公共空间与服务，反向增强留人能力", { shadow: false, fill: C.paper, line: C.light });
}

// 27 IP
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "05 · CITY IP", "城市IP不是一句口号，而是一套持续生产内容的系统");
  s.addShape(pptx.ShapeType.ellipse, { x: 4.98, y: 2.0, w: 3.25, h: 3.25, fill: { color: C.ink }, line: { color: C.gold, width: 2 } });
  addText(s, "城市母IP", 5.62, 2.75, 2.0, 0.4, { fontSize: 15, color: C.gold, bold: true, align: "center" });
  addText(s, "江山起点\n边境丹东", 5.55, 3.35, 2.1, 0.92, { fontSize: 20, color: C.white, bold: true, align: "center", breakLine: true });
  const satellites = [
    [0.65, 1.55, "331起点IP", "出发仪式 / 自驾节", C.red],
    [9.38, 1.55, "鸭绿江夜IP", "夜航 / 演艺 / 夜食", C.blue],
    [0.65, 4.75, "四季生活IP", "草莓 / 银杏 / 温泉", C.green],
    [9.38, 4.75, "和平记忆IP", "断桥 / 研学 / 国际表达", C.gold],
  ];
  satellites.forEach((a) => {
    addCard(s, a[0], a[1], 3.1, 1.25, a[2], a[3], { shadow: false, fill: C.paper, line: a[4], lineWidth: 1.5, titleSize: 12, bodySize: 8 });
    s.addShape(pptx.ShapeType.line, { x: a[0] < 4 ? a[0] + 3.1 : 8.22, y: a[1] + 0.62, w: a[0] < 4 ? 1.25 : 1.16, h: a[1] < 3 ? 0.68 : -0.68, line: { color: a[4], width: 1.3, dash: "dash" } });
  });
}

// 28 标杆
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "05 · BENCHMARKS", "学河南，不学“仿古”：学习持续运营、全城联动与内容更新");
  const cases = [
    ["洛阳", "全城场景化", "一个主题贯穿景区、街区、服饰、餐饮与传播"],
    ["开封", "高频演艺", "演出成为日常运营，不依赖一次性大型节庆"],
    ["老君山", "情绪内容", "用年轻化表达把资源转化为社交传播"],
    ["淄博 / 天水", "全城承接", "政府服务、价格治理与市民参与共同托住流量"],
    ["阿勒泰", "生活方式", "目的地卖的不是景点，而是向往的日常"],
  ];
  cases.forEach((c, i) => {
    const y = 1.62 + i * 0.92;
    addText(s, c[0], 0.7, y, 1.35, 0.42, { fontSize: 12, color: i === 0 ? C.red : C.ink, bold: true });
    addText(s, c[1], 2.22, y, 1.55, 0.42, { fontSize: 11, color: C.blue, bold: true });
    addText(s, c[2], 4.05, y, 7.9, 0.5, { fontSize: 8.8, color: C.gray });
    s.addShape(pptx.ShapeType.line, { x: 0.7, y: y + 0.65, w: 11.55, h: 0, line: { color: C.light, width: 0.8 } });
  });
  addPill(s, "丹东转化", 0.7, 6.32, 1.3, C.white, C.red);
  addText(s, "边境真实场景 + 鸭绿江生活 + 高频内容运营", 2.2, 6.23, 7.85, 0.42, { fontSize: 15, color: C.ink, bold: true });
}

// 29 行动机制章节
{
  const s = pptx.addSlide();
  addSectionBand(s, "06", "行动机制：\n从共识走向项目落地", "先解决跨部门统筹，再解决项目投资", ["一套机制", "一张清单", "一个示范区", "一组可量化指标"]);
}

// 30 治理
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "06 · GOVERNANCE", "建议建立市级沿江文旅统筹机制，打破条块分割");
  const centerX = 5.03;
  s.addShape(pptx.ShapeType.roundRect, { x: centerX, y: 2.65, w: 3.15, h: 1.3, fill: { color: C.ink }, line: { color: C.ink } });
  addText(s, "鸭绿江沿江文旅\n统筹协调机制", centerX + 0.3, 2.92, 2.55, 0.76, { fontSize: 16, color: C.white, bold: true, align: "center", breakLine: true });
  const deps = [
    [0.65, 1.42, "文旅", "产品与运营"],
    [0.65, 4.78, "住建 / 城管", "风貌与夜景"],
    [4.93, 5.18, "交通", "快线与慢行"],
    [9.5, 4.78, "属地政府", "村镇与社区"],
    [9.5, 1.42, "公安 / 边防", "安全与秩序"],
    [4.93, 1.05, "国资 / 市场主体", "投资与分账"],
  ];
  deps.forEach((d) => {
    addCard(s, d[0], d[1], 3.15, 0.9, d[2], d[3], { shadow: false, fill: C.paper, line: C.light, titleSize: 11, bodySize: 7.6 });
    const x1 = d[0] < 4 ? d[0] + 3.15 : d[0] > 8 ? 8.18 : d[0] + 1.58;
    const y1 = d[1] < 2.4 ? d[1] + 0.9 : d[1];
    const x2 = d[0] < 4 ? 5.03 : d[0] > 8 ? 8.18 : 6.6;
    const y2 = d[1] < 2.4 ? 2.65 : 3.95;
    s.addShape(pptx.ShapeType.line, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), line: { color: C.gold, width: 1, dash: "dash" } });
  });
}

// 31 90天
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "06 · FIRST 90 DAYS", "先做八件可启动、可见效、可形成共识的事");
  const actions = [
    ["01", "成立沿江统筹专班", "明确牵头领导、部门接口与周调度机制"],
    ["02", "启动专项规划", "编制虎山—断桥空间与产业一体化方案"],
    ["03", "确定夜游示范区", "优先断桥—码头，先内容后重资产"],
    ["04", "发布暑期行动", "夜航、快线、延时开放、周末演出"],
    ["05", "设计组合票", "打通景区、游船、交通、演艺和酒店"],
    ["06", "形成品质导则", "风貌、店招、灯光、业态准入统一"],
    ["07", "策划331起点", "标志、仪式、路书、车友运营同步"],
    ["08", "引入运营团队", "演艺、游船、票务和城市内容专业化"],
  ];
  actions.forEach((a, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.65 + col * 6.1;
    const y = 1.58 + row * 1.24;
    addText(s, a[0], x, y, 0.52, 0.36, { fontFace: "Arial", fontSize: 12, color: C.red, bold: true });
    addText(s, a[1], x + 0.68, y, 2.25, 0.35, { fontSize: 11.5, color: C.ink, bold: true });
    addText(s, a[2], x + 0.68, y + 0.43, 4.6, 0.38, { fontSize: 7.8, color: C.gray });
    s.addShape(pptx.ShapeType.line, { x, y: y + 0.98, w: 5.52, h: 0, line: { color: C.light, width: 0.8 } });
  });
  addText(s, "首个可见成果", 0.7, 6.62, 1.35, 0.24, { fontSize: 8, color: C.red, bold: true });
  addText(s, "“鸭绿江之夜”暑期样板 + 虎山—断桥沿江品质提升任务书", 2.12, 6.49, 8.8, 0.42, { fontSize: 14, color: C.ink, bold: true });
}

// 32 路线图
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "06 · ROADMAP", "三阶段推进：示范引爆—廊道成型—全域联动");
  const stages = [
    ["阶段一", "近期示范", "0—12个月", ["断桥—码头夜游", "暑期快线与组合票", "沿江导则与节点整治"], C.red],
    ["阶段二", "廊道成型", "1—3年", ["驿站与慢行系统", "三级演艺常态化", "331起点品牌运营"], C.gold],
    ["阶段三", "全域升级", "3—5年", ["山海温泉联动", "银发旅居网络", "东北亚边境旅游门户"], C.green],
  ];
  stages.forEach((st, i) => {
    const x = 0.7 + i * 4.15;
    addText(s, st[0], x, 1.62, 1.2, 0.3, { fontSize: 9, color: st[4], bold: true });
    addText(s, st[1], x, 2.02, 2.7, 0.42, { fontSize: 18, color: C.ink, bold: true });
    addPill(s, st[2], x, 2.62, 1.3, C.ink, C.paper);
    s.addShape(pptx.ShapeType.line, { x, y: 3.28, w: 3.58, h: 0, line: { color: st[4], width: 5 } });
    st[3].forEach((v, j) => {
      addText(s, `• ${v}`, x, 3.72 + j * 0.62, 3.42, 0.38, { fontSize: 10, color: j === 0 ? C.ink : C.gray, bold: j === 0 });
    });
    if (i < 2) addArrow(s, x + 3.62, 3.1, 0.32, C.red);
  });
  addText(s, "投资逻辑", 0.72, 6.18, 0.9, 0.25, { fontSize: 8, color: C.red, bold: true });
  addText(s, "公共空间政府先行｜运营项目市场主导｜重资产项目以验证后的真实需求为前提", 1.75, 6.06, 10.5, 0.42, { fontSize: 13, color: C.ink, bold: true });
}

// 33 指标
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "06 · KPI", "评价标准从“来了多少人”转向“留下多少价值”");
  const kpis = [
    ["停留", "平均停留时长", "过夜率"],
    ["消费", "游客客单价", "夜间消费占比"],
    ["运营", "组合票转化率", "演艺上座率"],
    ["四季", "淡季入住率", "季度客流波动"],
    ["城市", "返乡创业项目", "旅居人口规模"],
    ["口碑", "游客满意度", "网络正向声量"],
  ];
  kpis.forEach((k, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    addCard(s, 0.65 + col * 4.12, 1.68 + row * 2.15, 3.75, 1.75, k[0], `${k[1]}\n${k[2]}`, { number: `0${i + 1}`, shadow: false, fill: row === 0 ? C.paper : C.paleBlue, line: row === 0 ? C.light : C.paleBlue, titleSize: 13, bodySize: 10 });
  });
  addText(s, "建议建立月度驾驶舱：文旅、交通、住宿、票务、舆情数据联动", 0.72, 6.25, 11.85, 0.38, { fontSize: 14, color: C.red, bold: true, align: "center" });
}

// 34 政府讨论题
{
  const s = pptx.addSlide("MASTER");
  addTitle(s, "DISCUSSION", "本次政府研讨建议聚焦六个需要拍板的问题");
  const qs = [
    ["01", "是否将虎山—断桥确定为全市文旅第一战略廊道？"],
    ["02", "由哪个市级机制统一规划、建设、运营和利益协调？"],
    ["03", "断桥—码头夜游示范区的边界、投入和运营主体如何确定？"],
    ["04", "331起点如何从标志工程转为长期运营的国家级IP？"],
    ["05", "暑期行动中哪些事项可立即启动，哪些需要专项论证？"],
    ["06", "如何用过夜率、夜间消费和淡季入住率重设考核指标？"],
  ];
  qs.forEach((q, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.65 + col * 6.12;
    const y = 1.63 + row * 1.55;
    addText(s, q[0], x, y, 0.55, 0.35, { fontFace: "Arial", fontSize: 13, color: C.red, bold: true });
    addText(s, q[1], x + 0.72, y, 4.95, 0.8, { fontSize: 12.5, color: C.ink, bold: true, valign: "top" });
    s.addShape(pptx.ShapeType.line, { x, y: y + 1.17, w: 5.5, h: 0, line: { color: C.light, width: 1 } });
  });
  addText(s, "建议会后形成", 0.7, 6.35, 1.2, 0.25, { fontSize: 8, color: C.red, bold: true });
  addText(s, "一个领导机制｜一份专项任务书｜一批近期项目｜一套年度运营日历", 2.02, 6.22, 9.7, 0.42, { fontSize: 14, color: C.ink, bold: true });
}

// 35 结束
{
  const s = pptx.addSlide();
  s.background = { color: C.ink };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 0.18, h: 7.5, fill: { color: C.red }, line: { color: C.red } });
  addText(s, "下一步，不是再讨论丹东“有什么”", 0.78, 1.42, 8.9, 0.65, { fontSize: 24, color: "B9CCCA", bold: false });
  addText(s, "而是决定先把什么做成。", 0.78, 2.28, 8.9, 0.72, { fontSize: 31, color: C.white, bold: true });
  s.addShape(pptx.ShapeType.line, { x: 0.8, y: 3.42, w: 2.0, h: 0, line: { color: C.gold, width: 4 } });
  addText(s, "建议首抓：虎山—断桥沿江廊道 × 鸭绿江之夜", 0.8, 4.02, 8.7, 0.55, { fontSize: 17, color: C.gold, bold: true });
  addPhotoPlaceholder(s, 9.7, 1.05, 2.95, 5.05, "结束页城市夜景");
  addText(s, "图片替换说明：所有灰色虚线框均为独立形状，可在PowerPoint中删除后插入图片；其余图形和文字均可编辑。", 0.8, 6.64, 8.2, 0.3, { fontSize: 7, color: "789694" });
}

pptx.writeFile({ fileName: OUT });
