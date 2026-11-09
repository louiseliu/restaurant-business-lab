from pathlib import Path
import html,re,json,hashlib
p=Path(__file__).parent
md=p.joinpath("note.md").read_text(encoding="utf-8")
src=p.joinpath("sources.md").read_text(encoding="utf-8")
def render(s):
 out=[]
 for b in s.split("\n\n"):
  if b.startswith("<!--"): out.append(b); continue
  tag="h1" if b.startswith("# ") else "h2" if b.startswith("## ") else "p"
  if tag=="h1": b=b[2:]
  if tag=="h2": b=b[3:]
  out.append("<"+tag+">"+html.escape(b).replace("\n","<br>")+"</"+tag+">")
 return "\n".join(out)
fig1='<figure><figcaption>图 1 · 少抽一次车，先经过四道门<small>作者机制示意，不是实际流程数据</small></figcaption><div class="grid"><section>规则允许<br><b>不是自动获准延期</b></section><section>测量适用<br><b>不是只看总液位</b></section><section>费用可避免<br><b>不是所有包年都少收费</b></section><section>工作被承接<br><b>不是让店长追每个报警</b></section></div><p>任一环节缺失，都不能把减少次数直接记成已实现收益。</p></figure>'
fig2='<figure><figcaption>图 2 · 付款方式改变双方动机<small>作者风险示意，并非对具名服务商的事实指控</small></figcaption><div class="grid two"><section><h3>按次付费</h3><p>餐厅可能希望减少不必要清掏；服务方收入却可能随次数下降。</p><b>要查：测量与调整依据能否共同核对。</b></section><section><h3>按年包干</h3><p>费用更可预测；服务方也可能有少做必要作业的动机。</p><b>要查：必要维护、异常响应与完成记录。</b></section></div><p>两种合同都需要可验证的服务，不能单纯奖励次数越少越好。</p></figure>'
body=render(md).replace("<!-- FIGURE_1 -->",fig1).replace("<!-- FIGURE_2 -->",fig2)
css='*{box-sizing:border-box}body{margin:0;background:#f5f2e9;color:#20372f;font:18px/1.9 system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:40px 24px}header{border-top:6px solid #22634f;padding-top:18px;font-size:14px}h1{font-size:clamp(28px,4vw,42px);line-height:1.4}h2{margin-top:42px;border-left:5px solid #b98c47;padding-left:16px;font-size:26px}p{overflow-wrap:anywhere}figure{margin:32px 0;padding:24px;background:white;border:1px solid #cbd7cf;border-radius:12px}figcaption{font-size:23px;font-weight:bold}small{display:block;font-size:14px;font-weight:normal;color:#5e7067}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:22px}.grid.two{grid-template-columns:repeat(2,1fr)}section{background:#eaf2eb;padding:18px;font-size:16px}section b{display:block}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px}details{margin-top:28px}summary{cursor:pointer}footer{font-size:14px;color:#5e7067;margin-top:40px}@media(max-width:650px){.grid,.grid.two{grid-template-columns:1fr}main{padding:24px 16px}figure{padding:16px}}@media print{body{background:white}figure{break-inside:avoid}}'
result='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>隔油池能少抽两次，为什么老板仍可能不该买监测系统？</title><style>'+css+'</style></head><body><main><header>餐饮经营研究 · 2026 / 11 / 09<br>服务商业模式 × 安全维护</header><article>'+body+'</article><details><summary>原文 Markdown</summary><pre>'+html.escape(md)+'</pre></details><details><summary>来源台账与研究边界</summary><pre>'+html.escape(src)+'</pre></details><footer>独立图文读本。两图为作者示意。本文不是 AI 效果证明，也不代表既有站点已同步。</footer></main></body></html>'
assert result.count("<figure>")==2
assert all(x in result for x in ["研究说明","−200","Portland","1,086"])
assert not re.search(r"chatgpt[.]com/(?:c/|g/)|sk-[A-Za-z0-9]{20}",result)
out=p/"grease-interceptor-service.html"
out.write_text(result,encoding="utf-8")
print(json.dumps({"bytes":len(result.encode()),"sha256":hashlib.sha256(result.encode()).hexdigest(),"figures":2},ensure_ascii=False))
