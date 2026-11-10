#!/usr/bin/env python3
"""Build a self-contained Chinese research reader using only Python's standard library.
Run: python build.py
Inputs stay unchanged. All output is local. No network calls or publication steps.
"""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
import hashlib, json, re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
INPUTS = {name: (ROOT / name).read_bytes() for name in ('note.md', 'sources.md')}
HASHES = {name: hashlib.sha256(data).hexdigest() for name, data in INPUTS.items()}
NOTE = INPUTS['note.md'].decode('utf-8')
SOURCES = INPUTS['sources.md'].decode('utf-8')
DEDUP = json.loads((ROOT / 'dedup.json').read_text())
BASELINE = DEDUP['baseline_commit']
VERIFIED_PATHS = {item['path'] for item in DEDUP['scanned'] if item.get('ok') and item.get('sha') == item.get('returned_sha')}
RESEARCH_PATHS = ('research/2026-10-30-robot-kitchen/note.md', 'research/2026-11-06-robot-subscription-exit/note.md')
assert all(p in VERIFIED_PATHS for p in RESEARCH_PATHS), 'Existing-research link must be verified in source ledger.'
RESEARCH_LINKS = {'../' + p.removeprefix('research/'): 'https://github.com/louiseliu/restaurant-business-lab/blob/' + BASELINE + '/' + p for p in RESEARCH_PATHS}
PUBLIC_NOTE, OMITTED_OPERATIONAL_SENTENCES = re.subn(r'没有新增[^。]+。', '', NOTE)
assert OMITTED_OPERATIONAL_SENTENCES == 1
# Source excerpts retain substantive evidence boundaries, not project execution logs.
PUBLIC_SOURCES = SOURCES.split('## 去重和研究增量')[0].rstrip()

