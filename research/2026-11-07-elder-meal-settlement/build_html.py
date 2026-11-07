from pathlib import Path
import html, re, hashlib

ROOT=Path(__file__).parent
OUT=ROOT/'老年助餐补贴与现金流-完整图文.html'

def inline(s):
    s=html.escape(s)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>',s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    return s

def render(md, prefix):
    out=[]; para=[]; inlist=False; number=0
    def flush():
        if para:
            out.append('<p>'+inline(' '.join(para))+'</p>'); para.clear()
    for line in md.splitlines():
        if not line.strip():
            flush()
            if inlist: out.append('</ul>'); inlist=False
            continue
        if line.startswith('#'):
            flush()
            if inlist: out.append('</ul>'); inlist=False
            level=len(line)-len(line.lstrip('#'))
            number+=1
            out.append(f'<h{level} id="{prefix}-{number}">'+inline(line[level:].strip())+f'</h{level}>')
        elif line.strip().startswith('- '):
            flush()
            if not inlist: out.append('<ul>'); inlist=True
            out.append('<li>'+inline(line.strip()[2:])+'</li>')
        else:
            if inlist: out.append('</ul>'); inlist=False
            para.append(line.strip())
    flush()
    if inlist: out.append('</ul>')
    return '\n'.join(out)

css='''
:root{--ink:#193b35;--sub:#53655f;--paper:#f7f5ed;--line:#d5ded6;--green:#236b55;--tint:#e9f1e9;--amber:#f4e2b3;--white:#fffefa}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:var(--paper);font-family:"Noto Sans CJK SC","Microsoft YaHei",system-ui,sans-serif;font-size:17px;line-height:1.9}
a{color:#1a6a54;text-decoration-thickness:1px;text-underline-offset:4px;overflow-wrap:anywhere}a:focus-visible{outline:3px solid #b36e25;outline-offset:4px}
.mast{max-width:1180px;margin:auto;padding:26px 36px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;gap:18px;font-size:13px;letter-spacing:.12em}.brand{font-weight:800}
.hero{max-width:1180px;margin:auto;padding:66px 36px 48px;display:grid;grid-template-columns:1fr 220px;gap:50px;align-items:end}.eyebrow{font-size:12px;letter-spacing:.13em;font-weight:700;color:var(--green)}
.hero h1{font-size:clamp(30px,4.5vw,52px);line-height:1.35;letter-spacing:-.035em;margin:18px 0 24px;max-width:800px}.deck{font-size:19px;color:var(--sub);max-width:790px;margin:0}.meta{border-left:2px solid var(--line);padding-left:22px;font-size:14px;color:var(--sub)}.meta strong{color:var(--ink);display:block;margin:0 0 7px}.meta p{margin:0 0 20px}
.body-wrap{max-width:1180px;margin:0 auto;padding:0 36px 70px;display:grid;grid-template-columns:190px minmax(0,1fr);gap:45px}.toc{font-size:13px;align-self:start;position:sticky;top:20px;border-top:3px solid var(--ink);padding-top:16px}.toc a{display:block;margin:11px 0;text-decoration:none}.toc a:hover{text-decoration:underline}.toc strong{font-size:14px}
article{min-width:0}article>h1{display:none}article h2{font-size:27px;line-height:1.5;margin:52px 0 22px;padding-top:12px;border-top:1px solid var(--line);scroll-margin-top:24px}article p{margin:18px 0}article ul{padding-left:25px;margin:23px 0}article li{margin:10px 0}article>p:nth-of-type(2){background:var(--tint);border-left:4px solid var(--green);padding:23px 26px;margin:27px 0}
.diagram{margin:34px -1px;background:var(--white);border:1px solid var(--line);border-radius:16px;padding:26px}.diagram h3{font-size:24px;line-height:1.45;margin:10px 0 24px}.flow-row{display:grid;grid-template-columns:90px 1fr 24px 1fr 24px 1fr;gap:7px;align-items:stretch;margin:12px 0;font-size:13px;text-align:center}.lane{font-weight:800;display:flex;align-items:center;text-align:left}.step{background:var(--tint);border:1px solid var(--line);border-radius:8px;padding:12px 7px;display:flex;align-items:center;justify-content:center;line-height:1.6}.arrow{display:flex;align-items:center;justify-content:center;font-size:20px;color:var(--green)}
.warning{background:#fbf0d6;border-left:3px solid #b78028;padding:12px 15px;font-size:14px;margin:21px 0 15px;font-weight:700}figcaption{font-size:12px;line-height:1.8;color:var(--sub)}.scope-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px}.scope{border:1px solid var(--line);border-radius:10px;padding:18px;background:var(--tint)}.scope.muted{background:#f8f7f1}.chip{font-size:11px;font-weight:700;color:var(--green)}.scope h4{margin:7px 0 10px;font-size:18px}.price{font-size:32px;line-height:1.3;font-weight:800;letter-spacing:-.02em}.price span{font-size:12px;margin-left:5px;font-weight:400}.scope p{font-size:12px;line-height:1.8;margin:13px 0 0}.unknown{font-size:25px;font-weight:700}
.appendix{max-width:1180px;margin:0 auto 70px;padding:35px;background:#eef1ea;border-top:3px solid var(--ink)}.appendix h2{font-size:27px;margin:0 0 20px}.appendix h1{font-size:20px}.appendix p,.appendix li{font-size:13px}.appendix ul{padding-left:22px}.appendix li{margin:9px 0}.appendix p{margin:16px 0}.foot{max-width:1180px;margin:auto;padding:24px 36px 45px;border-top:1px solid var(--line);font-size:12px;color:var(--sub)}
@media(max-width:820px){.hero{grid-template-columns:1fr;gap:25px;padding-top:38px}.meta{display:flex;gap:24px}.meta p{margin:0}.body-wrap{grid-template-columns:1fr;gap:20px}.toc{position:static;border-top:1px solid var(--line);display:flex;flex-wrap:wrap;gap:8px 18px}.toc strong{width:100%}.toc a{margin:3px 0}.appendix{margin:0 24px 40px;padding:25px}.hero,.body-wrap,.mast,.foot{padding-left:24px;padding-right:24px}}
@media(max-width:520px){body{font-size:16px}.mast{font-size:10px;letter-spacing:.05em}.hero{padding-bottom:32px}.deck{font-size:17px}.meta{font-size:12px}.body-wrap{padding-bottom:40px}article h2{font-size:23px}.diagram{padding:18px 14px}.diagram h3{font-size:21px}.flow-row{grid-template-columns:1fr;gap:5px;border-bottom:1px solid var(--line);padding-bottom:17px;margin-bottom:17px}.lane{padding:3px 0}.step{padding:9px}.arrow{font-size:0;height:10px}.arrow:after{content:'↓';font-size:16px;line-height:1}.scope-grid{grid-template-columns:1fr}.scope p br{display:none}.price{font-size:30px}article>p:nth-of-type(2){padding:20px}.appendix{margin-left:18px;margin-right:18px;padding:20px}}
@media print{body{background:white;color:#111;font-size:11pt}.mast,.hero,.body-wrap,.appendix,.foot{max-width:none;padding:10px 0}.hero{display:block}.hero h1{font-size:25pt}.meta{display:none}.body-wrap{display:block}.toc{display:none}.diagram{break-inside:avoid;border:1px solid #aaa}.appendix{background:white;margin-top:30px}a{color:#111}.foot{margin-top:24px}}
'''

