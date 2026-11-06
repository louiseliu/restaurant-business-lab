"""Verify frozen originals, numerical scope, protected runtime and portable payload."""
import hashlib,json,re,sys
from pathlib import Path
P=Path(sys.argv[1]);NOTE=Path(sys.argv[2]);A=P/'source';R=P/'standalone/src/content/report';ID='research-2026-11-06-site-selection-rent-note'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
entry=read(A/'article-entry.json');story=read(A/'illustrated-story.json');reviewed=read(A/'article-reviewed-data.json');meta=read(A/'frozen.json')
assert entry['body']==NOTE.read_text() and sha(NOTE.read_bytes())==entry['originalBodySha256']==meta['sha256']
assert entry['firstGit'] in entry['sourceUrl'] and re.fullmatch('[a-f0-9]{40}',entry['firstGit'])
assert entry['publishedAt']==entry['updatedAt']==meta['time']
assert entry['topics']==['business'] and meta['remoteReadbackVerified'] is True
assert story['diagram']['layout']=='siteselection-decisions' and story['numericChart']['type']=='horizontalBar'
assert '定性' in story['diagram']['scope'] and '非门店实测' in story['diagram']['scope']
assert story['diagram']['sourceIds']==['S1','S2'] and len(story['diagram']['nodes'])==3
assert len(reviewed['queries'])==2 and len(story['sources'])==2
parts=re.split(r'^## ',entry['body'],flags=re.M);sections=[]
for section in parts[1:]:
 heading,body=section.split('\n',1);sections.append({'title':heading,'body':body.strip().split('\n\n')})
assert story['sections']==sections and len(sections)==6
assert story['technicalDetails']==[{'title':'首次研究台账，历史状态保留','body':NOTE.with_name('sources.md').read_text()}]
assert sha(NOTE.with_name('sources.md').read_bytes())==meta['sourcesSha256']
assert story['lead']=='\n\n'.join(parts[0].split('\n\n')[1:]).strip()
previews=read(A/'siteselection-source-previews.json')
for url in re.findall(r'\]\((https://[^\s)]+)\)',entry['body']):
 assert url in {s['url'] for s in story['sources']}
 assert url in previews and previews[url]['approvedForReport'] is True
assert all(isinstance(v,str) for row in reviewed['queries']['diagram-'+ID]['rows'] for v in row.values())
assert [s['title'].split(' · ')[0] for s in reviewed['queries']['diagram-'+ID]['source']['evidenceFlow'][1:]]==['S1','S2']
rows=reviewed['queries']['visual-'+ID]['rows'];results=read(NOTE.with_name('calculation-results.json'))
assert len(rows)==3 and [r['value'] for r in rows]==[2400,-960,-1500]
for row,scenario in zip(rows,results['scenarios']):
 assert row['value']==scenario['net_difference_after_rent_premium']
 assert row['grossContributionCny']==row['incrementalOrdersPerDay']*row['contributionPerOrderCny']*30
 assert row['value']==row['grossContributionCny']-row['rentPremiumCny']-row['otherCostDifferenceCny']
 assert row['dataStatus']=='作者构造的模拟假设，非实测'
assert results['required_average_incremental_orders_per_day']=='20'
assert '未把87%输入计算' in story['numericChart']['note'] and '分母' in story['diagram']['note']
assert '厂商声明' in story['diagram']['note'] and '不等于' in story['unknowns'][1]
assert reviewed['queries']['visual-'+ID]['methods'][0]['code']==NOTE.with_name('calculations.py').read_text()
for q,query in reviewed['queries'].items():
 for definition in query['source']['metricDefinitions']:assert definition['componentIds']==[q]
 assert all('/blob/'+meta['commit']+'/' in e['detail'] for e in query['source']['evidenceFlow'] if 'github.com' in e['detail'])