STYLE = '''
:root{color-scheme:light;--paper:#f8f6f0;--ink:#173b39;--muted:#5d706b;--rule:#d6ddd4;--orange:#af4c28;--accent:#eef1e8;--white:#fffdf7}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:28px}body{margin:0;background:var(--paper);color:var(--ink);font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",sans-serif;-webkit-font-smoothing:antialiased;line-height:1.9}
a{color:#20645e;text-decoration-thickness:1px;text-underline-offset:4px;overflow-wrap:anywhere}a:hover{color:var(--orange)}a:focus-visible{outline:3px solid var(--orange);outline-offset:5px}::selection{background:#e8cab5;color:#173b39}.skip{position:absolute;left:20px;top:-80px;background:white;padding:8px 18px;z-index:2}.skip:focus{top:12px}
.masthead{max-width:1320px;margin:0 auto;padding:25px 6vw 22px;border-bottom:1px solid var(--rule);display:flex;gap:16px;justify-content:space-between;font-size:13px;font-weight:650;letter-spacing:.12em}.masthead span:last-child{color:var(--muted);letter-spacing:.05em}
.hero{max-width:1320px;margin:0 auto;padding:64px 6vw 50px}.eyebrow{color:var(--orange);font-size:13px;font-weight:750;letter-spacing:.18em;margin:0 0 20px}.hero h1{font-size:clamp(36px,5.1vw,65px);line-height:1.25;letter-spacing:-.035em;max-width:980px;margin:0 0 25px;font-weight:780}.hero h1 span{display:block}.dek{max-width:830px;font-size:19px;color:var(--muted);margin:0}.scope{display:flex;flex-wrap:wrap;gap:12px 28px;font-size:13px;color:var(--muted);margin:28px 0 0;padding-top:20px;border-top:1px solid var(--rule)}.scope b{color:var(--ink);font-weight:650}
.layout{max-width:1320px;margin:0 auto;display:grid;grid-template-columns:190px minmax(0,800px);gap:58px;padding:0 6vw 75px}.contents{align-self:start;position:sticky;top:28px;padding-top:9px}.contents p{font-size:12px;color:var(--muted);font-weight:700;letter-spacing:.15em;margin:0 0 15px}.contents ol{list-style:none;margin:0;padding:0;counter-reset:section}.contents li{counter-increment:section;margin:0 0 12px;line-height:1.5}.contents a{font-size:13px;text-decoration:none;display:block;padding:5px 0 5px 22px;position:relative}.contents a::before{content:counter(section,decimal-leading-zero);font-variant-numeric:tabular-nums;font-size:10px;color:var(--orange);position:absolute;left:0;top:7px}.contents .nav-source{margin-top:22px;padding-top:18px;border-top:1px solid var(--rule)}
article{min-width:0;font-size:17px}article p{margin:0 0 20px;text-wrap:pretty}article strong{font-weight:750}article h2{font-size:29px;line-height:1.5;letter-spacing:-.015em;margin:58px 0 22px;font-weight:750;padding-top:28px;border-top:1px solid var(--rule)}article h2 .section-no{display:block;font-size:11px;letter-spacing:.12em;color:var(--orange);line-height:1.4;margin-bottom:11px;font-weight:700}.intro p:first-child{font-size:21px;line-height:1.9}.intro p:last-child{font-size:19px;border-left:3px solid var(--orange);padding-left:22px;margin-top:26px}.article-body ul{padding-left:1.4em}.article-body li{margin-bottom:12px}
.visual{margin:34px 0 36px;padding:24px 20px;background:var(--accent);border:1px solid #d4ddd0;border-radius:3px}.figure-label{font-size:12px;letter-spacing:.11em;color:var(--orange);font-weight:750;margin-bottom:16px}.visual svg{display:block;width:100%;height:auto;max-width:480px;margin:0 auto}.visual figcaption{max-width:580px;margin:20px auto 0;font-size:14px;color:var(--muted);line-height:1.8}.visual figcaption strong{color:var(--ink)}.formula-note{font-size:14px;color:var(--muted);padding:0 2px;margin:14px auto 0;max-width:580px}
.sources{font-size:14px;line-height:1.9;margin-top:55px;padding:32px 0 0;border-top:2px solid var(--ink)}.sources>h2{border:0;padding:0;margin:0 0 18px;font-size:28px}.sources h3{font-size:18px;line-height:1.5;margin:30px 0 15px}.sources ul{padding-left:1.4em}.sources li{margin-bottom:11px}.sources p{margin-bottom:14px}.sources a{word-break:normal}.sources .source-intro{color:var(--muted)}
footer{border-top:1px solid var(--rule);padding:25px 6vw 35px;max-width:1320px;margin:0 auto;display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px 24px;font-size:12px;color:var(--muted)}footer p{margin:0}
@media(max-width:1000px){.layout{grid-template-columns:145px minmax(0,1fr);gap:32px;padding-left:5vw;padding-right:5vw}.hero{padding-left:5vw;padding-right:5vw}.masthead{padding-left:5vw;padding-right:5vw}.contents a{font-size:12px}article{font-size:16px}article h2{font-size:26px}}
@media(max-width:760px){html{scroll-padding-top:16px}.masthead{padding:19px 22px;font-size:11px;letter-spacing:.06em}.masthead span:last-child{font-size:10px}.hero{padding:40px 23px 32px}.hero h1{font-size:36px;line-height:1.32;letter-spacing:-.035em}.eyebrow{font-size:11px;margin-bottom:17px;letter-spacing:.12em}.dek{font-size:16px}.scope{margin-top:23px;gap:6px 20px;font-size:11px;line-height:1.8}.layout{display:block;padding:0 23px 48px}.contents{position:static;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:18px 0 12px;margin-bottom:31px}.contents p{font-size:11px;margin-bottom:10px}.contents ol{display:grid;grid-template-columns:1fr 1fr;gap:5px 20px}.contents li{margin:0}.contents a{font-size:12px;line-height:1.55;padding-top:6px;padding-bottom:6px}.contents .nav-source{margin:0;padding:0;border:0}article{font-size:16px;line-height:1.95}.intro p:first-child{font-size:18px}.intro p:last-child{font-size:17px;padding-left:17px}article h2{font-size:24px;line-height:1.45;margin-top:43px;padding-top:24px}.visual{padding:18px 0 20px;margin:28px -9px 30px}.figure-label{padding:0 14px;font-size:10px;letter-spacing:.08em}.visual figcaption,.formula-note{padding:0 15px;font-size:13px}.sources{font-size:13px}.sources h3{font-size:17px}.sources>h2{font-size:25px}footer{padding:22px 23px 30px;display:block}footer p{margin-bottom:8px}}
@media(max-width:360px){.hero h1{font-size:32px}.layout,.hero{padding-left:19px;padding-right:19px}.contents ol{gap:3px 10px}.masthead{padding-left:19px;padding-right:19px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{body{background:white;color:#111;font-size:10pt}.masthead,.hero,.layout,footer{max-width:none;padding-left:0;padding-right:0}.hero{padding-top:20px;padding-bottom:20px}.hero h1{font-size:29pt}.dek{font-size:12pt}.contents{display:none}.layout{display:block}article{font-size:11pt;line-height:1.7}article h2{font-size:17pt;break-after:avoid}.intro p:first-child{font-size:13pt}.intro p:last-child{font-size:12pt}.visual{break-inside:avoid;padding:12px;background:#f8f8f3}.visual svg{max-width:350px}.sources{font-size:9pt}.sources h3{break-after:avoid}.skip{display:none}a{color:#111}footer{margin-top:20px}.scope{font-size:9pt}}
'''

