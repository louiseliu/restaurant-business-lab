import json,re,hashlib,sys
from pathlib import Path
base=Path(__file__).parent
a=json.loads((base/'article-entry.json').read_text());s=json.loads((base/'illustrated-story.json').read_text());d=json.loads((base/'article-reviewed-data.json').read_text())
sha='fe7cf3baeca717e24bf87239c0911b63dbfbd30f6010d8f7c7f7751a7d09a6c0'
assert hashlib.sha256(a['body'].encode()).hexdigest()==sha
assert (base/'note.md').read_text()==a['body']
assert a['firstGit']=='2099f57b263929a283a34c63871923441a824836'
assert a['publishedAt']==a['updatedAt']=='2026-11-04T21:08:17Z'
assert len(s['sections'])==4 and len(s['sources'])==3 and len(d['queries'])==2
assert d['buildStatus']=='complete'
for suffix,key in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix
 assert d['queries'][q]['rows']==s[key]['nodes']
 assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
for sec in s['sections']:assert f"## {sec['title']}\n\n"+'\n\n'.join(sec['body']) in a['body']
pattern=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_|Sentinel_|rtc_u\d'
scanned=0
for f in base.rglob('*'):
 if f.is_file() and f.suffix in ['.jsx','.css','.json','.md']:
  assert not re.search(pattern,f.read_text()),f;scanned+=1
h=Path(sys.argv[1]).read_text();assert 'data-app-local-thread' not in h;assert not re.search(pattern,h)
parsed=[]
for raw in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',h):
 try:parsed.append(json.loads(json.loads(raw)))
 except (ValueError,TypeError):pass
catalogs=[v for v in parsed if isinstance(v,dict) and 'articles' in v];assert len(catalogs)==1 and catalogs[0]['articles']==[a]
stories=[v for v in parsed if isinstance(v,dict) and a['id'] in v];assert len(stories)==1 and stories[0]=={a['id']:s}
for v in parsed:assert not re.search(pattern,json.dumps(v,ensure_ascii=False))
assert 'MenuDiagram' in h and 'menu-lane' in h
assert not re.search(r'(?:src|href)=["\']https?://',h)
r=(base/'ReportContent.jsx').read_text();assert 'catalog.articles[0]' in r
reader=(base/'IllustratedArticle.jsx').read_text();assert "if(el.tagName==='DETAILS')el.open=true" in reader
assert 'sourcePreviews={sourcePreviews}' in reader
print(json.dumps({'status':'passed','singleTargetArticle':True,'bodySHA256':sha,'bytes':len(h.encode()),'htmlSHA256':hashlib.sha256(h.encode()).hexdigest(),'decodedJsonModules':len(parsed),'scannedSourceFiles':scanned,'diagrams':2,'queries':2,'sections':4,'sources':3,'visual':'recorded separately; static QA is not browser verification','portal41':'unchanged; integration not performed'},ensure_ascii=False,indent=2))
