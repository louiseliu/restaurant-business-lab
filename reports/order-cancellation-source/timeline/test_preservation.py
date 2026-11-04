"""Verify the complete article-41 portal against its intact article-40 baseline."""
import base64,hashlib,io,json,re,sys,zipfile
from pathlib import Path

P=Path(sys.argv[1]); old=Path(sys.argv[2]); new=Path(sys.argv[3]); R=new/'content/report'
def j(p): return json.loads(p.read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
manifest=j(P/'source/verified-source-manifest.json'); assert len(manifest)==51
for f in manifest:
    b=(P/'recovered'/f['path']).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['sha'],f['path']
a=j(R/'articles.json')['articles']; s=j(R/'illustrated-stories.json'); q=j(new/'data.json')['queries']; sm=j(R/'samples.json')
assert len(a)==61 and len(s)==41 and len(sm)==2
research=[x for x in a if x['section']=='research']
assert len(research)==41 and sum('ai' in x['topics'] for x in research)==25
lookup={x['id']:x for x in a}; base=j(old/'content/report/articles.json')['articles']
assert len(base)==60 and all(lookup[x['id']]==x for x in base)
oldstories=j(old/'content/report/illustrated-stories.json')
assert len(oldstories)==40 and all(s[k]==v for k,v in oldstories.items())
shared=['LegacyReport.jsx','ReportContent.jsx','Samples.jsx','samples.json','samples.css','report.css','timeline.css','illustrated.css','adoption-brief.js']
for name in shared: assert (old/'content/report'/name).read_bytes()==(R/name).read_bytes(),name
oldqueries=j(old/'data.json')['queries']
assert len(q)==len(oldqueries)+2
for k,v in oldqueries.items(): assert q[k]==v,k
for id,story in s.items():
    for key,suffix in [('diagram',''),('secondDiagram',':second'),('thirdDiagram',':third')]:
        if key in story and not (key=='secondDiagram' and story.get('numericChart')):
            assert q['diagram-'+id+suffix]['rows']==story[key]['nodes'],id+suffix
item=lookup['research-2026-11-01-inventory-capture-note']
assert item['publishedAt']=='2026-11-01T13:03:33Z'
assert sha(item['body'].encode())=='361ddd7a23696f9c32735d44e39051c225ebb8da80ab6085438d911cbb7166b2'
reader=(R/'IllustratedArticle.jsx').read_text()
assert '<article key={item.id}' in reader and 'thirdDiagram' in reader and 'reader-adjacent' in reader
assert 'customer-agent-entry-note' in reader and '.split("，")' in reader
assert "startsWith('cancellation-')" in reader
# Removing the two authorized additions must reproduce the previous reader exactly.
reverted=reader.replace("\nimport {CancellationDiagram} from './CancellationDiagrams.jsx';",'').replace("\n if(diagram.layout?.startsWith('cancellation-'))return <CancellationDiagram diagram={diagram} id={id} rows={diagramRows}/>;",'')
assert reverted==(old/'content/report/IllustratedArticle.jsx').read_text()
newid='research-2026-11-03-order-cancellation-note'; n=lookup[newid]
assert sha(n['body'].encode())=='2ee3e6e5d9034614a32160bfa992d3186860fa2e153164af023273fbc4a7844b'
assert n['publishedAt']==n['updatedAt']=='2026-11-03T18:00:26Z'
assert n['firstGit']=='49bce5efc9fbf2d69d9fd922480f7690d07eae1f'
assert len(s[newid]['sources'])==3 and len(s[newid]['sections'])==4
for suffix,key in [('', 'diagram'),(':second','secondDiagram')]:
    queryid='diagram-'+newid+suffix
    assert q[queryid]['source']['metricDefinitions'][0]['componentIds']==[queryid]
    assert q[queryid]['rows']==s[newid][key]['nodes']
assert a==sorted(a,key=lambda x:x['publishedAt'],reverse=True)
before=j(old/'data.json'); after=j(new/'data.json')
for key,val in before.items():
    if key not in ['queries','generatedAt','buildStatus','exportPreferences']: assert after[key]==val,key
allowed={'data.json','content/report/IllustratedArticle.jsx','content/report/articles.json','content/report/illustrated-stories.json'}
unchanged=0
for f in old.rglob('*'):
    if not f.is_file(): continue
    rel=f.relative_to(old)
    if str(rel) in allowed: continue
    assert f.read_bytes()==(new/rel).read_bytes(),str(rel)
    unchanged+=1
# Check every report file plus embedded HTML, downloaded files, and ZIP members.
textpayloads=[]; zipcount=0; downloadcount=0
for f in R.glob('*'):
    if f.is_file(): textpayloads.append((f.name,f.read_bytes()))
textpayloads.extend([('data.json',(new/'data.json').read_bytes()),('offline',(P/'timeline41.html').read_bytes())])
for sample in sm.values():
    b=sample['html'].encode(); assert sha(b)==sample['sha256']; textpayloads.append(('embedded HTML',b))
    for f in sample['files']:
        downloadcount+=1
        b=base64.b64decode(f['body']) if f.get('encoding')=='base64' else f['body'].encode()
        assert sha(b)==f['sha256']
        if zipfile.is_zipfile(io.BytesIO(b)):
            zipcount+=1
            with zipfile.ZipFile(io.BytesIO(b)) as z:
                for name in z.namelist(): textpayloads.append((name,z.read(name)))
        else: textpayloads.append((f['name'],b))
assert downloadcount==5 and zipcount==2
patterns=[r'appgprj_',r'libfile_',r'Sentinel_',r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/',r'codex://threads/',r'data-app-local-thread["\x27]\s+content=',r'/workspace/',r'/home/agent/',r'rtc_u\d+_']
for name,b in textpayloads:
    for pattern in patterns: assert not re.search(pattern,b.decode('utf8','replace')),name+': '+pattern
h=(P/'timeline41.html').read_text(); parsed=[]
for raw in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',h):
    try: parsed.append(json.loads(json.loads(raw)))
    except (ValueError,TypeError): pass
catalogs=[v for v in parsed if isinstance(v,dict) and 'articles' in v]
assert len(catalogs)==1 and catalogs[0]['articles']==a
compiled_stories=[v for v in parsed if isinstance(v,dict) and newid in v]
assert len(compiled_stories)==1 and compiled_stories[0]==s
for v in parsed:
    for pattern in patterns: assert not re.search(pattern,json.dumps(v,ensure_ascii=False)),pattern
assert 'CancellationDiagram' in h and 'cancellation-stage-grid' in h and 'cancellation-lanes' in h
assert not re.search(r'(?:src|href)=["\x27]https?://',h), 'Unexpected network asset'
summary={'research':41,'fullOriginals':61,'samples':2,'ai':25,'verifiedPriorGitBlobs':51,'preservedOriginals':60,'preservedIllustratedStories':40,'preservedQueries':len(oldqueries),'unchangedSharedFiles':len(shared),'unchangedOtherSourceFiles':unchanged,'readerChanges':'exactly one import and one cancellation layout branch','compiledCatalogAndStories':'all 61 full bodies and 41 stories match source exactly','reviewedDiagramBindings':'passed including article 30 third diagram and article 41 scoped queries','preservedDownloadPayloads':downloadcount,'privacyTextPayloads':len(textpayloads),'zipContainers':zipcount,'offlineBytes':(P/'timeline41.html').stat().st_size,'offlineSha256':sha((P/'timeline41.html').read_bytes()),'visualQA':'not performed in this integration task; static checks are not visual acceptance','published':False,'largeHTMLGitArchive':'not attempted'}
(P/'qa41.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))

