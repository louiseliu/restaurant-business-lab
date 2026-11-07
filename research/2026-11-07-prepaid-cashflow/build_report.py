from pathlib import Path
import html,re,json,hashlib
p=Path(__file__).resolve().parent
note=(p/'note.md').read_text()
def inline(s):
 s=html.escape(s)
 s=re.sub(r'\[([^]]+)\]\((https://[^)]+)\)',r'<a href="\2">\1</a>',s)
 return re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',s)
def render(md):
 out=[]
 for block in md.strip().split('\n\n'):
  if block.startswith('# '):out.append('<h1>'+inline(block[2:])+'</h1>')
  elif block.startswith('## '):out.append('<h2>'+inline(block[3:])+'</h2>')
  else:out.append('<p>'+inline(block).replace('\n','<br>')+'</p>')
 return '\n'.join(out)
chart='''<figure><h2>余额是义务存量，不是可动用现金</h2><p class="tag">财报事实 + 作者单位换算｜仅预付卡相关合约负债</p><div class="row"><b>2024年末</b><div class="bar" style="width:92.65%">7,412.2 万元</div></div><div class="row"><b>2025年末</b><div class="bar second" style="width:84.29%">6,743.0 万元</div></div><p>减少 669.2 万元 / 9.03% <span class="tag">计算</span></p><figcaption>条长从零开始，同一比例；未含会员计划。余额变化不能识别充值、退款或现金用途。来源：小菜园2025年年报附注21，印刷页181。</figcaption></figure>'''
flow='''<figure><h2>扩店前，先把两条现金路径分开</h2><p class="tag">作者机制示意，非企业实测；不是法定资金留存比例</p><div class="flow"><div>已收资金<br><small>先排除受限款</small></div><span>→</span><div>老店逐周现金<br><small>正常现付收入<br>减到期支出、履约、退款</small></div><span>→</span><div>新店可承受投入？<br><small>看现金低谷，不只看月末</small></div></div><p class="warning">压力情景：暂不计后续新充值。已有预算包含的成本不重复扣；剩余义务不能在测试终点消失。</p><figcaption>测试通过只说明现金安排可能承受，不证明新店值得投资。</figcaption></figure>'''
body=render(note)
needle='<h2>为什么余额不变，店里仍可能需要不断补钱？</h2>'
body=body.replace(needle,chart+needle)
needle='<h2>退款账不能预设“全部按原价倒扣”</h2>'
body=body.replace(needle,flow+needle)
css='''body{margin:0;background:#f5f2eb;color:#203936;font:18px/1.85 system-ui,"Microsoft YaHei",sans-serif}main{max-width:900px;margin:auto;padding:50px 25px 80px}h1{font-size:clamp(30px,5vw,48px);line-height:1.3;margin-bottom:24px}h2{font-size:26px;line-height:1.45;margin-top:48px}p{margin:23px 0}strong{color:#154e45}a{color:#146c68;text-underline-offset:4px;overflow-wrap:anywhere}figure{margin:40px 0;padding:28px;background:#fff;border:1px solid #cad9d1;border-radius:18px}figure h2{margin-top:0}.tag,figcaption{font-size:14px;color:#5d716b}.row{margin:18px 0}.bar{box-sizing:border-box;margin-top:7px;background:#1c6558;color:white;padding:9px 15px;border-radius:4px;white-space:nowrap;min-width:170px}.second{background:#528a78}.flow{display:flex;align-items:center;gap:12px}.flow div{flex:1;background:#eef4ef;padding:18px;border-radius:10px;text-align:center}.flow small{font-size:14px}.warning{border-left:4px solid #b58b42;padding-left:15px;font-size:16px}footer{border-top:1px solid #b9c9c0;margin-top:50px;font-size:14px;color:#5d716b} @media(max-width:620px){main{padding:30px 18px}.flow{display:block}.flow>span{display:block;text-align:center;transform:rotate(90deg)}figure{padding:18px}h2{font-size:23px}} @media print{body{background:#fff}main{max-width:none;padding:0}figure{break-inside:avoid}}'''
output='<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>储值到账很多，为什么不能直接拿去开下一家店？</title><style>'+css+'</style></head><body><main><article>'+body+'</article><footer><p>餐饮商业模式研究院 · 独立图文读本 · 2026-11-07</p><p>本文已保留完整正文与原始来源。图表分别标明财报事实、计算及机制示意。独立附件不代表已同步既有网站。</p></footer></main></body></html>'
(p/'prepaid-cashflow.html').write_text(output)
# Static validation: compare each source paragraph's rendered text after stripping tags.
from html.parser import HTMLParser
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,d):self.parts.append(d)
t=Text();t.feed(output);plain=''.join(t.parts)
for block in note.strip().split('\n\n'):
 r=Text();r.feed(render(block));assert ''.join(r.parts) in plain,block[:40]
assert len(re.findall('<figure>',output))==2
assert '<script' not in output and '<iframe' not in output
for forbidden in ['chatgpt.com/c/','chatgpt.com/g/','file-service://','library_file_id','Bearer ','/workspace/','Sentinel_']:
 assert forbidden not in output
assert '7,412.2' in output and '6,743.0' in output and '669.2' in output
result={'full_text_paragraphs':len(note.strip().split('\n\n')),'figures':2,'source_links':re.findall('href="([^"]+)"',output),'html_bytes':len(output.encode()),'sha256':hashlib.sha256(output.encode()).hexdigest(),'tests':'static only; no browser or screen reader test'}
(p/'qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
