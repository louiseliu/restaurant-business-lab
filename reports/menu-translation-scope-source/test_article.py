import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'menu-translation-scope';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-31-menu-translation-scope-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-31T11:01:35Z'
assert a['firstGit']=='0a3ceaf0796e824d919723b4156ccfaef99a051f' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='18a7dbfd16d7e114d726f7c9f63cfb3a39d603dab691283fdc048f53ff0ac380'
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==2 and len(s['secondDiagram']['nodes'])==3
assert '不是同一套流程' in s['diagram']['scope'] and '研究院建议' in s['secondDiagram']['scope']
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed frozen full body, firstGit/time, two non-conflated mechanism diagrams, query/source binding and privacy')
