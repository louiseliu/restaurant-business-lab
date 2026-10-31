import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'energy-control';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-31-energy-control-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-31T20:07:57Z'
assert a['firstGit']=='c748b63ec97fae5b6fd93807a69dc793315f47b3' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='3168cd7820153dd4277daddc55624b69525364648756681cb3af6b41f6ec6de0'
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==3 and len(s['secondDiagram']['nodes'])==4
assert '不是优劣排名' in s['diagram']['scope'] and '无金额或回收期' in s['secondDiagram']['scope']
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_|turn[0-9]+(?:search|view|fetch)'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed frozen full body, firstGit/time, two non-conflated mechanism diagrams, query/source binding and privacy')
