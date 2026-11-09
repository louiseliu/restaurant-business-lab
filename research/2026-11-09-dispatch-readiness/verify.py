from pathlib import Path
from lxml import etree, html
import re, json, hashlib
R=Path(__file__).resolve().parent
n=(R/'note.md').read_text(); s=(R/'sources.md').read_text(); f=R/'骑手等待与厨房投入-完整图文.html'; b=f.read_bytes(); h=html.fromstring(b)
checks={}
checks['language']=h.get('lang')=='zh-CN'
checks['title']=h.xpath('string(//h1)')==n.splitlines()[0][2:]
checks['headings']=h.xpath('//h2/text()')==[x[3:] for x in n.splitlines() if x.startswith('## ')]
checks['two_figures']=len(h.xpath('//figure'))==2
checks['source_ledger_complete']=h.xpath('string(//details/pre)')==s
checks['no_external_runtime']=not h.xpath('//script|//iframe|//img|//link|//form')
checks['unique_ids']=len(h.xpath('//@id'))==len(set(h.xpath('//@id')))
checks['links_https']=all(u.startswith('https://') for u in h.xpath('//a/@href'))
checks['svg_well_formed']=all(etree.fromstring((R/p).read_bytes()) is not None for p in ['waiting-shift.svg','decision-path.svg'])
checks['no_private_content']=not re.search(r'/workspace/|/home/|chatgpt\.com/c/|sk-[A-Za-z0-9]|token=',n+s+b.decode())
checks['overlap_warning']='三段不能相加' in n and '骑手等待可能与备妥前流程' in n
checks['independent_projects']='不同平台和项目' in n
checks['source_boundary']='预测更准' in n and '上线月份' in n
ps=[]
for block in n.strip().split('\n\n'):
 if not block.startswith(('#','![')):
  block=re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)',r'\1',block).replace('**','');ps.append(block)
checks['all_body_paragraphs_preserved']=ps==[p.text_content() for p in h.xpath('//article/p')]
checks['mobile_diagram_scroll_declared']='overflow:auto' in b.decode() and '小屏可横向滑动图示' in b.decode()
checks['no_fabricated_timing_scale']='无分钟刻度' in b.decode()
qa={'checks':checks,'all_passed':all(checks.values()),'verification':{'evidence':'Independent read-only review completed; overlap and purchase conditions revised.','figures':'Two original SVGs rendered with Inkscape and visually inspected.','html':'Structural and content checks only. Browser layout, scrolling, details interaction, and assistive technology not tested.','site':'No existing site access or publication attempted.','pro':'No new consultation.'},'files':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [R/'note.md',R/'sources.md',R/'waiting-shift.svg',R/'decision-path.svg',R/'build.py',R/'verify.py',f]}}
(R/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa,ensure_ascii=False,indent=2));assert qa['all_passed']
