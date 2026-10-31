import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'training-content-insourcing';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-31-training-content-insourcing-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-31T23:08:47Z'
assert a['firstGit']=='50fa8b488fd011045582a3e4a26f92af911153c7' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='295b0717b9cbc236c6840f3bcb28eceb1ddff55259e52e03358c55c3850a136d'
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==2 and len(s['secondDiagram']['nodes'])==4
assert '不是itsu全部实际流程' in s['diagram']['scope'] and '不是实测分界' in s['secondDiagram']['scope']
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_|turn[0-9]+(?:search|view|fetch)'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed frozen full body, firstGit/time, two non-conflated mechanism diagrams, query/source binding and privacy')
