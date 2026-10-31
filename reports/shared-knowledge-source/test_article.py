import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'shared-knowledge';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-31-shared-knowledge-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-31T22:00:27Z'
assert a['firstGit']=='85444d7728fc03777de996ddf837ed8a37e3dbf1' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='ba39a078b672e87b74501572c6661aecf83e5c78934ee8d67a0e99c22fed7c32'
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==len(s['secondDiagram']['nodes'])==2
assert '非真实餐企部署' in s['diagram']['scope'] and '不画成一套已经验证' in s['secondDiagram']['scope']
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_|turn[0-9]+(?:search|view|fetch)'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed frozen full body, firstGit/time, two non-conflated mechanism diagrams, query/source binding and privacy')
