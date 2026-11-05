"""Append one frozen illustrated article, refusing changed or conflicting baselines."""
import hashlib,json,shutil,sys
from pathlib import Path
S=Path(sys.argv[1]);A=Path(sys.argv[2]);R=S/'content/report';ID='research-2026-11-05-kitchen-label-note'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json');n=read(A/'article-entry.json');st=read(A/'illustrated-story.json');q=read(A/'article-reviewed-data.json')['queries']
assert n['id']==ID and hashlib.sha256(n['body'].encode()).hexdigest()==n['originalBodySha256']
assert st['id']==ID and len(q)==2
for key,suffix in [('diagram',''),('secondDiagram',':second')]:assert q['diagram-'+ID+suffix]['rows']==st[key]['nodes']
assert (len(a['articles']),len(s),len(d['queries']))==(76,56,115),'Expected intact 56-story baseline'
research=[x for x in a['articles'] if x['section']=='research'];assert len(research)==56 and sum('ai' in x['topics'] for x in research)==36
assert ID not in s and ID not in [x['id'] for x in a['articles']] and not set(q)&set(d['queries'])
p=R/'IllustratedArticle.jsx';t=p.read_text();assert 'KitchenLabelDiagram' not in t
needle="import React from 'react';";assert t.count(needle)==1;t=t.replace(needle,needle+"\nimport kitchenLabelSourcePreviews from './kitchen-label-source-previews.json';\nimport {KitchenLabelDiagram} from './KitchenLabelDiagrams.jsx';")
needle='const diagramRows=reviewedRows(diagramId);';assert t.count(needle)==1;t=t.replace(needle,needle+"\n if(diagram.layout?.startsWith('kitchen-label-'))return <KitchenLabelDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
needle='sourcePreviews={';assert t.count(needle)==1;t=t.replace(needle,"sourcePreviews={id.includes('research-2026-11-05-kitchen-label-note')?kitchenLabelSourcePreviews:")
for name in ['KitchenLabelDiagrams.jsx','kitchen-label-diagrams.css','kitchen-label-source-previews.json']:
 assert (A/name).is_file(), 'Missing incoming file: '+name
 assert not (R/name).exists() and not (R/name).is_symlink(), 'Preserve existing file: '+name
assert n['publishedAt']==n['updatedAt']=='2026-11-05T19:11:27Z'
assert 'ai' in n['topics']
a['articles'].append(n);a['articles'].sort(key=lambda x:(x['publishedAt'],x['id']),reverse=True);a['sourceCommit']=n['firstGit'];a['syncNote']='本地待同步57篇图文；未发布站点。';s[ID]=st;d['queries'].update(q);d['buildStatus']='updating';d['generatedAt']=n['publishedAt'];d['exportPreferences']={'selected':None,'destinations':[]}
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d);p.write_text(t)
for name in ['KitchenLabelDiagrams.jsx','kitchen-label-diagrams.css','kitchen-label-source-previews.json']:shutil.copyfile(A/name,R/name)
print('Added one article and two queries, preserving all existing objects.')
