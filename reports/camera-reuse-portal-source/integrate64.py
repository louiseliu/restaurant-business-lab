"""Append one frozen article only after complete preflight. No external writes."""
import hashlib,json,shutil,sys
from pathlib import Path
S=Path(sys.argv[1]); archives=[Path(v) for v in sys.argv[2:]];assert len(archives)==1
R=S/'content/report'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json')
assert (len(a['articles']),len(s),len(d['queries']))==(83,63,129)
p=R/'IllustratedArticle.jsx';t=p.read_text(); additions=[]
configs=[('camera-reuse','camera-reuse','CameraReuse','ai','eaf8d57c523197ca67a04662f5d48dc45a201c22','2026-11-06T01:10:58Z')]
for A,(slug,prefix,component,topic,commit,time) in zip(archives,configs):
 ID='research-2026-11-06-'+slug+'-note';n=read(A/'article-entry.json');st=read(A/'illustrated-story.json');q=read(A/'article-reviewed-data.json')['queries'];f=read(A/'frozen.json')
 assert n['id']==st['id']==ID and n['originalBodySha256']==f['sha256']==hashlib.sha256(n['body'].encode()).hexdigest()
 assert n['firstGit']==f['commit']==commit and commit in n['sourceUrl']
 assert n['publishedAt']==n['updatedAt']==f['time']==time and n['topics']==[topic]
 assert ID not in s and ID not in [x['id'] for x in a['articles']] and not set(q)&set(d['queries'])
 assert len(q)==2
 for key,suffix in [('diagram',''),('secondDiagram',':second')]:
  query='diagram-'+ID+suffix
  assert q[query]['rows']==st[key]['nodes'] and q[query]['source']['metricDefinitions'][0]['componentIds']==[query]
 names=[component+'Diagrams.jsx',prefix+'-diagrams.css',prefix+'-source-previews.json']
 for name in names:
  assert (A/name).is_file() and not (R/name).exists() and not (R/name).is_symlink(),'File conflict: '+name
  additions.append((A/name,R/name))
 assert component+'Diagram' not in t
 needle="import React from 'react';";assert t.count(needle)==1
 t=t.replace(needle,needle+f"\nimport {component}SourcePreviews from './{prefix}-source-previews.json';\nimport {{{component}Diagram}} from './{component}Diagrams.jsx';")
 needle='const diagramRows=reviewedRows(diagramId);';assert t.count(needle)==1
 t=t.replace(needle,needle+f"\n if(diagram.layout?.startsWith('{prefix}-'))return <{component}Diagram diagram={{diagram}} id={{id}} rows={{diagramRows}}/>;")
 assert t.count('sourcePreviews={')==1
 t=t.replace('sourcePreviews={',f"sourcePreviews={{id.includes('{ID}')?{component}SourcePreviews:")
 a['articles'].append(n);s[ID]=st;d['queries'].update(q)
a['articles'].sort(key=lambda x:(x['publishedAt'],x['id']),reverse=True);a['sourceCommit']=configs[-1][4];a['syncNote']='本地待同步64篇图文；未发布站点。';d['buildStatus']='updating';d['generatedAt']=configs[-1][5]
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d);p.write_text(t)
for src,dst in additions:shutil.copyfile(src,dst)
print('Merged one frozen article and two queries; existing objects preserved.')
