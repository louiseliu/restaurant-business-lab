from pathlib import Path
import re, html, json, hashlib
ROOT=Path(__file__).resolve().parent
svg_head='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 610" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">{desc}</desc><style>text{{font-family:system-ui,'Noto Sans CJK SC',sans-serif;fill:#203d38}}.head{{font-size:27px;font-weight:700}}.label{{font-size:23px;font-weight:650}}.body{{font-size:21px}}.small{{font-size:19px;fill:#4c655f}}.fine{{font-size:17px;fill:#4c655f}}</style><rect width="960" height="610" fill="#ffffff" rx="12"/>'''
def text(x,y,s,cls='body',anchor=None):
 return f'<text x="{x}" y="{y}" class="{cls}"'+(f' text-anchor="{anchor}"' if anchor else '')+'>'+html.escape(s)+'</text>'
def box(x,y,w,h,fill,rx=9): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" rx="{rx}"/>'
s=svg_head.format(title='等待落在谁身上',desc='三个假设场景保持餐品备妥时刻相同。骑手早到会等餐，接近备妥时到店会缩短骑手等待，更晚到可能延迟取走并增加餐品等待。图不按分钟比例绘制。')
s+=text(34,47,'图1  同样的备妥时刻 不同的等待','head')+text(34,80,'作者假设场景 · 无分钟刻度 · 不是平台实测','small')
s+='<line x1="625" y1="112" x2="625" y2="498" stroke="#8aa49b" stroke-dasharray="8 6"/>'
s+=text(625,110,'餐品备妥','label','middle')
rows=[(142,'早到',275,700,'取走时间未必更早'),(267,'接近备妥时到',535,700,'匹配改善 厨房产能不一定变'),(392,'晚到',835,900,'骑手少等 餐可能更晚离店')]
for y,title,arrival,pickup,note in rows:
 s+=text(34,y+22,title,'label')+f'<line x1="260" y1="{y+43}" x2="925" y2="{y+43}" stroke="#b9c6c0" stroke-width="3"/>'
 s+=box(arrival,y+24,pickup-arrival,21,'#ecd7ab',3)
 s+=box(625,y+50,pickup-625,16,'#b7d9d1',3)
 s+=f'<circle cx="{arrival}" cy="{y+43}" r="7" fill="#1d5e52"/>'
 s+=f'<path d="M{pickup} {y+34} l9 9 l-9 9 l-9 -9 Z" fill="#173b34"/>'
 s+=text(arrival,y+89,'骑手到取餐点','fine','middle')+text(34,y+113,note,'small')
s+=box(34,549,28,16,'#ecd7ab',3)+text(73,564,'骑手等待','small')+box(204,549,28,16,'#b7d9d1',3)+text(243,564,'餐品等待','small')
s+=text(401,564,'● 到取餐点    ◆ 实际取走','small')
s+=text(34,597,'三种假设场景均保持备妥时刻相同；色带长度只表示关系 不代表分钟。','fine')+'</svg>'
(ROOT/'waiting-shift.svg').write_text(s)
s=svg_head.format(title='从哪段等待开始查',desc='接单至备妥拖长时查排队制作和打包；备妥至取走拖长时查上报、取餐点和交接；骑手到取餐点至取走拖长时先对照餐品是否已备妥。三段可能重叠，不能相加，不直接决定采购。')
s+=text(34,47,'图2  三段记录 指向不同的下一问','head')+text(34,80,'诊断顺序示意 · 多种问题可以同时存在','small')
for y,num,title,line1,line2 in [(116,'01','接单 → 真实备妥','开工前在排队 还是制作或打包卡住？','再查忙时工序、订单结构和人员部署。'),(256,'02','真实备妥 → 实际取走','信息晚报 取餐点难找 还是交接等待？','先查上报与交接 不直接增加厨房设备。'),(396,'03','骑手到取餐点 → 实际取走','餐是否已经备妥？等待发生在哪一侧？','对照前两段 再查人餐匹配与高峰积压。')]:
 s+=box(28,y,904,121,'#eff4ef')+text(49,y+43,num,'head')+text(108,y+43,title,'label')+text(108,y+79,line1,'body')+text(108,y+108,line2,'small')
s+=text(34,566,'三段不能相加；“接单至备妥”也不等于纯烹饪时间。','small')+'</svg>'
(ROOT/'decision-path.svg').write_text(s)