css+='''
.money-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.money-box{background:var(--tint);padding:18px;border-radius:10px}.money-box h4{margin:0 0 15px;font-size:16px}.money-row{display:flex;justify-content:space-between;gap:16px;padding:6px 0;font-size:14px;border-bottom:1px solid var(--line)}.money-row.total{font-weight:800;border-bottom:0;margin-top:8px}.pending{color:#905e17}.formula{font-weight:700;font-size:16px;line-height:1.7}.balance-row{display:grid;grid-template-columns:52px minmax(0,1fr) 82px;gap:12px;align-items:center;margin:20px 0;font-size:14px}.bar{height:28px;background:var(--green);border-radius:4px;min-width:4px}.bar-track{background:var(--tint);border-radius:4px}.number{text-align:right;font-weight:800}.legend{font-size:13px;color:var(--sub)}
@media(max-width:520px){.money-grid{grid-template-columns:1fr}.balance-row{grid-template-columns:45px minmax(0,1fr) 72px;gap:8px;font-size:12px}.formula{font-size:14px}}
'''

diagram1='''<figure class="diagram" aria-labelledby="meal-money-title">
<div class="eyebrow">图解 01 · 作者假设情景 / 人民币</div>
<h3 id="meal-money-title">财政部分补顾客少付的款，不再加一次收入</h3>
<p class="formula">假设标价 20元 × 九折 = 优惠后餐款 18元<br>门店先让利 2元，再由顾客与财政分担 18元。</p>
<div class="money-grid">
<section class="money-box"><h4>当次财政补贴 1.5元</h4><div class="money-row"><span>顾客支付</span><strong>16.5元</strong></div><div class="money-row pending"><span>财政待兑付</span><strong>1.5元</strong></div><div class="money-row total"><span>全额兑付后餐款</span><span>18元</span></div></section>
<section class="money-box"><h4>当次财政补贴 3元</h4><div class="money-row"><span>顾客支付</span><strong>15元</strong></div><div class="money-row pending"><span>财政待兑付</span><strong>3元</strong></div><div class="money-row total"><span>全额兑付后餐款</span><span>18元</span></div></section>
</div><div class="warning">18元是本情景的餐款合计，不是净利润，也不是顾客付款当天全部到账。</div>
<figcaption>20元标价与九折取值均为作者设置，不是具名食堂的实际售价。1.5元、3元的规则依据为昆山办法中的不同年龄档，另须满足户籍、当日次数等资格。本图假设财政部分全额兑付，无退款、冲正或其他调整；未包含银行优惠、食材等费用，也不指导会计确认。原始规则与完整限制见正文。</figcaption>
</figure>'''

