import json,hashlib,sys,base64,zipfile,io,re
from pathlib import Path
P=Path(sys.argv[1]); old=Path(sys.argv[2]); new=Path(sys.argv[3]);R=new/'content/report'
def j(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
manifest=j(P/'source/verified-source-manifest.json')
assert len(manifest)==51
for f in manifest:
 b=(P/'recovered'/f['path']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['sha'],f['path']
a=j(R/'articles.json')['articles'];s=j(R/'illustrated-stories.json');q=j(new/'data.json')['queries'];sm=j(R/'samples.json')
assert len(a)==59 and len(s)==39 and len(sm)==2
lookup={x['id']:x for x in a};base=j(old/'content/report/articles.json')['articles']
assert all(lookup[x['id']]==x for x in base)
assert all(s[k]==v for k,v in j(old/'content/report/illustrated-stories.json').items())
for f in ['LegacyReport.jsx','ReportContent.jsx','Samples.jsx','samples.json','samples.css','report.css','timeline.css','illustrated.css','adoption-brief.js']:
 assert (old/'content/report'/f).read_bytes()==(R/f).read_bytes(),f
for k,v in j(old/'data.json')['queries'].items():assert q[k]==v,k
for id,story in s.items():
 for key,suffix in [('diagram',''),('secondDiagram',':second'),('thirdDiagram',':third')]:
  if key in story and not (key=='secondDiagram' and story.get('numericChart')):
   assert q['diagram-'+id+suffix]['rows']==story[key]['nodes'],id+suffix
item=lookup['research-2026-11-01-inventory-capture-note'];assert item['publishedAt']=='2026-11-01T13:03:33Z';assert sha(item['body'].encode())=='361ddd7a23696f9c32735d44e39051c225ebb8da80ab6085438d911cbb7166b2'
assert '<article key={item.id}' in (R/'IllustratedArticle.jsx').read_text()
assert 'thirdDiagram' in (R/'IllustratedArticle.jsx').read_text() and 'reader-adjacent' in (R/'IllustratedArticle.jsx').read_text()
textpayloads=[];zipcount=0
for f in R.glob('*'):
 if f.is_file():textpayloads.append((f.name,f.read_bytes()))
textpayloads.append(('data.json',(new/'data.json').read_bytes()));textpayloads.append(('offline',(P/'timeline39.html').read_bytes()))
for sample in sm.values():
 b=sample['html'].encode();assert sha(b)==sample['sha256'];textpayloads.append(('embedded HTML',b))
 for f in sample['files']:
  b=base64.b64decode(f['body']) if f.get('encoding')=='base64' else f['body'].encode();assert sha(b)==f['sha256']
  if zipfile.is_zipfile(io.BytesIO(b)):
   zipcount+=1
   with zipfile.ZipFile(io.BytesIO(b)) as z:
    for n in z.namelist():textpayloads.append((n,z.read(n)))
  else:textpayloads.append((f['name'],b))
patterns=[r'appgprj_',r'libfile_',r'Sentinel_',r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/',r'codex://threads/',r'data-app-local-thread["\x27]\s+content=',r'/workspace/',r'/home/agent/',r'rtc_u\d+_']
for name,b in textpayloads:
 t=b.decode('utf8','replace')
 for pattern in patterns:assert not re.search(pattern,t),name+': '+pattern
# Decode the actual compiled catalog/stories, not only source files.
h=(P/'timeline39.html').read_text(); parsed=[]
for raw in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',h):
 try:parsed.append(json.loads(json.loads(raw)))
 except (ValueError,TypeError):pass
catalogs=[v for v in parsed if isinstance(v,dict) and 'articles' in v]
assert len(catalogs)==1 and catalogs[0]['articles']==a
newid='research-2026-11-03-customer-agent-entry-note'
compiled_stories=[v for v in parsed if isinstance(v,dict) and newid in v]
assert len(compiled_stories)==1 and compiled_stories[0]==s
n=lookup[newid];assert sha(n['body'].encode())=='4096e9ea61b55452e68d4d79a07201324ac4ce83963c05f8f4531b39c5d66c91'
assert n['publishedAt']==n['updatedAt']=='2026-11-03T07:05:31Z'
assert n['firstGit']=='90a3b9b65e399b3df0169092f1685adb857658f9'
assert len(s[newid]['sources'])==3 and len(s[newid]['sections'])==4
assert len(q)==len(j(old/'data.json')['queries'])+2
assert a==sorted(a,key=lambda x:x['publishedAt'],reverse=True)
# All original report bytes and any data outside the allowed three fields are preserved.
before=j(old/'data.json');after=j(new/'data.json')
for key,val in before.items():
 if key not in ['queries','generatedAt','buildStatus']:assert after[key]==val,key
for f in old.rglob('*'):
 if not f.is_file():continue
 rel=f.relative_to(old)
 if str(rel) in ['data.json','content/report/IllustratedArticle.jsx','content/report/articles.json','content/report/illustrated-stories.json']:continue
 assert f.read_bytes()==(new/rel).read_bytes(),str(rel)
# Recursive source JSON objects including escaped/nested body strings are checked above after decoding.
for v in parsed:
 for pattern in patterns:assert not re.search(pattern,json.dumps(v,ensure_ascii=False)),pattern
summary={'research' :39,'fullOriginals':59,'samples':2,'ai':24,'verifiedGitBlobs':51,'preservedOriginals':len(base),'preservedIllustratedStories':38,'unchangedSharedFiles':9,'allOtherSourceFilesByteIdentical':True,'compiledCatalogAndStories':'all 59 full bodies and 39 stories match source exactly','reviewedDiagramBindings':'passed including #30 third diagram','privacyTextPayloads':len(textpayloads),'zipContainers':zipcount,'offlineBytes':(P/'timeline39.html').stat().st_size,'offlineSha256':sha((P/'timeline39.html').read_bytes()),'visualQA':'see visual-qa.json for observed desktop checks; mobile and other articles remain untested','published':False,'largeHTMLGitArchive':'not attempted'}
(P/'source/qa.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2))
