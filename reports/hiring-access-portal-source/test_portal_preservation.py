"""Verify the additive portal, frozen narrative, payloads, and official build offline."""
import base64, hashlib, io, json, re, sys, zipfile
from pathlib import Path

P=Path(sys.argv[1]); BASE=Path(sys.argv[2]); NOTE=Path(sys.argv[3]); A=P/'archive-source'
ROOT=P/'portal59'; R=ROOT/'src/content/report'; OLD=BASE/'src/content/report'
ID='research-2026-11-05-hiring-access-note'
def read(p): return json.loads(p.read_text())
def sha(b): return hashlib.sha256(b).hexdigest()

entry=read(A/'article-entry.json'); story=read(A/'illustrated-story.json')
reviewed=read(A/'article-reviewed-data.json'); frozen=read(A/'frozen.json')
assert entry['body']==NOTE.read_text()
assert sha(NOTE.read_bytes())==entry['originalBodySha256']==frozen['sha256']
assert entry['firstGit']==frozen['commit']=='fc02d8ca4db8a14ab86572d1d936fcdd6eaa8cb8'
assert entry['firstGit'] in entry['sourceUrl']
assert entry['publishedAt']==entry['updatedAt']==frozen['time']=='2026-11-05T21:05:54Z'
assert sha(NOTE.with_name('sources.md').read_bytes())==frozen['sourcesSha256']
assert story['technicalDetails']==[{'title':'公开来源与主张边界','body':NOTE.with_name('sources.md').read_text()}]
parts=re.split(r'^## ',entry['body'],flags=re.M); expected=[]
for section in parts[1:]:
    heading,body=section.split('\n',1)
    expected.append({'title':heading,'body':body.strip().split('\n\n')})
assert story['sections']==expected and len(expected)==7
assert story['lead']=='\n\n'.join(parts[0].split('\n\n')[1:]).strip()
assert len(story['sources'])==5 and len(reviewed['queries'])==2
previews=read(A/'ai-hiring-source-previews.json')
for url in re.findall(r'\]\((https://[^\s)]+)\)',entry['body']):
    assert url in {source['url'] for source in story['sources']}
    assert previews[url]['approvedForReport'] is True
for suffix,scope in [('', ['S1','S2','S5']),(':second',['S1','S2','S3','S4','S5'])]:
    q=reviewed['queries']['diagram-'+ID+suffix]
    assert [s['title'].split(' · ')[0] for s in q['source']['evidenceFlow'][1:]]==scope
    assert all(isinstance(value,str) for row in q['rows'] for value in row.values())

a=read(R/'articles.json'); st=read(R/'illustrated-stories.json'); d=read(ROOT/'src/data.json')
oldA=read(OLD/'articles.json'); oldSt=read(OLD/'illustrated-stories.json'); oldD=read(BASE/'src/data.json')
assert (len(oldA['articles']),len(oldSt),len(oldD['queries']))==(78,58,119)
assert (len(a['articles']),len(st),len(d['queries']))==(79,59,121)
assert d['buildStatus']=='complete' and d['surface']=='report'
assert d['id']==oldD['id'],'Portal identity must remain unchanged'
assert a['sourceCommit']==entry['firstGit']
lookup={v['id']:v for v in a['articles']}; assert len(lookup)==79
assert lookup[ID]==entry and st[ID]==story
assert all(lookup[v['id']]==v for v in oldA['articles'])
assert all(st[k]==v for k,v in oldSt.items())
assert all(d['queries'][k]==v for k,v in oldD['queries'].items())
for k,v in oldD.items():
    if k not in ['queries','generatedAt','buildStatus']: assert d[k]==v,k
for k,v in oldA.items():
    if k not in ['articles','sourceCommit','syncNote']: assert a[k]==v,k
for q,v in reviewed['queries'].items(): assert d['queries'][q]==v
for key,suffix in [('diagram',''),('secondDiagram',':second')]:
    q='diagram-'+ID+suffix
    assert d['queries'][q]['rows']==story[key]['nodes']
    assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
