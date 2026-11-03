import json,hashlib,shutil,sys
from pathlib import Path
P=Path(sys.argv[1]); S=Path(sys.argv[2]); R=S/'content/report'; NEW=Path(sys.argv[3]); ASSETS=Path(__file__).parent.parent
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
manifest=read(P/'recovery-manifest.json')
for f in manifest:
 b=(P/'recovered'/f['path']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['sha']
a=read(R/'articles.json');stories=read(R/'illustrated-stories.json');data=read(S/'data.json'); old={x['id']:x for x in a['articles']}
roots=sorted((P/'recovered/reports').glob('*/*/article-entry.json'))+[NEW/'article-entry.json']
for ep in roots:
 e=read(ep);story=read(ep.with_name('illustrated-story.json'));d=read(ep.with_name('article-reviewed-data.json'))
 assert hashlib.sha256(e['body'].encode()).hexdigest()==e['originalBodySha256']
 old[e['id']]=e;stories[e['id']]=story;data['queries'].update(d['queries'])
topics=read(P/'article_topics.json')
for e in old.values():
 if e['path'] in topics:e['topics']=topics[e['path']]
a['articles']=sorted(old.values(),key=lambda x:x['publishedAt'],reverse=True);a['sourceCommit']='d6655ef13a9924efa4c6ee6998ed733c06078bd9';a['syncNote']='本地待同步38篇图文；未发布站点。'
data['buildStatus']='complete';data['generatedAt']='2026-11-03T04:08:00Z'
write(R/'articles.json',a);write(R/'illustrated-stories.json',stories);write(S/'data.json',data)
p=R/'IllustratedArticle.jsx';t=p.read_text();assert 'WasteDiagram' not in t, 'Use an unmodified complete 22-article baseline; do not apply twice';t=t.replace("import React from 'react';","import React from 'react';\nimport {WasteDiagram} from './WasteDiagrams.jsx';")
t=t.replace('const diagramRows=reviewedRows(diagramId);','const diagramRows=reviewedRows(diagramId);\n if(diagram.layout?.startsWith(\'waste-\'))return <WasteDiagram diagram={diagram} id={id} rows={diagramRows}/>;')
t=t.replace('  </section>','  </section>')
needle="{story.secondDiagram&&!story.numericChart&&<Diagram diagram={story.secondDiagram} id={`${item.id}:second`}/>}"
assert needle in t;t=t.replace(needle,needle+'\n {story.thirdDiagram&&<Diagram diagram={story.thirdDiagram} id={`${item.id}:third`}/>}')
# Preserve generic page metadata and adjacent navigation; disclose the archived #30 revision separately.
needle='<a href={item.sourceUrl} target="_blank" rel="noreferrer">查看固定版本研究原文与计算附件 ↗</a>'
replacement='<a href={item.sourceUrl} target="_blank" rel="noreferrer">查看首次固定版本研究原文与计算附件 ↗</a>{item.id===\'research-2026-11-01-inventory-capture-note\'&&<p>本篇保留首次入库时间；持续复查修订见<a href="https://github.com/louiseliu/restaurant-business-lab/blob/8e8bf1681d80990f0fefbea01ed27e5881c4773d/research/2026-11-01-inventory-capture/note.md" target="_blank" rel="noreferrer">修订归档原文 ↗</a>。</p>}'
assert needle in t;t=t.replace(needle,replacement);p.write_text(t)
for name in ['WasteDiagrams.jsx','waste-diagrams.css']:shutil.copy2(ASSETS/name,R/name)
print(len(a['articles']),len(stories),sum('ai' in e['topics'] for e in a['articles'] if e['section']=='research'))
