from pathlib import Path
from html import escape
import re,json,hashlib
R=Path(__file__).resolve().parent
CONTENT=R if (R/'note.md').exists() else R.parents[1]/'research'/'2026-11-06-dishwashing-workflow'

def inline(s):
 return re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)',r'<a href="\2">\1</a>',escape(s))
def md(s):
 out=[]
 for b in s.strip().split('\n\n'):
  if b.startswith('# '):out.append('<h1>'+inline(b[2:])+'</h1>')
  elif b.startswith('## '):
   lines=b.splitlines();out.append('<h2>'+inline(lines[0][3:])+'</h2>')
   if len(lines)>1:out.append(md('\n'.join(lines[1:])))
  elif b.startswith('- '):out.append('<ul>'+''.join('<li>'+inline(i[2:])+'</li>' for i in b.splitlines())+'</ul>')
  else:out.append('<p>'+inline(b.replace('\n',' '))+'</p>')
 return '\n'.join(out)
css='''*{box-sizing:border-box}body{margin:0;background:#f4f1e9;color:#20312f;font-family:system-ui,"Microsoft YaHei",sans-serif;line-height:1.85}main{max-width:960px;margin:auto;background:white;padding:56px 62px}h1{font-size:38px;line-height:1.3}h2{font-size:25px;margin-top:45px}p{font-size:17px}a{color:#176d60;overflow-wrap:anywhere}.meta,figcaption{font-size:13px;color:#586c66}figure{margin:35px 0;padding:25px;background:#eff6f2;border:1px solid #cadbd1}h3{margin:0 0 20px;font-size:23px}.flow{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.box{padding:18px;background:white;border-top:4px solid #26765f}.box small{display:block;color:#586c66}.bar{height:34px;background:#287963;color:white;padding:2px 8px;font-size:14px}.rent{height:4px;background:#aa6445;margin:5px 0 13px}.row{margin:18px 0}.row label{display:block;font-size:14px}table{width:100%;border-collapse:collapse;font-size:14px}th,td{padding:9px;border-bottom:1px solid #cadbd1;text-align:right}th:first-child,td:first-child{text-align:left}details{border-top:1px solid #cadbd1;margin-top:50px;padding-top:20px}summary{cursor:pointer;font-size:20px}li{overflow-wrap:anywhere;font-size:14px}@media(max-width:650px){main{padding:24px 20px}h1{font-size:30px}.flow{grid-template-columns:1fr}figure{padding:17px}p{font-size:16px}}@media print{body{background:white}main{padding:0}figure{break-inside:avoid}h2{break-after:avoid}details{display:block}}'''
fig1='''<figure><h3>取消岗位前，先找到剩下的工作由谁接手</h3><div class="flow"><div class="box">预处理与装筐<small>不能只看机器额定速度</small></div><div class="box">卸筐、检查与返洗<small>合格结果优先于减排班</small></div><div class="box">收尾与故障接手<small>只有可减少付薪工时才计工资节省</small></div></div><figcaption>原创机制示意，依据原文分析，不是门店实测或设备操作指导。完整流程成立不代表必然能减岗。</figcaption></figure>'''
fig2='''<figure><h3>同一笔省电收益，不能省略每年的租金</h3><div class="flow"><div class="box">27,315.84 港元<small>原表16,656 kWh × 1.64港元/kWh<br>电费毛节省复算</small></div><div class="box">－14,400 港元<small>历史月租1,200 × 12<br>只列设备租金</small></div><div class="box">＝12,915.84 港元<small>两项金额之差，非净利润<br>尚未扣其他增量成本</small></div></div><figcaption>计算，非另一次测量。输入来自茶饭历史案例，原表电量已取整；完整成本与当前报价未知。不得当作AI收益。</figcaption></figure>'''
fig3='''<figure><h3>使用得少，节电毛额可能还不够付租金</h3><p class="meta">条件情景：每小时省4.01 kWh、电价1.64港元/kWh、365日、月租1,200港元均固定。绿色为毛节省，棕线为年租金14,400港元；两者按同一尺度绘制。</p>'''
vals=json.loads((R/'calculations.json').read_text())['scenarios']
for v in vals:
 h=v['hours_per_day'];g=float(v['gross']);net=float(v['gross_less_rent'])
 fig3+=f'<div class="row"><label>{h} 小时/日 · 毛额 {g:,.2f} 港元 · 扣租金差额 {net:+,.2f}</label><div class="bar" style="width:{g/30000*100:.3f}%"></div><div class="rent" style="width:48%"></div></div>'
fig3+='''<figcaption>连续小时情景实际运行计算，非门店预测。约6小时只是电费毛额刚覆盖租金的门槛；运行小时不等于开门小时。11.38小时情景未沿用原表取整电量，故比前图毛额高约0.55港元；不得混同口径。实际节电差随负荷变化。</figcaption></figure>'''
note=(CONTENT/'note.md').read_text();body=md(note)
body=body.replace('<h2>三个可以落实的决定</h2>',fig1+'<h2>三个可以落实的决定</h2>')
body=body.replace('<p>更能改变小店决定的是运行时间。',fig2+'<p>更能改变小店决定的是运行时间。')
body=body.replace('<p>因此，不能减岗但设备高频使用',fig3+'<p>因此，不能减岗但设备高频使用')
html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>洗碗机的人工与能源两本账｜同篇修订</title><style>'+css+'</style></head><body><main><div class="meta">餐饮商业模式研究院 · 原文首次入库2026-11-06 11:10:04 UTC · 2026-11-09同篇补充，不计新篇<br>完整正文独立阅读本。保留原正文，不覆盖历史图文附件或门户；新增三幅原创图。不代表已上站。</div><article>'+body+'</article><details><summary>来源与核验范围（完整台账）</summary>'+md((CONTENT/'sources.md').read_text())+'</details></main></body></html>'
(R/'report.html').write_text(html)
assert html.count('<figure>')==3
for bad in ['chatgpt.com/c/','chatgpt.com/g/','/workspace/','/tmp/','token=']:
 assert bad not in html,bad
assert note.startswith('''# 买了洗碗机，什么时候才能真正少排一个人？''')
print(json.dumps({'html_bytes':len(html.encode()),'sha256':hashlib.sha256(html.encode()).hexdigest(),'figures':3,'browser_verified':False,'live_site_updated':False},indent=2))
