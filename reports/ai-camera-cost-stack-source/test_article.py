import json,hashlib,re,sys,base64,zipfile,io
from pathlib import Path
p=Path(__file__).parent/'ai-camera-cost-stack';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-11-02-ai-camera-cost-stack-note'
assert a['publishedAt']==a['updatedAt']=='2026-11-02T13:20:53Z'
assert a['firstGit']=='2adfee7edeb9b6598c38560de8d5bedfee0364f7' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='63c1ca019f25d1f4de88638b444569381e920860e1283ef29e38ef0baf8432b0'
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==3 and len(s['secondDiagram']['nodes'])==3
reconstructed='# '+s['headline']+'\n\n'+s['lead']+'\n\n'+'\n\n'.join('## '+x['title']+'\n\n'+x['body'] for x in s['sections'])+'\n'
assert reconstructed.strip()==a['body'].strip()
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
 compiled=[]
 for m in re.finditer(r'"(?:[^"\\]|\\.)*"',h):
  try: v=json.loads(m.group())
  except: continue
  if isinstance(v,str) and 'originalBodySha256' in v:
   try: compiled.append(json.loads(v))
   except: pass
 assert len(compiled)==1 and compiled[0]['articles']==[a], 'HTML must contain exactly this frozen article, not an old portal'
 assert 'catalog.articles[0]' in (Path(sys.argv[1]).parents[2]/'src/content/report/ReportContent.jsx').read_text(), 'Default route must be standalone article'
print('Passed frozen full body + complete illustrated prose, firstGit/time, two mechanism diagrams, query/source binding and privacy')
