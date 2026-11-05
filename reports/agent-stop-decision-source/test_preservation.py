"""Check the frozen article, scoped queries, preserved 53-story portal and portable exports."""
import base64,hashlib,io,json,re,sys,zipfile
from pathlib import Path
P=Path(sys.argv[1]); BASE=Path(sys.argv[2]); NOTE=Path(sys.argv[3]); A=P/'source'; ID='research-2026-11-05-agent-stop-decision-note'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
entry=read(A/'article-entry.json');story=read(A/'illustrated-story.json');reviewed=read(A/'article-reviewed-data.json')
assert entry['body']==NOTE.read_text() and sha(NOTE.read_bytes())==entry['originalBodySha256']
assert entry['firstGit'] in entry['sourceUrl'] and re.fullmatch('[a-f0-9]{40}',entry['firstGit'])
assert entry['publishedAt']==entry['updatedAt']
assert len(reviewed['queries'])==2 and len(story['sources'])==1
parts=re.split(r'^## ',entry['body'],flags=re.M)
expected_sections=[]
for section in parts[1:]:
 heading,body=section.split('\n',1)
 expected_sections.append({'title':heading,'body':body.strip().split('\n\n')})
assert story['sections']==expected_sections,'Illustrated sections must retain the complete frozen narrative'
assert story['lead']=='\n\n'.join(parts[0].split('\n\n')[1:]).strip()
previews=read(A/'agent-stop-decision-source-previews.json')
for url in re.findall(r'\]\((https://[^\s)]+)\)',entry['body']):
 assert url in {s['url'] for s in story['sources']},'Missing cited source: '+url
 assert url in previews and previews[url]['approvedForReport'] is True,'Missing approved preview: '+url
 for query in reviewed['queries'].values():assert url in {e['detail'] for e in query['source']['evidenceFlow']},'Missing evidence-flow source: '+url

for query in reviewed['queries'].values():
 assert all(isinstance(value,str) for row in query['rows'] for value in row.values()),'Source preview rows must remain readable strings'
