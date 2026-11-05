"""Generate frozen narrative and reviewed conceptual diagrams, without remote writes."""
from pathlib import Path
import hashlib,json,re,sys
A=Path(__file__).resolve().parent;body=Path(sys.argv[1]).read_text();meta=json.loads(Path(sys.argv[2]).read_text());ID='research-2026-11-05-satellite-store-note';P='research/2026-11-05-satellite-store/note.md';U=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['commit']}/{P}"
assert hashlib.sha256(body.encode()).hexdigest()==meta['sha256']
def write(n,v):(A/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:];lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1);sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=[]
for label,url in re.findall(r'\[([^\]]+)\]\((https://[^\s)]+)\)',body):
 if url not in {s['url'] for s in sources}:sources.append({'title':label,'url':url})
config=json.loads((A/'reviewed-illustration-copy.json').read_text());dg=config.pop('diagram');second=config.pop('secondDiagram')
story={'id':ID,'headline':title,'lead':lead,**config,'diagram':dg,'secondDiagram':second,'sections':sections,'sources':sources}
entry={'id':ID,'path':P,'title':title,'section':'research','topics':['business-model'],'publishedAt':meta['time'],'updatedAt':meta['time'],'excerpt':'小面积卫星店需要怎样的菜单与补货配合？从公开案例拆解SKU、存储和配送的经营取舍。','body':body,'originalBodySha256':meta['sha256'],'sourceUrl':U,'firstGit':meta['commit']}
queries={}
for diagram,suffix in [(dg,''),(second,':second')]:
 q='diagram-'+ID+suffix;queries[q]={'rows':diagram['nodes'],'source':{'label':diagram['label'],'files':[P],'metricDefinitions':[{'label':'空间、菜单与补货的条件比较','definition':diagram['scope']+' '+diagram['note'],'componentIds':[q]}],'evidenceFlow':[{'title':'作者机制分析，案例事实边界见固定正文','detail':U}]+[{'title':s['title'],'detail':s['url']} for s in sources],'caveats':[diagram['completion'],diagram['note']]}}
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',{'surface':'report','title':title,'generatedAt':meta['time'],'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries})
print(meta['sha256'],len(sections),'complete sections; two original diagrams')
