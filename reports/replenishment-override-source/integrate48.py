"""Append one frozen illustrated article, refusing changed or conflicting baselines."""
import hashlib,json,shutil,sys
from pathlib import Path
S=Path(sys.argv[1]);A=Path(sys.argv[2]);R=S/'content/report';ID='research-2026-11-05-replenishment-override-note'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json');n=read(A/'article-entry.json');st=read(A/'illustrated-story.json');q=read(A/'article-reviewed-data.json')['queries']
assert n['id']==ID and hashlib.sha256(n['body'].encode()).hexdigest()==n['originalBodySha256']
assert st['id']==ID and len(q)==2
for key,suffix in [('diagram',''),('secondDiagram',':second')]:assert q['diagram-'+ID+suffix]['rows']==st[key]['nodes']
assert (len(a['articles']),len(s),len(d['queries']))==(67,47,97),'Expected intact 47-story baseline'
research=[x for x in a['articles'] if x['section']=='research'];assert len(research)==47 and sum('ai' in x['topics'] for x in research)==30
assert ID not in s and ID not in [x['id'] for x in a['articles']] and not set(q)&set(d['queries'])
p=R/'IllustratedArticle.jsx';t=p.read_text();assert 'OverrideDiagram' not in t
needle="import React from 'react';";assert t.count(needle)==1;t=t.replace(needle,needle+"\nimport overrideSourcePreviews from './override-source-previews.json';\nimport {OverrideDiagram} from './OverrideDiagrams.jsx';")
needle='const diagramRows=reviewedRows(diagramId);';assert t.count(needle)==1;t=t.replace(needle,needle+"\n if(diagram.layout?.startsWith('override-'))return <OverrideDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
needle='sourcePreviews={';assert t.count(needle)==1;t=t.replace(needle,"sourcePreviews={id.includes('research-2026-11-05-replenishment-override-note')?overrideSourcePreviews:")
a['articles'].append(n);a['articles'].sort(key=lambda x:(x['publishedAt'],x['id']),reverse=True);a['sourceCommit']=n['firstGit'];a['syncNote']='本地待同步48篇图文；未发布站点。';s[ID]=st;d['queries'].update(q);d['buildStatus']='updating';d['generatedAt']=n['publishedAt'];d['exportPreferences']={'selected':None,'destinations':[]}
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d);p.write_text(t)
for name in ['OverrideDiagrams.jsx','override-diagrams.css','override-source-previews.json']:shutil.copyfile(A/name,R/name)
print('Added one article and two queries, preserving all existing objects.')
