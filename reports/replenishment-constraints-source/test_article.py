import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'replenishment-constraints';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-31-replenishment-constraints-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-31T02:01:09Z'
assert '/3f54786dbaef70486ad6c67b2324c5f18921ca3f/' in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='aab3d3e2fe291ef5d7ee3ec3ae17f8f8aff109931a7041f0cbcfd2586094baee'
assert a['topics']==['business-model']
assert len(s['diagram']['nodes'])==3 and len(s['secondDiagram']['nodes'])==2
assert '非企业系统截图' in s['diagram']['scope'] and '不是海底捞与蜀海共同项目' in s['secondDiagram']['scope']
assert len(d['queries'])==2 and d['buildStatus']=='complete'
for suffix,key in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[key]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pattern=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'): assert not re.search(pattern,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert 'data-app-local-thread' not in h;assert not re.search(pattern,h)
print('Passed frozen full-body/hash/firstGit, two mechanism diagrams/query bindings, business-only category and privacy')