SVG_STYLE = '''<style>text{font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",sans-serif;fill:#173b39}.small{font-size:21px}.body{font-size:23px}.title{font-size:26px;font-weight:750}.muted{fill:#5d706b}.accent{fill:#af4c28}.bold{font-weight:750}</style>'''
SVG1 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="664" viewBox="0 0 480 664" role="img" aria-labelledby="level-title level-desc">
<title id="level-title">标准原例 2、C3、S1综合判为L2</title><desc id="level-desc">自动性2、协同性C3、学习性S1，三个维度需同时达到相应要求。标准原例综合判为L2。L3要求2、C3、S2，原例学习性S1未达S2。强项不能抵消不足。这是标准例解读，不是产品实测。</desc>{SVG_STYLE}
<rect width="480" height="664" rx="4" fill="#fffdf7"/>
<text x="26" y="42" class="small accent bold">附录A · 表A.5 / A.3.2.2</text>
<text x="26" y="88" class="title">三个维度必须同时达标</text>
<text x="26" y="124" class="small muted">下面是标准原例，不是产品实测</text>
<g fill="#eef1e8" stroke="#d4ddd0"><rect x="26" y="156" width="132" height="123" rx="8"/><rect x="174" y="156" width="132" height="123" rx="8"/><rect x="322" y="156" width="132" height="123" rx="8"/></g>
<g class="body" text-anchor="middle"><text x="92" y="194">自动性</text><text x="240" y="194">协同性</text><text x="388" y="194">学习性</text></g>
<g font-size="42" font-weight="800" text-anchor="middle"><text x="92" y="252">2</text><text x="240" y="252">C3</text><text x="388" y="252">S1</text></g>
<path d="M92 292v20h296v-20M240 312v29" fill="none" stroke="#55786b" stroke-width="2"/>
<path d="m233 334 7 10 7-10" fill="none" stroke="#55786b" stroke-width="2"/>
<rect x="26" y="364" width="428" height="128" rx="8" fill="#173b39"/>
<text x="49" y="406" style="fill:#dbe7d6;font-size:23px">综合等级</text>
<text x="48" y="465" style="fill:#fffdf7;font-size:49px;font-weight:800">L2</text>
<text x="183" y="455" style="fill:#fffdf7;font-size:23px">强项不能抵消不足</text>
<text x="26" y="543" class="body bold">L3要求：2 / C3 / S2</text>
<text x="26" y="582" class="body accent">原例学习性S1未达到S2</text>
<text x="26" y="631" class="small muted">等级用于核对能力，不直接代表回本</text>
</svg>'''

SVG2 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="1196" viewBox="0 0 480 1196" role="img" aria-labelledby="tests-title tests-desc">
<title id="tests-title">两项标准试验与门店补充验证不能混为一谈</title><desc id="tests-desc">6.4.9在蒜苔炒肉质量比3比1条件下，从单次最大生料量起始，按规定条件可减料重测，连续工作3次，记录总出菜量G、总能耗E、总时间T，出菜率W等于G除以T，能耗率η等于G除以E。6.5.3.1另检验五类食材各一道菜的自动烹饪和平均时间。门店常用菜单、常用批量和完整劳动仍需另作验证，不能把标准出菜率直接当成整餐段合格交付能力。</desc>{SVG_STYLE}
<rect width="480" height="1196" rx="4" fill="#fffdf7"/>
<text x="26" y="42" class="small accent bold">试验口径与外推边界</text>
<text x="26" y="87" class="title">两项试验，回答不同问题</text>
<rect x="22" y="116" width="436" height="486" rx="8" fill="#eef1e8" stroke="#d4ddd0"/>
<text x="42" y="156" class="small accent bold">标准 6.4.9</text>
<text x="42" y="195" class="title">出菜率与能耗率</text>
<text x="42" y="240" class="body bold">蒜苔炒肉 · 蒜苔∶猪肉＝3∶1</text>
<text x="42" y="279" class="small">生料从单次最大烹饪量起始</text>
<text x="42" y="314" class="small">不达规定温度条件时减料重测</text>
<text x="42" y="353" class="body bold">连续工作3次</text>
<path d="M42 375h396" stroke="#c4d1c2"/>
<text x="42" y="411" class="small">G 总出菜量 · E 总能耗</text>
<text x="42" y="446" class="small">T 总时间</text>
<text x="42" y="493" class="body bold">W＝G / T　kg/h</text>
<text x="42" y="535" class="body bold">η＝G / E　kg/(kWh)</text>
<text x="42" y="577" class="small muted">生料起始量不等于总出菜量G</text>
<rect x="22" y="626" width="436" height="212" rx="8" fill="#f3eee5" stroke="#ddd4c8"/>
<text x="42" y="666" class="small accent bold">标准 6.5.3.1</text>
<text x="42" y="705" class="title">自动烹饪与平均时间</text>
<text x="42" y="750" class="body bold">五类食材 · 每类一道菜</text>
<text x="42" y="796" class="small muted">另一项验证，不拼成同一个结果</text>
<path d="M240 855v32" fill="none" stroke="#55786b" stroke-width="2" stroke-dasharray="4 4"/>
<path d="m233 880 7 10 7-10" fill="none" stroke="#55786b" stroke-width="2"/>
<rect x="22" y="909" width="436" height="259" rx="8" fill="#173b39"/>
<text x="42" y="949" style="fill:#dbe7d6;font-size:21px;font-weight:750">门店补充验证 · 研究建议</text>
<text x="42" y="991" style="fill:#fffdf7;font-size:26px;font-weight:750">菜单、批量、完整劳动</text>
<text x="42" y="1033" style="fill:#fffdf7;font-size:23px">用本店常卖菜与常用批量比较</text>
<text x="42" y="1074" style="fill:#fffdf7;font-size:23px">记录合格交付与全过程劳动</text>
<text x="42" y="1122" style="fill:#dbe7d6;font-size:21px">不直接换算成整餐段交付能力</text>
</svg>'''

