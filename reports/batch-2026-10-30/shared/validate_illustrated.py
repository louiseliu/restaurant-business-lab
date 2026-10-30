"""Check complete illustrated research coverage before build; no network or writes."""
import json,re,sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1]);index=json.loads((root/'articles.json').read_text());stories=json.loads((root/'illustrated-stories.json').read_text());ids={x['id'] for x in index['articles']}
for a in index['articles']:
 assert a['body'] and a['sourceUrl'],a['id']
 for link in re.findall(r'\]\(#read/([^)]*)\)',a['body']):assert link in ids|{'illustrated-report'},link
 if a['section']!='research':continue
 s=stories[a['id']]
 for k in ['lead','findings','diagram','meaning','unknowns','actions']:assert s[k],(a['id'],k)
 assert 'secondDiagram' in s or 'numericChart' in s,(a['id'],'needs second useful graphic')
 for key in ['diagram','secondDiagram']:
  if key in s:
   d=s[key];assert d['label'] and d['scope'] and len(d['nodes'])>=2
 if 'numericChart' in s:
  d=s['numericChart'];assert d['title'] and d['unit'] and d['note'] and d['rows']
  for r in d['rows']:
   assert isinstance(r['value'],(int,float))
   if d['type']=='interval':assert r['low']<=r['value']<=r['high']
assert index['articles']==sorted(index['articles'],key=lambda x:(x['publishedAt'],x['id']),reverse=True)
print(json.dumps({'documents':len(index['articles']),'illustratedResearch':len(stories),'coverage':'complete','articleLinks':'resolved','order':'descending-first-commit'}))
