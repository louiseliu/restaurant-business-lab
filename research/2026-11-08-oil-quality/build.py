from pathlib import Path
import html,re,hashlib,json
p=Path(__file__).parent
md=p.joinpath('note.md').read_text()
def inline(s):
 s=html.escape(s)
 return re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)',r'<a href="\2">\1</a>',s)
def render(s):
 out=[]
 for b in s.split('\n\n'):
  if b.startswith('# '):out.append('<h1>'+inline(b[2:])+'</h1>')
  elif b.startswith('## '):out.append('<h2>'+inline(b[3:])+'</h2>')
  elif b.startswith('<!--'):out.append(b)
  else:out.append('<p>'+inline(b).replace('\n','<br>')+'</p>')
 return '\n'.join(out)
fig1='''<figure><figcaption>01 · 买工具之前，先接通三件事 <small>作者机制示意</small></figcaption><div class="flow"><div><b>判什么</b><strong>适用指标</strong><span>酸价、极性组分等<br>不能用实验标签直接替换</span></div><i>→</i><div><b>怎样判</b><strong>可信测量</strong><span>适用方法与条件<br>校准、维护、异常复核</span></div><i>→</i><div><b>谁来做</b><strong>实际处置</strong><span>检测记录关联换油<br>交接与责任明确</span></div></div><p>任一环节未接通，增加识别速度都不等于改善换油决定。</p></figure>'''
fig2='''<figure><figcaption>02 · 三种证据，各自回答不同问题 <small>定性比较，不是效果排名</small></figcaption><div class="compare"><section><h3>适用标准</h3><b>判定要求是什么？</b><p>GB 2716—2018的相应指标与检验方法</p><em>不等于只看两个数就能放行</em></section><section><h3>传统快检</h3><b>现场读数可信吗？</b><p>校准、适用油种和条件、异常复核</p><em>不等于任意仪器都替代法定检验</em></section><section><h3>AI实验</h3><b>限定数据中能否分类？</b><p>FryNet按Totox标签测试；并非中国门店验证</p><em>不等于获得延长用油的依据</em></section></div><p>采购比较应在同一目标和可比工况下进行，不能把三层证据画等号。</p></figure>'''
body=render(md).replace('<!-- FIGURE_1 -->',fig1).replace('<!-- FIGURE_2 -->',fig2)
css='''*{box-sizing:border-box}body{margin:0;background:#f4f1e9;color:#1e302e;font-family:system-ui,"Noto Sans CJK SC",sans-serif;line-height:1.85}main{max-width:1000px;margin:auto;padding:44px 24px 72px}header{border-top:7px solid #185b51;padding-top:18px;font-size:14px;letter-spacing:.06em;color:#4d6861}h1{font-size:clamp(28px,4.5vw,46px);line-height:1.35;max-width:850px;margin:24px 0}h2{font-size:26px;margin-top:46px;line-height:1.5;border-left:5px solid #bc8433;padding-left:16px}p{font-size:18px;max-width:850px}a{color:#145d75;text-underline-offset:4px;overflow-wrap:anywhere}figure{margin:36px 0;padding:26px;background:#fff;border:1px solid #d5ded8;border-radius:14px}figcaption{font-size:22px;font-weight:700;line-height:1.5}small{display:block;color:#64746b;font-size:13px;font-weight:400}.flow{display:flex;align-items:stretch;gap:13px;margin-top:24px}.flow div{flex:1;background:#e8f1ea;padding:20px;border-radius:8px}.flow b{color:#64746b;font-size:14px}.flow strong{display:block;font-size:23px;margin:8px 0}.flow span{font-size:15px}.flow i{align-self:center;font-size:26px}.compare{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:22px}.compare section{padding:18px;background:#f7f6ee;border-top:4px solid #bf934c}.compare h3{margin:0 0 12px;font-size:22px}.compare p,figure>p{font-size:15px}.compare em{font-style:normal;font-size:14px;color:#805528}details{margin-top:40px;border-top:1px solid #b9c8bf;padding-top:22px}summary{cursor:pointer;font-weight:700}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px}footer{margin-top:40px;font-size:14px;color:#64746b}@media(max-width:650px){main{padding:24px 18px}.flow{flex-direction:column}.flow i{transform:rotate(90deg)}.compare{grid-template-columns:1fr}figure{padding:18px}h2{font-size:23px}p{font-size:17px}}@media print{body{background:white}main{padding:0}figure{break-inside:avoid}details{display:none}}'''
src=p.joinpath('sources.md').read_text()
result='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>炸油该不该换：先买可信的测量，再考虑 AI 视觉</title><style>'+css+'</style><main><header>餐饮经营研究 · 2026 / 11 / 08<br>测量边界 × 小店采购</header><article>'+body+'</article><details><summary>原文 Markdown</summary><pre>'+html.escape(md)+'</pre></details><details><summary>来源台账与研究边界</summary><pre>'+html.escape(src)+'</pre></details><footer>独立附件读本。完整正文与来源保留；两图均为作者定性分析。未宣称同步既有站点。</footer></main></html>'
p.joinpath('oil-quality.html').write_text(result)
print(json.dumps({'html_bytes':len(result.encode()),'sha256':hashlib.sha256(result.encode()).hexdigest(),'figures':result.count('<figure>'),'article_present':all(html.escape(t) in result for t in ['酸价','极性组分','研究说明'])},ensure_ascii=False))
