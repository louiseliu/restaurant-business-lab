"""Append two frozen articles after all input and destination checks. Never replace a reader."""
import hashlib,json,shutil,sys
from pathlib import Path
from reader_patch import patch_reader,IDS,NAMES
S,*INPUTS=[Path(v) for v in sys.argv[1:]];R=S/'content/report';T=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
assert len(INPUTS)==2
fprints=read(T/'input-fingerprints.json')
for folder,records in zip(INPUTS,fprints):
 for name,row in records.items():
  b=(folder/name).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'],'Frozen input changed: '+name
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json')
assert (len(a['articles']),len(s),len(d['queries']))==(85,65,134),'Unexpected baseline counts'
assert len({v['id'] for v in a['articles']})==85
assert all(ID not in s and all(v['id']!=ID for v in a['articles']) for ID in IDS)
assert d.get('id') and d.get('surface')=='report'
new=[];newStories={};newQueries={};copies=[]
for folder,ID,names in zip(INPUTS,IDS,NAMES):
 entry=read(folder/'article-entry.json');story=read(folder/'illustrated-story.json');queries=read(folder/'article-reviewed-data.json')['queries'];frozen=read(folder/'frozen.json')
 assert frozen['editorialFrozen'] and frozen['remoteReadbackVerified']
 assert entry['id']==story['id']==ID and entry['topics']==['ai']
 assert entry['firstGit']==frozen['commit'] and entry['publishedAt']==entry['updatedAt']==frozen['time']
 assert entry['originalBodySha256']==frozen['sha256']==sha(entry['body'].encode())==sha((folder/'note.md').read_bytes())
 assert frozen['sourcesSha256']==sha((folder/'sources.md').read_bytes())
 assert len(queries)==2 and not set(queries)&(set(d['queries'])|set(newQueries))
 for key,suffix in [('diagram',''),('secondDiagram',':second')]:
  q='diagram-'+ID+suffix
  assert queries[q]['rows']==story[key]['nodes'] and queries[q]['source']['metricDefinitions'][0]['componentIds']==[q]
 for name in names:
  assert (folder/name).is_file() and not (R/name).exists() and not (R/name).is_symlink(),'File conflict: '+name
  copies.append((folder/name,R/name))
 new.append(entry);newStories[ID]=story;newQueries.update(queries)
reader=patch_reader((R/'IllustratedArticle.jsx').read_text())
# No writes above. Existing objects, source baseline and unrelated runtime remain intact.
a['articles']+=new;a['articles'].sort(key=lambda x:(x['publishedAt'],x['id']),reverse=True)
a['sourceCommit']=new[-1]['firstGit'];a['syncNote']='本地67篇图文已合并；原站未同步。'
s.update(newStories);d['queries'].update(newQueries);d['buildStatus']='updating';d['generatedAt']=new[-1]['publishedAt']
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d);(R/'IllustratedArticle.jsx').write_text(reader)
for src,dst in copies:shutil.copyfile(src,dst)
print('Two articles and four queries appended; existing content preserved.')