a=read(R/'articles.json');st=read(R/'illustrated-stories.json');d=read(P/'standalone/src/data.json')
assert a['articles']==[entry] and st=={ID:story}
assert d['surface']=='report' and d['buildStatus']=='complete' and d['queries']==reviewed['queries']
unchanged=0
for rel,expected in read(P/'standalone-prepared-sha256.json').items():
 if rel.startswith('src/content/') or rel in ('src/data.json','src/theme.css'):continue
 assert sha((P/'standalone'/rel).read_bytes())==expected,rel;unchanged+=1
patterns=[r'appgprj_[A-Za-z0-9]{6,}',r'libfile_[A-Za-z0-9]{6,}',r'Sentinel_[A-Za-z0-9]{6,}',r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/',r'codex://threads/',r'data-app-local-thread["\x27]\s+content=',r'/workspace/[A-Za-z0-9]',r'/home/agent/[A-Za-z0-9]',r'rtc_u\d+_',r'https?://git\.chatgpt-team\.site',r'github_pat_[A-Za-z0-9_]+',r'ghp_[A-Za-z0-9]{20,}']
payloads=[(str(p.relative_to(R)),p.read_bytes()) for p in R.rglob('*') if p.is_file()]+[('data.json',(P/'standalone/src/data.json').read_bytes()),('offline',(P/'siteselection.html').read_bytes())]
for name,b in payloads:
 for pat in patterns:assert not re.search(pat,b.decode('utf8','replace')),name+': '+pat
html=(P/'siteselection.html').read_text();parsed=[]
for raw in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',html):
 try:parsed.append(json.loads(json.loads(raw)))
 except (ValueError,TypeError):pass
catalogs=[v for v in parsed if isinstance(v,dict) and 'articles' in v];stories=[v for v in parsed if isinstance(v,dict) and ID in v]
assert len(catalogs)==len(stories)==1 and catalogs[0]==a and stories[0]==st
for v in parsed:
 for pat in patterns:assert not re.search(pat,json.dumps(v,ensure_ascii=False)),pat
assert 'robotsubscription' not in html and 'RobotSubscription' not in html
reader=(A/'shared/IllustratedArticle.jsx').read_text()
assert '<article lang="zh-CN"' in reader,'Chinese article must declare its language without modifying protected root'
assert 'new URL(url,item.sourceUrl)' in reader and 'calculations\\.py' in reader and 'calculation-results\\.json' in reader
assert 'resolveLinks(item.body)' in reader and 'resolveLinks(story.lead)' in reader
assert not re.search(r'(?:src|href)=["\x27]https?://',html),'Network asset in portable HTML'
manifest=read(P/'standalone/dist/data-app-build.json')
for key in ['html','snapshot']:
 b=(P/'standalone/dist'/manifest[key]['path']).read_bytes();assert len(b)==manifest[key]['bytes'] and sha(b)==manifest[key]['sha256']
built=read(P/'standalone/dist'/manifest['snapshot']['path']);assert built['queries']==d['queries'] and built['id']==d['id']
qa={'standalone':{'buildStatus':d['buildStatus'],'fullOriginals':1,'illustratedStories':1,'narrativeSections':len(sections),'queries':2,'sourceUrls':len(story['sources']),'unchangedOfficialFiles':unchanged,'privacyTextPayloads':len(payloads),'compiledContents':'equal reviewed source','buildManifest':'verified exact HTML/snapshot bytes and hashes','runtimeSha256':manifest['runtimeSha256'],'bytes':(P/'siteselection.html').stat().st_size,'sha256':sha((P/'siteselection.html').read_bytes())},'calculation':{'status':'author constructed assumptions only','netMonthlyCny':[r['value'] for r in rows],'breakEvenOrdersPerDay':20,'accuracy87UsedAsInput':False},'scope':{'articleId':ID,'firstGit':entry['firstGit'],'publishedAt':entry['publishedAt'],'bodySha256':entry['originalBodySha256'],'published':False,'largeHTMLGitArchive':'not attempted','portalIntegration':'not performed; standalone only'},'visualQA':'Browser visual and interaction checks were not run. Static checks do not establish rendered acceptance.'}
(P/'build-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa,ensure_ascii=False,indent=2))
