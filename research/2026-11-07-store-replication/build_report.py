from pathlib import Path
import html,re,json,hashlib
p=Path(__file__).parent

def inline(s):
 s=html.escape(s)
 s=re.sub(r'\[([^]]+)\]\((https://[^)]+)\)',r'<a href="\2">\1</a>',s)
 return re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',s)
def render(md):
 out=[]
 for b in md.strip().split('\n\n'):
  if b.startswith('# '):out.append('<h1>'+inline(b[2:])+'</h1>')
  elif b.startswith('## '):out.append('<h2>'+inline(b[3:])+'</h2>')
  else:out.append('<p>'+inline(b).replace('\n','<br>')+'</p>')
 return '\n'.join(out)
fig='''<section class="figure" aria-labelledby="map"><h2 id="map">一笔收购，三层证据</h2><p class="label">作者机制示意 · 不是餐愿的经营结果或实测流程</p><div class="grid"><div><span>01 / 历史</span><h3>原店在原组合里赚钱</h3><p>人、铺位、熟客、供应条件同时存在</p><strong>不直接证明接手结余</strong></div><div><span>02 / 交接</span><h3>接班后能持续经营</h3><p>替代劳动、召回、返工与补偿均有记录</p><strong>不直接证明异地需求</strong></div><div><span>03 / 复制</span><h3>换环境后仍能成立</h3><p>常态获客、新租金、爬坡和分流分别核对</p><strong>才有扩大投入的依据</strong></div></div><p>每跨一层，都增加需要验证的条件。不能用同一份历史流水证明三层价值。</p></section><section class="figure"><h2>结果不好，先判断该回到哪一步</h2><p class="label">作者决策示意 · 尚未执行的验证建议</p><div class="grid"><div><h3>离开老板就要救火</h3><p>回到岗位交接和授权。保留单店或继续培养，不急着增加品牌。</p></div><div><h3>交接稳，但新店靠促销</h3><p>回到需求、价格和店址。不要用更多培训工具解释获客不成立。</p></div><div><h3>多店独立运转，重复事务重</h3><p>再比较共享服务和自动整理。此时工具投入的优先级可以提高。</p></div></div></section>'''
css='''body{margin:0;background:#f5f2ea;color:#203b36;font-family:system-ui,"Noto Sans CJK SC",sans-serif;line-height:1.85}main{max-width:920px;margin:auto;padding:40px 24px 80px}h1{font-size:clamp(28px,5vw,42px);line-height:1.35}h2{margin-top:2em;font-size:24px}h3{font-size:18px}p{font-size:17px}a{color:#146b67;overflow-wrap:anywhere}strong{color:#145b50}.figure{background:#e4eee5;padding:24px;border-radius:18px;margin:32px 0}.figure h2{margin:0}.label{font-size:14px;color:#52675d}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.grid>div{background:white;border-top:4px solid #c28d46;padding:16px}.grid p{font-size:15px}.grid span{font-size:13px;letter-spacing:.1em}.source{border-top:1px solid #bcc9bd;margin-top:44px}.source p{font-size:15px}.badge{font-size:13px;letter-spacing:.1em} @media(max-width:650px){.grid{grid-template-columns:1fr}main{padding:24px 18px}.figure{padding:18px}}@media print{body{background:white}main{padding:0}.grid{break-inside:avoid}a{color:inherit}}'''
note=(p/'note.md').read_text(); sources=(p/'sources.md').read_text();body=render(note);parts=body.split('\n',3);body='\n'.join(parts[:3])+'\n'+fig+'\n'+'\n'.join(parts[3:])
s='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>买下盈利老店与复制能力｜餐饮商业模式研究院</title><style>'+css+'</style></head><body><main><p class="badge">经营决策研究 · 单篇全文图文</p>'+body+'<section class="source">'+render(sources)+'</section><p class="label">交付边界：独立HTML，原站未同步；浏览器视觉与交互未验。图解为条件分析，不是统计图或已验证成效。</p></main></body></html>'
(p/'store-replication.html').write_text(s)
from html.parser import HTMLParser
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.text=[]
 def handle_data(self,d):self.text.append(d)
a=Parser();a.feed(s); visible=''.join(a.text)
for md in [note,sources]:
 for b in md.split('\n\n'):
  raw=re.sub(r'\[([^]]+)\]\((https://[^)]+)\)',r'\1',b);raw=re.sub(r'^#{1,2} ','',raw).replace('**','').replace('\n','')
  assert raw.strip() in visible,raw[:40]
assert not re.search(r'chatgpt.com/[cg]/|/workspace/|/tmp/|Bearer |sk-[a-zA-Z0-9]{20}',s)
assert '<script' not in s
qa={'full_note_and_sources_text_preserved':True,'diagram_count':2,'diagrams':'author conditional mechanisms, not measured','privacy_scan':True,'external_scripts':False,'browser_visual_or_interaction_tested':False,'site_synced':False,'html_github_archived':False,'html_bytes':len(s.encode()),'html_sha256':hashlib.sha256(s.encode()).hexdigest()}
(p/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa,ensure_ascii=False))
