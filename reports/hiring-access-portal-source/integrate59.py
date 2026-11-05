"""Append one frozen illustrated article, refusing changed or conflicting baselines."""
import hashlib,json,shutil,sys
from pathlib import Path
S=Path(sys.argv[1]);A=Path(sys.argv[2]);R=S/'content/report';ID='research-2026-11-05-hiring-access-note'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json');n=read(A/'article-entry.json');st=read(A/'illustrated-story.json');q=read(A/'article-reviewed-data.json')['queries']
assert n['id']==ID and hashlib.sha256(n['body'].encode()).hexdigest()==n['originalBodySha256']
assert st['id']==ID and len(q)==2
for key,suffix in [('diagram',''),('secondDiagram',':second')]:assert q['diagram-'+ID+suffix]['rows']==st[key]['nodes']
assert (len(a['articles']),len(s),len(d['queries']))==(78,58,119),'Expected intact 58-story baseline'
research=[x for x in a['articles'] if x['section']=='research'];assert len(research)==58 and sum('ai' in x['topics'] for x in research)==37
assert ID not in s and ID not in [x['id'] for x in a['articles']] and not set(q)&set(d['queries'])
p=R/'IllustratedArticle.jsx';t=p.read_text();assert 'AIHiringDiagram' not in t
needle="import React from 'react';";assert t.count(needle)==1;t=t.replace(needle,needle+"\nimport aiHiringSourcePreviews from './ai-hiring-source-previews.json';\nimport {AIHiringDiagram} from './AIHiringDiagrams.jsx';")
needle='const diagramRows=reviewedRows(diagramId);';assert t.count(needle)==1;t=t.replace(needle,needle+"\n if(diagram.layout?.startsWith('ai-hiring-'))return <AIHiringDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
needle='sourcePreviews={';assert t.count(needle)==1;t=t.replace(needle,"sourcePreviews={id.includes('research-2026-11-05-hiring-access-note')?aiHiringSourcePreviews:")
for name in ['AIHiringDiagrams.jsx','ai-hiring-diagrams.css','ai-hiring-source-previews.json']:
 assert (A/name).is_file(), 'Missing incoming file: '+name
 assert not (R/name).exists() and not (R/name).is_symlink(), 'Preserve existing file: '+name
assert n['publishedAt']==n['updatedAt']=='2026-11-05T21:05:54Z'
assert n['topics']==['ai']
assert n['firstGit']=='fc02d8ca4db8a14ab86572d1d936fcdd6eaa8cb8' and n['firstGit'] in n['sourceUrl']
assert len(st['sections'])==7 and len(st['sources'])==5
assert len(st['diagram']['nodes'])==4 and len(st['secondDiagram']['nodes'])==3
a['articles'].append(n);a['articles'].sort(key=lambda x:(x['publishedAt'],x['id']),reverse=True);a['sourceCommit']=n['firstGit'];a['syncNote']='本地待同步59篇图文；未发布站点。';s[ID]=st;d['queries'].update(q);d['buildStatus']='updating';d['generatedAt']=n['publishedAt']
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d);p.write_text(t)
for name in ['AIHiringDiagrams.jsx','ai-hiring-diagrams.css','ai-hiring-source-previews.json']:shutil.copyfile(A/name,R/name)
print('Added one article and two queries, preserving all existing objects.')
