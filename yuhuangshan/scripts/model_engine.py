# -*- coding: utf-8 -*-
"""通化玉皇山公园经营测算引擎：先校准约束，再供 Excel 生成器复用。"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# 表5 改造投资（万元）
# ---------------------------------------------------------------------------
CAPEX_LINES = [
    ("1.1.1", "南入口车场改造提升", 600, "平方米", 300, "临建+构筑物", "基础设施"),
    ("1.1.2", "大门及5处亭子银丝古建改造", 1, "项", 120000, "", "基础设施"),
    ("1.1.3", "游客中心建设", 300, "平方米", 3500, "", "基础设施"),
    ("1.1.4", "卫生间/园区导视", 1, "项", 650000, "", "基础设施"),
    ("1.1.5", "智慧公园系统", 1, "项", 350000, "", "基础设施"),
    ("1.1.6", "零碳园区设施改造", 1, "项", 500000, "", "基础设施"),
    ("1.1.7", "园区亮化", 1, "项", 350000, "", "基础设施"),
    ("1.1.8", "观景台改造", 6, "项", 150000, "", "基础设施"),
    ("1.1.9", "山谷栈道", 300, "米", 4500, "含灯光", "基础设施"),
    ("1.1.10", "许愿树", 1, "项", 300000, "", "基础设施"),
    ("1.1.11", "观光车购买", 8, "辆", 110000, "", "基础设施"),
    ("1.2.1", "儿童公园IP引入及设施购置", 1, "项", 7500000, "", "超级儿童乐园"),
    ("1.2.2", "儿童公园冬季戏雪换装及设备", 1, "项", 600000, "", "超级儿童乐园"),
    ("1.2.3", "儿童乐园配套设施", 687, "平方米", 2500, "按160万元计", "超级儿童乐园"),
    ("1.3.1", "情景造型搭建", 500, "平方米", 4500, "", "青年街区"),
    ("1.3.2", "夜场灯光", 1, "项", 150000, "", "青年街区"),
    ("1.3.3", "配套水电", 1, "项", 450000, "", "青年街区"),
    ("1.4.1", "原舍改造", 1, "项", None, "30万元", "动物观赏区"),
    ("1.4.2", "新增萌宠", 5, "项", None, "35万元", "动物观赏区"),
    ("1.4.3", "动物互动", 2, "项", None, "35万元", "动物观赏区"),
    ("1.4.4", "动物零食售卖亭", 1, "项", None, "10万元", "动物观赏区"),
    ("1.4.5", "动物医院", 1, "项", None, "15万元", "动物观赏区"),
    ("1.5.1", "玉皇山大马戏", 1000, "平方米", 1500, "原网球场", "网球场/水塘"),
    ("1.5.2", "室内高尔夫", 1, "项", 450000, "", "网球场/水塘"),
    ("1.5.3", "湖畔影院", 500, "平方米", 3500, "水体治理及构筑物", "网球场/水塘"),
    ("1.5.4", "健身区提升", 1, "项", 250000, "", "网球场/水塘"),
    ("1.6.1", "场地整理", 1, "项", 250000, "", "庙会/市集"),
    ("1.6.2", "照明/美陈", 1, "项", 80000, "", "庙会/市集"),
    ("1.6.3", "商亭/摊位", 1, "项", 450000, "", "庙会/市集"),
    ("1.7.1", "素食餐厅", 354, "平方米", 2000, "索道房", "既有房屋"),
    ("1.7.2", "森林剧场", 350, "平方米", 1800, "迷宫", "既有房屋"),
    ("1.7.3", "茶屋氧吧", 920, "平方米", 1500, "花窖", "既有房屋"),
    ("1.8.1", "研学展馆临建", 1, "项", 650000, "VR大空间", "红色记忆"),
    ("1.8.2", "冬季抗联体验", 1, "项", 250000, "", "红色记忆"),
    ("1.8.3", "林学科普及衍生品", 1, "项", 350000, "", "红色记忆"),
    ("1.9.1", "山洞酒庄", 1, "项", 150000, "防空洞", "花海/露营/低碳林"),
    ("1.9.2", "婚礼花园", 1, "项", 350000, "", "花海/露营/低碳林"),
    ("1.9.3", "林地树屋", 1, "项", 400000, "", "花海/露营/低碳林"),
    ("1.9.4", "禅修道苑", 1, "项", 180000, "", "花海/露营/低碳林"),
    ("1.9.5", "雪地冰屋", 1, "项", 200000, "", "花海/露营/低碳林"),
    ("1.9.6", "悬崖咖啡", 1, "项", 3000000, "", "花海/露营/低碳林"),
    ("1.9.7", "低碳林", 1, "项", 450000, "", "花海/露营/低碳林"),
    ("1.9.8", "星空露营区", 1, "项", 300000, "", "花海/露营/低碳林"),
    ("1.9.9", "花海", 1, "项", 150000, "", "花海/露营/低碳林"),
    ("1.9.10", "林间小品", 1, "项", 250000, "", "花海/露营/低碳林"),
]

# 表5中直接给造价、不走 工程量×单价 的行
CAPEX_LUMPSUM = {
    "1.2.3": 160.0,
    "1.4.1": 30.0,
    "1.4.2": 35.0,
    "1.4.3": 35.0,
    "1.4.4": 10.0,
    "1.4.5": 15.0,
}


def capex_amount(qty, unit_price, code):
    if code in CAPEX_LUMPSUM:
        return CAPEX_LUMPSUM[code]
    return qty * unit_price / 10000.0


def build_investment():
    engineering = 0.0
    groups = {}
    lines = []
    for code, name, qty, unit, price, note, group in CAPEX_LINES:
        amt = capex_amount(qty, price or 0, code)
        engineering += amt
        groups[group] = groups.get(group, 0.0) + amt
        lines.append(
            {
                "code": code,
                "name": name,
                "qty": qty,
                "unit": unit,
                "price": price,
                "amount": amt,
                "note": note,
                "group": group,
            }
        )
    class2 = engineering * 0.095
    contingency = (engineering + class2) * 0.05
    construction = engineering + class2 + contingency
    interest = construction * 0.8 * 0.048 * 2.0
    mgmt = 300.0
    total = construction + interest + mgmt
    loan = construction * 0.8
    return {
        "lines": lines,
        "groups": groups,
        "engineering": engineering,
        "class2": class2,
        "contingency": contingency,
        "construction": construction,
        "interest": interest,
        "mgmt": mgmt,
        "total": total,
        "loan": loan,
        "rate": 0.048,
        "loan_ratio": 0.8,
    }


# ---------------------------------------------------------------------------
# 表6 人流模型
# ---------------------------------------------------------------------------
# 项目年1-2建设；第3年对齐表6「3年」达产；第4-18年对齐「4~18年保底」
VISITOR_MAP = {
    1: {"stage": "建设期", "visitors": 0.0, "pay_rate": 0.0, "ticket": 0.0},
    2: {"stage": "建设期", "visitors": 0.0, "pay_rate": 0.0, "ticket": 0.0},
    3: {"stage": "开业达产", "visitors": 75.0, "pay_rate": 0.85, "ticket": 150.0},
}
for _y in range(4, 19):
    VISITOR_MAP[_y] = {
        "stage": "稳定保底",
        "visitors": 80.0,
        "pay_rate": 0.85,
        "ticket": 150.0,
    }

# 表6原四档，供对照
VISITOR_TABLE6 = {
    "1年": (50.0, 0.50, 80.0),
    "2年": (60.0, 0.60, 120.0),
    "3年": (75.0, 0.85, 150.0),
    "4~18年": (80.0, 0.85, 150.0),
}


# ---------------------------------------------------------------------------
# 业态参数（公园账面收入口径）
# 联营：收入=游客GMV×公园分成，成本不再二次扣分成、不承担对方人工
# 出租：收入=租金
# 自营：收入=全额GMV，承担货品/能源/编制
# 品牌加盟：全额流水入账，万达门票分成进成本
# ---------------------------------------------------------------------------
# driver:
#   traffic: visitors(万人) * conv * price * share / 1  → 万元  (price元)
#   rent: area * daily * days * occ / 10000
#   event: events * price_wan * util
#   babyking: 专项
#   fixed: 固定万元 * 人流系数


@dataclass
class Project:
    key: str
    name: str
    sector: str
    nature: str  # 联营 / 自营 / 出租 / 品牌加盟
    driver: str
    share: float = 1.0
    conv: float = 0.0
    price: float = 0.0
    area: float = 0.0
    daily_rent: float = 0.0
    days: float = 365.0
    occ: float = 1.0
    events: float = 0.0
    event_price: float = 0.0
    util: float = 1.0
    fixed: float = 0.0
    cogs: float = 0.0
    channel: float = 0.0
    opex: float = 0.0
    staff: int = 0
    cap_note: str = ""
    source: str = "表6"
    fill: bool = False


PROJECTS = [
    Project(
        "circus",
        "玉皇山大马戏",
        "核心引流",
        "联营",
        "traffic",
        share=0.20,
        conv=0.18,
        price=62,
        cogs=0.02,
        channel=0.01,
        opex=0.03,
        staff=0,
        cap_note="600座×2场×240天×70%×58元≈1,169万GMV，公园分成20%",
        source="表6+表5原网球场",
    ),
    Project(
        "babyking",
        "超级宝贝王",
        "亲子核心",
        "品牌加盟",
        "babyking",
        share=1.0,
        staff=26,
        cap_note="年接待上限40万人；万达仅对门票/体验流水计提10%",
        source="表6品牌加盟",
    ),
    Project(
        "gift",
        "土特产伴手礼",
        "文创零售",
        "自营",
        "traffic",
        share=1.0,
        conv=0.18,
        price=48,
        cogs=0.48,
        channel=0.04,
        opex=0.03,
        staff=3,
        cap_note="全园转化16%、客单48元，低于20%×60元上限",
        source="表6自营",
    ),
    Project(
        "pet",
        "动物萌宠互动",
        "亲子互动",
        "联营",
        "traffic",
        share=0.40,
        conv=0.08,
        price=25,
        cogs=0.02,
        channel=0.01,
        opex=0.03,
        staff=0,
        cap_note="互动接待约日350人，公园分成40%",
        source="表6联营",
    ),
    Project(
        "cinema",
        "湖畔影院",
        "文化娱乐",
        "联营",
        "traffic",
        share=0.60,
        conv=0.08,
        price=32,
        cogs=0.02,
        channel=0.01,
        opex=0.03,
        staff=0,
        cap_note="160座×2.2场×250天容量内",
        source="表6联营",
    ),
    Project(
        "youth",
        "青年街区",
        "青年消费",
        "出租",
        "rent",
        area=500,
        daily_rent=6.8,
        days=365,
        occ=0.95,
        cogs=0.0,
        channel=0.0,
        opex=0.06,
        staff=0,
        cap_note="500㎡情景街区，租金6.2元/㎡/天",
        source="表6出租",
    ),
    Project(
        "teahouse",
        "茶屋氧吧",
        "餐饮休闲",
        "联营",
        "rent",
        area=920,
        daily_rent=5.4,
        days=365,
        occ=1.0,
        cogs=0.0,
        channel=0.0,
        opex=0.04,
        staff=0,
        cap_note="花窖920㎡保底租金5.4元/㎡/天，另按人流计提15%茶饮分成",
        source="表6联营(保底+分成)",
    ),
    Project(
        "veg",
        "素食餐厅",
        "餐饮休闲",
        "联营",
        "traffic",
        share=0.20,
        conv=0.14,
        price=72,
        cogs=0.02,
        channel=0.01,
        opex=0.03,
        staff=0,
        cap_note="索道房改造，公园分成20%；翻台受4次/日约束",
        source="表6联营",
    ),
    Project(
        "market",
        "庙会/市集",
        "商业配套",
        "联营",
        "event",
        events=40,
        event_price=8.8,
        util=1.0,
        cogs=0.02,
        channel=0.01,
        opex=0.04,
        staff=2,
        cap_note="36个经营日×摊位及联营综合8.5万元/日",
        source="表6联营",
    ),
    Project(
        "wedding",
        "婚礼花园",
        "活动经济",
        "自营",
        "event",
        events=90,
        event_price=2.4,
        util=0.75,
        cogs=0.28,
        channel=0.08,
        opex=0.04,
        staff=3,
        cap_note="年可承接90个经营日，场地费为主",
        source="表6自营",
    ),
    Project(
        "icehouse",
        "雪地冰屋",
        "冬季产品",
        "出租",
        "fixed",
        fixed=36,
        cogs=0.0,
        opex=0.06,
        staff=0,
        cap_note="季节性出租，租金年度浮动",
        source="表6出租",
    ),
    Project(
        "theater",
        "森林剧场",
        "演艺夜游",
        "联营",
        "traffic",
        share=0.60,
        conv=0.12,
        price=58,
        cogs=0.02,
        channel=0.02,
        opex=0.03,
        staff=1,
        cap_note="迷宫改建，公园分成60%",
        source="表6联营",
    ),
    Project(
        "zen",
        "禅修道苑",
        "康养文化",
        "联营",
        "traffic",
        share=0.40,
        conv=0.012,
        price=120,
        cogs=0.02,
        channel=0.01,
        opex=0.03,
        staff=0,
        cap_note="小团预约，公园分成40%",
        source="表6联营",
    ),
    Project(
        "coffee",
        "悬崖咖啡",
        "餐饮休闲",
        "联营",
        "traffic",
        share=0.20,
        conv=0.16,
        price=58,
        cogs=0.02,
        channel=0.01,
        opex=0.03,
        staff=0,
        cap_note="表5已列300万元改造，公园分成20%",
        source="表6联营",
    ),
    Project(
        "wish",
        "许愿祈福",
        "文化体验",
        "联营",
        "traffic",
        share=0.60,
        conv=0.06,
        price=22,
        cogs=0.02,
        channel=0.01,
        opex=0.02,
        staff=0,
        cap_note="许愿树已投资，公园分成60%",
        source="表6联营",
    ),
    Project(
        "treehouse",
        "树屋及星空露营",
        "住宿体验",
        "联营",
        "traffic",
        share=0.30,
        conv=0.015,
        price=220,
        cogs=0.02,
        channel=0.02,
        opex=0.04,
        staff=0,
        cap_note="树屋+露营区表5已投资，不新增单元，公园分成30%",
        source="表6联营+表5露营填充",
        fill=True,
    ),
    Project(
        "winery",
        "山洞酒庄",
        "特色消费",
        "自营",
        "traffic",
        share=1.0,
        conv=0.07,
        price=42,
        cogs=0.38,
        channel=0.05,
        opex=0.04,
        staff=3,
        cap_note="防空洞酒窖，品鉴+礼盒，自营利润约30%目标",
        source="表6自营",
    ),
    Project(
        "photo",
        "公园旅拍",
        "内容消费",
        "联营",
        "traffic",
        share=0.40,
        conv=0.008,
        price=380,
        cogs=0.03,
        channel=0.04,
        opex=0.03,
        staff=0,
        cap_note="表6已列业态但原收入为空；按单分佣，不新增硬件",
        source="表6联营(原空值填充)",
        fill=True,
    ),
    Project(
        "tram",
        "园区交通",
        "交通服务",
        "自营",
        "traffic",
        share=1.0,
        conv=0.28,
        price=12,
        cogs=0.18,
        channel=0.02,
        opex=0.06,
        staff=10,
        cap_note="8辆观光车不新增，转化28%、票价12元",
        source="表6自营",
    ),
    Project(
        "study",
        "红色研学/VR展馆",
        "研学团建",
        "自营",
        "traffic",
        share=1.0,
        conv=0.10,
        price=80,
        cogs=0.22,
        channel=0.06,
        opex=0.05,
        staff=2,
        cap_note="表5研学展馆+林学已投资，公园自营课程，不含宝贝王内部研学门票",
        source="表5红色记忆填充",
        fill=True,
    ),
    Project(
        "night",
        "夜游/主题灯光",
        "夜间经济",
        "自营",
        "traffic",
        share=1.0,
        conv=0.16,
        price=38,
        cogs=0.16,
        channel=0.05,
        opex=0.08,
        staff=4,
        cap_note="利用已列亮化/栈道/观景台，不新增改造项目",
        source="表5亮化栈道填充",
        fill=True,
    ),
    Project(
        "golf",
        "室内高尔夫",
        "运动休闲",
        "联营",
        "traffic",
        share=0.30,
        conv=0.03,
        price=80,
        cogs=0.02,
        channel=0.01,
        opex=0.03,
        staff=0,
        cap_note="表5已列45万元设备，公园分成30%",
        source="表5填充",
        fill=True,
    ),
    Project(
        "flower",
        "花海摄影",
        "观光打卡",
        "自营",
        "traffic",
        share=1.0,
        conv=0.10,
        price=18,
        cogs=0.15,
        channel=0.03,
        opex=0.05,
        staff=1,
        cap_note="表5花海已投资，摄影票/摆拍，轻运营",
        source="表5填充",
        fill=True,
    ),
    Project(
        "winter",
        "冬季抗联及戏雪",
        "冬季产品",
        "联营",
        "traffic",
        share=0.35,
        conv=0.10,
        price=48,
        cogs=0.02,
        channel=0.02,
        opex=0.04,
        staff=0,
        cap_note="表5抗联体验+儿童戏雪设备，季节性联营",
        source="表5填充",
        fill=True,
    ),
    Project(
        "snack",
        "动物零食售卖",
        "亲子互动",
        "自营",
        "traffic",
        share=1.0,
        conv=0.10,
        price=12,
        cogs=0.52,
        channel=0.02,
        opex=0.03,
        staff=1,
        cap_note="表5零食亭10万元已列",
        source="表5填充",
        fill=True,
    ),
    Project(
        "parkfee",
        "南入口停车场",
        "交通服务",
        "自营",
        "fixed",
        fixed=28,
        cogs=0.08,
        opex=0.10,
        staff=1,
        cap_note="600㎡车场提升后临停周转，不新增用地",
        source="表5填充",
        fill=True,
    ),
    Project(
        "gym",
        "健身区档期出租",
        "运动休闲",
        "出租",
        "fixed",
        fixed=18,
        opex=0.08,
        staff=0,
        cap_note="表5健身区提升25万元，轻出租",
        source="表5填充",
        fill=True,
    ),
    Project(
        "carbon",
        "林学科普衍生品",
        "文创零售",
        "自营",
        "traffic",
        share=1.0,
        conv=0.04,
        price=22,
        cogs=0.42,
        channel=0.04,
        opex=0.03,
        staff=1,
        cap_note="表5林学科普35万元已列",
        source="表5填充",
        fill=True,
    ),
    Project(
        "teahouse_share",
        "茶屋氧吧销售分成",
        "餐饮休闲",
        "联营",
        "traffic",
        share=0.15,
        conv=0.08,
        price=82,
        cogs=0.02,
        channel=0.01,
        opex=0.03,
        staff=0,
        cap_note="在保底租金之外，按茶饮流水15%分成，不新增改造",
        source="表6联营填充",
        fill=True,
    ),
    Project(
        "viewpoint",
        "栈道观景打卡",
        "观光打卡",
        "自营",
        "traffic",
        share=1.0,
        conv=0.08,
        price=16,
        cogs=0.08,
        channel=0.02,
        opex=0.04,
        staff=0,
        cap_note="表5观景台6处+山谷栈道已投资，售打卡票/预约时段",
        source="表5填充",
        fill=True,
    ),
]


# 人力：通化2026年含单位社保公积金的年成本
STAFF_ROWS = [
    ("公共", "园区负责人", 1, 18.0, "建设期后到岗"),
    ("公共", "运营副职", 1, 15.0, ""),
    ("公共", "财务/出纳", 2, 9.0, ""),
    ("公共", "行政人事", 2, 8.0, ""),
    ("公共", "企划营销", 2, 9.0, ""),
    ("公共", "票务客服", 6, 7.2, ""),
    ("公共", "安保", 7, 7.2, "两班，旺季用弹性补"),
    ("公共", "保洁", 5, 6.5, "核心节点保洁，其余外包进维修"),
    ("公共", "绿化", 3, 6.8, ""),
    ("公共", "维修电工", 3, 8.5, ""),
    ("公共", "动物保育员", 4, 7.5, "既有55只动物，不新增项目"),
    ("加盟", "宝贝王主管", 2, 9.6, "表6配备26人"),
    ("加盟", "宝贝王设备技工", 6, 7.8, ""),
    ("加盟", "宝贝王营运员", 18, 7.6, ""),
    ("自营", "礼品店员", 3, 7.2, "表6配备3人"),
    ("自营", "婚礼执行", 3, 8.0, "表6配备3人"),
    ("自营", "酒庄店员", 3, 7.5, "表6配备3人"),
    ("自营", "观光车司机", 8, 7.5, "8车"),
    ("自营", "交通调度", 2, 8.0, "表6交通共10人"),
    ("联营协助", "市集管理", 2, 7.5, "表6配备2人"),
    ("联营协助", "剧场场务", 1, 7.5, "表6配备1人"),
    ("自营", "研学讲解", 2, 8.0, "展馆自营填充"),
    ("自营", "夜游值班(年折算)", 4, 4.5, "季节工折年"),
    ("自营", "花海/零食/文创兼岗", 3, 6.8, "轻运营兼岗"),
    ("自营", "停车场值守", 1, 6.8, ""),
    ("公共", "旺季弹性用工", 1, 18.0, "按年包干，人数记1行"),
]


def staff_cost_full():
    rows = []
    total_head = 0
    total_cost = 0.0
    by_type = {}
    for typ, post, n, unit, note in STAFF_ROWS:
        cost = n * unit
        rows.append({"type": typ, "post": post, "n": n, "unit": unit, "cost": cost, "note": note})
        if post != "旺季弹性用工":
            total_head += n
        total_cost += cost
        by_type[typ] = by_type.get(typ, 0.0) + cost
    return {"rows": rows, "headcount": total_head, "cost": total_cost, "by_type": by_type}


def babyking_volume(visitors_wan: float):
    """研学+一般客流随全园人流放大，但封顶40万人。"""
    if visitors_wan <= 0:
        return dict(study=0, general=0, study_price=35, general_price=48, conv2=0.32, p2=18)
    study = min(20.0, visitors_wan * 0.24)
    general = min(20.0, visitors_wan * 0.24)
    if study + general > 40.0:
        scale = 40.0 / (study + general)
        study *= scale
        general *= scale
    return dict(study=study, general=general, study_price=35, general_price=48, conv2=0.32, p2=18)


def babyking_revenue(visitors_wan: float):
    v = babyking_volume(visitors_wan)
    ticket = v["study"] * v["study_price"] + v["general"] * v["general_price"]
    second = (v["study"] + v["general"]) * v["conv2"] * v["p2"]
    return ticket, second, ticket + second, v


def project_revenue(p: Project, visitors_wan: float) -> float:
    if visitors_wan <= 0 and p.driver != "fixed":
        return 0.0
    flow = visitors_wan * 10000.0  # 人
    if p.driver == "traffic":
        return flow * p.conv * p.price * p.share / 10000.0
    if p.driver == "rent":
        if visitors_wan <= 0:
            return 0.0
        return p.area * p.daily_rent * p.days * p.occ / 10000.0
    if p.driver == "event":
        if visitors_wan <= 0:
            return 0.0
        return p.events * p.event_price * p.util
    if p.driver == "fixed":
        if visitors_wan <= 0:
            return 0.0
        return p.fixed * (visitors_wan / 75.0)
    if p.driver == "babyking":
        return babyking_revenue(visitors_wan)[2]
    return 0.0


def project_direct_cost(p: Project, revenue: float) -> float:
    if revenue <= 0:
        return 0.0
    if p.nature == "品牌加盟":
        return 0.0  # 宝贝王单独拆
    # 联营/出租：收入已是公园所得，只留管理与分摊
    return revenue * (p.cogs + p.channel + p.opex)


def babyking_cost(visitors_wan: float, staff_cost_bk: float) -> dict:
    ticket, second, total, v = babyking_revenue(visitors_wan)
    if total <= 0:
        return dict(
            wanda=0,
            commission=0,
            maintain=0,
            cogs2=0,
            marketing=0,
            special=0,
            staff=0,
            utility=0,
            security=0,
            total=0,
            ticket=0,
            second=0,
            income=0,
        )
    wanda = ticket * 0.10
    commission = ticket * 0.70 * 0.10 * (v["general"] / max(v["study"] + v["general"], 1e-9))
    # 线上佣金仅一般客流：一般收入×70%×10%
    general_rev = v["general"] * v["general_price"]
    commission = general_rev * 0.70 * 0.10
    sales_bonus = total * 0.02
    maintain = ticket * 0.08
    cogs2 = second * 0.58
    marketing = ticket * 0.04
    special = 8.0 if visitors_wan >= 70 else 12.0
    utility = (v["study"] + v["general"]) * 1.65
    security = 28.0
    staff = staff_cost_bk
    cost = (
        wanda
        + commission
        + sales_bonus
        + maintain
        + cogs2
        + marketing
        + special
        + staff
        + utility
        + security
    )
    return dict(
        wanda=wanda,
        commission=commission,
        sales_bonus=sales_bonus,
        maintain=maintain,
        cogs2=cogs2,
        marketing=marketing,
        special=special,
        staff=staff,
        utility=utility,
        security=security,
        total=cost,
        ticket=ticket,
        second=second,
        income=total,
        volume=v,
    )


def public_overhead(visitors_wan: float, staff_public: float, total_rev: float) -> dict:
    if visitors_wan <= 0:
        return dict(
            staff=0,
            utility=0,
            marketing=0,
            maintain=0,
            insurance=0,
            office=0,
            animal_feed=0,
            total=0,
        )
    scale = visitors_wan / 75.0
    utility = 95.0 * scale
    marketing = max(90.0, total_rev * 0.018)
    maintain = 70.0 * scale
    insurance = 22.0
    office = 28.0
    animal_feed = 48.0  # 既有动物饲料医疗
    return dict(
        staff=staff_public,
        utility=utility,
        marketing=marketing,
        maintain=maintain,
        insurance=insurance,
        office=office,
        animal_feed=animal_feed,
        total=staff_public + utility + marketing + maintain + insurance + office + animal_feed,
    )


def run_model():
    inv = build_investment()
    staff = staff_cost_full()
    staff_bk = staff["by_type"].get("加盟", 0.0)
    staff_public = staff["by_type"].get("公共", 0.0)
    staff_self = (
        staff["by_type"].get("自营", 0.0) + staff["by_type"].get("联营协助", 0.0)
    )

    years = list(range(1, 19))
    rows = []
    for y in years:
        vm = VISITOR_MAP[y]
        vis = vm["visitors"]
        rec = {
            "year": y,
            "stage": vm["stage"],
            "visitors": vis,
            "pay_rate": vm["pay_rate"],
            "ticket": vm["ticket"],
            "visitor_check": vis * vm["pay_rate"] * vm["ticket"],
            "projects": {},
        }
        rev_liany = rev_self = rev_rent = rev_join = 0.0
        cost_liany = cost_self = cost_rent = 0.0
        for p in PROJECTS:
            if p.driver == "babyking":
                bk = babyking_cost(vis, staff_bk if vis > 0 else 0)
                rev = bk["income"]
                cost = bk["total"]
                rec["projects"][p.key] = {
                    "name": p.name,
                    "nature": p.nature,
                    "rev": rev,
                    "cost": cost,
                    "bk": bk,
                }
                rev_join += rev
                rec["bk"] = bk
            else:
                rev = project_revenue(p, vis)
                cost = project_direct_cost(p, rev)
                rec["projects"][p.key] = {
                    "name": p.name,
                    "nature": p.nature,
                    "rev": rev,
                    "cost": cost,
                }
                if p.nature == "联营":
                    rev_liany += rev
                    cost_liany += cost
                elif p.nature == "出租":
                    rev_rent += rev
                    cost_rent += cost
                else:
                    rev_self += rev
                    cost_self += cost
        # 自营编制进自营成本（不含宝贝王）
        if vis > 0:
            cost_self += staff_self

        total_rev = rev_liany + rev_self + rev_rent + rev_join
        oh = public_overhead(vis, staff_public if vis > 0 else 0, total_rev)
        rec["rev"] = dict(联营=rev_liany, 自营=rev_self, 出租=rev_rent, 加盟=rev_join, 合计=total_rev)
        rec["cost_direct"] = dict(联营=cost_liany, 自营=cost_self, 出租=cost_rent, 加盟=rec.get("bk", {}).get("total", 0.0))
        rec["overhead"] = oh
        rec["opex"] = (
            cost_liany
            + cost_self
            + cost_rent
            + rec["cost_direct"]["加盟"]
            + oh["total"]
            - oh["staff"]  # staff_public 已在 oh.total；自营编制已在 cost_self
        )
        # oh.total 含公共人力；加盟人力在 bk.total；自营人力在 cost_self
        rec["opex"] = cost_liany + cost_self + cost_rent + rec["cost_direct"]["加盟"] + (oh["total"] - 0)
        rec["contribution"] = total_rev - rec["opex"]
        rows.append(rec)

    # 折旧：总投资残值5%，经营期16年平均
    dep_annual = inv["total"] * 0.95 / 16.0
    # 贷款：建设期末余额，经营期前10年等额本金
    loan0 = inv["loan"]
    principal_annual = loan0 / 10.0

    for rec in rows:
        y = rec["year"]
        if y <= 2:
            rec["depreciation"] = 0.0
            rec["interest_exp"] = 0.0
            rec["principal"] = 0.0
            rec["loan_end"] = loan0 if y == 2 else loan0  # 建设期末形成贷款
            if y == 1:
                rec["loan_end"] = loan0
            rec["ebt"] = 0.0
            rec["tax"] = 0.0
            rec["net"] = 0.0
            rec["da"] = 0.0
            rec["ocf"] = 0.0
            rec["invest_cf"] = -inv["total"] / 2.0
            rec["fcf"] = rec["ocf"] + rec["invest_cf"]
        else:
            rec["depreciation"] = dep_annual
            k = y - 2  # 经营年 1..16
            if k <= 10:
                loan_beg = loan0 - principal_annual * (k - 1)
                rec["interest_exp"] = loan_beg * inv["rate"]
                rec["principal"] = principal_annual
                rec["loan_end"] = loan_beg - principal_annual
            else:
                rec["interest_exp"] = 0.0
                rec["principal"] = 0.0
                rec["loan_end"] = 0.0
            rec["ebt"] = rec["contribution"] - rec["depreciation"] - rec["interest_exp"]
            rec["tax"] = max(rec["ebt"], 0.0) * 0.25
            rec["net"] = rec["ebt"] - rec["tax"]
            rec["ocf"] = rec["net"] + rec["depreciation"] - rec["principal"]
            rec["invest_cf"] = 0.0
            rec["fcf"] = rec["ocf"] + rec["invest_cf"]

    # 累计与回收
    cum = 0.0
    payback = None
    for rec in rows:
        cum += rec["fcf"]
        rec["cum_fcf"] = cum
        if payback is None and rec["year"] >= 3 and cum >= 0:
            # 年内插值
            prev = rec["cum_fcf"] - rec["fcf"]
            frac = 0.0 if rec["fcf"] == 0 else (0 - prev) / rec["fcf"]
            payback = rec["year"] - 1 + frac

    # 经营期回收（不含建设期投资时间，用累计经营净现金流覆盖总投资）
    cum_ops = 0.0
    payback_ops = None
    for rec in rows:
        if rec["year"] < 3:
            rec["cum_ops"] = 0.0
            continue
        # 经营净现金流（还本前，用于静态回收）：净利润+折旧
        rec["static_cf"] = rec["net"] + rec["depreciation"]
        cum_ops += rec["static_cf"]
        rec["cum_ops"] = cum_ops
        if payback_ops is None and cum_ops >= inv["total"]:
            prev = cum_ops - rec["static_cf"]
            frac = 0 if rec["static_cf"] == 0 else (inv["total"] - prev) / rec["static_cf"]
            payback_ops = (rec["year"] - 3) + frac  # 从开业起的年数

    profits = [r["ebt"] for r in rows if r["year"] >= 3]
    nets = [r["net"] for r in rows if r["year"] >= 3]
    avg_ebt = sum(profits) / len(profits)
    avg_net = sum(nets) / len(nets)

    return {
        "inv": inv,
        "staff": staff,
        "years": rows,
        "dep_annual": dep_annual,
        "payback_from_start": payback,
        "payback_ops": payback_ops,
        "avg_ebt_3_18": avg_ebt,
        "avg_net_3_18": avg_net,
        "min_ebt_3_18": min(profits),
        "min_net_3_18": min(nets),
    }


def print_summary(m):
    inv = m["inv"]
    print("=== 投资 ===")
    print(f"工程费用 {inv['engineering']:.2f}")
    print(f"二类 {inv['class2']:.2f} 预备 {inv['contingency']:.2f}")
    print(f"建设投资 {inv['construction']:.2f} 利息 {inv['interest']:.2f} 管理 {inv['mgmt']:.2f}")
    print(f"总投资 {inv['total']:.2f} 贷款 {inv['loan']:.2f}")
    print(f"人力 {m['staff']['headcount']}人 {m['staff']['cost']:.2f}万 {m['staff']['by_type']}")
    print("=== 分年 ===")
    for r in m["years"]:
        print(
            f"Y{r['year']:02d} {r['stage']:6s} 人流{r['visitors']:5.1f} "
            f"收入{r['rev']['合计']:8.1f} 校验{r['visitor_check']:8.1f} "
            f"贡献{r['contribution']:8.1f} EBT{r['ebt']:8.1f} NI{r['net']:8.1f} "
            f"OCF{r['ocf']:8.1f} CUM{r['cum_fcf']:9.1f} 静态累计{r.get('cum_ops', 0):8.1f}"
        )
    print(
        f"年均利润总额3-18 {m['avg_ebt_3_18']:.2f}  "
        f"年均净利润 {m['avg_net_3_18']:.2f}  "
        f"最低EBT {m['min_ebt_3_18']:.2f}  "
        f"经营期静态回收年 {m['payback_ops']}"
    )
    print("=== 达产年项目 ===")
    y3 = m["years"][2]
    for k, v in y3["projects"].items():
        print(f"  {v['name']:12s} {v['nature']:4s} 收入{v['rev']:8.1f} 成本{v['cost']:8.1f}")
    print("收入结构", y3["rev"])


if __name__ == "__main__":
    print_summary(run_model())
