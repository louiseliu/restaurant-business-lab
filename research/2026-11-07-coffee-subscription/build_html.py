"""Build the full standalone illustrated edition using only local source files."""
from pathlib import Path
from html.parser import HTMLParser
from decimal import Decimal
import html, re, json, hashlib

root = Path(__file__).parent
note = (root / 'note.md').read_text(encoding='utf-8')
sources = (root / 'sources.md').read_text(encoding='utf-8')
calcs = json.loads((root / 'calculations.json').read_text(encoding='utf-8'))

def inline(text):
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)', r'<a href="\2" rel="noopener noreferrer">\1</a>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    return text

def markdown(text):
    blocks = []
    for block in text.strip().split('\n\n'):
        if block.startswith('# '):
            blocks.append('<h1>' + inline(block[2:]) + '</h1>')
        elif block.startswith('## '):
            blocks.append('<h2>' + inline(block[3:]) + '</h2>')
        elif block.startswith('- '):
            blocks.append('<ul>' + ''.join('<li>' + inline(line[2:]) + '</li>' for line in block.splitlines()) + '</ul>')
        else:
            blocks.append('<p>' + inline(block).replace('\n', '<br>') + '</p>')
    return '\n'.join(blocks)

rows = [r for r in calcs['rows'] if r['cups'] in (5, 15, 30)]
bars = []
for r in rows:
    old = Decimal(r['old_total_gbp'])
    new = Decimal(r['new_total_gbp'])
    bars.append(f'''<div class="bar-group"><h3>每月 {r['cups']} 杯</h3>
    <div class="bar-row"><span>旧结构</span><div class="track"><div class="bar old" style="width:{old / Decimal(70) * 100:.4f}%"></div></div><b>£{old:.0f}</b></div>
    <div class="bar-row"><span>新结构</span><div class="track"><div class="bar new" style="width:{new / Decimal(70) * 100:.4f}%"></div></div><b>£{new:.0f}</b></div></div>''')

chart = '''<figure aria-labelledby="chart-title"><figcaption id="chart-title">图一 月费更低，总支出未必更低</figcaption>
<p class="label">作者假设计算 · 英镑/月 · 假设每杯原价£4，并非Pret实际统一售价</p>
<p>仅比较合格饮品：旧结构£30；新结构£5 + £2 × 杯数。图中两种结构使用同一杯数。</p>''' + ''.join(bars) + '''
<div class="threshold"><strong>实际整杯边界</strong><span>12杯：新结构£29，低于£30<br>13杯：新结构£31，高于£30</span></div>
<p class="caption">条形从零起，同一比例尺上限£70。连续计算交点为12.5杯，不表示可以兑换半杯。未计餐食优惠、其他福利、消费行为变化或税费会计拆分；不是利润图。</p></figure>'''

diagram = '''<figure aria-labelledby="mechanism-title"><figcaption id="mechanism-title">图二 使用越多，谁承担新增负担？</figcaption>
<p class="label">作者机制示意 · 没有实测成本、利润或因果收益</p>
<div class="mechanisms"><section><h3>月费内含饮品权益</h3><div class="step">先收到固定月费</div><div class="arrow" aria-hidden="true">↓</div><div class="step">规则内再做一杯<br><small>增加履约成本，不新增该杯收款</small></div><p>需要核验完整周期收入能否支持使用分布，特别是重度使用和高峰占用。</p></section>
<section><h3>月费购买折扣资格</h3><div class="step">先收到较低月费</div><div class="arrow" aria-hidden="true">↓</div><div class="step">再做一杯，也再收一笔钱<br><small>单杯收入随使用量增加</small></div><p>仍须核验总贡献与原价业务替代，不能把每杯正毛利都当成增量。</p></section></div>
<div class="threshold"><strong>共同验收单位</strong><span>完整订阅周期的增量贡献<br>同时检查忙时服务与顾客续订</span></div>
<p class="caption">月费只能计一次；餐食贡献已扣餐食成本，不能重复扣除。单杯收费低于新增成本，不足以单独判定整个订阅应退出。</p></figure>'''

