import json,re,hashlib,sys
from pathlib import Path
base=Path(__file__).parent;p=base/'food-waste-measurement'
a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
sha='f308fc35fbe0eb64c59a86e1119aa70a3a9e55e4d38b1c7dba31e588e6602a7b'
assert hashlib.sha256(a['body'].encode()).hexdigest()==sha
assert (base/'note.md').read_text()==a['body']
assert a['firstGit']=='d6655ef13a9924efa4c6ee6998ed733c06078bd9'
assert a['publishedAt']==a['updatedAt']=='2026-11-03T04:03:57Z'
assert len(s['sections'])==4
assert len(s['sources'])==3 and len(d['queries'])==2
for suffix,key in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix
 assert d['queries'][q]['rows']==s[key]['nodes']
 assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
assert s['diagram']['layout']=='waste-origins' and s['secondDiagram']['layout']=='waste-workflow'
for sec in s['sections']:
 assert f"## {sec['title']}\n\n"+'\n\n'.join(sec['body']) in a['body']
pattern=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_|Sentinel_|rtc_u\d'
scanned=0
for f in base.rglob('*'):
 if f.is_file() and f.suffix in ['.jsx','.css','.json','.md']:
  assert not re.search(pattern,f.read_text()),f
  scanned+=1
h=Path(sys.argv[1]).read_text()
assert 'data-app-local-thread' not in h
assert not re.search(pattern,h)
parsed=[]
for raw in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',h):
 try: parsed.append(json.loads(json.loads(raw)))
 except (ValueError,TypeError):pass
catalogs=[v for v in parsed if isinstance(v,dict) and 'articles' in v]
assert len(catalogs)==1
assert catalogs[0]['articles']==[a], 'Final HTML must contain ONLY the target article, with identical full body'
stories=[v for v in parsed if isinstance(v,dict) and a['id'] in v]
assert len(stories)==1 and stories[0]=={a['id']:s}
for v in parsed:assert not re.search(pattern,json.dumps(v,ensure_ascii=False))
assert 'WasteDiagram' in h and 'waste-origin-row' in h
assert not re.search(r'(?:src|href)=["\']https?://',h), 'Unexpected network asset'
print(json.dumps({'status':'passed','singleTargetArticle':True,'bodySHA256':sha,'bytes':len(h.encode()),'htmlSHA256':hashlib.sha256(h.encode()).hexdigest(),'decodedJsonModules':len(parsed),'scannedSourceFiles':scanned,'diagrams':2,'queries':2,'sections':4,'sources':3,'visual':'desktop manually checked separately; not a mobile-device claim'},ensure_ascii=False,indent=2))
