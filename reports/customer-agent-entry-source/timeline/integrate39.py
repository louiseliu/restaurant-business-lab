"""Add article 39 to an intact, validated complete 38-article Data project."""
import json,sys,hashlib,shutil
from pathlib import Path
S=Path(sys.argv[1]); A=Path(sys.argv[2]);R=S/'content/report'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json')
assert len(a['articles'])==58 and len(s)==38
n=read(A/'customer-agent-entry/article-entry.json');st=read(A/'customer-agent-entry/illustrated-story.json');q=read(A/'customer-agent-entry/article-reviewed-data.json')['queries']
assert n['id'] not in s and not any(x['id']==n['id'] for x in a['articles'])
assert hashlib.sha256(n['body'].encode()).hexdigest()=='4096e9ea61b55452e68d4d79a07201324ac4ce83963c05f8f4531b39c5d66c91'
assert not set(q)&set(d['queries'])
a['articles'].append(n);a['articles'].sort(key=lambda x:x['publishedAt'],reverse=True)
a['sourceCommit']=n['firstGit'];a['syncNote']='本地待同步39篇图文；未发布站点。'
s[n['id']]=st;d['queries'].update(q);d['buildStatus']='complete';d['generatedAt']='2026-11-03T07:05:31Z'
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d)
p=R/'IllustratedArticle.jsx';t=p.read_text();assert 'AgentEntryDiagram' not in t
needle="import React from 'react';";assert needle in t;t=t.replace(needle,needle+"\nimport {AgentEntryDiagram} from './AgentEntryDiagrams.jsx';")
needle='const diagramRows=reviewedRows(diagramId);';assert needle in t;t=t.replace(needle,needle+"\n if(diagram.layout?.startsWith('agent-entry-'))return <AgentEntryDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
needle='<h1>{story.headline||item.title}</h1>';assert needle in t
t=t.replace(needle, '<h1>{item.id===\'research-2026-11-03-customer-agent-entry-note\'?(story.headline||item.title).split("，").map((part,i,parts)=><React.Fragment key={i}>{part}{i<parts.length-1&&<>，<br/></>}</React.Fragment>):(story.headline||item.title)}</h1>')
t=t.replace('<article className="study-page"', '<article key={item.id} className="study-page"')
p.write_text(t)
for name in ['AgentEntryDiagrams.jsx','agent-entry-diagrams.css']:shutil.copy2(A/name,R/name)
print('Added article 39, two queries, and scoped diagram component; old portal retained.')
