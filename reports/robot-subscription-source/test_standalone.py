"""Validate complete article, scoped diagrams, protected files and portable output."""
import hashlib,json,re,sys
from pathlib import Path
P=Path(sys.argv[1]);NOTE=Path(sys.argv[2]);A=P/'source';R=P/'standalone/src/content/report';ID='research-2026-11-06-robot-subscription-exit-note'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
entry=read(A/'article-entry.json');story=read(A/'illustrated-story.json');reviewed=read(A/'article-reviewed-data.json')
assert entry['body']==NOTE.read_text() and sha(NOTE.read_bytes())==entry['originalBodySha256']
assert entry['firstGit'] in entry['sourceUrl'] and re.fullmatch('[a-f0-9]{40}',entry['firstGit'])
assert entry['publishedAt']==entry['updatedAt']
assert entry['topics']==['business']
assert read(A/'frozen.json')['remoteReadbackVerified'] is True
assert story['diagram']['layout']=='robotsubscription-timelines' and story['secondDiagram']['layout']=='robotsubscription-supply'
assert '定性示意' in story['diagram']['scope'] and '非门店实测' in story['diagram']['scope']
assert 'numericChart' not in story, 'No synthetic numerical comparison'
assert story['diagram']['sourceIds']==['S1','S2']
assert story['secondDiagram']['sourceIds']==['S1','S3']
assert len(story['diagram']['nodes'])>=3 and len(story['secondDiagram']['nodes'])==2
assert '作者' in story['diagram']['note'] and '作者' in story['secondDiagram']['note']
assert len(reviewed['queries'])==2 and len(story['sources'])>=1
parts=re.split(r'^## ',entry['body'],flags=re.M);sections=[]
for section in parts[1:]:
 heading,body=section.split('\n',1);sections.append({'title':heading,'body':body.strip().split('\n\n')})
assert story['sections']==sections
assert story['technicalDetails']==[{'title':'首次研究台账，历史状态保留','body':NOTE.with_name('sources.md').read_text()}]
assert sha(NOTE.with_name('sources.md').read_bytes())==read(A/'frozen.json')['sourcesSha256']
assert story['lead']=='\n\n'.join(parts[0].split('\n\n')[1:]).strip()
previews=read(A/'robotsubscription-source-previews.json')
for url in re.findall(r'\]\((https://[^\s)]+)\)',entry['body']):
 assert url in {s['url'] for s in story['sources']},'Missing source: '+url
 assert url in previews and previews[url]['approvedForReport'] is True
for query in reviewed['queries'].values():assert all(isinstance(value,str) for row in query['rows'] for value in row.values())
for suffix in ['',':second']:
 expected=story['diagram' if suffix=='' else 'secondDiagram']['sourceIds']
 links=reviewed['queries']['diagram-'+ID+suffix]['source']['evidenceFlow'][1:]
 assert [s['title'].split(' · ')[0] for s in links]==expected,'Diagram source scope changed'
a=read(R/'articles.json');st=read(R/'illustrated-stories.json');d=read(P/'standalone/src/data.json')
assert a['articles']==[entry] and st=={ID:story}
assert d['surface']=='report' and d['buildStatus']=='complete' and d['queries']==reviewed['queries']
for key,suffix in [('diagram',''),('secondDiagram',':second')]:
 q='diagram-'+ID+suffix;assert d['queries'][q]['rows']==story[key]['nodes']
 assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
 assert d['queries'][q]['source']['metricDefinitions'][0]['label']==story[key]['label']
unchanged=0
for rel,expected in read(P/'standalone-prepared-sha256.json').items():
 if rel.startswith('src/content/') or rel in ('src/data.json','src/theme.css'):continue
 assert sha((P/'standalone'/rel).read_bytes())==expected,rel;unchanged+=1
patterns=[r'appgprj_[A-Za-z0-9]{6,}',r'libfile_[A-Za-z0-9]{6,}',r'Sentinel_[A-Za-z0-9]{6,}',r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/',r'codex://threads/',r'data-app-local-thread["\x27]\s+content=',r'/workspace/[A-Za-z0-9]',r'/home/agent/[A-Za-z0-9]',r'rtc_u\d+_',r'https?://git\.chatgpt-team\.site']
payloads=[(str(p.relative_to(R)),p.read_bytes()) for p in R.rglob('*') if p.is_file()]+[('data.json',(P/'standalone/src/data.json').read_bytes()),('offline',(P/'robotsubscription.html').read_bytes())]
for name,b in payloads:
 for pat in patterns:assert not re.search(pat,b.decode('utf8','replace')),name+': '+pat
html=(P/'robotsubscription.html').read_text();parsed=[]
for raw in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',html):
 try:parsed.append(json.loads(json.loads(raw)))
 except (ValueError,TypeError):pass
catalogs=[v for v in parsed if isinstance(v,dict) and 'articles' in v];stories=[v for v in parsed if isinstance(v,dict) and ID in v]
assert len(catalogs)==len(stories)==1 and catalogs[0]==a and stories[0]==st
for v in parsed:
 for pat in patterns:assert not re.search(pat,json.dumps(v,ensure_ascii=False)),pat
assert 'digitalhuman' not in html and 'DigitalHuman' not in html
assert '12个月只是研究者选取的比较长度' in entry['body']
assert '部分配图因读取超时未完整核验' in entry['body']
assert '两家条件分开引用' in story['diagram']['note']
assert '同一企业来源链' in story['secondDiagram']['note']
assert '每月付款 ≠ 每月都能取消' in (A/'RobotSubscriptionDiagrams.jsx').read_text()
assert 'new URL(url,item.sourceUrl)' in (A/'shared/IllustratedArticle.jsx').read_text()
assert 'resolveLinks(item.body)' in (A/'shared/IllustratedArticle.jsx').read_text()
assert 'resolveLinks(story.lead)' in (A/'shared/IllustratedArticle.jsx').read_text()
assert not re.search(r'(?:src|href)=["\x27]https?://',html),'Network asset in portable HTML'
manifest=read(P/'standalone/dist/data-app-build.json')
for key in ['html','snapshot']:
 b=(P/'standalone/dist'/manifest[key]['path']).read_bytes();assert len(b)==manifest[key]['bytes'] and sha(b)==manifest[key]['sha256']
built=read(P/'standalone/dist'/manifest['snapshot']['path']);assert built['queries']==d['queries'] and built['id']==d['id']
qa={'standalone':{'buildStatus':d['buildStatus'],'fullOriginals':1,'illustratedStories':1,'narrativeSections':len(sections),'queries':2,'sourceUrls':len(story['sources']),'unchangedOfficialFiles':unchanged,'privacyTextPayloads':len(payloads),'compiledContents':'equal reviewed source','buildManifest':'verified exact HTML/snapshot bytes and hashes','runtimeSha256':manifest['runtimeSha256'],'bytes':(P/'robotsubscription.html').stat().st_size,'sha256':sha((P/'robotsubscription.html').read_bytes())},'scope':{'articleId':ID,'firstGit':entry['firstGit'],'publishedAt':entry['publishedAt'],'bodySha256':entry['originalBodySha256'],'published':False,'largeHTMLGitArchive':'not attempted','portalIntegration':'not performed; standalone only'},'visualQA':'Browser visual and interaction checks were not run. Static checks do not establish rendered acceptance.'}
(P/'build-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa,ensure_ascii=False,indent=2))