research=[v for v in a['articles'] if v['section']=='research']
assert len(research)==59 and sum('ai' in v['topics'] for v in research)==38
assert a['articles']==sorted(a['articles'],key=lambda x:(x['publishedAt'],x['id']),reverse=True)
assert research[0]['id']==ID
assert st['research-2026-11-01-inventory-capture-note']['thirdDiagram']
reader=(R/'IllustratedArticle.jsx').read_text(); oldReader=(OLD/'IllustratedArticle.jsx').read_text()
expectedReader=oldReader.replace("import React from 'react';", "import React from 'react';\nimport aiHiringSourcePreviews from './ai-hiring-source-previews.json';\nimport {AIHiringDiagram} from './AIHiringDiagrams.jsx';")
expectedReader=expectedReader.replace('const diagramRows=reviewedRows(diagramId);', "const diagramRows=reviewedRows(diagramId);\n if(diagram.layout?.startsWith('ai-hiring-'))return <AIHiringDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
expectedReader=expectedReader.replace('sourcePreviews={', "sourcePreviews={id.includes('research-2026-11-05-hiring-access-note')?aiHiringSourcePreviews:")
assert reader==expectedReader,'Unexpected shared reader change'
allowed={'src/data.json','src/content/report/articles.json','src/content/report/illustrated-stories.json','src/content/report/IllustratedArticle.jsx'}
baseline=read(P/'baseline58-sha256.json'); unchanged=0
assert baseline==read(P/'portal-archive-source/baseline58-sha256.json')
for rel,expectedHash in baseline.items():
    assert sha((BASE/rel).read_bytes())==expectedHash,'Baseline changed: '+rel
    if rel not in allowed:
        assert (ROOT/rel).read_bytes()==(BASE/rel).read_bytes(),'Existing file changed: '+rel
        unchanged+=1
for name in ['AIHiringDiagrams.jsx','ai-hiring-diagrams.css','ai-hiring-source-previews.json']:
    assert (R/name).read_bytes()==(A/name).read_bytes()
sourcePaths={str(f.relative_to(ROOT)) for f in ROOT.rglob('*') if f.is_file() and not any(p in ['dist','.data-app-offline','__pycache__'] for p in f.relative_to(ROOT).parts)}
assert sourcePaths-set(baseline)=={'src/content/report/'+n for n in ['AIHiringDiagrams.jsx','ai-hiring-diagrams.css','ai-hiring-source-previews.json']}

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
html=(P/'timeline59-hiring-access.html').read_text(); inspect('offline HTML',html.encode())
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
qa={'portal59':{'buildStatus':'complete','researchArticles':59,'fullOriginals':79,'illustratedStories':59,'samples':2,'aiArticles':38,'queries':121,'preservedOriginals':78,'preservedStories':58,'preservedQueries':119,'unchangedBaselineFiles':unchanged,'legacyReportSha256':sha((R/'LegacyReport.jsx').read_bytes()),'portalReaderSha256':sha((R/'ReportContent.jsx').read_bytes()),'privacyTextPayloads':len(payloads),'downloadPayloads':downloads,'recursiveZipContainers':len(containers),'verifiedReleaseManifests':len(releaseManifests),'compiledContents':'catalog, stories and embedded sample payloads equal reviewed source','buildManifest':'exact HTML and snapshot bytes and hashes verified','runtimeSha256':manifest['runtimeSha256'],'bytes':len(html.encode()),'sha256':sha(html.encode())},'scope':{'articleId':ID,'firstGit':entry['firstGit'],'publishedAt':entry['publishedAt'],'bodySha256':entry['originalBodySha256'],'sourcesSha256':frozen['sourcesSha256'],'published':False,'largeHTMLGitArchive':'not attempted','baselineLimit':'Preserves the readable local 58-story baseline; does not recover unavailable historical or unarchived edits.','visualQA':'Full portal browser rendering and interactions not checked. The latest standalone HTTP preview failed with ERR_CONNECTION_REFUSED; older file-protocol access was denied. No retry, rehosting or alternative route was used.'}}
(P/'portal-build-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(qa,ensure_ascii=False,indent=2))
