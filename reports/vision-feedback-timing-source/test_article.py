import json,hashlib,re,sys,base64,zipfile,io
from pathlib import Path
p=Path(__file__).parent/'vision-feedback-timing';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-11-02-vision-feedback-timing-note'
assert a['publishedAt']==a['updatedAt']=='2026-11-02T09:29:26Z'
assert a['firstGit']=='cb1d36b11f6d6166cf6e0cbff81bca3fc96da65b' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='f5aa6bd4542c8a5bf9b8246d12d7dd5c9259cd2552de1628619d574a49779fb8'
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==2 and len(s['secondDiagram']['nodes'])==2
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
