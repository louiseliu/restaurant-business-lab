"""Build a self-contained revision reader, preserving full prose and source ledger."""
from pathlib import Path
from decimal import Decimal
import re,html,json,hashlib
p=Path(__file__).parent
note=(p/'note.md').read_text();sources=(p/'sources.md').read_text()
def md(s):
 out=[]
 for block in s.strip().split('\n\n'):
  b=html.escape(block)
  b=re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)',r'<a href="\2">\1</a>',b)
  b=b.replace('[来源台账](sources.md)','<a href="#sources">来源台账</a>')
  b=re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',b,flags=re.S)
  if b.startswith('# '):out.append('<h1>'+b[2:]+'</h1>')
  elif b.startswith('## '):out.append('<h2>'+b[3:]+'</h2>')
  else:out.append('<p>'+b.replace('\n','<br>')+'</p>')
 return '\n'.join(out)
rows=[('录用通知','8.70','9.73'),('满一个月仍在岗','4.98','5.89')]
calc={n:{'human_percent':a,'ai_percent':b,'difference_pp':str(Decimal(b)-Decimal(a))} for n,a,b in rows}
(p/'revision-calculations.json').write_text(json.dumps(calc,ensure_ascii=False,indent=2)+'\n')
chart='<figure><h2>同一分母，两个漏斗结果</h2><p>事实：论文披露的两组比例。分母为各组全体随机申请，不是仅已录用员工。</p>'
for n,a,b in rows:
 chart+=f'<h3>{n}</h3>'
 for label,value,color in [('人工访谈',a,'#637b86'),('AI访谈',b,'#167760')]:
  chart+=f'<div class="barrow"><span>{label}</span><div class="track"><div style="width:{float(value)*8}%;background:{color}" class="bar"></div></div><b>{value}%</b></div>'
 chart+=f'<p>计算：相差 {calc[n]["difference_pp"]} 个百分点。</p>'
chart+='<figcaption>条长共用0—12.5%比例尺；非餐饮效果、非成本收益。来源：<a href="https://arxiv.org/html/2607.28222v2#S3">论文 §3</a>。人工仍决定录用。</figcaption></figure>'
diagram='''<figure><h2>采购权限分三层验收</h2><div class="steps"><section><b>① 行政辅助</b><p>答疑、预约、提醒</p><small>先比普通表单与固定回复，检查岗位信息更新。</small></section><section><b>② 信息采集</b><p>统一覆盖岗位问题<br>允许必要澄清</p><small>重复量足够时再评估；保留替代入口与完整记录。</small></section><section><b>③ 评价与录用</b><p>由负责人判断</p><small>前两层通过不等于这一层通过，不建立自动淘汰阈值。</small></section></div><figcaption>作者定性示意，不是品牌后台复刻或论文已验证的餐饮部署。若障碍是待遇、班次、通勤或需现场操作考察，先处理这些条件。</figcaption></figure>'''
css='''body{margin:0;background:#f4f1e9;color:#18312c;font:18px/1.85 system-ui,"Noto Sans CJK SC",sans-serif}main{max-width:880px;margin:auto;padding:48px 24px}h1{font-size:clamp(30px,5vw,48px);line-height:1.3}h2{font-size:27px;margin-top:2em;line-height:1.45}h3{font-size:19px}p{margin:1em 0}a{color:#126854;overflow-wrap:anywhere}figure{margin:32px 0;padding:28px;background:white;border:1px solid #d3d9cf;border-radius:18px}figure h2{margin-top:0}.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.steps section{padding:16px;background:#edf3ee;border-radius:10px}.steps p{font-size:17px}small,figcaption,.meta{font-size:14px;color:#49635b}figcaption{margin-top:20px}.barrow{display:flex;gap:12px;align-items:center;font-size:15px}.barrow span{width:70px}.barrow b{width:65px}.track{flex:1;background:#edf0ed;height:22px}.bar{height:22px}details{margin-top:24px;padding:20px;border:1px solid #ccd6cb}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.7 monospace}@media(max-width:600px){main{padding:24px 16px}.steps{grid-template-columns:1fr}figure{padding:18px}body{font-size:17px}}@media print{body{background:white}details{display:block}figure{break-inside:avoid}}'''
body=md(note)
body=body.replace('<h2>不只排期：',chart+diagram+'<h2>不只排期：',1)
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI招聘：入口、信息采集与录用权</title><style>'+css+'</style><main><p class="meta">餐饮商业模式研究院 · 同篇修订 · 首次入库 2026-11-05 21:05:54 UTC · 修订 2026-11-11</p>'+body+'<details id="sources"><summary>完整来源台账（含原核验日期）</summary>'+md(sources)+'</details><details><summary>修订版完整 Markdown 原文</summary><pre>'+html.escape(note)+'</pre></details><p class="meta">本附件为完整修订阅读版，未替换历史图文或门户。原站未同步；HTML GitHub 归档未完成。图解为作者分析或披露值计算，未作门店试验。</p></main></html>'
assert not re.search(r'chatgpt\.com/[cg]/|/workspace/|file_|3156a0c9|6abcb5b0',page)
assert all(html.escape(b.strip()) in page for b in note.split('\n\n') if b.strip()) # raw original preserves every block
(p/'AI招聘-入口与信息采集-修订版.html').write_text(page)
qa={'article_id':'research-2026-11-05-hiring-access-note','publishedAt':'2026-11-05T21:05:54Z','updatedDate':'2026-11-11','full_prose_and_ledger':True,'private_link_scan':True,'external_script_or_image_dependencies':False,'html_sha256':hashlib.sha256(page.encode()).hexdigest(),'html_bytes':len(page.encode()),'browser_visual_test':'not_run; existing access limitations not retried','site_synced':False,'github_html_archived':False}
(p/'revision-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(qa,ensure_ascii=False,indent=2))
