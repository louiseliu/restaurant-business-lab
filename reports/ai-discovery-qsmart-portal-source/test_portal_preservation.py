"""Check frozen entries, unchanged baseline, compiled data, embedded downloads and private-data patterns."""
import base64,hashlib,io,json,re,sys,zipfile
from pathlib import Path
from reader_patch import patch_reader,ID,QID
P,A,Q=[Path(v) for v in sys.argv[1:]];BASE=P/'baseline64';ROOT=P/'portal65';R=ROOT/'src/content/report';OLD=BASE/'src/content/report'
read=lambda p:json.loads(p.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
a=read(R/'articles.json');st=read(R/'illustrated-stories.json');d=read(ROOT/'src/data.json');oldA=read(OLD/'articles.json');oldSt=read(OLD/'illustrated-stories.json');oldD=read(BASE/'src/data.json')
assert (len(a['articles']),len(st),len(d['queries']))==(85,65,134)
assert (len(oldA['articles']),len(oldSt),len(oldD['queries']))==(84,64,131)
lookup={v['id']:v for v in a['articles']};assert len(lookup)==85
assert all(lookup[v['id']]==v for v in oldA['articles'] if v['id']!=QID)
assert all(st[k]==v for k,v in oldSt.items() if k!=QID)
assert all(d['queries'][k]==v for k,v in oldD['queries'].items())
for k,v in oldD.items():
 if k not in ['queries','generatedAt','buildStatus']:assert d[k]==v,k
for k,v in oldA.items():
 if k not in ['articles','sourceCommit','syncNote']:assert a[k]==v,k
assert d['buildStatus']=='complete'
research=[v for v in a['articles'] if v['section']=='research']
assert len(research)==65 and sum('ai' in v['topics'] for v in research)==43
assert a['articles']==sorted(a['articles'],key=lambda v:(v['publishedAt'],v['id']),reverse=True)
assert research[0]['id']==ID
frozenInputs=[]
for archive,entryID in [(A,ID),(Q,QID)]:
 entry=read(archive/'article-entry.json');story=read(archive/'illustrated-story.json');reviewed=read(archive/'article-reviewed-data.json');frozen=read(archive/'frozen.json')
 assert lookup[entryID]==entry and st[entryID]==story
 assert all(d['queries'][k]==v for k,v in reviewed['queries'].items())
 assert entry['body']==(archive/'note.md').read_text()
 for key,suffix in [('diagram',''),('secondDiagram',':second')]:
  q='diagram-'+entryID+suffix
  assert d['queries'][q]['rows']==story[key]['nodes'] and d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
 frozenInputs.append({'id':entryID,**frozen})
entry=lookup[ID];story=st[ID];frozen=read(A/'frozen.json')
assert sha(entry['body'].encode())==entry['originalBodySha256']==frozen['sha256']
assert entry['firstGit']==frozen['commit']=='40e158a2766f7edd8e3d684b66436dd197624ecb' and entry['publishedAt']==entry['updatedAt']==frozen['time']=='2026-11-06T02:15:50Z'
assert sha(story['technicalDetails'][0]['body'].encode())==frozen['sourcesSha256']
parts=re.split(r'^## ',entry['body'],flags=re.M);expected=[]
for section in parts[1:]:
 heading,body=section.split('\n',1);expected.append({'title':heading,'body':body.strip().split('\n\n')})
assert story['sections']==expected
previews=read(A/'ai-discovery-value-source-previews.json')
for url in re.findall(r'\]\((https://[^\s)]+)\)',entry['body']):
 assert url in {source['url'] for source in story['sources']} and previews[url]['approvedForReport'] is True
original=read(Q/'original-article-entry.json');qentry=lookup[QID];qstory=st[QID];qf=read(Q/'frozen.json')
assert qentry['publishedAt']==original['publishedAt']=='2026-10-30T07:29:17Z'
assert qentry['updatedAt']==qf['revisionTime']=='2026-11-06T02:12:43Z'
assert qentry['body'].startswith(original['body']) and qentry['firstSourceUrl']==original['sourceUrl']
assert sha(qentry['body'].encode())==qentry['revisedBodySha256']==qf['bodySha256']
assert {k:v for k,v in qstory.items() if k!='revision'}==oldSt[QID]
assert qstory['revision']['sourceLedger']==(Q/'sources-update-2026-11-06.md').read_text()
assert sha(qstory['revision']['sourceLedger'].encode())==qf['sourcesSha256']
rq='diagram-'+QID+':revision-2026-11-06';assert d['queries'][rq]['rows']==qstory['revision']['diagram']['nodes']
assert d['queries'][rq]['source']['metricDefinitions'][0]['componentIds']==[rq]
expectedReader=patch_reader((OLD/'IllustratedArticle.jsx').read_text());assert (R/'IllustratedArticle.jsx').read_text()==expectedReader
assert 'QSmartRevision item={item}' in expectedReader and 'resolveQSmartLinks(item.body)' in expectedReader
assert "lang={item.id==='"+ID+"'?'zh-CN':undefined}" in expectedReader
added=set()
for archive,names in [(A,['AIDiscoveryDiagrams.jsx','ai-discovery-value-diagrams.css','ai-discovery-value-source-previews.json']),(Q,['QSmartRevision.jsx','qsmart-revision.css'])]:
 for name in names:assert (R/name).read_bytes()==(archive/name).read_bytes();added.add('src/content/report/'+name)
baseline=read(P/'portal-archive-source/baseline64-sha256.json');assert baseline==read(P/'baseline64-sha256.json')
allowed={'src/data.json','src/content/report/articles.json','src/content/report/illustrated-stories.json','src/content/report/IllustratedArticle.jsx'};unchanged=0
for rel,h in baseline.items():
 assert sha((BASE/rel).read_bytes())==h
 if rel not in allowed:assert (ROOT/rel).read_bytes()==(BASE/rel).read_bytes();unchanged+=1
paths={str(f.relative_to(ROOT)) for f in ROOT.rglob('*') if f.is_file() and not {'dist','.data-app-offline','node_modules','__pycache__'}.intersection(f.relative_to(ROOT).parts)}
assert paths-set(baseline)==added
patterns=[r'appgprj_[A-Za-z0-9]{6,}',r'libfile_[A-Za-z0-9]{6,}',r'Sentinel_[A-Za-z0-9]{6,}',r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/',r'codex://threads/',r'data-app-local-thread["\x27]\s+content=',r'/workspace/[A-Za-z0-9]',r'/home/agent/[A-Za-z0-9]',r'rtc_u\d+_',r'https?://git\.chatgpt-team\.site',r'gh[pousr]_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
payloads=[]; containers=[]; releaseManifests=[]
def inspect(label,b,depth=0):
    assert depth<=10,'Unexpected archive depth'
    if zipfile.is_zipfile(io.BytesIO(b)):
        containers.append(label)
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            assert z.testzip() is None,'Archive CRC failed: '+label
            names=z.namelist(); assert len(names)==len(set(names))
            contents={n:z.read(n) for n in names if not n.endswith('/')}
            for n,value in contents.items():
                inspect(label+'!'+n,value,depth+1)
                if n.endswith('release-manifest.json'):
                    m=json.loads(value); prefix=n.rsplit('/',1)[0]+'/' if '/' in n else ''
                    for row in m.get('files',[]):
                        target=prefix+row['path']; assert target in contents,target
                        if 'sha256' in row: assert sha(contents[target])==row['sha256'],target
                        if 'bytes' in row: assert len(contents[target])==row['bytes'],target
                    releaseManifests.append(label+'!'+n)
    else:
        payloads.append(label)
        text=b.decode('utf8','replace')
        for pattern in patterns: assert not re.search(pattern,text),label+': '+pattern
for f in R.rglob('*'):
    if f.is_file(): inspect(str(f.relative_to(R)),f.read_bytes())
inspect('data.json',(ROOT/'src/data.json').read_bytes())
samples=read(R/'samples.json'); assert len(samples)==2
downloads=0
for sample in samples.values():
    b=sample['html'].encode(); assert sha(b)==sample['sha256']; inspect('embedded sample HTML',b)
    for file in sample['files']:
        downloads+=1
        b=base64.b64decode(file['body'],validate=True) if file.get('encoding')=='base64' else file['body'].encode()
        assert sha(b)==file['sha256']; inspect(file['name'],b)
assert downloads==5 and len(containers)==2
html=(P/'timeline65-discovery-qsmart.html').read_text(); inspect('offline HTML',html.encode())
parsed=[]
for raw in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',html):
    try: parsed.append(json.loads(json.loads(raw)))
    except (ValueError,TypeError): pass
catalogs=[v for v in parsed if isinstance(v,dict) and 'articles' in v]
stories=[v for v in parsed if isinstance(v,dict) and ID in v]
assert len(catalogs)==len(stories)==1 and catalogs[0]==a and stories[0]==st
assert samples in parsed,'Compiled embedded samples differ'
for index,v in enumerate(parsed): inspect('decoded compiled JSON '+str(index),json.dumps(v,ensure_ascii=False).encode())
assert not re.search(r'(?:src|href)=["\x27]https?://',html),'Network asset in portable HTML'
manifest=read(ROOT/'dist/data-app-build.json')
for key in ['html','snapshot']:
    b=(ROOT/'dist'/manifest[key]['path']).read_bytes()
    assert len(b)==manifest[key]['bytes'] and sha(b)==manifest[key]['sha256']
    inspect('dist '+key,b)
built=read(ROOT/'dist'/manifest['snapshot']['path'])
assert built==d,'Split-build snapshot differs from source'
qa={'counts':{'research':65,'fullOriginals':85,'stories':65,'samples':2,'ai':43,'queries':134},'preserved':{'unmodifiedOriginals':83,'unmodifiedStories':63,'originalQueries':131,'qsmartOriginalStoryFields':'all unchanged; revision appended','qsmartOriginalBody':'exact prefix retained','qsmartFirstTime':qentry['publishedAt'],'unchangedBaselineFiles':unchanged,'legacySha256':sha((R/'LegacyReport.jsx').read_bytes()),'readerSha256':sha((R/'ReportContent.jsx').read_bytes())},'checks':{'privacyPayloads':len(payloads),'downloads':downloads,'recursiveZipContainers':len(containers),'releaseManifests':len(releaseManifests),'compiledJSON':'matches source','buildManifest':'verified','runtimeSha256':manifest['runtimeSha256']},'frozenInputs':frozenInputs,'html':{'bytes':len(html.encode()),'sha256':sha(html.encode())},'limits':{'visual':'Not checked. Prior HTTP refusal, file-protocol denial and original-site restrictions not retried or bypassed.','published':False,'uploadedHTMLorZIP':False,'historicalAuditGaps':'Five held items remain open; no retry or same-content upload.','presentationCorrection':'GEO authored article only gains zh-CN language metadata. Fourth shared S2 title still omits page 19; prior display issue unchanged.','baseline':'Readable local 64-story baseline only; unavailable original-site user edits/history not recovered.'}}
(P/'portal-build-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa,ensure_ascii=False,indent=2))
