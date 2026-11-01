import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'inventory-capture';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-11-01-inventory-capture-note'
assert a['publishedAt']==a['updatedAt']=='2026-11-01T13:03:33Z'
assert a['firstGit']=='7754605220237525f8e76c522d747b2ade7efe41' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='29aa64782031c793bd810c132923e03e5d04f0acf53d7889ad7feacbdfb47203'
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==len(s['secondDiagram']['nodes'])==4
assert '非实测时长' in s['diagram']['scope'] and '不是餐链全品类' in s['secondDiagram']['scope']
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed frozen full body, firstGit/time, two non-conflated mechanism diagrams, query/source binding and privacy')
