"""Add the frozen release-validation article to an intact 46-story portal."""
import hashlib,json,shutil,sys
from pathlib import Path
S=Path(sys.argv[1]); A=Path(sys.argv[2]); R=S/'content/report'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json')
n=read(A/'article-entry.json');st=read(A/'illustrated-story.json');q=read(A/'article-reviewed-data.json')['queries']
assert n['id']=='research-2026-11-05-self-built-release-validation-note'
assert hashlib.sha256(n['body'].encode()).hexdigest()==n['originalBodySha256']
assert st['id']==n['id'] and len(q)==2
for key,suffix in [('diagram',''),('secondDiagram',':second')]:
 assert q['diagram-'+n['id']+suffix]['rows']==st[key]['nodes']
assert len(a['articles'])==66 and len(s)==46 and len(d['queries'])==95,'Expected 46-story baseline; refuse unexpected content.'
assert len([v for v in a['articles'] if v['section']=='research'])==46
assert sum('ai' in v['topics'] for v in a['articles'] if v['section']=='research')==29
assert n['id'] not in s and n['id'] not in [v['id'] for v in a['articles']] and not set(q)&set(d['queries'])
p=R/'IllustratedArticle.jsx';t=p.read_text();assert 'ReleaseValidationDiagram' not in t
needle="import React from 'react';";assert t.count(needle)==1
t=t.replace(needle,needle+"\nimport releaseSourcePreviews from './release-source-previews.json';\nimport {ReleaseValidationDiagram} from './ReleaseValidationDiagrams.jsx';")
needle='const diagramRows=reviewedRows(diagramId);';assert t.count(needle)==1
t=t.replace(needle,needle+"\n if(diagram.layout?.startsWith('release-'))return <ReleaseValidationDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
old="['research-2026-11-05-monthly-meal-customization-note','research-2026-11-05-model-update-acceptance-note'].includes(item.id)"
new="['research-2026-11-05-monthly-meal-customization-note','research-2026-11-05-model-update-acceptance-note','research-2026-11-05-self-built-release-validation-note'].includes(item.id)"
assert t.count(old)==1;t=t.replace(old,new)
old_wrapper='value={children} className={className}/>;'
new_wrapper="value={children} className={className} sourcePreviews={id.includes('research-2026-11-05-self-built-release-validation-note')?releaseSourcePreviews:undefined}/>;"
assert t.count(old_wrapper)==1;t=t.replace(old_wrapper,new_wrapper)
# Validate all incoming content before writes. Preserve existing objects and presentation identity.
a['articles'].append(n);a['articles'].sort(key=lambda x:(x['publishedAt'],x['id']),reverse=True)
a['sourceCommit']=n['firstGit'];a['syncNote']='本地待同步47篇图文；未发布站点。';s[n['id']]=st;d['queries'].update(q)
d['buildStatus']='updating';d['generatedAt']=n['publishedAt'];d['exportPreferences']={'selected':None,'destinations':[]}
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d);p.write_text(t)
for name in ['ReleaseValidationDiagrams.jsx','release-validation-diagrams.css','release-source-previews.json']:shutil.copyfile(A/name,R/name)
print('Added release-validation article and two scoped queries; preserved 46-story baseline.')
