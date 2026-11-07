"""Build a standalone illustrated HTML from the public prose and calculation.

Standard-library only. No runtime requests, external assets, tracking or private data.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
NOTE = (ROOT / "note.md").read_text()
SOURCES = (ROOT / "sources.md").read_text()
CALC = json.loads((ROOT / "calculations.json").read_text())


def inline(text):
    text = escape(text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def markdown(text, prefix="sec"):
    """Minimal renderer for this article's headings, paragraphs and flat lists."""
    chunks = []
    headings = []
    for block in re.split(r"\n\s*\n", text.strip()):
        if block.startswith("# "):
            continue
        if block.startswith("## "):
            name = block[3:]
            ident = f"{prefix}-{len(headings)+1}"
            headings.append((ident, name))
            chunks.append(f'<h2 id="{ident}">{inline(name)}</h2>')
        elif all(line.startswith("- ") for line in block.splitlines()):
            chunks.append('<ul>' + ''.join('<li>'+inline(line[2:])+'</li>' for line in block.splitlines()) + '</ul>')
        elif all(re.match(r"\d+\. ", line) for line in block.splitlines()):
            chunks.append('<ol>' + ''.join('<li>'+inline(re.sub(r"^\d+\. ", "", line))+'</li>' for line in block.splitlines()) + '</ol>')
        else:
            chunks.append('<p>'+inline(block.replace('\n', ' '))+'</p>')
    return '\n'.join(chunks), headings


def evidence_figure():
    return '''<figure class="evidence" aria-labelledby="evidence-title">
<div class="eyebrow">图 1 · 来源分层示意，不是效果统计</div>
<h3 id="evidence-title">四份材料，各回答一个不同问题</h3>
<div class="cards">
<div class="card"><span class="year">2021</span><h4>商户为什么愿意买？</h4><p>鸽速来公开讲述保费、银行与宽带优惠。</p><p class="limit">历史自述，不是同保障合同对照，也不是今天的报价。</p></div>
<div class="card"><span class="year">2023</span><h4>组合服务有运行记录吗？</h4><p>监管部门走访齐得福酒楼，了解保险、收银、宽带与明厨亮灶。</p><p class="limit">具名运行走访，不是单店经营效果研究。</p></div>
<div class="card"><span class="year">2024</span><h4>有哪些优惠本来可得？</h4><p>广发银行公告延续部分小微企业与个体工商户费用减免。</p><p class="limit">适用范围、费目与期限各异，不是二维码交易全部免费。</p></div>
<div class="card"><span class="year">2026</span><h4>套餐还在推广什么？</h4><p>三角镇餐饮联盟活动介绍“食安赢”及 AI 抓拍、证照提醒等。</p><p class="limit">推广记录，不证明全部成员已部署，更不沿用旧合同价。</p></div>
</div><figcaption>依据正文四个公开来源整理。年份顺序不表示同一家门店、同一份合同持续运行；同一政府机构的多篇材料也不是多份独立效果验证。</figcaption></figure>'''


def sensitivity_figure():
    rows = CALC["scenarios"]
    bars = []
    table = []
    labels = ["全部流水 × 12个月", "一半合格流水 × 12个月", "原费率0.2% × 12个月", "全部流水 × 6个月", "原渠道已经免费"]
    for i, row in enumerate(rows):
        y = 54 + 48 * i
        value = int(float(row["fee_difference_rmb"]))
        width = value / 3600 * 290
        bars.append(f'<text x="12" y="{y+18}" class="svg-label">{labels[i]}</text><rect x="258" y="{y}" width="290" height="25" rx="3" fill="#e8eee9"/><rect x="258" y="{y}" width="{width:.2f}" height="25" rx="3" fill="{("#14675c" if i==0 else "#789889")}"/><text x="565" y="{y+18}" class="svg-value">{value:,}</text>')
        table.append('<tr><th scope="row">'+escape(row['name'])+'</th><td>'+str(int(float(row['eligible_share'])*100))+'%</td><td>'+format(float(row['baseline_rate'])*100,'.1f')+'%</td><td>'+str(row['effective_months'])+'</td><td>'+f'{value:,}'+'</td></tr>')
    return '''<figure class="sensitivity" aria-labelledby="sensitivity-title"><div class="eyebrow">图 2 · 作者假设与实际计算，不是门店数据</div>
<h3 id="sensitivity-title">同样月结算 10 万元，可抵扣的差额能从 3,600 元变成 0</h3>
<p class="chart-note">单位：元；新费率均假设为零；比较各情景有效优惠期内的手续费差额。</p>
<svg viewBox="0 0 650 322" role="img" aria-label="五种假设情景手续费差额分别为3600、1800、2400、1800和0元。"><text x="12" y="23" class="svg-top">情景</text><text x="565" y="23" class="svg-top">差额（元）</text>'''+''.join(bars)+'''</svg>
<div class="table-wrap"><table><caption>同一计算的可读数据表</caption><thead><tr><th scope="col">假设情景</th><th scope="col">合格比例</th><th scope="col">原费率</th><th scope="col">优惠月数</th><th scope="col">差额（元）</th></tr></thead><tbody>'''+''.join(table)+'''</tbody></table></div>
<figcaption>公式：月交易额 × 合格比例 × 实际费率差 × 有效月数。全部输入为作者设定，无上限、阶梯、退款或其他调整。差额未扣套餐、保险、安装、迁移和运维支出，不是 AI 收益、净节省或回本结论。</figcaption></figure>'''


