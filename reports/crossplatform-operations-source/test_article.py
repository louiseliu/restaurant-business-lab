import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'crossplatform-operations';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-11-01-crossplatform-operations-note'
assert a['publishedAt']==a['updatedAt']=='2026-11-01T03:58:29Z'
assert a['firstGit']=='7eb8843d5019f3d6c35e7e02d9b27859f16f354e' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='cb2ba9e90b2130613125caeedb221d1e096f38b8d3b2c0990eeb325a2140ffc0'
assert a['topics']==['business-model']
assert len(s['diagram']['nodes'])==2 and len(s['secondDiagram']['nodes'])==4
assert '非完整架构' in s['diagram']['scope'] and '不是实际门店分类' in s['secondDiagram']['scope']
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_|turn[0-9]+(?:search|view|fetch)'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed frozen full body, firstGit/time, two non-conflated mechanism diagrams, query/source binding and privacy')
