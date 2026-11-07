from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parent

def inline(s):
    s = escape(s)
    return re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)', r'<a href="\2" rel="noopener noreferrer">\1</a>', s)

def md(source):
    out=[]
    for block in source.strip().split('\n\n'):
        if block.startswith('<!-- FIGURE_'):
            out.append(block)
        elif block.startswith('# '):
            out.append('<h1>'+inline(block[2:])+'</h1>')
        elif block.startswith('## '):
            out.append('<h2>'+inline(block[3:])+'</h2>')
        else:
            out.append('<p>'+inline(block.replace('\n',' '))+'</p>')
    return '\n'.join(out)

fig1='''<figure aria-labelledby="fig1-title"><div class="figure-meta">图一 · 定性机制示意 · 非实测</div>
<h3 id="fig1-title">省下一次授权 可能多等一次上门</h3>
<div class="flow chain"><div class="node"><span>控制点</span><strong>上限低于合理处置所需</strong><small>并非所有低上限都有问题</small></div><div class="node"><span>等待点</span><strong>追加报价与审批</strong><small>无法及时获批时才形成瓶颈</small></div><div class="node"><span>恢复点</span><strong>延后维修或再次上门</strong><small>还受师傅与配件供给约束</small></div><div class="node"><span>经营结果</span><strong>停机损失可能增加</strong><small>看真正流失的贡献而非全店营业额</small></div></div>
<div class="balance"><div><h4>倾向减少等待</h4><p>关键设备无替代，范围与责任已清楚，授权确能提前恢复。</p></div><div><h4>倾向保留复核</h4><p>设备有冗余，报价不清，或保修与返修责任待确认。</p></div></div>
<figcaption>本文条件推演。箭头表示可能的传导路径，不表示必然因果、耗时或损失幅度。安全要求不因营业压力而降低。</figcaption></figure>'''

fig2='''<figure aria-labelledby="fig2-title"><div class="figure-meta">图二 · 原创层次示意 · 非实测</div>
<h3 id="fig2-title">先让记录闭合 再让 AI 辅助</h3>
<div class="layers"><div class="layer"><b>01</b><div><strong>可追溯的基础记录</strong><p>资产身份 · 保修归属 · 原工单 · 处理结果</p></div><span class="tag">事实底座</span></div><div class="connector">↓</div><div class="layer"><b>02</b><div><strong>稳定运行的普通流程</strong><p>报修 → 派工 → 回传 → 安全恢复确认</p></div><span class="tag">不必依赖 AI</span></div><div class="connector">↓</div><div class="layer ai"><b>03</b><div><strong>可检验的 AI 辅助</strong><p>识别、摘要与异常提示，减少翻找和遗漏</p></div><span class="tag">先验证增量</span></div><div class="connector">↓</div><div class="layer"><b>04</b><div><strong>有边界的人工决定</strong><p>核对责任、审批例外、确认资产与修换选择</p></div><span class="tag">不交出责任</span></div></div>
<figcaption>根据本文分析归纳，不是 ServiceChannel 产品架构。普通流程的收益不能直接归到 AI 名下。</figcaption></figure>'''

