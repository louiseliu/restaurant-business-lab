import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'pass-confirmation';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-11-02-pass-confirmation-note'
assert a['publishedAt']==a['updatedAt'] and a['publishedAt'].startswith('2026-11-02T')
assert len(a['firstGit'])==40 and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==2 and len(s['secondDiagram']['nodes'])==3
assert '研究者推论' in s['diagram']['note'] and '两条链不能画等号' in s['diagram']['scope']
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed frozen full body, firstGit/time, two diagrams, query/source binding and privacy')
