from pathlib import Path
import re,html,json,hashlib
p=Path(__file__).parent
text=(p/'note.md').read_text()
def inline(s):
 s=html.escape(s)
 s=re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)',r'<a href="\2" rel="noreferrer">\1</a>',s)
 return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
body=[]
for para in text.strip().split('\n\n'):
 m=re.match(r'^(#{1,3}) (.+)$',para)
 body.append(f'<h{len(m[1])}>{inline(m[2])}</h{len(m[1])}>' if m else '<p>'+inline(para).replace('\n','<br>')+'</p>')
story=json.loads((p/'illustrated-story.json').read_text())
figure=''
for d in [story['diagram'],story['secondDiagram']]:
 figure+='<figure><figcaption>'+inline(d['label'])+'</figcaption><div class="flow">'+''.join('<div>'+inline(n['title'])+'<br><small>'+inline(n['text'])+'</small></div>' for n in d['nodes'])+'</div><p>'+inline(d['scope']+' '+d['note'])+'</p></figure>'
figure+='<figure><figcaption>计算示意：费用率下降，费用未必下降</figcaption><p>仅假设8.5%与6.2%是同口径能源费用率。上期营收归一化为100，费用8.5；不是旺顺阁账本。</p><div class="flow"><div>本期营收100<br>费用6.20<br>费用下降27.06%</div><div>本期营收137.10<br>费用约8.50<br>费用基本不变</div><div>本期营收140<br>费用8.68<br>费用增加2.12%</div></div><p>实际营收、分子计量单位及能源价格未公开。图中营收情景是假设，结果是计算，不是实测或AI效果。</p></figure>'
css='''body{margin:0;background:#f7f6f1;color:#25352c;font:17px/1.9 system-ui,sans-serif}main{max-width:900px;padding:48px 24px;margin:auto}h1{font-size:clamp(30px,5vw,46px);line-height:1.3}h2{margin-top:2.3em;border-top:1px solid #ccd5ce;padding-top:1em;font-size:26px}a{color:#176754;overflow-wrap:anywhere}figure{margin:32px 0;padding:22px;background:#e7eee8;border-radius:14px}figcaption{font-weight:700}.flow{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:20px}.flow div{padding:14px;background:white;border-left:4px solid #38765a}.flow small{color:#58675e}header,footer{color:#58675e;font-size:14px}p{overflow-wrap:anywhere}@media(max-width:650px){.flow{grid-template-columns:1fr 1fr}main{padding:24px 16px}}'''
out='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>餐厅要为 AI 节能多付多少钱？</title><style>'+css+'</style><main><header>餐饮商业模式研究院 · 完整修订读本<br>首次入库：2026-10-31 20:07:57 UTC · 本次修订：2026-11-08<br>附件读本；站点尚未同步。不是新增文章。</header>'+figure+''.join(body)+'<footer>公开资料研究 · 不替代具体门店尽调</footer></main></html>'
for bad in ['chatgpt.com/g/','chatgpt.com/c/','data-app-local-thread','api_key','access_token']:
 assert bad not in out
assert all(inline(s) in out for s in text.strip().split('\n\n') if not s.startswith('#'))
(p/'report-revised.html').write_text(out)
(p/'qa.json').write_text(json.dumps({'full_body_paragraphs':len(body),'private_pattern_scan':'passed','new_articles':0,'html_github_archived':False,'site_synced':False,'visual_check':'not performed','sha256':hashlib.sha256(out.encode()).hexdigest()},indent=2)+'\n')
