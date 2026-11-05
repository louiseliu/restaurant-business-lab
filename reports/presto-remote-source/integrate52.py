"""Append one frozen illustrated article, refusing changed or conflicting baselines."""
import hashlib,json,shutil,sys
from pathlib import Path
S=Path(sys.argv[1]);A=Path(sys.argv[2]);R=S/'content/report';ID='research-2026-11-05-presto-remote-note'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json');n=read(A/'article-entry.json');st=read(A/'illustrated-story.json');q=read(A/'article-reviewed-data.json')['queries']
assert n['id']==ID and hashlib.sha256(n['body'].encode()).hexdigest()==n['originalBodySha256']
assert st['id']==ID and len(q)==2
for key,suffix in [('diagram',''),('secondDiagram',':second')]:assert q['diagram-'+ID+suffix]['rows']==st[key]['nodes']
assert (len(a['articles']),len(s),len(d['queries']))==(71,51,105),'Expected intact 51-story baseline'
research=[x for x in a['articles'] if x['section']=='research'];assert len(research)==51 and sum('ai' in x['topics'] for x in research)==33
assert ID not in s and ID not in [x['id'] for x in a['articles']] and not set(q)&set(d['queries'])
p=R/'IllustratedArticle.jsx';t=p.read_text();assert 'PrestoDiagram' not in t
needle="import React from 'react';";assert t.count(needle)==1;t=t.replace(needle,needle+"\nimport prestoSourcePreviews from './presto-remote-source-previews.json';\nimport {PrestoDiagram} from './PrestoDiagrams.jsx';")
needle='const diagramRows=reviewedRows(diagramId);';assert t.count(needle)==1;t=t.replace(needle,needle+"\n if(diagram.layout?.startsWith('presto-remote-'))return <PrestoDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
needle='sourcePreviews={';assert t.count(needle)==1;t=t.replace(needle,"sourcePreviews={id.includes('research-2026-11-05-presto-remote-note')?prestoSourcePreviews:")
a['articles'].append(n);a['articles'].sort(key=lambda x:(x['publishedAt'],x['id']),reverse=True);a['sourceCommit']=n['firstGit'];a['syncNote']='本地待同步52篇图文；未发布站点。';s[ID]=st;d['queries'].update(q);d['buildStatus']='updating';d['generatedAt']=n['publishedAt'];d['exportPreferences']={'selected':None,'destinations':[]}
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d);p.write_text(t)
for name in ['PrestoDiagrams.jsx','presto-remote-diagrams.css','presto-remote-source-previews.json']:shutil.copyfile(A/name,R/name)
print('Added one article and two queries, preserving all existing objects.')
