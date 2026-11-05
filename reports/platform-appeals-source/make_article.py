"""Generate frozen narrative and reviewed conceptual diagrams, without remote writes."""
from pathlib import Path
import hashlib,json,re,sys
A=Path(__file__).resolve().parent;body=Path(sys.argv[1]).read_text();meta=json.loads(Path(sys.argv[2]).read_text());ID='research-2026-11-05-platform-appeals-note';P='research/2026-11-05-platform-appeals/note.md';U=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['commit']}/{P}"
assert hashlib.sha256(body.encode()).hexdigest()==meta['sha256']
source_body=Path(sys.argv[1]).with_name('sources.md').read_text()
assert hashlib.sha256(source_body.encode()).hexdigest()==meta['sourcesSha256']
def write(n,v):(A/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:];lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1);sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=[]
for label,url in re.findall(r'\[([^\]]+)\]\((https://[^\s)]+)\)',body):
 if url not in {s['url'] for s in sources}:sources.append({'title':f'S{len(sources)+1} · {label}','url':url})
config=json.loads((A/'reviewed-illustration-copy.json').read_text());dg=config.pop('diagram');second=config.pop('secondDiagram')
story={'id':ID,'headline':title,'lead':lead,**config,'diagram':dg,'secondDiagram':second,'sections':sections,'sources':sources,'technicalDetails':[{'title':'公开来源与主张边界','body':source_body}]}
entry={'id':ID,'path':P,'title':title,'section':'research','topics':['ai'],'publishedAt':meta['time'],'updatedAt':meta['time'],'excerpt':'平台宣称可辅助识假。小店先核对能受理什么，再判断留证、检索和申诉投入。','body':body,'originalBodySha256':meta['sha256'],'sourceUrl':U,'firstGit':meta['commit']}
queries={}
for diagram,suffix in [(dg,''),(second,':second')]:
 scoped_sources=[s for s in sources if s['title'].split(' · ')[0] in diagram['sourceIds']]
 assert len(scoped_sources)==len(diagram['sourceIds'])
 q='diagram-'+ID+suffix;queries[q]={'rows':diagram['nodes'],'source':{'label':diagram['label'],'files':[P],'metricDefinitions':[{'label':'平台技术核查、门店事实责任与作者建议的边界','definition':diagram['scope']+' '+diagram['note'],'componentIds':[q]}],'evidenceFlow':[{'title':'作者机制分析，案例事实边界见固定正文','detail':U}]+[{'title':s['title'],'detail':s['url']} for s in scoped_sources],'caveats':[diagram['completion'],diagram['note']]}}
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',{'surface':'report','title':title,'generatedAt':meta['time'],'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries})
print(meta['sha256'],len(sections),'complete sections; two original diagrams')