css='''
:root{--ink:#17262c;--muted:#5a686b;--teal:#11635c;--paper:#f6f4ef;--line:#cbd5d3;--warm:#f3e8dc}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:"Noto Sans CJK SC","Microsoft YaHei","PingFang SC",sans-serif;line-height:1.95;-webkit-font-smoothing:antialiased}main{max-width:1040px;margin:0 auto;padding:64px 70px 72px;background:#fff}.eyebrow{font-size:13px;letter-spacing:.18em;color:var(--teal);font-weight:700;margin:0 0 20px}h1{font-size:clamp(30px,4.2vw,46px);line-height:1.35;letter-spacing:-.03em;margin:0 0 18px;color:#111}h2{font-size:25px;line-height:1.5;margin:49px 0 18px;color:#111}p{font-size:17px;margin:0 0 20px;overflow-wrap:anywhere}article>p:first-of-type{font-size:13px;color:var(--muted);margin-bottom:30px}article>p:nth-of-type(2){font-size:19px;line-height:1.9}a{color:var(--teal);text-decoration-thickness:1px;text-underline-offset:4px}figure{margin:38px -28px;padding:30px;background:#f2f6f4;border-radius:3px}.figure-meta{font-size:12px;letter-spacing:.1em;color:var(--teal);font-weight:700}h3{font-size:24px;line-height:1.5;margin:8px 0 24px;color:#111}h4{font-size:16px;line-height:1.5;margin:0 0 7px}.flow{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}.node{position:relative;padding:18px 15px;background:#fff;border-top:3px solid var(--teal);min-width:0}.node:not(:last-child):after{content:"→";position:absolute;right:-21px;top:43%;color:var(--teal);font-size:19px}.node span{display:block;font-size:11px;color:var(--teal);letter-spacing:.1em;margin-bottom:8px}.node strong{display:block;font-size:17px;line-height:1.6}.node small{display:block;font-size:12px;color:var(--muted);line-height:1.8;margin-top:9px}.balance{display:grid;grid-template-columns:1fr 1fr;margin-top:22px;gap:24px}.balance>div{padding-top:14px;border-top:1px solid var(--line)}.balance p{font-size:14px;margin:0;line-height:1.8}figcaption{font-size:12px;color:var(--muted);line-height:1.8;margin-top:22px}.layers{max-width:720px;margin:auto}.layer{display:grid;grid-template-columns:36px 1fr auto;gap:17px;align-items:center;background:#fff;padding:18px 20px;border:1px solid var(--line)}.layer b{font-size:24px;color:#6d8983;font-weight:400}.layer strong{font-size:18px}.layer p{font-size:14px;color:var(--muted);margin:3px 0 0;line-height:1.6}.tag{font-size:11px;white-space:nowrap;border:1px solid var(--line);padding:3px 7px;color:var(--muted)}.ai{background:var(--warm);border-color:#ddc9b6}.connector{color:var(--teal);line-height:1.3;text-align:center;font-size:21px;margin:2px 0}.sources{margin-top:55px;padding-top:24px;border-top:1px solid var(--line)}.sources h2{font-size:19px;margin:26px 0 10px}.sources p{font-size:14px;line-height:1.85}.sources>h2:first-child{font-size:25px;margin-top:0}.footer{color:var(--muted);font-size:12px;margin-top:30px}
@media(max-width:700px){main{padding:32px 23px 45px}h1{font-size:32px}h2{font-size:23px;margin-top:36px}p{font-size:16px}article>p:nth-of-type(2){font-size:18px}figure{margin:28px -7px;padding:22px 17px}h3{font-size:22px}.flow{grid-template-columns:1fr;gap:23px}.node{padding:13px 17px;display:grid;grid-template-columns:54px 1fr;column-gap:9px}.node span{margin:0;grid-row:span 2;align-self:center}.node strong{font-size:17px}.node small{margin-top:4px;grid-column:2}.node:not(:last-child):after{content:"↓";right:calc(50% - 7px);top:auto;bottom:-25px}.balance{grid-template-columns:1fr;gap:15px}.layer{grid-template-columns:25px 1fr;gap:10px;padding:15px 12px}.layer b{font-size:20px}.layer strong{font-size:16px}.layer p{font-size:13px}.tag{grid-column:2;justify-self:start}.sources{margin-top:35px}}
@media print{body{background:#fff}main{padding:0;max-width:none}figure{break-inside:avoid;margin:24px 0}h2,h3{break-after:avoid}p{widows:3;orphans:3}a{color:#111}.sources{break-before:page}}
'''

article=md((ROOT/'note.md').read_text()).replace('<!-- FIGURE_1 -->',fig1).replace('<!-- FIGURE_2 -->',fig2)
source=md((ROOT/'sources.md').read_text()).replace('<h1>','<h2>',1).replace('</h1>','</h2>',1)
html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="餐厅维修授权上限、停机损失、普通工单流程与AI的边界。含Razzoo’s和Silver Diner案例分析及两幅原创定性图。"><title>餐厅维修支出上限为何可能拖慢恢复</title><style>'''+css+'''</style></head><body><main><div class="eyebrow">餐饮经营研究 / 设备与维修</div><article>'''+article+'''</article><section class="sources" aria-label="来源与证据边界">'''+source+'''</section><p class="footer">公开资料研究 · 2026年11月7日 · 两幅图为原创示意，不含实测数值</p></main></body></html>'''
(ROOT/'report.html').write_text(html,encoding='utf-8')
print(f'Built report.html: {len(html.encode())} bytes')
