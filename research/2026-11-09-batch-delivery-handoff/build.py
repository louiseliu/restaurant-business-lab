from pathlib import Path
import re, html, json, hashlib
P=Path(__file__).parent
md=(P/'note.md').read_text()
svg1='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 680" role="img" aria-labelledby="flow-title flow-desc">
<title id="flow-title">合批把运输工作和取餐工作放在了不同环节</title><desc id="flow-desc">多桌同趟可能减少往返，但需要装载分组、说明与辨认。顺利取餐时形成运输节省；出现异常则增加核单补餐、重新配送和解释工作。评估时应比较人工净工时，同时单列顾客等待。本图是原创定性流程图，不含实测数据。</desc>
<defs><marker id="flow-arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#65796e"/></marker></defs>
<rect width="560" height="680" rx="14" fill="#f1f4ee"/>
<g font-family="Noto Sans CJK SC,Microsoft YaHei,sans-serif" fill="#173b31">
<text x="28" y="44" font-size="25" font-weight="700">少跑一趟之后 工作去了哪里</text><text x="28" y="78" font-size="19" fill="#53675e">原创定性流程图 · 非实测数据</text>
<rect x="28" y="110" width="504" height="77" rx="10" fill="#d6e5d7"/><text x="280" y="142" text-anchor="middle" font-size="24" font-weight="700">一次装载多桌餐品</text><text x="280" y="172" text-anchor="middle" font-size="20">运输机会　少往返　少空跑</text>
<path d="M280 190V216" stroke="#65796e" stroke-width="2" marker-end="url(#flow-arrow)"/>
<rect x="28" y="228" width="504" height="80" rx="10" fill="#fff" stroke="#bccbbd"/><text x="280" y="261" text-anchor="middle" font-size="24" font-weight="700">每一桌仍要辨认和取餐</text><text x="280" y="291" text-anchor="middle" font-size="20">装载分组　入店说明　现场协助</text>
<path d="M280 311V331" stroke="#65796e" stroke-width="2" fill="none"/><path d="M280 331H150V356" stroke="#65796e" stroke-width="2" fill="none" marker-end="url(#flow-arrow)"/><path d="M280 331H410V356" stroke="#65796e" stroke-width="2" fill="none" marker-end="url(#flow-arrow)"/>
<rect x="28" y="368" width="244" height="174" rx="10" fill="#d6e5d7"/><text x="150" y="407" text-anchor="middle" font-size="24" font-weight="700">顺利取餐</text><text x="150" y="447" text-anchor="middle" font-size="22">运输节省有机会</text><text x="150" y="479" text-anchor="middle" font-size="22">转为服务能力</text><text x="150" y="517" text-anchor="middle" font-size="19">仍须核对新增工时</text>
<rect x="288" y="368" width="244" height="174" rx="10" fill="#ede0cb"/><text x="410" y="407" text-anchor="middle" font-size="24" font-weight="700">需要纠正</text><text x="410" y="447" text-anchor="middle" font-size="22">核单补餐</text><text x="410" y="479" text-anchor="middle" font-size="22">重新配送与解释</text><text x="410" y="517" text-anchor="middle" font-size="19">前厅和厨房都计入</text>
<rect x="28" y="570" width="504" height="80" rx="10" fill="#173b31"/><text x="280" y="603" text-anchor="middle" font-size="23" fill="#fff" font-weight="700">验收人工净负担 另看顾客等待</text><text x="280" y="634" text-anchor="middle" font-size="19" fill="#eef4eb">机器少跑的分钟数 ≠ 现金节省</text>
</g></svg>'''
svg2='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 690" role="img" aria-labelledby="matrix-title matrix-desc">
<title id="matrix-title">运输节省空间与取餐辨认负担共同决定合批范围</title><desc id="matrix-desc">定性决策矩阵：运输节省大且辨认容易时保留合批并验证净收益；节省大但辨认困难时先改分组和交付方式；节省小时不必追求装满，辨认困难时优先小批或单桌。分档需要门店观察，不是实测分类。</desc>
<rect width="560" height="690" rx="14" fill="#f1f4ee"/>
<g font-family="Noto Sans CJK SC,Microsoft YaHei,sans-serif" fill="#173b31">
<text x="28" y="44" font-size="25" font-weight="700">同一台机器人 可以有不同批次</text><text x="28" y="78" font-size="19" fill="#53675e">原创定性决策矩阵 · 非实测分档</text>
<text x="150" y="119" text-anchor="middle" font-size="22" font-weight="700">辨认较容易</text><text x="410" y="119" text-anchor="middle" font-size="22" font-weight="700">辨认负担较高</text>
<rect x="28" y="140" width="504" height="44" rx="7" fill="#173b31"/><text x="280" y="170" text-anchor="middle" font-size="21" fill="#fff">运输节省空间较大</text>
<rect x="28" y="195" width="244" height="160" rx="10" fill="#d6e5d7"/><text x="150" y="234" text-anchor="middle" font-size="23" font-weight="700">保留合批</text><text x="150" y="277" text-anchor="middle" font-size="21">验证净工时与等待</text><text x="150" y="311" text-anchor="middle" font-size="21">再逐步扩大范围</text>
<rect x="288" y="195" width="244" height="160" rx="10" fill="#ede0cb"/><text x="410" y="234" text-anchor="middle" font-size="23" font-weight="700">先改分组与交付</text><text x="410" y="277" text-anchor="middle" font-size="21">让需要帮助的任务</text><text x="410" y="311" text-anchor="middle" font-size="21">回到人工可接手处</text>
<rect x="28" y="380" width="504" height="44" rx="7" fill="#53675e"/><text x="280" y="410" text-anchor="middle" font-size="21" fill="#fff">运输节省空间较小</text>
<rect x="28" y="435" width="244" height="160" rx="10" fill="#fff" stroke="#bccbbd"/><text x="150" y="474" text-anchor="middle" font-size="23" font-weight="700">不必追求装满</text><text x="150" y="517" text-anchor="middle" font-size="21">保留简单安排</text><text x="150" y="551" text-anchor="middle" font-size="21">优先解决真正瓶颈</text>
<rect x="288" y="435" width="244" height="160" rx="10" fill="#eee6dc"/><text x="410" y="474" text-anchor="middle" font-size="23" font-weight="700">优先小批或单桌</text><text x="410" y="517" text-anchor="middle" font-size="21">少量路程收益</text><text x="410" y="551" text-anchor="middle" font-size="21">未必值得多道规则</text>
<text x="280" y="638" text-anchor="middle" font-size="20" fill="#53675e">分档依据门店观察 不按机型或套餐自动归类</text><text x="280" y="669" text-anchor="middle" font-size="19" fill="#53675e">所有区域都保留必要的人工帮助</text>
</g></svg>'''
figs={'batch-workload.svg':svg1,'batch-decision.svg':svg2}
for name,s in figs.items(): (P/name).write_text(s)