def comparison_figure():
    return '''<figure class="comparison" aria-labelledby="comparison-title"><div class="eyebrow">图 3 · 采购分析示意</div><h3 id="comparison-title">先把两边放在同样的服务与期限上</h3>
<div class="compare-grid"><section><h4>打包方案</h4><p>全部必要保障与服务的现金支出</p><p>＋未包含的安装、维保、迁移等必要支出</p><p>− 仅通过套餐新增、实际可得的优惠</p></section><section><h4>可行的分开采购方案</h4><p>同等必要保障与服务的现金支出</p><p>＋现有设备仍需发生的维护与交接支出</p><p>− 不买套餐也已能取得的优惠</p></section></div>
<p class="callout">同期限比较之后，还要确认责任能否接得住。最低报价不自动代表合适方案。</p><figcaption>不是费用报价或数学最优化结果。店内协调时间等非现金负担另列，不直接当作已发生现金支出；不能为降低比较基线而省略必要保障或食安管理。</figcaption></figure>'''


body, headings = markdown(NOTE)
body = body.replace('<h2 id="sec-2">', evidence_figure() + '<h2 id="sec-2">', 1)
body = body.replace('<h2 id="sec-4">', sensitivity_figure() + '<h2 id="sec-4">', 1)
body = body.replace('<h2 id="sec-6">', comparison_figure() + '<h2 id="sec-6">', 1)
source_html, _ = markdown(SOURCES, 'source')
title = NOTE.splitlines()[0][2:]
toc = ''.join(f'<a href="#{ident}">{escape(name)}</a>' for ident, name in headings)
css = '''
:root{--ink:#172e2b;--muted:#526560;--accent:#14675c;--paper:#fffdf8;--line:#ccd8d1;--warm:#eee7d9}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:#eef1ec;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.9;font-size:17px}a{color:#08665c;text-decoration-thickness:1px;text-underline-offset:3px;overflow-wrap:anywhere}a:hover{text-decoration-thickness:2px}a:focus-visible{outline:3px solid #c07c2b;outline-offset:4px}.shell{max-width:1120px;margin:auto;background:var(--paper);box-shadow:0 0 70px #142e2710}.masthead{padding:60px 64px 38px;border-top:9px solid var(--accent);border-bottom:1px solid var(--line)}.eyebrow{font-size:12px;font-weight:750;letter-spacing:.12em;color:var(--accent)}h1{font-size:clamp(31px,4.1vw,47px);line-height:1.35;letter-spacing:-.025em;max-width:880px;margin:18px 0 24px}h2{font-size:27px;line-height:1.5;margin:44px 0 19px;scroll-margin-top:20px}h3{font-size:23px;line-height:1.5;margin:12px 0 18px}h4{font-size:18px;line-height:1.5;margin:7px 0 12px}.meta{font-size:14px;color:var(--muted)}.tags{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}.tag{font-size:12px;padding:3px 10px;border:1px solid var(--line);border-radius:16px}nav{padding:24px 64px;background:#f1f5f0;border-bottom:1px solid var(--line)}nav a{display:block;font-size:14px;margin:5px 0}article,.sources{padding:0 64px 24px}p{margin:18px 0}strong{font-weight:750}li{margin:10px 0}article>p:first-child{font-size:13px;color:var(--muted)}article>p:nth-child(2){font-size:21px;line-height:1.9;border-left:4px solid var(--accent);padding:4px 0 4px 24px;margin:30px 0}.evidence,.sensitivity,.comparison{margin:38px -20px;background:#f2f5ef;border:1px solid var(--line);padding:28px 28px 24px;border-radius:8px}figcaption{color:var(--muted);font-size:13px;line-height:1.8;margin-top:18px}.cards{display:grid;grid-template-columns:1fr 1fr;gap:14px}.card{background:var(--paper);padding:21px;border:1px solid var(--line)}.year{font-size:26px;line-height:1.1;font-weight:800;color:var(--accent)}.card p{font-size:15px;line-height:1.8;margin:12px 0}.card .limit{font-size:13px;border-top:1px solid var(--line);padding-top:10px;color:var(--muted)}svg{display:block;width:100%;height:auto}.svg-label{font-size:16px;fill:#172e2b}.svg-value{font-size:19px;font-weight:750;fill:#14675c}.svg-top{font-size:14px;fill:#526560}.chart-note{font-size:13px;color:var(--muted)}table{width:100%;border-collapse:collapse;font-size:13px;margin-top:14px}caption{text-align:left;color:var(--muted);font-size:12px;margin:6px 0}th,td{border-bottom:1px solid var(--line);padding:9px;text-align:right}th:first-child{text-align:left}thead th{background:#e3ece4}tbody th{font-weight:500}.table-wrap{overflow-x:auto}.compare-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.compare-grid section{background:var(--paper);border-top:4px solid var(--accent);padding:20px}.compare-grid p{font-size:15px;line-height:1.8}.callout{font-size:16px;font-weight:700;color:var(--accent)}.sources{font-size:14px;background:#f6f4ee;padding-top:20px;border-top:1px solid var(--line)}.sources h2{font-size:20px}.sources>h2:first-child{font-size:26px}footer{padding:28px 64px;font-size:12px;color:var(--muted);border-top:1px solid var(--line)}.note{background:var(--warm);padding:12px 16px;border-radius:4px;font-size:13px;line-height:1.8}@media(max-width:680px){.masthead{padding:35px 24px 28px}nav{padding:22px 24px}article,.sources{padding-left:24px;padding-right:24px}footer{padding:24px}h2{font-size:24px}h3{font-size:21px}.cards,.compare-grid{grid-template-columns:1fr}.evidence,.sensitivity,.comparison{margin:30px -8px;padding:20px 14px}.svg-label{font-size:17px}.tag{font-size:11px}article>p:nth-child(2){font-size:19px;padding-left:16px}table{font-size:12px;min-width:500px}}@media print{body{background:white;font-size:11pt}.shell{box-shadow:none;max-width:none}.masthead{padding:22px 20px}article,.sources,footer{padding-left:20px;padding-right:20px}nav{display:none}h1{font-size:26pt}h2{font-size:18pt;break-after:avoid}h3{font-size:16pt}.card,.compare-grid section,figure{break-inside:avoid}figure{margin:20px 0}.sources{font-size:9pt}a{color:inherit}svg{max-height:250px}article>p:nth-child(2){font-size:13pt}.table-wrap{overflow:visible}table{min-width:0}}
'''
html = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="从中山食安赢历史报道与银行费用公告，区分AI组合采购的真实新增优惠、必要成本与未验证效果。"><title>{escape(title)}｜餐饮商业模式研究院</title><style>{css}</style></head><body><div class="shell"><header class="masthead"><div class="eyebrow">餐饮商业模式研究院 · 经营决策读本</div><h1>{escape(title)}</h1><div class="meta">研究日期：2026年11月7日 · 完整正文与来源 · 约12分钟</div><div class="tags"><span class="tag">事实：历史自述与公开记录</span><span class="tag">计算：作者假设</span><span class="tag">判断：有条件的采购比较</span></div></header><nav aria-label="文章目录"><div class="eyebrow">本文路线</div>{toc}<a href="#sources">来源与研究边界</a></nav><main><article>{body}</article><section class="sources" id="sources"><h2>来源与研究边界</h2><p class="note">本地独立图文版。未完成站点同步；大型 HTML 未归档 GitHub。本文不构成保险投保、法律或个别经营投资建议。</p>{source_html}</section></main><footer>餐饮商业模式研究院 · 本文件内含全部正文、原创图解与来源，无外部字体、图片或脚本依赖。阅读外部来源链接需要联网。静态结构与计算已核对，未完成浏览器视觉、交互或打印验收。</footer></div></body></html>'''

class Check(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.text=[]; self.active=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.append(d['id'])
        if 'href' in d:self.links.append(d['href'])
        assert tag not in ['script','iframe','object','embed'], tag
        assert not any(k.startswith('on') for k in d), d
    def handle_data(self,data):self.text.append(data)

parser=Check();parser.feed(html)
assert len(parser.ids)==len(set(parser.ids))
assert all(h[1:] in parser.ids for h in parser.links if h.startswith('#'))
assert all(h.startswith(('https://','#')) for h in parser.links)
assert '<svg' in html and html.count('<figure') == 3
assert [int(float(r['fee_difference_rmb'])) for r in CALC['scenarios']] == [3600,1800,2400,1800,0]
for denied in [r'chatgpt\.com/(?:c|g)/',r'file-[A-Za-z0-9]',r'/workspace/',r'/tmp/',r'library_file_id',r'Bearer\s',r'ghp_[A-Za-z0-9]']:
    assert not re.search(denied,html),denied
text=''.join(parser.text)
for para in re.split(r'\n\s*\n',NOTE.strip()):
    clean=re.sub(r'^#{1,2} ','',para)
    clean=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',clean).replace('**','')
    if not para.startswith(('- ','1. ')):
        assert clean.replace('\n',' ') in text, clean[:60]
out=ROOT/'food-safety-bundle.html';out.write_text(html)
print(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'figures':3,'prose_preserved':True,'checks':'static structure, content, calculations and privacy only'},ensure_ascii=False))
