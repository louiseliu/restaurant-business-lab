"""Validate complete article, scoped diagrams, protected files and portable output."""
import hashlib,json,re,sys
from pathlib import Path
P=Path(sys.argv[1]);NOTE=Path(sys.argv[2]);A=P/'source';R=P/'standalone/src/content/report';ID='research-2026-11-06-reservation-policy-note'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
entry=read(A/'article-entry.json');story=read(A/'illustrated-story.json');reviewed=read(A/'article-reviewed-data.json');frozen=read(A/'frozen.json')
assert entry['body']==NOTE.read_text() and sha(NOTE.read_bytes())==entry['originalBodySha256']==frozen['sha256']
assert entry['firstGit']==frozen['commit'] and entry['firstGit'] in entry['sourceUrl'] and re.fullmatch('[a-f0-9]{40}',entry['firstGit'])
assert entry['publishedAt']==entry['updatedAt']==frozen['time']
assert entry['topics']==['ai','business']
assert frozen['remoteReadbackVerified'] is True and frozen['editorialFrozen'] is True
assert 'numericChart' not in story, 'No synthetic numerical comparison'
assert story['diagram']['layout']=='reservation-policy-methods'
assert story['secondDiagram']['layout']=='reservation-policy-denominator'
assert story['thirdDiagram']['layout']=='reservation-policy-evidence'
assert '定性示意' in story['diagram']['scope'] and '非门店实测' in story['diagram']['scope']
assert story['diagram']['sourceIds']==['S2','S3','S4']
assert story['secondDiagram']['sourceIds']==[]
assert story['thirdDiagram']['sourceIds']==['S1','S2','S3','S5','S6']
assert len(reviewed['queries'])==3 and len(story['sources'])==7
parts=re.split(r'^## ',entry['body'],flags=re.M);sections=[]
for section in parts[1:]:
 heading,body=section.split('\n',1);sections.append({'title':heading,'body':body.strip().split('\n\n')})
assert story['sections']==sections and len(sections)==7
assert story['technicalDetails']==[{'title':'首次研究台账，历史状态保留','body':NOTE.with_name('sources.md').read_text()}]
assert sha(NOTE.with_name('sources.md').read_bytes())==frozen['sourcesSha256']
assert story['lead']=='\n\n'.join(parts[0].split('\n\n')[1:]).strip()
previews=read(A/'reservation-policy-source-previews.json')
for url in re.findall(r'\]\((https://[^\s)]+)\)',entry['body']):
 assert url in {s['url'] for s in story['sources']},'Missing source: '+url
 assert url in previews and previews[url]['approvedForReport'] is True
for query in reviewed['queries'].values():assert all(isinstance(value,str) for row in query['rows'] for value in row.values())
a=read(R/'articles.json');st=read(R/'illustrated-stories.json');d=read(P/'standalone/src/data.json')
assert a['articles']==[entry] and st=={ID:story}
assert d['surface']=='report' and d['buildStatus']=='complete' and d['queries']==reviewed['queries']
for key,suffix in [('diagram',''),('secondDiagram',':second'),('thirdDiagram',':third')]:
 q='diagram-'+ID+suffix;assert d['queries'][q]['rows']==story[key]['nodes']
 assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
 assert d['queries'][q]['source']['metricDefinitions'][0]['label']==story[key]['label']
 expected=[{'title':s['title'],'detail':s['url']} for s in story['sources'] if s['id'] in story[key]['sourceIds']]
 assert reviewed['queries'][q]['source']['evidenceFlow'][1:]==expected,'Diagram source scope changed'
unchanged=0
for rel,expected in read(P/'standalone-prepared-sha256.json').items():
 if rel.startswith('src/content/') or rel in ('src/data.json','src/theme.css'):continue
 assert sha((P/'standalone'/rel).read_bytes())==expected,rel;unchanged+=1