def inline(t):
 t=html.escape(t)
 t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
 t=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<a href="\2" rel="noopener noreferrer">\1</a>',t)
 t=re.sub(r'\[([12])\](?!\()',r'<a class="cite" href="#source-\1" aria-label="来源\1">[\1]</a>',t)
 return t
blocks=[];toc=[];i=0
for p in md.strip().split('\n\n'):
 if p.startswith('# '): title=p[2:];continue
 if p.startswith('餐饮商业研究院'): meta=p;continue
 if p.startswith('## '):
  i+=1;h=p[3:];sid=f'section-{i}';toc.append((sid,h));blocks.append(f'<h2 id="{sid}">{html.escape(h)}</h2>');continue
 if p.startswith('!['):
  m=re.fullmatch(r'!\[(.*?)\]\((.*?)\)',p);alt,path=m.groups();blocks.append(f'<figure>{figs[path]}<figcaption>{html.escape(alt)}</figcaption></figure>');continue
 if re.match(r'^\[[12]\] ',p):
  n=p[1];blocks.append(f'<p class="source" id="source-{n}"><span class="source-index">[{n}]</span> {inline(p[4:])}</p>');continue
 blocks.append(f'<p>{inline(p)}</p>')
body='\n'.join(blocks)
nav=''.join(f'<a href="#{s}">{html.escape(t)}</a>' for s,t in toc)
page='''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>__TITLE__</title><meta name="description" content="从しゃぶ葉多桌配送的补救措施出发，比较合批运输节省与辨认、补餐、解释负担，给餐厅老板一套有退出条件的验收办法。"><style>
:root{--ink:#183b31;--text:#263c34;--muted:#52675c;--line:#cfdbcf;--paper:#fffef8;--wash:#edf1e8;--accent:#916632}*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:28px}body{margin:0;background:var(--wash);color:var(--text);font-family:"Noto Sans CJK SC","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.86}a{color:#295a45;text-underline-offset:.22em;overflow-wrap:anywhere}a:focus-visible{outline:3px solid #b17629;outline-offset:4px}.skip{position:absolute;top:-60px;left:12px}.skip:focus{top:12px;background:#fff;padding:8px;z-index:1}.page{max-width:1100px;margin:0 auto;background:var(--paper);min-height:100vh}.masthead{padding:25px 7.2% 0;font-size:13px;letter-spacing:.13em;color:var(--muted);display:flex;gap:14px;justify-content:space-between;flex-wrap:wrap}.masthead span:last-child{letter-spacing:.04em}.hero{padding:46px 7.2% 36px;max-width:980px}.eyebrow{font-size:14px;color:var(--accent);letter-spacing:.06em;font-weight:700;margin:0 0 17px}h1{font-family:"Noto Serif CJK SC","Songti SC",serif;font-size:clamp(30px,4.2vw,47px);line-height:1.42;letter-spacing:.015em;color:var(--ink);margin:0;font-weight:800}.subtitle{font-size:16px;color:var(--muted);margin:22px 0 0}.layout{display:grid;grid-template-columns:minmax(0,1fr) 230px;gap:45px;padding:0 7.2% 58px}article{min-width:0;font-size:17px}article>p:first-child{font-size:19px;color:var(--ink);line-height:1.95;margin-top:0}p{margin:0 0 1.2em}h2{font-size:25px;line-height:1.55;color:var(--ink);margin:2.4em 0 .9em;letter-spacing:.01em}strong{font-weight:750;color:var(--ink)}.cite{font-size:.77em;vertical-align:super;text-decoration:none;padding:0 .08em;white-space:nowrap}figure{margin:32px 0 34px}svg{display:block;max-width:100%;width:100%;height:auto;border:1px solid #d9e2d5;border-radius:14px}figcaption{font-size:13px;color:var(--muted);line-height:1.75;margin:12px 3px 0}.source{font-size:14px;line-height:1.85}.source-index{font-weight:700;color:var(--ink)}.source~p:last-child{font-size:14px;color:var(--muted)}aside{align-self:start;position:sticky;top:28px;border-top:3px solid var(--ink);padding-top:17px;color:var(--muted)}aside h2{font-size:14px;margin:0 0 14px;letter-spacing:.06em}aside a{display:block;font-size:13px;line-height:1.65;margin:0 0 14px;text-decoration:none}aside a:hover{text-decoration:underline}.aside-note{font-size:12px;border-top:1px solid var(--line);padding-top:17px;margin-top:22px;line-height:1.8}footer{padding:24px 7.2%;border-top:1px solid var(--line);font-size:12px;color:var(--muted);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}footer a{white-space:nowrap}@media(max-width:850px){.layout{display:block;padding:0 7% 40px}.hero{padding:35px 7% 30px}.masthead{padding-left:7%;padding-right:7%}aside{position:static;margin-top:45px;columns:2;column-gap:28px}aside h2,.aside-note{column-span:all}article{font-size:18px}h2{font-size:26px}figure{max-width:560px;margin-left:auto;margin-right:auto}}@media(max-width:480px){.hero{padding-top:32px}.masthead{font-size:11px;gap:4px}.masthead span:last-child{width:100%}h1{font-size:32px;line-height:1.48}.eyebrow{font-size:12px}.subtitle{font-size:14px}.layout{padding-left:6%;padding-right:6%}.hero{padding-left:6%;padding-right:6%}article{font-size:17px}article>p:first-child{font-size:18px}h2{font-size:23px;margin-top:2em}figcaption{font-size:12px}aside{columns:1}footer{font-size:11px}.source{font-size:13px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{body{background:#fff}.page{max-width:none}.masthead,.hero,.layout,footer{padding-left:0;padding-right:0}.hero{padding-top:20px}.layout{display:block}aside,.skip,footer a{display:none}h1{font-size:28pt}h2{font-size:18pt;break-after:avoid}article{font-size:11pt}article>p:first-child{font-size:12pt}figure{max-width:410px;break-inside:avoid}a{color:inherit}p{orphans:3;widows:3}footer{margin-top:20px}svg{max-height:210mm}}
</style></head><body id="top"><a class="skip" href="#article">跳到正文</a><div class="page"><div class="masthead"><span>餐饮商业研究院</span><span>门店自动化 · 经营判断</span></div><header class="hero"><p class="eyebrow">老板读本　/　送餐合批</p><h1>__TITLE__</h1><p class="subtitle">__META__</p></header><div class="layout"><main id="article"><article>__BODY__</article></main><aside aria-label="本文目录"><h2>阅读导航</h2>__NAV__<p class="aside-note">本文研究合批范围与服务工时，不据投诉估算损失，不将自动化功能写成已验证的 AI 成效。两图均为原创定性分析。</p></aside></div><footer><span>公开资料研究 · 事实与建议分开 · 完整离线读本</span><a href="#top">返回顶部 ↑</a></footer></div></body></html>'''
page=page.replace('__TITLE__',html.escape(title)).replace('__META__',html.escape(meta)).replace('__BODY__',body).replace('__NAV__',nav)
(P/'report.html').write_text(page)
print(json.dumps({'title':title,'body_cjk_chars':len(re.findall(r'[\u4e00-\u9fff]',md.split('## 来源与研究范围')[0])),'html_bytes':len(page.encode()),'sha256':hashlib.sha256(page.encode()).hexdigest()},ensure_ascii=False,indent=2))
