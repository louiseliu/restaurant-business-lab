"""Standalone complete reader; no site mutation or HTML GitHub upload."""
from pathlib import Path
import html,re,json,hashlib
p=Path(__file__).parent
inputs=p if (p/'note.md').exists() else p.parents[1]/'research'/'2026-11-12-procurement-friction'
note=(inputs/'note.md').read_text().rstrip()+'\n\n'; sources=(inputs/'sources.md').read_text().rstrip()+'\n\n'
def render(s):
 out=[]
 for block in s.strip().split('\n\n'):
  b=html.escape(block)
  b=re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)',r'<a href="\2">\1</a>',b)
  b=re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',b,flags=re.S)
  if b.startswith('# '): out.append('<h1>'+b[2:]+'</h1>')
  elif b.startswith('## '): out.append('<h2>'+b[3:]+'</h2>')
  else: out.append('<p>'+b.replace('\n','<br>')+'</p>')
 return '\n'.join(out)
css='''body{margin:0;background:#f4f1e9;color:#18312c;font:18px/1.85 system-ui,sans-serif}main{max-width:880px;margin:auto;padding:44px 24px}h1{font-size:clamp(30px,5vw,46px);line-height:1.3}h2{font-size:26px;line-height:1.5;margin-top:2em}a{color:#126854;overflow-wrap:anywhere}figure{margin:32px 0;padding:26px;background:white;border:1px solid #ccd8cf;border-radius:16px}figure h2{margin-top:0}.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.steps section{padding:16px;background:#edf3ee;border-radius:9px}.warn{border-left:4px solid #ab5b35;padding-left:16px}figcaption,.meta{font-size:14px;color:#49635b}figcaption{margin-top:16px}table{width:100%;border-collapse:collapse;font-size:16px}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #d3ddd4;padding:12px 8px}details{padding:18px;border:1px solid #ccd6cb;margin-top:24px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.7 monospace}@media(max-width:600px){body{font-size:17px}main{padding:24px 15px}.steps{grid-template-columns:1fr}figure{padding:17px}th,td{padding:8px 5px;font-size:14px}}@media print{body{background:white}figure{break-inside:avoid}}'''
fig1='''<figure><h2>图解 1：操作障碍在何时进入选择？</h2><div class="steps"><section><b>业务筛选</b><p>服务、预算、期限<br>先判断是否合适</p></section><section><b>办理障碍</b><p>需要负责人认证<br>不自动等于不合适</p></section><section><b>一次交接</b><p>保留候选和准备<br>再决定是否继续</p></section></div><p class="warn">风险路径：先按“能否独立办理”过滤，再把剩余选项误当成完整比较。</p><figcaption>作者定性分析，不是实验方系统流程。事实锚点：项目方自报未系统比价、选择免 BankID 办理的三年电力合同；没有证明因此买贵。<a href="https://andonlabs.com/blog/ai-cafe-stockholm">原始资料</a></figcaption></figure>'''
fig2='''<figure><h2>图解 2：什么时候应多保留一次交接？</h2><table><thead><tr><th>经营条件</th><th>合理重心</th><th>建议反转点</th></tr></thead><tbody><tr><td>合格供应商内的稳定复购</td><td>按已批准条件及时完成</td><td>规格、期限或供应条件改变</td></tr><tr><td>有可比选项的长期承诺</td><td>先比较，再办理</td><td>等待的实际代价超过保留选项价值</td></tr><tr><td>必要服务即将中断</td><td>显式权衡时效与条件</td><td>紧迫性解除，重新评估长期方案</td></tr></tbody></table><figcaption>建议矩阵，不是实测收益表。价格差、退出费用、人工时间与延误损失须按本店查证；无金额、比例或回本估算。</figcaption></figure>'''
body=render(note).replace('<h2>一次求助与多年承诺',fig1+'<h2>一次求助与多年承诺',1).replace('<h2>下一次采购',fig2+'<h2>下一次采购',1)
page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI替老板办采购，少问一次是否值得签三年？</title><style>'+css+'</style></head><body><main><p class="meta">餐饮商业模式研究院 · 完整图文读本 · 2026-11-12</p>'+body+'<details><summary>来源台账及未采用材料</summary>'+render(sources)+'</details><details><summary>完整 Markdown 原文</summary><pre>'+html.escape(note)+'</pre></details></main></body></html>'
assert page.count('<figure>')==2
assert all(html.escape(b.strip()) in page for b in note.split('\n\n') if b.strip())
assert not re.search(r'chatgpt\.com/[cg]/|/workspace/|libfile_|3156a0c9|6abcb5b0',page)
assert '<script' not in page and '<iframe' not in page
(p/'AI采购-少问一次是否值得签三年.html').write_text(page)
qa={'full_prose':True,'sources_preserved':True,'diagrams':2,'diagram_type':'qualitative author analysis','private_link_scan':'pass','external_script_images':False,'html_sha256':hashlib.sha256(page.encode()).hexdigest(),'html_bytes':len(page.encode()),'browser_visual_test':'not_run','site_synced':False,'github_html_archived':False}
(p/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(qa,ensure_ascii=False))
