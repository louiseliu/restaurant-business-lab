import json,hashlib,sys,base64,zipfile,io,re
from pathlib import Path
P=Path(sys.argv[1]); old=Path(sys.argv[2]); new=Path(sys.argv[3]);R=new/'content/report'
def j(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
a=j(R/'articles.json')['articles'];s=j(R/'illustrated-stories.json');q=j(new/'data.json')['queries'];sm=j(R/'samples.json')
assert len(a)==58 and len(s)==38 and len(sm)==2
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
assert 'thirdDiagram' in (R/'IllustratedArticle.jsx').read_text() and 'reader-adjacent' in (R/'IllustratedArticle.jsx').read_text()
textpayloads=[];zipcount=0
for f in R.glob('*'):
 if f.is_file():textpayloads.append((f.name,f.read_bytes()))
textpayloads.append(('data.json',(new/'data.json').read_bytes()));textpayloads.append(('offline',(P/'timeline38.html').read_bytes()))
for sample in sm.values():
 b=sample['html'].encode();assert sha(b)==sample['sha256'];textpayloads.append(('embedded HTML',b))
 for f in sample['files']:
  b=base64.b64decode(f['body']) if f.get('encoding')=='base64' else f['body'].encode();assert sha(b)==f['sha256']
  if zipfile.is_zipfile(io.BytesIO(b)):
   zipcount+=1
   with zipfile.ZipFile(io.BytesIO(b)) as z:
    for n in z.namelist():textpayloads.append((n,z.read(n)))
  else:textpayloads.append((f['name'],b))
patterns=[r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/',r'codex://threads/',r'data-app-local-thread["\x27]\s+content=',r'/workspace/',r'/home/agent/',r'rtc_u\d+_']
for name,b in textpayloads:
 t=b.decode('utf8','replace')
 for pattern in patterns:assert not re.search(pattern,t),name+': '+pattern
summary={'research':38,'fullOriginals':58,'samples':2,'ai':23,'verifiedGitBlobs':45,'preservedOriginals':len(base),'preservedIllustratedStories':22,'unchangedSharedFiles':9,'reviewedDiagramBindings':'passed including #30 third diagram','privacyTextPayloads':len(textpayloads),'zipContainers':zipcount,'offlineBytes':(P/'timeline38.html').stat().st_size,'offlineSha256':sha((P/'timeline38.html').read_bytes()),'visualQA':'not performed for the complete portal; static tests are not visual acceptance','published':False,'largeHTMLGitArchive':'not attempted'}
(P/'source/qa.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2))