patterns=[r'appgprj_[A-Za-z0-9]{6,}',r'libfile_[A-Za-z0-9]{6,}',r'Sentinel_[A-Za-z0-9]{6,}',r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/',r'codex://threads/',r'data-app-local-thread["\x27]\s+content=',r'/workspace/[A-Za-z0-9]',r'/home/agent/[A-Za-z0-9]',r'rtc_u\d+_',r'https?://git\.chatgpt-team\.site',r'gh[pousr]_[A-Za-z0-9]{20,}',r'sk-[A-Za-z0-9_-]{24,}']
payloads=[(str(p.relative_to(R)),p.read_bytes()) for p in R.rglob('*') if p.is_file()]+[('data.json',(P/'standalone/src/data.json').read_bytes()),('offline',(P/'reservation-policy.html').read_bytes())]
for name,b in payloads:
 for pat in patterns:assert not re.search(pat,b.decode('utf8','replace')),name+': '+pat
html=(P/'reservation-policy.html').read_text();parsed=[]
for raw in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',html):
 try:parsed.append(json.loads(json.loads(raw)))
 except (ValueError,TypeError):pass
catalogs=[v for v in parsed if isinstance(v,dict) and 'articles' in v];stories=[v for v in parsed if isinstance(v,dict) and ID in v]
assert len(catalogs)==len(stories)==1 and catalogs[0]==a and stories[0]==st
for v in parsed:
 for pat in patterns:assert not re.search(pat,json.dumps(v,ensure_ascii=False)),pat
assert 'robotsubscription' not in html and 'RobotSubscription' not in html
for phrase in ['取消收费按实际净留存另列','已扣过的成本不重复扣','被释放的工作时间没有改变付薪支出时','不代表今天政策','未核验上述各店的AI启用状态']:
 assert phrase in entry['body'],phrase
for phrase in ['订金抵餐费不重复记收入','未知不填成被订金劝退','同一可售时段只计一次容量收益','观察比较不能直接证明因果','不是未披露店规的生效日']:
 assert phrase in json.dumps(story,ensure_ascii=False),phrase
reader=(A/'shared/IllustratedArticle.jsx').read_text()
assert '<article lang="zh-CN"' in reader, 'Chinese article language must be scoped in authored content'
for phrase in ['new URL(url,item.sourceUrl)','resolveLinks(item.body)','resolveLinks(story.lead)','story.thirdDiagram']:
 assert phrase in reader,phrase
assert not re.search(r'(?:src|href)=["\x27]https?://',html),'Network asset in portable HTML'
manifest=read(P/'standalone/dist/data-app-build.json')
for key in ['html','snapshot']:
 b=(P/'standalone/dist'/manifest[key]['path']).read_bytes();assert len(b)==manifest[key]['bytes'] and sha(b)==manifest[key]['sha256']
built=read(P/'standalone/dist'/manifest['snapshot']['path']);assert built['queries']==d['queries'] and built['id']==d['id']
qa={'standalone':{'buildStatus':d['buildStatus'],'fullOriginals':1,'illustratedStories':1,'narrativeSections':len(sections),'queries':3,'sourceUrls':len(story['sources']),'unchangedOfficialFiles':unchanged,'privacyTextPayloads':len(payloads),'compiledContents':'equal reviewed source','buildManifest':'verified exact HTML/snapshot bytes and hashes','runtimeSha256':manifest['runtimeSha256'],'bytes':(P/'reservation-policy.html').stat().st_size,'sha256':sha((P/'reservation-policy.html').read_bytes())},'scope':{'articleId':ID,'firstGit':entry['firstGit'],'publishedAt':entry['publishedAt'],'bodySha256':entry['originalBodySha256'],'published':False,'largeHTMLGitArchive':'not attempted','portalIntegration':'not performed; standalone only'},'visualQA':'Browser visual and interaction checks were not run. Static checks do not establish rendered acceptance.'}
(P/'build-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa,ensure_ascii=False,indent=2))
