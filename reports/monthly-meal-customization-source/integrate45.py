"""Add the frozen monthly-meal article to a preserved 44-story local portal."""
import hashlib,json,shutil,sys
from pathlib import Path
S=Path(sys.argv[1]); A=Path(sys.argv[2]); R=S/'content/report'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json')
n=read(A/'article-entry.json');st=read(A/'illustrated-story.json');q=read(A/'article-reviewed-data.json')['queries']
assert n['id']=='research-2026-11-05-monthly-meal-customization-note'
assert hashlib.sha256(n['body'].encode()).hexdigest()==n['originalBodySha256']
assert st['id']==n['id'] and len(q)==2
for key,suffix in [('diagram',''),('secondDiagram',':second')]:
    assert q['diagram-'+n['id']+suffix]['rows']==st[key]['nodes']
assert len(a['articles'])==64 and len(s)==44 and len(d['queries'])==91,'Expected current 44-story baseline; refuse unexpected content.'
assert len([v for v in a['articles'] if v['section']=='research'])==44
assert sum('ai' in v['topics'] for v in a['articles'] if v['section']=='research')==27
assert n['id'] not in s and n['id'] not in [v['id'] for v in a['articles']] and not set(q)&set(d['queries'])
p=R/'IllustratedArticle.jsx';t=p.read_text();assert 'MonthlyMealDiagram' not in t
needle="import React from 'react';";assert t.count(needle)==1
t=t.replace(needle,needle+"\nimport {MonthlyMealDiagram} from './MonthlyMealDiagrams.jsx';")
needle='const diagramRows=reviewedRows(diagramId);';assert t.count(needle)==1
t=t.replace(needle,needle+"\n if(diagram.layout?.startsWith('meal-'))return <MonthlyMealDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
old_original='>{item.body}</R>';new_original=">{item.id==='research-2026-11-05-monthly-meal-customization-note'?item.body.replace('(sources.md)',`(${item.sourceUrl.replace(/note\\.md$/,'sources.md')})`):item.body}</R>"
assert t.count(old_original)==1;t=t.replace(old_original,new_original)
# All validation occurs before writes. Existing entries, stories, queries, routes and identity remain unchanged.
a['articles'].append(n);a['articles'].sort(key=lambda x:(x['publishedAt'],x['id']),reverse=True)
a['sourceCommit']=n['firstGit'];a['syncNote']='本地待同步45篇图文；未发布站点。';s[n['id']]=st;d['queries'].update(q)
d['buildStatus']='updating';d['generatedAt']=n['publishedAt'];d['exportPreferences']={'selected':None,'destinations':[]}
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d);p.write_text(t)
for name in ['MonthlyMealDiagrams.jsx','monthly-meal-diagrams.css']:shutil.copyfile(A/name,R/name)
print('Added monthly-meal article and two scoped queries; preserved 44-story baseline.')
