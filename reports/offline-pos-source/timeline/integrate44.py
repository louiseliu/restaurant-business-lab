"""Merge the reviewed offline article into a complete, preserved 43-story portal."""
import json,shutil,sys,hashlib
from pathlib import Path
S=Path(sys.argv[1]); A=Path(sys.argv[2]); R=S/'content/report'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json')
assert len(a['articles'])==63 and len(s)==43
n=read(A/'article-entry.json');st=read(A/'illustrated-story.json');q=read(A/'article-reviewed-data.json')['queries']
assert n['id'] not in s and not set(q)&set(d['queries'])
assert hashlib.sha256(n['body'].encode()).hexdigest()==n['originalBodySha256']
p=R/'IllustratedArticle.jsx';t=p.read_text();assert 'OfflineDiagram' not in t
needle="import React from 'react';";assert t.count(needle)==1;t=t.replace(needle,needle+"\nimport {OfflineDiagram} from './OfflineDiagrams.jsx';")
needle='const diagramRows=reviewedRows(diagramId);';assert t.count(needle)==1;t=t.replace(needle,needle+"\n if(diagram.layout?.startsWith('offline-'))return <OfflineDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
a['articles'].append(n);a['articles'].sort(key=lambda x:x['publishedAt'],reverse=True);a['sourceCommit']=n['firstGit'];a['syncNote']='本地待同步44篇图文；未发布站点。';s[n['id']]=st;d['queries'].update(q);d['buildStatus']='complete';d['generatedAt']=n['publishedAt'];d['exportPreferences']={'selected':None,'destinations':[]}
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d);p.write_text(t)
for name in ['OfflineDiagrams.jsx','offline-diagrams.css']:shutil.copyfile(A/name,R/name)
print('Added offline article and two scoped queries; previous portal preserved.')