for rel,expected in read(P/'baseline-sha256.json').items():assert sha((BASE/rel).read_bytes())==expected,'Baseline modified: '+rel
patterns=[r'appgprj_[A-Za-z0-9]{6,}',r'libfile_[A-Za-z0-9]{6,}',r'Sentinel_[A-Za-z0-9]{6,}',r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/',r'codex://threads/',r'data-app-local-thread["\x27]\s+content=',r'/workspace/[A-Za-z0-9]',r'/home/agent/[A-Za-z0-9]',r'rtc_u\d+_',r'https?://git\.chatgpt-team\.site']
results={}
for mode,filename in [('portal54','timeline54-agent-stop-decision.html'),('standalone','agent-stop-decision.html')]:
 root=P/mode;R=root/'src/content/report';a=read(R/'articles.json');st=read(R/'illustrated-stories.json');d=read(root/'src/data.json')
 assert [v for v in a['articles'] if v['id']==ID]==[entry] and st[ID]==story
 assert d['buildStatus'] in ['complete','creating','updating'] and d['surface']=='report'
 for q,v in reviewed['queries'].items():assert d['queries'][q]==v
 for key,suffix in [('diagram',''),('secondDiagram',':second')]:
  q='diagram-'+ID+suffix;assert d['queries'][q]['rows']==story[key]['nodes']
  assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
 if mode=='portal54':
  oldR=BASE/'src/content/report';oldA=read(oldR/'articles.json');oldSt=read(oldR/'illustrated-stories.json');oldD=read(BASE/'src/data.json')
  lookup={x['id']:x for x in a['articles']};assert all(lookup[x['id']]==x for x in oldA['articles'])
  assert all(st[k]==v for k,v in oldSt.items());assert all(d['queries'][k]==v for k,v in oldD['queries'].items())
  assert d['id']==oldD['id']
  for k,v in oldD.items():
   if k not in ['queries','generatedAt','buildStatus','exportPreferences']:assert d[k]==v,k
  for k,v in oldA.items():
   if k not in ['articles','sourceCommit','syncNote']:assert a[k]==v,k
  reader=(R/'IllustratedArticle.jsx').read_text();oldReader=(oldR/'IllustratedArticle.jsx').read_text()
  expected=oldReader.replace("import React from 'react';","import React from 'react';\nimport agentStopSourcePreviews from './agent-stop-decision-source-previews.json';\nimport {AgentStopDiagram} from './AgentStopDiagrams.jsx';").replace('const diagramRows=reviewedRows(diagramId);',"const diagramRows=reviewedRows(diagramId);\n if(diagram.layout?.startsWith('agent-stop-decision-'))return <AgentStopDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
  expected=expected.replace('sourcePreviews={',"sourcePreviews={id.includes('research-2026-11-05-agent-stop-decision-note')?agentStopSourcePreviews:")
  assert reader==expected,'Unexpected shared reader edit'
  allowed={'src/data.json','src/content/report/articles.json','src/content/report/illustrated-stories.json','src/content/report/IllustratedArticle.jsx'};unchanged=0
  for rel in read(P/'baseline-sha256.json'):
   if rel in allowed:continue
   assert (BASE/rel).read_bytes()==(root/rel).read_bytes(),rel;unchanged+=1
  assert len(a['articles'])==74 and len(st)==54 and len(d['queries'])==111
  research=[v for v in a['articles'] if v['section']=='research'];assert len(research)==54 and sum('ai' in v['topics'] for v in research)==36
  assert a['articles']==sorted(a['articles'],key=lambda x:(x['publishedAt'],x['id']),reverse=True)
  assert st['research-2026-11-01-inventory-capture-note']['thirdDiagram']
 else:
  assert len(a['articles'])==len(st)==1 and len(d['queries'])==2
  assert d['id']!=read(BASE/'src/data.json')['id']
  unchanged=0
  for rel,expected in read(P/'standalone-prepared-sha256.json').items():
   if rel.startswith('src/content/') or rel in ('src/data.json','src/theme.css'):continue
   assert sha((root/rel).read_bytes())==expected,rel;unchanged+=1
 payloads=[(str(p.relative_to(R)),p.read_bytes()) for p in R.rglob('*') if p.is_file()]+[('data.json',(root/'src/data.json').read_bytes()),('offline',(P/filename).read_bytes())]
 downloads=zipcount=0
 if mode=='portal54':
  sm=read(R/'samples.json');assert len(sm)==2
  for sample in sm.values():
   b=sample['html'].encode();assert sha(b)==sample['sha256'];payloads.append(('sample HTML',b))
   for file in sample['files']:
    downloads+=1;b=base64.b64decode(file['body']) if file.get('encoding')=='base64' else file['body'].encode();assert sha(b)==file['sha256']
    if zipfile.is_zipfile(io.BytesIO(b)):
     zipcount+=1
     with zipfile.ZipFile(io.BytesIO(b)) as z:
      for n in z.namelist():payloads.append((n,z.read(n)))
    else:payloads.append((file['name'],b))
  assert downloads==5 and zipcount==2
 for label,b in payloads:
  for pat in patterns:assert not re.search(pat,b.decode('utf8','replace')),mode+': '+label+': '+pat
 html=(P/filename).read_text();parsed=[]
 for raw in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',html):
  try:parsed.append(json.loads(json.loads(raw)))
  except (ValueError,TypeError):pass
 catalogs=[v for v in parsed if isinstance(v,dict) and 'articles' in v];stories=[v for v in parsed if isinstance(v,dict) and ID in v]
 assert len(catalogs)==len(stories)==1 and catalogs[0]==a and stories[0]==st
 for v in parsed:
  for pat in patterns:assert not re.search(pat,json.dumps(v,ensure_ascii=False)),mode+': compiled '+pat
 assert not re.search(r'(?:src|href)=["\x27]https?://',html),'Network asset in portable HTML'
 manifest=read(root/'dist/data-app-build.json')
 for key in ['html','snapshot']:
  b=(root/'dist'/manifest[key]['path']).read_bytes();assert len(b)==manifest[key]['bytes'] and sha(b)==manifest[key]['sha256']
 built=read(root/'dist'/manifest['snapshot']['path']);assert built['queries']==d['queries'] and built['id']==d['id']
 results[mode]={'buildStatus':d['buildStatus'],'fullOriginals':len(a['articles']),'illustratedStories':len(st),'queries':len(d['queries']),'unchangedBaselineFiles':unchanged,'privacyTextPayloads':len(payloads),'downloadPayloads':downloads,'zipContainers':zipcount,'compiledContents':'equal reviewed source','buildManifest':'verified exact HTML/snapshot bytes and hashes','runtimeSha256':manifest['runtimeSha256'],'bytes':(P/filename).stat().st_size,'sha256':sha((P/filename).read_bytes()),'visualQA':('Desktop first view, two diagrams, contents navigation, full-text expansion and diagram 2 source inspector checked in supported local preview; narrow/mobile, print and real offline not checked.' if mode=='standalone' else 'Portal browser visual and interactions not checked; preservation and routing are static checks.')}
results['scope']={'articleId':ID,'firstGit':entry['firstGit'],'publishedAt':entry['publishedAt'],'bodySha256':entry['originalBodySha256'],'published':False,'largeHTMLGitArchive':'not attempted','baselineLimit':'Preserved readable archived 53-story baseline; not proof that missing historical edits were recovered.'}
(P/'build-qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n');print(json.dumps(results,ensure_ascii=False,indent=2))

