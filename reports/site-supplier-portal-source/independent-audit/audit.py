"""Independent read-only portal audit. Usage: audit.py PRODUCTION SITE_SOURCE SUPPLIER_SOURCE [OFFICIAL_RUNTIME_JS]."""
import base64, hashlib, io, json, re, subprocess, sys, zipfile
from pathlib import Path
p, site, supplier=map(Path,sys.argv[1:4])
old=p/'baseline69'; new=p/'portal71'; rel=Path('src/content/report'); o=old/rel; n=new/rel
read=lambda f:json.loads(f.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
a,b=read(o/'articles.json'),read(n/'articles.json'); lookup={x['id']:x for x in b['articles']}
s,t=read(o/'illustrated-stories.json'),read(n/'illustrated-stories.json')
d,e=read(old/'src/data.json'),read(new/'src/data.json')
assert len(lookup)==len(b['articles'])==91 and len(a['articles'])==89
assert len(s)==69 and len(t)==71 and len(d['queries'])==142 and len(e['queries'])==146
assert all(lookup[x['id']]==x for x in a['articles'])
assert all(t[k]==v for k,v in s.items()) and all(e['queries'][k]==v for k,v in d['queries'].items())
changed={'src/data.json',str(rel/'articles.json'),str(rel/'illustrated-stories.json'),str(rel/'ReportContent.jsx'),str(rel/'IllustratedArticle.jsx')}
fingerprints=read(p/'baseline69-sha256.json'); kept=0
for path,h in fingerprints.items():
 assert sha((old/path).read_bytes())==h
 if path not in changed: assert (old/path).read_bytes()==(new/path).read_bytes(); kept+=1
ids=[]; sections=[]
for folder,topics,count in [(site,['business'],6),(supplier,['ai'],7)]:
 entry=read(folder/'article-entry.json'); story=read(folder/'illustrated-story.json'); frozen=read(folder/'frozen.json'); ids.append(entry['id'])
 assert lookup[entry['id']]==entry and t[entry['id']]==story and entry['topics']==topics
 assert entry['body'].encode()==(folder/'note.md').read_bytes()
 assert sha(entry['body'].encode())==frozen['sha256']
 assert story['technicalDetails'][0]['body'].encode()==(folder/'sources.md').read_bytes()
 assert sha((folder/'sources.md').read_bytes())==frozen['sourcesSha256']
 assert frozen['commit'] in entry['sourceUrl'] and entry['firstGit']==frozen['commit']
 parts=re.split(r'^## ',entry['body'],flags=re.M)[1:]
 assert len(parts)==len(story['sections'])==count
 assert story['sections']==[{'title':x.split('\n',1)[0],'body':x.split('\n',1)[1].strip().split('\n\n')} for x in parts]
 sections.append(count)
 queries=read(folder/'article-reviewed-data.json')['queries']; assert len(queries)==2
 for key,q in queries.items():
  assert e['queries'][key]==q
  assert all(m['componentIds']==[key] for m in q['source']['metricDefinitions'])
  if key.startswith('diagram-'):
   fig=story['secondDiagram'] if key.endswith(':second') else story['diagram']; assert q['rows']==fig['nodes']
  else:
   assert [r['value'] for r in q['rows']]==[2400,-960,-1500]
   for r in q['rows']: assert r['value']==r['incrementalOrdersPerDay']*r['contributionPerOrderCny']*r['operatingDays']-r['rentPremiumCny']-r['otherCostDifferenceCny']
reader=(n/'IllustratedArticle.jsx').read_text(); prior=(o/'IllustratedArticle.jsx').read_text()
lang=lambda text:re.search(r'<article lang=\{(.*?)\} key=',text).group(1)
assert lang(reader).replace("'"+ids[0]+"',",'')==lang(prior)
assert ids[1] not in lang(reader) and '首次研究台账，历史状态保留' in reader and '属于当时状态' in reader
html=(p/'timeline71-site-supplier.html').read_text()
parsed=[]
for match in re.finditer(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',html):
 try: parsed.append(json.loads(json.loads(match.group(1))))
 except (ValueError,TypeError): pass
assert b in parsed and t in parsed
samples=read(n/'samples.json'); assert len(samples)==2 and samples in parsed
patterns=[r'/workspace/[A-Za-z0-9]',r'/home/agent/[A-Za-z0-9]',r'codex://threads/',r'https?://(?:www\.)?chatgpt\.com/(?:c|g|share)/',r'github_pat_[A-Za-z0-9_]{20,}',r'gh[pousr]_[A-Za-z0-9]{20,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'appgprj_[A-Za-z0-9]+',r'libfile_[A-Za-z0-9]+',r'rtc_u\d+_']
scanned=archives=downloads=0
def scan(data):
 global scanned,archives
 if zipfile.is_zipfile(io.BytesIO(data)):
  archives+=1
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   assert z.testzip() is None
   assert len(z.namelist())==len(set(z.namelist()))
   for name in z.namelist():
    if not name.endswith('/'):scan(z.read(name))
 else:
  scanned+=1; text=data.decode('utf8','replace')
  assert not any(re.search(pattern,text) for pattern in patterns),'Private marker detected'
for f in n.rglob('*'):
 if f.is_file():scan(f.read_bytes())
for sample in samples.values():
 assert sha(sample['html'].encode())==sample['sha256']
 for f in sample['files']:
  downloads+=1; data=base64.b64decode(f['body'],validate=True) if f.get('encoding')=='base64' else f['body'].encode(); assert sha(data)==f['sha256']; scan(data)
assert downloads==5 and archives==2
scan(html.encode())
for value in parsed:scan(json.dumps(value,ensure_ascii=False).encode())
m=read(new/'dist/data-app-build.json')
for key in ['html','snapshot']:
 data=(new/'dist'/m[key]['path']).read_bytes();assert len(data)==m[key]['bytes'] and sha(data)==m[key]['sha256'];scan(data)
assert read(new/'dist'/m['snapshot']['path'])==e
# Execute functions extracted directly from both actual JSX files. No DOM or browser.
js=r'''
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const [oldDir,newDir]=process.argv.slice(1),read=(p)=>fs.readFileSync(p,'utf8');
const a=JSON.parse(read(oldDir+'/articles.json')).articles,b=JSON.parse(read(newDir+'/articles.json')).articles;
const load=(dir)=>{let text=read(dir+'/ReportContent.jsx');let ctx=vm.createContext({URLSearchParams,location:{hash:''},URL});vm.runInContext(text.slice(text.indexOf('function topicMatch('),text.indexOf('export function ReportContent()')),ctx);let r=read(dir+'/IllustratedArticle.jsx');vm.runInContext(r.slice(r.indexOf('const portal69Sources='),r.indexOf('const R=')),ctx);return ctx;};
const old=load(oldDir),now=load(newDir);let tests=0;
for(const x of a){for(const topic of ['ai','business','business-model','all','other']){assert.equal(now.topicMatch(x,topic),old.topicMatch(x,topic));tests++;}for(const id of [x.id,x.id+':lead','article:'+x.id]){assert.equal(now.resolvePortal71Links(now.resolvePortal69Links(x.body,id),id),old.resolvePortal69Links(x.body,id));tests++;}}
const research=b.filter(x=>x.section==='research');assert.equal(research.filter(x=>x.topics.includes('ai')).length,47);assert.equal(research.filter(x=>now.topicMatch(x,'ai')).length,48);
for(const x of b){now.location.hash='#read/'+x.id;assert.equal(now.readRoute().id,x.id);tests++;}
for(const x of b.filter(x=>!a.some(y=>x.id===y.id))){assert.equal(now.topicMatch(x,'ai'),true);for(const id of [x.id,x.id+':section:0','article:'+x.id]){const resolved=now.resolvePortal71Links(x.body,id);for(const match of x.body.matchAll(/\]\((\.\.?\/[^)]+|sources\.md|calculations\.py|calculation-results\.json)\)/g)){assert.ok(resolved.includes(new URL(match[1],x.sourceUrl).href));tests++;}}}
assert.equal(now.topicMatch(b.find(x=>x.id.includes('site-selection')),'business-model'),true);
console.log(JSON.stringify({tests,rawAi:47,effectiveAi:48,browser:false}));
'''
result=subprocess.run(['node','-e',js,str(o),str(n)],check=True,capture_output=True,text=True)
print(json.dumps({'result':'PASS','originalsPreserved':89,'storiesPreserved':69,'queriesPreserved':142,'unchangedFiles':kept,'sections':sections,'downloads':downloads,'recursiveArchives':archives,'privacyPayloads':scanned,'actualJsHelpers':json.loads(result.stdout),'limits':'Static data and source checks, plus pure JavaScript only. No browser, HTTP, remote history, publication or visual checks.'},ensure_ascii=False,indent=2))

if len(sys.argv)>4:
 runtime=Path(sys.argv[4]).read_bytes()
 assert sha(runtime)==m['runtimeSha256']
 for target in [p/'timeline71-site-supplier.html',new/'dist'/m['html']['path']]:
  assert base64.b64encode(runtime) in target.read_bytes()
 if (p/'reproduce71/timeline71-site-supplier.html').exists():
  assert (p/'reproduce71/timeline71-site-supplier.html').read_bytes()==(p/'timeline71-site-supplier.html').read_bytes()
