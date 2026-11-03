"""Add article 40 to an intact, validated 39-article Data authoring project."""
import hashlib,json,shutil,sys
from pathlib import Path

S=Path(sys.argv[1]); A=Path(sys.argv[2]); R=S/'content/report'
def read(p): return json.loads(p.read_text())
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

inputs=read(A/'timeline/integration-inputs.json')
for item in inputs['inputs']:
    b=(A/item['path']).read_bytes()
    assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],item['path']
a=read(R/'articles.json'); s=read(R/'illustrated-stories.json'); d=read(S/'data.json')
assert len(a['articles'])==59 and len(s)==39
n=read(A/'service-handoff/article-entry.json'); st=read(A/'service-handoff/illustrated-story.json'); q=read(A/'service-handoff/article-reviewed-data.json')['queries']
assert n['id'] not in s and not any(x['id']==n['id'] for x in a['articles'])
assert hashlib.sha256(n['body'].encode()).hexdigest()=='a0f7b6d072401409a1383388da56058901667426f8d71d8571a3dfd2afdb3332'
assert n['firstGit']=='98fa4044144f56ec5d6b22bf25ea5bef5e6fee74'
assert n['publishedAt']==n['updatedAt']=='2026-11-03T11:10:36Z'
assert not set(q)&set(d['queries'])
p=R/'IllustratedArticle.jsx'; t=p.read_text()
assert 'HandoffDiagram' not in t, 'Use the intact 39-article baseline; do not apply twice.'
assert '<article key={item.id}' in t and 'customer-agent-entry-note' in t and '.split("，")' in t
needle="import React from 'react';"; assert t.count(needle)==1
t=t.replace(needle,needle+"\nimport {HandoffDiagram} from './HandoffDiagrams.jsx';")
needle='const diagramRows=reviewedRows(diagramId);'; assert t.count(needle)==1
t=t.replace(needle,needle+"\n if(diagram.layout?.startsWith('handoff-'))return <HandoffDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
a['articles'].append(n); a['articles'].sort(key=lambda x:x['publishedAt'],reverse=True)
a['sourceCommit']=n['firstGit']; a['syncNote']='本地待同步40篇图文；未发布站点。'
s[n['id']]=st; d['queries'].update(q); d['buildStatus']='complete'; d['generatedAt']=n['publishedAt']
write(R/'articles.json',a); write(R/'illustrated-stories.json',s); write(S/'data.json',d); p.write_text(t)
for name in ['HandoffDiagrams.jsx','handoff-diagrams.css']: shutil.copy2(A/name,R/name)
print('Added article 40 and two reviewed queries. Existing portal and article 39 title behavior preserved.')