def inline(t):
 t=html.escape(t)
 t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
 t=re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)',r'<a href="\2">\1</a>',t)
 return t
note=(ROOT/'note.md').read_text(); sources=(ROOT/'sources.md').read_text()
blocks=[]
for block in note.strip().split('\n\n'):
 if block.startswith('# '): blocks.append('<h1>'+inline(block[2:])+'</h1>')
 elif block.startswith('## '): blocks.append('<h2>'+inline(block[3:])+'</h2>')
 elif block.startswith('!['):
  m=re.fullmatch(r'!\[(.*?)\]\((.*?)\)',block); caption,file=m.groups()
  svg=(ROOT/file).read_text(); slug=file.removesuffix('.svg')
  svg=svg.replace('id="title"',f'id="{slug}-title"').replace('id="desc"',f'id="{slug}-desc"').replace('aria-labelledby="title desc"',f'aria-labelledby="{slug}-title {slug}-desc"')
  blocks.append('<figure><div class="diagram" tabindex="0">'+svg+'</div><figcaption>'+html.escape(caption)+'</figcaption></figure>')
 else: blocks.append('<p>'+inline(block)+'</p>')
css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f4f1e9;color:#203d38;font-family:system-ui,"Noto Sans CJK SC",sans-serif;line-height:1.9}main{max-width:1040px;margin:auto;padding:38px 28px 80px}header{border-top:7px solid #215f53;padding-top:17px;letter-spacing:.08em;font-size:14px;color:#526c61}h1{font-size:clamp(30px,4.4vw,48px);line-height:1.35;margin:30px 0 18px;max-width:900px}h2{font-size:27px;line-height:1.5;margin:48px 0 18px;border-left:5px solid #bd8c3b;padding-left:16px}p{font-size:18px;max-width:870px;margin:19px 0}a{color:#156278;text-underline-offset:4px;overflow-wrap:anywhere}strong{font-weight:750;color:#153f35}figure{margin:34px 0;background:#fff;border:1px solid #d7dfd7;border-radius:14px;overflow:hidden}.diagram{overflow:auto;padding:10px}.diagram svg{display:block;width:100%;height:auto;min-width:620px}figcaption{padding:13px 22px 22px;font-size:15px;color:#52675d;line-height:1.7}details{border-top:1px solid #b4c5ba;margin-top:45px;padding-top:20px}summary{cursor:pointer;font-size:20px;font-weight:650}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:15px/1.85 system-ui,"Noto Sans CJK SC",sans-serif}footer{margin-top:40px;font-size:14px;color:#52675d}a:focus-visible,summary:focus-visible,.diagram:focus-visible{outline:3px solid #bd8c3b;outline-offset:5px}.scroll-hint{font-size:14px;color:#52675d}@media(max-width:650px){main{padding:25px 18px 60px}h2{font-size:23px;margin-top:36px}p{font-size:17px}figcaption{padding:12px 17px 20px}.diagram{padding:5px}.diagram svg{min-width:620px}}@media print{body{background:white}main{max-width:none;padding:0}h2{break-after:avoid}figure{break-inside:avoid}.diagram{overflow:visible}.diagram svg{min-width:0}details{display:none}}'''
page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="区分骑手等餐、餐品停留和门店备餐，用真实交接节点决定厨房预算。"><title>骑手等餐少了 后厨就真的更快了吗</title><style>'+css+'</style></head><body><main><header>餐饮商业研究院 · 中国餐饮 AI 实施<br>人餐匹配 × 厨房投入</header><article>'+''.join(blocks)+'</article><p class="scroll-hint">小屏可横向滑动图示。图示文字解释已包含在正文中。</p><details><summary>展开来源台账与研究边界</summary><pre>'+html.escape(sources)+'</pre></details><footer>独立图文读本 · 完整正文与两幅原创机制图 · 无外部脚本、字体或图片依赖<br>本文件为离线附件，不表示在线研究站点已更新。</footer></main></body></html>'
(ROOT/'骑手等待与厨房投入-完整图文.html').write_text(page)
print(json.dumps({'html_bytes':len(page.encode()),'note_bytes':len(note.encode()),'html_sha256':hashlib.sha256(page.encode()).hexdigest()},ensure_ascii=False))
