from pathlib import Path
from html.parser import HTMLParser
import re,json,xml.etree.ElementTree as ET,hashlib
class Reader(HTMLParser):
 def __init__(self):
  super().__init__();self.elements=[];self.in_article=False;self.article=[];self.caption=False;self.captions=[]
 def handle_starttag(self,tag,attrs):
  self.elements.append((tag,dict(attrs)))
  if tag=='article':self.in_article=True
  if tag=='figcaption':self.caption=True;self.captions.append('')
 def handle_endtag(self,tag):
  if tag=='article':self.in_article=False
  if tag=='figcaption':self.caption=False
 def handle_data(self,data):
  if self.in_article:self.article.append(data)
  if self.caption:self.captions[-1]+=data
P=Path(__file__).parent
md=(P/'note.md').read_text();raw=(P/'report.html').read_text();r=Reader();r.feed(raw)
elems=r.elements
alltag=lambda name:[attrs for tag,attrs in elems if tag==name]
checks={}
checks['lang_zh_CN']=alltag('html')[0].get('lang')=='zh-CN'
checks['viewport']=any(e.get('name')=='viewport' for e in alltag('meta'))
checks['one_h1']=len(alltag('h1'))==1
checks['one_main']=len(alltag('main'))==1
checks['two_inline_svg']=len(alltag('svg'))==2
checks['two_captions']=len(r.captions)==2
checks['no_script']=not alltag('script')
checks['no_external_assets']=not any('src' in e or (t=='link' and 'href' in e) for t,e in elems) and 'url(http' not in raw and '@import' not in raw
svgs=[ET.fromstring((P/n).read_text()) for n in ['batch-workload.svg','batch-decision.svg']]
checks['svg_parse']=all(s.tag.endswith('svg') for s in svgs)
ns='{http://www.w3.org/2000/svg}'
checks['svg_accessibility']=all(s.get('aria-labelledby') and s.find(ns+'title') is not None and s.find(ns+'desc') is not None for s in svgs)
checks['qualitative_labels']=all('非实测' in c for c in r.captions)
ids=[e.get('id') for t,e in elems if 'id' in e]
checks['unique_ids']=len(ids)==len(set(ids))
links=[e.get('href','') for e in alltag('a')]
checks['internal_links_resolve']=all(l[1:] in ids for l in links if l.startswith('#'))
expected=['https://www.j-cast.com/2026/10/02518266.html?p=all','https://news.tv-asahi.co.jp/news_society/articles/900201165.html']
checks['exact_external_sources']=[l for l in links if l.startswith('http')]==expected
article=''.join(r.article);complete=[]
for p in md.strip().split('\n\n'):
 if p.startswith(('# ','餐饮商业研究院','![')): continue
 t=re.sub(r'^## ','',p);t=re.sub(r'\*\*(.*?)\*\*',r'\1',t);t=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',t);complete.append(t)
normalize=lambda s:re.sub(r'\s+','',s)
checks['all_markdown_paragraphs_in_html']=all(normalize(p) in normalize(article) for p in complete)
checks['body_length_2200_3000']=2200<=len(re.findall(r'[\u4e00-\u9fff]',md.split('## 来源与研究范围')[0]))<=3000
checks['no_private_paths_or_tokens']=not re.search(r'/tmp/|/workspace/|/home/|/user_notes/|sk-[A-Za-z0-9]{12}|ghp_|Bearer |BEGIN.*PRIVATE KEY|chatgpt.com/c/|chatgpt.com/g/',raw+md)
checks['no_unresolved_placeholders']=not re.search(r'__TITLE__|__META__|__BODY__|__NAV__|TODO|TBD',raw)
checks['responsive_css']='@media(max-width:480px)' in raw
checks={k:bool(v) for k,v in checks.items()}
result={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'body_cjk_chars':len(re.findall(r'[\u4e00-\u9fff]',md.split('## 来源与研究范围')[0])),'artifacts':{n:{'bytes':(P/n).stat().st_size,'sha256':hashlib.sha256((P/n).read_bytes()).hexdigest()} for n in ['note.md','report.html','batch-workload.svg','batch-decision.svg']}}
(P/'static-qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2));assert all(checks.values())