body = markdown(note)
body = body.replace('<h2>月费降低，谁的总支出真的下降？</h2>', chart + '<h2>月费降低，谁的总支出真的下降？</h2>')
body = body.replace('<h2>每杯收钱，也不代表每杯都增加利润</h2>', diagram + '<h2>每杯收钱，也不代表每杯都增加利润</h2>')
sources_linked = re.sub(r'(https://[^\s]+)', r'[原始页面](\1)', sources)
css = '''*{box-sizing:border-box}body{margin:0;background:#f2f1ed;color:#29322b;font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.9}main{max-width:960px;margin:auto;background:white;padding:48px 42px}header{font-size:14px;letter-spacing:.09em;color:#6a725e}h1{font-size:clamp(28px,5vw,42px);line-height:1.35;margin:24px 0 30px}h2{font-size:25px;line-height:1.5;margin:44px 0 16px}h3{font-size:19px;line-height:1.5;margin:8px 0 12px}p,li{font-size:17px}a{color:#216b55;text-underline-offset:4px;overflow-wrap:anywhere}strong{font-weight:670}nav{font-size:14px;margin-top:20px}figure{margin:38px 0;padding:28px;border:1px solid #d8ddcf;border-radius:16px;background:#f6f7f1}figcaption{font-size:25px;line-height:1.5;font-weight:700}.label,.caption{font-size:14px;color:#59674f}.bar-group{margin:22px 0}.bar-row{display:grid;grid-template-columns:65px 1fr 45px;align-items:center;gap:12px;font-size:14px;margin:10px 0}.bar-row b{text-align:right}.track{height:22px;background:#e5e7de;border-radius:3px;overflow:hidden}.bar{height:100%}.old{background:#7c8777}.new{background:#206748}.threshold{display:grid;grid-template-columns:1fr 2fr;gap:15px;padding:18px;margin-top:25px;border-left:4px solid #206748;background:white}.mechanisms{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:24px}.mechanisms section{padding:20px;background:white;border-radius:9px;border-top:4px solid #627957}.mechanisms p{font-size:15px}.step{padding:16px 12px;text-align:center;background:#f1f4eb;border:1px solid #d6ddce;border-radius:5px;font-size:16px}.step small{font-size:13px}.arrow{text-align:center;font-size:24px}.foot{font-size:14px;color:#64705d;margin-top:40px}#sources{border-top:1px solid #d7ddcf;margin-top:50px;padding-top:20px}#sources h1{font-size:27px}#sources h2{font-size:21px}#sources p,#sources li{font-size:14px}ul{padding-left:22px}@media(max-width:650px){main{padding:28px 20px}figure{padding:20px}.mechanisms{grid-template-columns:1fr}.threshold{grid-template-columns:1fr;gap:8px}figcaption{font-size:22px}.bar-row{grid-template-columns:56px 1fr 40px;gap:7px}h2{font-size:23px}}@media print{body{background:white}main{max-width:none;padding:0}figure{break-inside:avoid}h2{break-after:avoid}nav{display:none}a{color:inherit}}'''
doc = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>咖啡订阅：月费与单杯收费怎样分担风险</title><style>' + css + '</style></head><body><main><header>餐饮商业模式研究院 · 商业模式分析</header><nav><a href="#sources">来源与计算边界</a></nav><article>' + body + '</article><section id="sources">' + markdown(sources_linked) + '</section><p class="foot">全文图文读本。图表是作者计算与机制示意，均非经营成效实测。此版本为独立附件，不表示已同步站点。已完成静态内容检查，浏览器及打印版式尚未复核。</p></main></body></html>'

class Check(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = []; self.links = []; self.tags = []
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag); attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'a': self.links.append(attrs.get('href', ''))
        assert not any(k.startswith('on') for k in attrs)
check = Check(); check.feed(doc)
assert len(check.ids) == len(set(check.ids))
assert all(url[1:] in check.ids for url in check.links if url.startswith('#'))
assert all(url.startswith(('https://', '#')) for url in check.links)
assert check.tags.count('figure') == 2
assert not set(check.tags).intersection({'script', 'iframe', 'form', 'img'})
assert not re.search(r'<(?:script|link)[^>]+(?:src|href)="https?', doc)
assert all(x not in doc for x in ['chatgpt.com/c/', 'chatgpt.com/g/', '/workspace/', '/tmp/', 'Sentinel_', 'libfile_'])
assert all(inline(block.strip()) in doc for block in note.split('\n\n') if block and not block.startswith('#'))
assert all(url in doc for url in re.findall(r'https://[^\s]+', sources))
out = root / '咖啡订阅月费与单杯收费.html'
out.write_text(doc, encoding='utf-8')
print(json.dumps({'file': out.name, 'bytes': out.stat().st_size, 'sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'full_text_preserved': True, 'figures': 2, 'static_checks_passed': True, 'browser_checked': False, 'print_checked': False}, ensure_ascii=False, indent=2))
