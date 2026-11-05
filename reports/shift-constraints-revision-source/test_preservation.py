"""Validate source preservation, fixed evidence, portable output and recursive privacy."""
import base64,hashlib,io,json,re,sys,zipfile
from pathlib import Path
from patch_reader_label import OLD as OLD_LABEL, NEW as NEW_LABEL
P=Path(sys.argv[1]).resolve();BASE_PORTAL=Path(sys.argv[2]).resolve();BASE_STANDALONE=Path(sys.argv[3]).resolve()
ID='research-2026-11-01-shift-constraints-note'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
source=Path(sys.argv[4]).resolve()
entry=read(source/'article-entry.json');story=read(source/'illustrated-story.json');reviewed=read(source/'article-reviewed-data.json')
expectedBody=Path(sys.argv[5]).read_text()
assert entry['body']==expectedBody and sha(expectedBody.encode())==entry['originalBodySha256']
assert entry['publishedAt']=='2026-11-01T14:03:18Z' and entry['updatedAt']=='2026-11-05T03:09:32Z'
assert '/2b466f57a0176f05386b4e0915443e2a28d3b2e8/' in entry['sourceUrl']
assert '员工' in json.dumps(story,ensure_ascii=False)
assert len(story['sources'])==4
changedQueries=set(reviewed['queries']); assert len(changedQueries)==2
baselineChecks=read(P/'baseline-sha256.json') if (P/'baseline-sha256.json').exists() else None
summary={}
patterns=[r'appgprj_',r'libfile_',r'Sentinel_',r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/',r'codex://threads/',r'data-app-local-thread["\x27]\s+content=',r'/workspace/',r'/home/agent/',r'rtc_u\d+_',r'git\.chatgpt-team\.site']
for mode,base,name in [('portal44',BASE_PORTAL,'timeline44-shift-revised.html'),('standalone',BASE_STANDALONE,'shift-constraints-revised.html')]:
    # All bytes of the original workspaces remain unchanged, including their recorded user edits.
    if baselineChecks:
        for rel,expected in baselineChecks[mode].items():assert sha((base/rel).read_bytes())==expected,mode+': base changed: '+rel
    root=P/mode;old=base/'src';new=root/'src';R=new/'content/report';before=read(old/'content/report/articles.json');after=read(R/'articles.json')
    a=after['articles']; olda=before['articles'];lookup={v['id']:v for v in a}
    assert len(a)==len(olda) and len(lookup)==len(a)
    assert lookup[ID]==entry
    assert all(lookup[v['id']]==v for v in olda if v['id']!=ID)
    assert [{k:v for k,v in d.items() if k!='articles'} for d in [before,after]][0]=={k:v for k,v in after.items() if k!='articles'}
    s=read(R/'illustrated-stories.json');olds=read(old/'content/report/illustrated-stories.json')
    assert len(s)==len(olds) and s[ID]==story
    assert all(s[k]==v for k,v in olds.items() if k!=ID)
    d=read(new/'data.json');oldd=read(old/'data.json');q=d['queries'];oldq=oldd['queries']
    assert len(q)==len(oldq) and d['id']==oldd['id'] and d['buildStatus']=='complete'
    for k,v in oldd.items():
        if k not in ['queries','generatedAt','buildStatus']:assert d[k]==v,k
    for k,v in oldq.items():assert q[k]==(reviewed['queries'][k] if k in changedQueries else v),k
    for id,st in s.items():
        for key,suffix in [('diagram',''),('secondDiagram',':second'),('thirdDiagram',':third')]:
            if key in st and not(key=='secondDiagram' and st.get('numericChart')):
                assert q['diagram-'+id+suffix]['rows']==st[key]['nodes'],id+suffix
    allowed={'data.json','content/report/articles.json','content/report/illustrated-stories.json'}
    if mode=='portal44':
        before_reader=(old/'content/report/IllustratedArticle.jsx').read_text()
        after_reader=(new/'content/report/IllustratedArticle.jsx').read_text()
        assert before_reader.count(OLD_LABEL)==1 and after_reader.count(NEW_LABEL)==1
        assert after_reader==before_reader.replace(OLD_LABEL,NEW_LABEL),'Only the scoped shift source label may change'
        allowed.add('content/report/IllustratedArticle.jsx')
    if mode=='standalone':allowed.update(['content/report/LegacyReport.jsx','content/report/samples.json'])
    unchanged=0
    for f in old.rglob('*'):
        if not f.is_file():continue
        rel=f.relative_to(old)
        if str(rel) in allowed:continue
        assert f.read_bytes()==(new/rel).read_bytes(),mode+': '+str(rel)
        unchanged+=1
    for f in base.rglob('*'):
        if not f.is_file():continue
        rel=f.relative_to(base)
        if rel.parts[0] in ['.git','dist','.data-app-offline','node_modules','src']:continue
        assert f.read_bytes()==(root/rel).read_bytes(),mode+': protected '+str(rel)
    sm=read(R/'samples.json');payloads=[(str(f.relative_to(R)),f.read_bytes()) for f in R.glob('*') if f.is_file()]
    payloads.extend([('data.json',(new/'data.json').read_bytes()),('offline',(P/name).read_bytes())])
    downloads=0;zipcount=0
    for sample in sm.values():
        b=sample['html'].encode();assert sha(b)==sample['sha256'];payloads.append(('embedded HTML',b))
        for file in sample['files']:
            downloads+=1;b=base64.b64decode(file['body']) if file.get('encoding')=='base64' else file['body'].encode()
            assert sha(b)==file['sha256']
            if zipfile.is_zipfile(io.BytesIO(b)):
                zipcount+=1
                with zipfile.ZipFile(io.BytesIO(b)) as archive:
                    for n in archive.namelist():payloads.append((n,archive.read(n)))
            else:payloads.append((file['name'],b))
    assert downloads==5 and zipcount==2
    for label,b in payloads:
        for pat in patterns:assert not re.search(pat,b.decode('utf8','replace')),mode+': '+label+': '+pat
    html=(P/name).read_text();parsed=[]
    for raw in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',html):
        try:parsed.append(json.loads(json.loads(raw)))
        except (ValueError,TypeError):pass
    catalogs=[v for v in parsed if isinstance(v,dict) and 'articles' in v];stories=[v for v in parsed if isinstance(v,dict) and ID in v]
    assert len(catalogs)==1 and catalogs[0]==after
    assert len(stories)==1 and stories[0]==s
    for v in parsed:
        for pat in patterns:assert not re.search(pat,json.dumps(v,ensure_ascii=False)),mode+': compiled '+pat
    assert not re.search(r'(?:src|href)=["\x27]https?://',html),'Network asset in portable HTML'
    manifest=read(root/'dist/data-app-build.json')
    for key in ['html','snapshot']:
        payload=(root/'dist'/manifest[key]['path']).read_bytes()
        assert len(payload)==manifest[key]['bytes'] and sha(payload)==manifest[key]['sha256'],mode+': build manifest '+key
    built_snapshot=read(root/'dist'/manifest['snapshot']['path'])
    assert built_snapshot['queries']==q and built_snapshot['id']==d['id'],mode+': split snapshot differs from reviewed source'
    research=[v for v in a if v['section']=='research']
    if mode=='portal44':
        assert len(research)==44 and len(a)==64 and len(s)==44 and len(sm)==2 and sum('ai' in v['topics'] for v in research)==27
        assert a==sorted(a,key=lambda x:(x['publishedAt'],x['id']),reverse=True)
        reader=(R/'IllustratedArticle.jsx').read_text()
        assert '<article key={item.id}' in reader and 'thirdDiagram' in reader and 'reader-adjacent' in reader
        assert s['research-2026-11-01-inventory-capture-note']['thirdDiagram']
        assert sha(lookup['research-2026-11-01-inventory-capture-note']['body'].encode())=='361ddd7a23696f9c32735d44e39051c225ebb8da80ab6085438d911cbb7166b2'
    else:assert len(a)==len(s)==1 and len(q)==2
    summary[mode]={'research':len(research),'fullOriginals':len(a),'illustratedStories':len(s),'ai':sum('ai' in v['topics'] for v in research),'preservedOtherOriginals':len(a)-1,'preservedOtherStories':len(s)-1,'queries':len(q),'preservedOtherQueries':len(q)-2,'unchangedOtherSourceFiles':unchanged,'articleAndArtifactIdentity':'unchanged','recoveredBaselineBytes':'unchanged' if baselineChecks else 'before/after workspace snapshot not supplied','allProtectedFiles':'unchanged','compiledCatalogAndStories':'equal to reviewed source','splitBuildManifest':'verified HTML and snapshot bytes/SHA256; reviewed queries and artifact ID equal source','splitHTMLSha256':manifest['html']['sha256'],'snapshotSha256':manifest['snapshot']['sha256'],'runtimeSha256':manifest['runtimeSha256'],'privacyTextPayloads':len(payloads),'downloadPayloadsChecked':downloads,'zipContainersChecked':zipcount,'bytes':(P/name).stat().st_size,'sha256':sha((P/name).read_bytes()),'visualQA':'separate independent review; not claimed by this static test'}
summary['scope']={'sourceRevision':'2b466f57a0176f05386b4e0915443e2a28d3b2e8','smallSourceCommit':'91dc53aa9fc10a34468e607b3efad0849799ef03','sameArticleId':ID,'firstPublishedAt':entry['publishedAt'],'sameArticleRevision':True,'newResearchCount':0,'newAICount':0,'sourceLabelFix':'One article-scoped conditional in portal reader; all other reader bytes, article labels and URLs preserved','published':False,'largeHTMLGitArchive':'not attempted','oldAttachments':'scope 403; not replaced or duplicated'}
(P/'build-qa.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2))