# This small renderer intentionally supports only constructs in the reviewed inputs.
def inline(value):
    tokens=[]
    def stash(m):
        label, url = m.group(1), m.group(2)
        url = RESEARCH_LINKS.get(url, '#sources' if url == 'sources.md' else url)
        assert url.startswith(('https://','#')), 'Unexpected link destination: '+url
        tok=f'ZZLINKTOKEN{len(tokens)}ZZ'
        tokens.append('<a href="'+escape(url,quote=True)+'">'+escape(label)+'</a>')
        return tok
    value=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',stash,value)
    value=escape(value)
    value=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',value)
    for i,token in enumerate(tokens): value=value.replace(f'ZZLINKTOKEN{i}ZZ',token)
    return value

def render_md(text, source=False):
    chunks=[]; para=[]; in_list=False
    def flush():
        if para: chunks.append('<p>'+inline(' '.join(para))+'</p>'); para.clear()
    for line in text.splitlines():
        if not line.strip():
            flush()
            if in_list: chunks.append('</ul>'); in_list=False
            continue
        if line.startswith('# '):
            flush(); continue
        if line.startswith('## '):
            flush()
            if in_list: chunks.append('</ul>'); in_list=False
            chunks.append('<h3>'+inline(line[3:])+'</h3>')
        elif line.startswith('- '):
            flush()
            if not in_list: chunks.append('<ul>'); in_list=True
            chunks.append('<li>'+inline(line[2:])+'</li>')
        else:
            if in_list: chunks.append('</ul>'); in_list=False
            para.append(line)
    flush()
    if in_list: chunks.append('</ul>')
    return '\n'.join(chunks)

