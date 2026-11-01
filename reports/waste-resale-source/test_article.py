import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'waste-resale';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-11-01-waste-resale-note'
assert a['publishedAt']==a['updatedAt']=='2026-11-01T10:03:53Z'
assert a['firstGit']=='186b8649f9776380ea16ecb88f9d6f590c0b4547' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='45f1faa4011757c784156f976551bbfa8348f42a0aee22f9117b994f6fd385d8'
assert a['topics']==['business-model']
assert len(s['diagram']['nodes'])==len(s['secondDiagram']['nodes'])==2
assert '不是酵墅实际' in s['diagram']['scope'] and '不宣称具名品牌' in s['secondDiagram']['scope']
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed frozen full body, firstGit/time, two non-conflated mechanism diagrams, query/source binding and privacy')
