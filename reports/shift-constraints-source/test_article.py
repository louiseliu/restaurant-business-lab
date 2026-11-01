import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'shift-constraints';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-11-01-shift-constraints-note'
assert a['publishedAt']==a['updatedAt']=='2026-11-01T14:03:18Z'
assert a['firstGit']=='daa2e94fd3780500f5d3a7e3291e1a3c1df86743' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='fc5729f4a4ca4bb5387d1b3f0b9393a0fad944ee8af0e7e921ba692257d3ec32'
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==3 and len(s['secondDiagram']['nodes'])==2
assert '未验证规则记忆' in s['diagram']['scope'] and '非收益测算' in s['secondDiagram']['scope']
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed frozen full body, firstGit/time, two non-conflated mechanism diagrams, query/source binding and privacy')
