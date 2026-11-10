"""Build a local-only, self-contained illustrated reader using stdlib only."""
from pathlib import Path
import hashlib, html, json, re

ROOT = Path(__file__).resolve().parent
LINK = re.compile(r'\[([^\]]+)\]\((https://[^\s)]+)\)')

def plain(text):
    return re.sub(r'https://[^\s)]+', lambda m: '<a href="'+m[0]+'" rel="noopener noreferrer">'+m[0]+'</a>', html.escape(text))

def inline(text):
    out, last = [], 0
    for m in LINK.finditer(text):
        out += [plain(text[last:m.start()]), '<a href="' + html.escape(m[2], quote=True) + '" rel="noopener noreferrer">' + html.escape(m[1]) + '</a>']
        last = m.end()
    out.append(plain(text[last:]))
    return ''.join(out)

def render(md, prefix):
    out, section, para = [], 0, []
    def flush():
        if para:
            out.append('<p>'+inline(' '.join(para))+'</p>')
            para.clear()
    for line in md.splitlines():
        if line.startswith('# '):
            flush(); out.append('<h1>'+inline(line[2:])+'</h1>' if prefix == 'article' else '<h2>'+inline(line[2:])+'</h2>')
        elif line.startswith('## '):
            flush()
            if prefix == 'article' and section in [1,3]:
                filename, caption = ({1: ('test-conditions.svg','两组毫米数对应不同条件。图示不表示性能排名，也不代表已实测达标。来源：买方技术方案第4页；第三层为作者建议。'), 3: ('inspection-workflow.svg','建议在隔离的受控验证中核对整条处置关系。图中各项为研究者建议，不是案例的现场操作规程。')}[section])
                out.append('<figure>'+ (ROOT/filename).read_text() + '<figcaption>'+caption+'</figcaption></figure>')
            section += 1; out.append(f'<h2 id="{prefix}-{section}">'+inline(line[3:])+'</h2>')
        elif line.startswith('- '):
            flush(); out.append('<p class="source-line">'+inline(line[2:])+'</p>')
        elif line.strip(): para.append(line)
        else: flush()
    flush()
    return '\n'.join(out)

note, sources = [(ROOT/f).read_text() for f in ['note.md','sources.md']]
nav=''.join(f'<a href="#article-{i+1}">{html.escape(t[3:])}</a>' for i,t in enumerate(x for x in note.splitlines() if x.startswith('## ')))
style='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f8f8f2;color:#23332d;font:18px/1.9 system-ui,-apple-system,"Noto Sans CJK SC","Microsoft YaHei",sans-serif}header,main,footer{max-width:900px;margin:auto;padding:28px}header{padding-top:44px;padding-bottom:0}.eyebrow{font-size:14px;letter-spacing:.12em;color:#547066}.meta{font-size:15px;color:#5a695f}h1{font-size:clamp(30px,5.5vw,45px);line-height:1.38;margin:18px 0 32px;font-weight:750;letter-spacing:-.025em}h2{font-size:25px;line-height:1.5;margin:54px 0 20px;scroll-margin-top:24px}p{margin:18px 0}a{color:#17674e;text-underline-offset:4px;overflow-wrap:anywhere}nav{display:flex;gap:10px 20px;flex-wrap:wrap;border-top:1px solid #cad5cb;border-bottom:1px solid #cad5cb;padding:18px 0;margin-top:22px;font-size:14px}figure{margin:34px 0 40px;display:flex;flex-direction:column;align-items:center}svg{display:block;width:min(100%,480px);height:auto}figcaption{font-size:15px;line-height:1.7;color:#53685a;max-width:620px;margin-top:16px}details{margin-top:46px;padding-top:20px;border-top:1px solid #cad5cb}summary{cursor:pointer;font-weight:650}details h2{font-size:22px;margin-top:28px}.source-line{font-size:15px;line-height:1.8;margin:10px 0}footer{font-size:14px;color:#5a695f;border-top:1px solid #cad5cb}a:focus-visible,summary:focus-visible{outline:3px solid #9f7318;outline-offset:5px}@media(max-width:550px){body{font-size:17px}header,main,footer{padding-left:20px;padding-right:20px}header{padding-top:28px}h2{font-size:23px}}@media(prefers-color-scheme:dark){body{background:#14241e;color:#e3eee5}.meta,.eyebrow,figcaption,footer{color:#b6c9bb}a{color:#9cdbb9}nav,details,footer{border-color:#486151}}@media print{body{background:#fff;color:#111;font-size:11pt}header,main,footer{max-width:none;padding:0}nav{display:none}h1{font-size:24pt}h2{font-size:17pt;break-after:avoid}figure{break-inside:avoid}svg{max-height:650px}a{color:#111}details{display:block}summary{display:none}details>*{display:block!important}}'''
doc='<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="以西南航食公开资料分析餐食AI异物检测的采购验收条件和证据边界"><title>餐食AI异物检测采购｜餐饮商业研究</title><style>'+style+'</style></head><body><header><div class="eyebrow">餐饮商业模式研究院 · 设备采购与AI实施</div><p class="meta">公开研究 · 2026年11月10日核验 · 独立离线图文</p><nav aria-label="文章目录">'+nav+'</nav></header><main><article>'+render(note,'article')+'</article><details><summary>查看完整来源台账与核验边界</summary>'+render(sources,'source')+'</details></main><footer>独立读本，不代表原站已同步。仅静态检查；浏览器视觉、交互和打印未验。文中建议不替代食安专业判断及适用合规要求。</footer></body></html>\n'
out=ROOT/'xray-acceptance.html'; out.write_text(doc)
print(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},ensure_ascii=False))
