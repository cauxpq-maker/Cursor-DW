import re, glob, json, html as H
from html.parser import HTMLParser

class Strip(HTMLParser):
    def __init__(s): super().__init__(); s.out=[]
    def handle_data(s, d): s.out.append(d)
def text(fn):
    h=open(fn,encoding='utf-8',errors='ignore').read()
    p=Strip(); p.feed(h); t=''.join(p.out)
    return re.sub(r'\s+','',H.unescape(t))

def num(s): return float(s.replace(',',''))
def grab(t, pat, group=1, conv=num):
    m=re.search(pat,t)
    return conv(m.group(group)) if m else None
def growth(t, pat):
    """return signed growth from '增长X%' / '下降X%' following pat"""
    m=re.search(pat+r'[^。；]{0,40}?(增长|下降|上涨|增加)(\d+\.?\d*)%',t)
    if not m: return None
    v=float(m.group(2)); return -v if m.group(1)=='下降' else v

rows={}
files=sorted(glob.glob('p_*.html'))
for fn in files:
    t=text(fn)
    m=re.search(r'(\d{4})年国民经济和社会发展统计公报',t)
    yr=int(m.group(1)) if m else None
    if yr is None:
        m=re.search(r'<title>(\d{4})年',open(fn,encoding='utf-8',errors='ignore').read()); yr=int(m.group(1)) if m else None
    if yr is None or yr<2004: continue
    r={'year':yr,'file':fn}
    r['gdp_100m_cny']=grab(t,r'国内生产总值(?:\[\d+\])?(\d{5,8})亿元')
    r['gdp_growth']=growth(t,r'国内生产总值(?:\[\d+\])?\d{5,8}亿元，(?:按可比价格计算，)?比上年')
    mc=re.search(r'居民消费价格(?:总水平)?(?:[^。，]{0,30}全年平均)?比上年(上涨|下降|持平)(\d+\.?\d*)?%?',t)
    r['cpi']=(0.0 if mc.group(1)=='持平' else (-1 if mc.group(1)=='下降' else 1)*float(mc.group(2))) if mc else None
    r['retail_100m_cny']=grab(t,r'社会消费品零售总额(?:\[\d+\])?(?:达到)?(\d{4,7})亿元')
    r['retail_growth']=growth(t,r'社会消费品零售总额(?:\[\d+\])?(?:达到)?\d{4,7}亿元，比上年')
    mr=re.search(r'社会消费品零售总额(?:\[\d+\])?(?:达到)?\d{4,7}亿元，比上年(?:增长|下降)\d+\.?\d*%，扣除价格(?:上涨)?因素，实际增长(\d+\.?\d*)%',t)
    r['retail_real_growth']=float(mr.group(1)) if mr else None
    # exports: 其中，出口X亿元/亿美元，增长Y%
    me=re.search(r'其中，(?:货物)?出口(\d{4,7})亿(美元|元)，(增长|下降)(\d+\.?\d*)%',t)
    if me:
        r['exports_value']=num(me.group(1)); r['exports_unit']='亿'+me.group(2)
        r['exports_growth']=(-1 if me.group(3)=='下降' else 1)*float(me.group(4))
    mf=re.search(r'(?:全国一般公共预算收入|全国一般公共财政收入|全国财政收入|全年财政收入|全国公共财政收入|全年全国财政收入)(?:\[\d+\])?(\d{5,7})亿元，(?:比上年)?(?:增加\d+亿元，)?(增长|下降)(\d+\.?\d*)%',t)
    if mf:
        r['fiscal_rev_100m_cny']=num(mf.group(1)); r['fiscal_rev_growth']=(-1 if mf.group(2)=='下降' else 1)*float(mf.group(3))
    mt=re.search(r'税收收入(\d{5,7})亿元(?:（[^）]*）)?，?(?:比上年)?(?:增加\d+亿元，)?(增长|下降)(\d+\.?\d*)%',t)
    if mt:
        r['tax_rev_100m_cny']=num(mt.group(1)); r['tax_rev_growth']=(-1 if mt.group(2)=='下降' else 1)*float(mt.group(3))
    mp=re.search(r'年末全国(?:大陆)?(?:人口|总人口)(?:\[\d+\])?(\d{5,6})万人',t)
    r['pop_10k']=num(mp.group(1)) if mp else None
    # age structure (bulletin table, text form e.g. "60周岁及以上 31031 22.0" or "65岁及以上 ... ")
    for lab,key in [('60周岁及以上','pop60'),('65周岁及以上','pop65'),('60岁及以上','pop60'),('65岁及以上','pop65')]:
        ma=re.search(lab+r'(?:\[\d+\])?(\d{5})(\d{1,2}\.\d)(?!\d)',t)
        if ma and key+'_10k' not in r:
            r[key+'_10k']=num(ma.group(1)); r[key+'_pct']=float(ma.group(2))
    r['urban_pct']=grab(t,r'(?:常住人口)?城镇化率[）)]?(?:为)?(\d{2}\.\d+)%')
    rows[yr]=r
for yr in sorted(rows):
    r=rows[yr]; print(yr, {k:v for k,v in r.items() if k not in('file','year')})
json.dump([rows[y] for y in sorted(rows)],open('china_bulletin.json','w'),ensure_ascii=False,indent=1)