TITLE=PUBLIC_NOTE.splitlines()[0].removeprefix('# ')
body=PUBLIC_NOTE.split('\n\n',2)[2]
parts=re.split(r'^## (.+)$',body,flags=re.M)
intro=render_md(parts[0])
headings=parts[1::2]; texts=parts[2::2]
anchors=['model','levels','tests','trial','decision','scope']
assert len(headings)==len(anchors)==6
short_titles=['核对具体型号','怎样理解智能等级','怎样读试验结果','把预算留给差距','下一笔钱怎样决定','研究说明']
nav=''.join('<li><a href="#'+anchor+'">'+label+'</a></li>' for anchor,label in zip(anchors,short_titles))
nav+='<li class="nav-source"><a href="#sources">来源与核验范围</a></li>'
FIG1='<figure class="visual"><div class="figure-label">图一 / 标准例解读</div>'+SVG1+'<figcaption>依据附录A表A.5与A.3.2.2绘制。<strong>2 / C3 / S1 → L2</strong>是条款原例；L3对照仅说明三个维度须同时达标。图中没有被测品牌或机型。</figcaption></figure>'
FIG2='<figure class="visual"><div class="figure-label">图二 / 标准试验与门店补充验证</div>'+SVG2+'<figcaption>依据6.4.9和6.5.3.1绘制。两项标准试验不可合并解释，门店验证为研究建议。<strong>T只称“总时间”</strong>，条款未逐项说明备料、上料、清洗、换菜和交接是否包含，需对照原报告。</figcaption><p class="formula-note">η沿用标准名称“能耗率”，单位为kg/(kWh)，不是其倒数kWh/kg。图示为口径说明，不提供食品安全温度指导。</p></figure>'
sections=[]
for i,(heading,text,anchor) in enumerate(zip(headings,texts,anchors),1):
    prose=render_md(text)
    if anchor=='levels':
        paras=prose.split('\n'); paras.insert(1,FIG1); prose='\n'.join(paras)
    if anchor=='tests':
        paras=prose.split('\n'); paras.insert(2,FIG2); prose='\n'.join(paras)
    sections.append(f'<section id="{anchor}" aria-labelledby="heading-{anchor}"><h2 id="heading-{anchor}"><span class="section-no">{i:02d}</span>{escape(heading)}</h2>{prose}</section>')
source_html=render_md(PUBLIC_SOURCES,source=True)
html='''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="解读GB/T 46718-2025的智能等级与试验口径，区分标准证据和餐厅采购仍需核实的事项。"><title>'''+escape(TITLE)+'''</title><style>'''+STYLE+'''</style></head>
<body><a class="skip" href="#article">跳到正文</a><header class="masthead"><span>餐饮商业研究</span><span>2026年11月10日</span></header>
<div class="hero"><p class="eyebrow">GB/T 46718-2025 · 采购中的技术参照</p><h1>炒菜机器人新国标<span>怎样用智能等级谈采购</span></h1><p class="dek">先看等级由什么能力构成，再看试验在什么条件下成立。购买理由最终仍要落在本店实际得到的能力上。</p><div class="scope"><span><b>标准发布</b> 2025-10-31</span><span><b>标准实施</b> 2026-11-01</span><span><b>官方状态</b> 推荐性 · 现行</span><span>非产品认证或推荐</span></div></div>
<div class="layout"><nav class="contents" aria-label="本文目录"><p>阅读目录</p><ol>'''+nav+'''</ol></nav><main id="article"><article class="article-body"><div class="intro">'''+intro+'''</div>'''+''.join(sections)+'''<section class="sources" id="sources" aria-labelledby="heading-sources"><h2 id="heading-sources">来源与核验范围</h2>'''+source_html+'''</section></article></main></div>
<footer><p>餐饮商业研究 · 公开证据与研究分析</p><p>正文与图表可离线阅读 · 外部来源链接需要联网</p><p><a href="#article">回到正文</a></p></footer></body></html>'''

