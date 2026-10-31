import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'review-to-action';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-31-review-to-action-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-31T00:01:07Z'
assert '/95ec37357d02ff957e86f36f720210b15c0feaeb/' in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='6b17fc115e3969ca1c2b37a9443b19824591a9063f0da6d20c26f7d7570c6543'
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==len(s['secondDiagram']['nodes'])==2
assert '假设示例' in s['diagram']['scope'] and '非真实顾客记录' in s['diagram']['scope']
assert '不是靓靓蒸虾或肥肥虾庄' in s['secondDiagram']['scope']
assert '食品安全反馈' in s['secondDiagram']['note']
assert len(d['queries'])==2 and d['buildStatus']=='complete'
for suffix,key in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[key]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pattern=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'): assert not re.search(pattern,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert 'data-app-local-thread' not in h;assert not re.search(pattern,h)
print('Passed exact frozen full-body/hash/firstGit, both schematic limits and query bindings, privacy')
