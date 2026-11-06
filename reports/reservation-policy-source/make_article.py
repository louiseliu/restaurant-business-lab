"""Generate frozen narrative and reviewed conceptual diagrams, without remote writes."""
from pathlib import Path
import hashlib,json,re,sys
A=Path(__file__).resolve().parent;body=Path(sys.argv[1]).read_text();meta=json.loads(Path(sys.argv[2]).read_text());ID='research-2026-11-06-reservation-policy-note';P='research/2026-11-06-reservation-policy/note.md';U=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['commit']}/{P}"
assert re.fullmatch(r'[a-f0-9]{40}',meta['commit']), 'Require verified first commit'
assert re.fullmatch(r'2026-11-06T[0-9:]{8}Z',meta['time']), 'Require actual first commit timestamp'
assert meta.get('editorialFrozen') is True, 'Require editorial freeze'
assert meta.get('remoteReadbackVerified') is True, 'Require verified remote source'
assert hashlib.sha256(body.encode()).hexdigest()==meta['sha256']
source_body=Path(sys.argv[1]).with_name('sources.md').read_text()
assert hashlib.sha256(source_body.encode()).hexdigest()==meta['sourcesSha256']
def write(n,v):(A/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:];lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1);sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=json.loads((A/'reviewed-source-catalog.json').read_text());source_urls={s['url'] for s in sources}
assert set(re.findall(r'\]\((https://[^\s)]+)\)',body)).issubset(source_urls)
config=json.loads((A/'reviewed-illustration-copy.json').read_text())
story={'id':ID,'headline':title,'lead':lead,**config,'sections':sections,'sources':sources,'technicalDetails':[{'title':'首次研究台账，历史状态保留','body':source_body}]}
entry={'id':ID,'path':P,'title':title,'section':'research','topics':['ai','business'],'publishedAt':meta['time'],'updatedAt':meta['time'],'excerpt':'先看损失与补售，再比较订金、卡担保和普通确认；爽约率下降不等于净贡献改善','body':body,'originalBodySha256':meta['sha256'],'sourceUrl':U,'firstGit':meta['commit']}
queries={}
for name,suffix in [('diagram',''),('secondDiagram',':second'),('thirdDiagram',':third')]:
 diagram=config[name];scoped_sources=[s for s in sources if s['id'] in diagram['sourceIds']]
 assert {s['id'] for s in scoped_sources}==set(diagram['sourceIds'])
 q='diagram-'+ID+suffix;queries[q]={'rows':diagram['nodes'],'source':{'label':diagram['label'],'files':[P],'metricDefinitions':[{'label':diagram['label'],'definition':diagram['scope']+' '+diagram['note'],'componentIds':[q]}],'evidenceFlow':[{'title':'作者机制分析，案例事实边界见固定正文','detail':U}]+[{'title':s['title'],'detail':s['url']} for s in scoped_sources],'caveats':[diagram['completion'],diagram['note']]}}
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',{'surface':'report','title':title,'generatedAt':meta['time'],'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-06'},'queries':queries})
print(meta['sha256'],len(sections),'complete sections; three original diagrams')