# Deterministic content, structure and safety checks; not a browser/render check.
class CheckHTML(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.external_assets=[]; self.stack=[]; self.texts=[]; self.script_count=0; self.inline_svg=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='a': self.links.append(a.get('href',''))
        if tag=='script': self.script_count+=1
        if tag=='svg': self.inline_svg+=1
        if tag in ('img','script','iframe','link','video','audio','object','embed'):
            for k in ('src','href','data'):
                if a.get(k): self.external_assets.append(a[k])
        self.stack.append(tag)
    def handle_endtag(self,tag):
        if tag in self.stack:
            self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
    def handle_data(self,data):
        if not any(t in self.stack for t in ('style','script')): self.texts.append(data)

checks=CheckHTML(); checks.feed(html)
assert len(checks.ids)==len(set(checks.ids)), 'Duplicate ID'
assert all(link[1:] in checks.ids for link in checks.links if link.startswith('#')), 'Broken internal link'
assert not checks.external_assets and checks.script_count==0, 'Reader must be self-contained'
assert checks.inline_svg==2
assert '<meta name="viewport"' in html
assert not re.search(r'(?i)(?:file://|localhost|127\.0\.0\.1|publication-status|dedup\.json)',html)
assert str(ROOT) not in html
assert '70℃' not in SVG1+SVG2
assert 'η＝G / E' in SVG2 and 'kg/(kWh)' in SVG2
assert 'S1未达到S2' in SVG1
assert all(p in html for p in ('6.4.9','6.5.3.1','总时间','减料重测','每类一道菜','完整劳动'))
for svg in (SVG1,SVG2): ET.fromstring(svg)
plain=''.join(checks.texts)
# Every source body paragraph and heading is preserved after Markdown markup/link labels are stripped.
def plain_md(s):
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',s)
    return s.replace('**','').strip()
paragraphs=[p.strip() for p in PUBLIC_NOTE.split('\n\n') if p.strip() and not p.startswith('# ') and not p.startswith('餐饮商业研究｜')]
missing=[]
for paragraph in paragraphs:
    p=plain_md(paragraph.removeprefix('## '))
    if p not in plain: missing.append(p[:100])
assert not missing, 'Source content missing: '+repr(missing)
# Each substantive source bullet is also included verbatim, with links rendered.
source_bullets=[plain_md(line[2:]) for line in PUBLIC_SOURCES.splitlines() if line.startswith('- ')]
assert all(s in plain for s in source_bullets)
assert {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in INPUTS}==HASHES, 'Inputs changed during build; rebuild.'
DELIVERY_NAME = '炒菜机器人新国标-采购研究-20261110.html'
for name,data in [('index.html',html),(DELIVERY_NAME,html),('intelligence-levels.svg',SVG1),('test-boundaries.svg',SVG2)]:
    (ROOT/name).write_text(data,encoding='utf-8')
manifest={
 'input_sha256':HASHES,'output_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['index.html',DELIVERY_NAME,'intelligence-levels.svg','test-boundaries.svg']},
 'verified_research_baseline':BASELINE,'retained_note_blocks':len(paragraphs),'retained_source_bullets':len(source_bullets),
 'inline_svg_count':checks.inline_svg,'external_asset_count':len(checks.external_assets),'script_count':checks.script_count,
 'hyperlink_count':len(checks.links),'unique_external_urls':sorted(set(u for u in checks.links if u.startswith('https://'))),
 'source_exclusions':{'note':'正文末尾一条执行记录（不涉及研究论证）','sources':['去重和研究增量','执行与交付边界']},
 'static_checks':'passed','browser_visual_qa':'not_run','network_link_recheck':'not_run; links inherited from reviewed sources and verified repository snapshot'
}
(ROOT/'reader-qa.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
qa='''# 图文附件静态核验

- 结果：通过本文列出的静态检查；**未做浏览器视觉验收**，不将静态通过表述为桌面或手机实际渲染通过。
- 离线性：CSS与两幅原创SVG均内联；无外部字体、脚本、图像请求和统计追踪。只有点击来源链接时需要联网。
- 内容：正文保留全部研究论证，逐段对照源文通过。仅删除正文末尾的一句执行记录；来源保留S1至S3与访问/证据限制，省略项目去重过程与交付操作记录。
- 原图：SVG均通过XML结构解析。智能等级图仅解释标准原例；试验图区分6.4.9、6.5.3.1和门店补充验证，最大生料量为起始口径，允许按规定条件减料重测，η不是倒数，T不擅自定义细项。图中不列食品温度值。
- 结构：唯一ID、所有内部锚点、两幅内联图、移动端viewport与响应式断点检查通过。没有私人本地路径、凭据、标准原件截图或原站链接。
- 外链：使用已核验的官方/报道URL；两项既有研究链接均指向去重记录中已核实的GitHub提交及文件。未再次联网逐个点击验收。
- 构建：在本目录运行`python build.py`。脚本只读取输入、在本目录重建附件，不访问网络，不发布或写入GitHub。
- 本轮只创建本地HTML、SVG、脚本与QA，不修改原稿、门户或历史归档。描述性文件名HTML与index.html逐字一致。

详细输入/输出SHA256与链接清单见`reader-qa.json`。若原稿变动，请重新运行脚本后再交付。
'''
(ROOT/'reader-qa.md').write_text(qa,encoding='utf-8')
print(json.dumps({'result':'PASS','input_sha256':HASHES,'html_bytes':len(html.encode()),'retained_note_blocks':len(paragraphs),'retained_source_bullets':len(source_bullets),'browser_visual_qa':'not_run'},ensure_ascii=False,indent=2))
