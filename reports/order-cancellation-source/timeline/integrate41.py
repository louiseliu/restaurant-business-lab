"""Add reviewed cancellation article to the preserved complete 40-article portal."""
import json,hashlib,shutil,sys
from pathlib import Path
S=Path(sys.argv[1]); A=Path(sys.argv[2]); R=S/'content/report'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json')
assert len(a['articles'])==60 and len(s)==40
n=read(A/'order-cancellation/article-entry.json');st=read(A/'order-cancellation/illustrated-story.json');q=read(A/'order-cancellation/article-reviewed-data.json')['queries']
assert n['id'] not in s and not set(q)&set(d['queries'])
assert hashlib.sha256(n['body'].encode()).hexdigest()=='2ee3e6e5d9034614a32160bfa992d3186860fa2e153164af023273fbc4a7844b'
p=R/'IllustratedArticle.jsx';t=p.read_text();assert 'CancellationDiagram' not in t
needle="import React from 'react';";assert t.count(needle)==1;t=t.replace(needle,needle+"\nimport {CancellationDiagram} from './CancellationDiagrams.jsx';")
needle='const diagramRows=reviewedRows(diagramId);';assert t.count(needle)==1;t=t.replace(needle,needle+"\n if(diagram.layout?.startsWith('cancellation-'))return <CancellationDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
a['articles'].append(n);a['articles'].sort(key=lambda x:x['publishedAt'],reverse=True);a['sourceCommit']=n['firstGit'];a['syncNote']='本地待同步41篇图文；未发布站点。';s[n['id']]=st;d['queries'].update(q);d['buildStatus']='complete';d['generatedAt']=n['publishedAt'];d['exportPreferences']={'selected':None,'destinations':[]}
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d);p.write_text(t)
for name in ['CancellationDiagrams.jsx','cancellation-diagrams.css']:shutil.copyfile(A/name,R/name)
print('Added cancellation article and two scoped queries; original portal preserved.')
