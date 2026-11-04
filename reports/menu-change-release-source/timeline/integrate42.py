"""Add reviewed menu change article to the preserved complete 41-article portal."""
import json,hashlib,shutil,sys
from pathlib import Path
S=Path(sys.argv[1]); A=Path(sys.argv[2]); R=S/'content/report'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json')
assert len(a['articles'])==61 and len(s)==41
n=read(A/'article-entry.json');st=read(A/'illustrated-story.json');q=read(A/'article-reviewed-data.json')['queries']
assert n['id'] not in s and not set(q)&set(d['queries'])
assert hashlib.sha256(n['body'].encode()).hexdigest()=='fe7cf3baeca717e24bf87239c0911b63dbfbd30f6010d8f7c7f7751a7d09a6c0'
p=R/'IllustratedArticle.jsx';t=p.read_text();assert 'MenuDiagram' not in t
needle="import React from 'react';";assert t.count(needle)==1;t=t.replace(needle,needle+"\nimport {MenuDiagram} from './MenuDiagrams.jsx';")
needle='const diagramRows=reviewedRows(diagramId);';assert t.count(needle)==1;t=t.replace(needle,needle+"\n if(diagram.layout?.startsWith('menu-'))return <MenuDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
a['articles'].append(n);a['articles'].sort(key=lambda x:x['publishedAt'],reverse=True);a['sourceCommit']=n['firstGit'];a['syncNote']='本地待同步42篇图文；未发布站点。';s[n['id']]=st;d['queries'].update(q);d['buildStatus']='complete';d['generatedAt']=n['publishedAt'];d['exportPreferences']={'selected':None,'destinations':[]}
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d);p.write_text(t)
for name in ['MenuDiagrams.jsx','menu-diagrams.css']:shutil.copyfile(A/name,R/name)
print('Added menu change article and two scoped queries; original portal preserved.')

