"""Make a separate public-safe authored export. Never edit original/private files."""
import argparse,json,re,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('destination');a=p.parse_args();src=Path(a.source);dst=Path(a.destination);dst.mkdir(parents=True,exist_ok=False)
private_url=r'https?://(?:www\.)?chatgpt\.com/(?:g/[^\s)<>"\x27`]+|c/[^\s)<>"\x27`]+|share/[^\s)<>"\x27`]+)'
def safe(t):
 t=re.sub(r'\[([^\]]+)\]\(('+private_url+r')\)',lambda m:m[1]+'（私人协作会话，未公开）',t)
 return re.sub(private_url,'私人协作会话，未公开',t)
def structured(x):
 if isinstance(x,str):return safe(x)
 if isinstance(x,list):return [structured(v) for v in x]
 if isinstance(x,dict):return {k:structured(v) for k,v in x.items()}
 return x
for name in ['ReportContent.jsx','LegacyReport.jsx','IllustratedArticle.jsx','report.css','timeline.css','illustrated.css','articles.json','illustrated-stories.json']:
 f=src/'src/content/report'/name
 if f.exists(): (dst/name).write_text(json.dumps(structured(json.loads(f.read_text())),ensure_ascii=False,indent=2) if f.suffix=='.json' else safe(f.read_text()))
public_data=structured(json.loads((src/'src/data.json').read_text()));public_data['id']='report:public-restaurant-research'
(dst/'reviewed-data.json').write_text(json.dumps(public_data,ensure_ascii=False,indent=2))
for tool in ['generate_index.py','validate_illustrated.py','sync_illustrated_queries.py','sanitize_public.py']:
 shutil.copyfile(src/'src/content/report/timeline-tools'/tool,dst/tool)
for f in dst.iterdir():
 if f.is_file():
  t=f.read_text();assert not re.search(private_url,t),f
  if f.suffix!='.py':assert 'git.chatgpt-team.site' not in t and '/workspace/' not in t and 'appgprj_' not in t,f
print('Public authored export sanitized; private project/conversation/share URLs removed.')