diagram2='''<figure class="diagram" aria-labelledby="balance-title">
<div class="eyebrow">图解 02 · 作者计算 / 非门店观测</div>
<h3 id="balance-title">记录了更多补贴，现金却未必已到账</h3>
<p class="formula">待兑付余额 = 60笔合格消费 / 天 × 1.5元 / 笔 × 观察天数</p>
<div class="balance-row"><span>30天</span><div class="bar-track"><div class="bar" style="width:33.3333%"></div></div><span class="number">2,700元</span></div>
<div class="balance-row"><span>60天</span><div class="bar-track"><div class="bar" style="width:66.6667%"></div></div><span class="number">5,400元</span></div>
<div class="balance-row"><span>90天</span><div class="bar-track"><div class="bar" style="width:100%"></div></div><span class="number">8,100元</span></div>
<p class="legend">横向长度与金额成正比，统一比例尺；不是收益增长图。</p>
<div class="warning">90天是演示观察段，不是官方承诺、实际逾期记录或固定等待时间。</div>
<figcaption>假设每天60笔均符合当日一次等限制，观察段内没有收到这批财政补贴，也无退款、重复申报、冲正及资格调整。金额由随文Python脚本实际计算。待兑付余额不等于全部周转资金；顾客款、采购、工资等现金日期须另列。昆山办法按季据实结算，但本图没有推算任何一家食堂的实际到账日。</figcaption>
</figure>'''

note=(ROOT/'note.md').read_text()
sources=(ROOT/'sources.md').read_text()
body=render(note,'article')
body=body.replace('<h2 id="article-4">',diagram1+'\n<h2 id="article-4">')
body=body.replace('<h2 id="article-5">',diagram2+'\n<h2 id="article-5">')
links=[]
for i,title in re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>',body): links.append(f'<a href="#{i}">{title}</a>')
title=note.splitlines()[0].removeprefix('# ')
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="从昆山具名助餐项目与地方原始政策，核清顾客减免、商户兑付和持续费用。完整研究、两幅图解及来源。"><title>'''+html.escape(title)+'''｜餐饮商业模式研究院</title><style>'''+css+'''</style></head><body>
<header class="mast"><span class="brand">餐饮商业模式研究院</span><span>助餐服务 / 核销与现金流</span></header>
<section class="hero"><div><div class="eyebrow">老板决策读本 · 2026年11月7日</div><h1>'''+html.escape(title)+'''</h1><p class="deck">顾客当场少付，食堂何时收齐？加入助餐项目前，把每餐让利、财政兑付和持续服务成本分开算清。</p></div><div class="meta"><p><strong>证据类型</strong>地方政策、官方项目发布</p><p><strong>金额性质</strong>作者计算情景<br>不是门店盈利实测</p></div></section>
<main class="body-wrap"><nav class="toc" aria-label="本文目录"><strong>完整论证</strong>'''+''.join(links)+'''<a href="#sources">来源与边界</a></nav><article>'''+body+'''</article></main>
<section class="appendix" id="sources"><h2>来源与核验说明</h2>'''+render(sources,'source')+'''</section>
<footer class="foot">完整独立HTML，保留研究正文、两幅信息图解及来源。政策事实、计算情景与经营建议分开标示。无门店现场测试、净收益验证或回本承诺。</footer></body></html>'''
OUT.write_text(page)
print(OUT.name,len(page.encode()),hashlib.sha256(page.encode()).hexdigest())

