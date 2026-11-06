"""Independent offline artifact audit. Args: PRODUCTION BASELINE71 RESERVATION_SOURCE ALERT_SOURCE."""
import base64,hashlib,io,json,re,subprocess,sys,zipfile
from pathlib import Path
p,old,res,alert=map(Path,sys.argv[1:]);new=p/'portal73';rel=Path('src/content/report');o=old/rel;n=new/rel
read=lambda f:json.loads(f.read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
a,b=read(o/'articles.json'),read(n/'articles.json');s,t=read(o/'illustrated-stories.json'),read(n/'illustrated-stories.json');d,e=read(old/'src/data.json'),read(new/'src/data.json')
lookup={x['id']:x for x in b['articles']}
assert len(lookup)==len(b['articles'])==93 and len(a['articles'])==91
assert len(s)==71 and len(t)==73 and len(d['queries'])==146 and len(e['queries'])==151
assert all(lookup[x['id']]==x for x in a['articles'])
assert [x['publishedAt'] for x in b['articles']]==sorted([x['publishedAt'] for x in b['articles']],reverse=True)
assert [x['id'] for x in b['articles'][:2]]==['research-2026-11-06-order-alert-note','research-2026-11-06-reservation-policy-note']
assert all(t[k]==v for k,v in s.items()) and all(e['queries'][k]==v for k,v in d['queries'].items())
changed={'src/data.json',str(rel/'articles.json'),str(rel/'illustrated-stories.json'),str(rel/'IllustratedArticle.jsx')}
fingerprints=read(p/'portal-archive-source/baseline71-sha256.json');kept=0
for path,h in fingerprints.items():
 assert sha((old/path).read_bytes())==h,path
 if path not in changed:assert (old/path).read_bytes()==(new/path).read_bytes(),path;kept+=1
assert (old/'protected-runtime.json').read_bytes()==(new/'protected-runtime.json').read_bytes()
assert (old/'.openai/hosting.json').read_bytes()==(new/'.openai/hosting.json').read_bytes()
ids=[];sections=[];query_checks=[]
for folder,topics,count in [(res,['ai','business'],7),(alert,['operations'],6)]:
 entry=read(folder/'article-entry.json');story=read(folder/'illustrated-story.json');frozen=read(folder/'frozen.json');ids.append(entry['id'])
 assert lookup[entry['id']]==entry and t[entry['id']]==story and entry['topics']==topics
 assert entry['body'].encode()==(folder/'note.md').read_bytes() and sha(entry['body'].encode())==frozen['sha256']
 assert story['technicalDetails'][0]['body'].encode()==(folder/'sources.md').read_bytes()
 assert sha((folder/'sources.md').read_bytes())==frozen['sourcesSha256']
 assert frozen['commit'] in entry['sourceUrl'] and entry['firstGit']==frozen['commit'] and entry['publishedAt']==entry['updatedAt']==frozen['time']
 parts=re.split(r'^## ',entry['body'],flags=re.M)[1:];assert len(parts)==len(story['sections'])==count
 assert story['sections']==[{'title':x.split('\n',1)[0],'body':x.split('\n',1)[1].strip().split('\n\n')} for x in parts];sections.append(count)
 queries=read(folder/'article-reviewed-data.json')['queries'];assert len(queries)==(3 if folder==res else 2)
 for key,q in queries.items():
  assert e['queries'][key]==q
  assert all(m['componentIds']==[key] for m in q['source']['metricDefinitions'])
  fig=story['thirdDiagram'] if key.endswith(':third') else story['secondDiagram'] if key.endswith(':second') else story['diagram']
  assert q['rows']==fig['nodes'];flow=q['source']['evidenceFlow'];assert entry['sourceUrl']==flow[0]['detail']
  source_urls={v['url'] for v in story['sources']};assert all(v['detail'] in source_urls for v in flow[1:])
  query_checks.append({'id':key,'rows':len(q['rows']),'evidence':flow})
reader=(n/'IllustratedArticle.jsx').read_text();prior=(o/'IllustratedArticle.jsx').read_text()
assert (n/'ReportContent.jsx').read_bytes()==(o/'ReportContent.jsx').read_bytes()
for prefix in [' const contents=', " <section id={anchor('evidence')}", ' {story.secondDiagram', ' {story.thirdDiagram']:
 assert [v for v in reader.splitlines() if v.startswith(prefix)]==[v for v in prior.splitlines() if v.startswith(prefix)]
for folder in [res,alert]:
 for f in folder.iterdir():
  if f.name.endswith('Diagrams.jsx') or f.name.endswith('-diagrams.css') or f.name.endswith('-source-previews.json'):
   assert (n/f.name).read_bytes()==f.read_bytes()

assert '首次研究台账，历史状态保留' in reader and '属于当时状态' in reader
html_files=list(p.glob('timeline73*.html'));assert len(html_files)==1;html=html_files[0].read_text();parsed=[]
for match in re.finditer(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',html):
 try:parsed.append(json.loads(json.loads(match.group(1))))
 except (ValueError,TypeError):pass
assert b in parsed and t in parsed
samples=read(n/'samples.json');assert len(samples)==2 and samples in parsed
patterns=[r'/workspace/[A-Za-z0-9]',r'/home/agent/[A-Za-z0-9]',r'codex://threads/',r'https?://(?:www\.)?chatgpt\.com/(?:c|g|share)/',r'github_pat_[A-Za-z0-9_]{20,}',r'gh[pousr]_[A-Za-z0-9]{20,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'appgprj_[A-Za-z0-9]+',r'libfile_[A-Za-z0-9]+',r'rtc_u\d+_']
scanned=archives=downloads=0
archive_inventory=[]
def scan(data):
 global scanned,archives
 if zipfile.is_zipfile(io.BytesIO(data)):
  archives+=1
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
   archive_inventory.append(z.namelist())
   for manifest in ['manifest.json','ai-weekly/release-manifest.json']:
    if manifest in z.namelist():
     manifest_data=json.loads(z.read(manifest));files=manifest_data['files'];prefix='' if manifest=='manifest.json' else 'ai-weekly/'
     entries=files.items() if isinstance(files,dict) else [(v['path'],v) for v in files]
     declared=[]
     for path,info in entries:
      payload=z.read(prefix+path);assert len(payload)==info['bytes'] and sha(payload)==info['sha256'];declared.append(prefix+path)
     assert set(declared+[manifest])==set(z.namelist())
   for name in z.namelist():
    assert not name.startswith('/') and '..' not in Path(name).parts
    if not name.endswith('/'):scan(z.read(name))
 else:
  scanned+=1;text=data.decode('utf8','replace');assert not any(re.search(pattern,text) for pattern in patterns),'Private marker detected'
for f in n.rglob('*'):
 if f.is_file():scan(f.read_bytes())
for sample in samples.values():
 assert sha(sample['html'].encode())==sample['sha256'];scan(sample['html'].encode())
 for f in sample['files']:
  downloads+=1;data=base64.b64decode(f['body'],validate=True) if f.get('encoding')=='base64' else f['body'].encode();assert sha(data)==f['sha256'];scan(data)
assert downloads==5 and archives==2
scan(html.encode())
for value in parsed:scan(json.dumps(value,ensure_ascii=False).encode())
m=read(new/'dist/data-app-build.json')
for key in ['html','snapshot']:
 data=(new/'dist'/m[key]['path']).read_bytes();assert len(data)==m[key]['bytes'] and sha(data)==m[key]['sha256'];scan(data)
assert read(new/'dist'/m['snapshot']['path'])==e
js=r'''
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const [oldDir,newDir]=process.argv.slice(1),read=p=>fs.readFileSync(p,'utf8');
const a=JSON.parse(read(oldDir+'/articles.json')).articles,b=JSON.parse(read(newDir+'/articles.json')).articles;
const load=dir=>{let text=read(dir+'/ReportContent.jsx'),ctx=vm.createContext({URLSearchParams,location:{hash:''},URL});vm.runInContext(text.slice(text.indexOf('function topicMatch('),text.indexOf('export function ReportContent()')),ctx);let r=read(dir+'/IllustratedArticle.jsx');vm.runInContext(r.slice(r.indexOf('const portal69Sources='),r.indexOf('const R=')),ctx);return ctx;};
const old=load(oldDir),now=load(newDir);let tests=0;
for(const x of a){for(const topic of ['ai','business','business-model','operations','all','other']){assert.equal(now.topicMatch(x,topic),old.topicMatch(x,topic));tests++;}for(const id of [x.id,x.id+':lead','article:'+x.id]){let original=old.resolvePortal71Links(old.resolvePortal69Links(x.body,id),id);assert.equal(now.resolvePortal73Links(now.resolvePortal71Links(now.resolvePortal69Links(x.body,id),id),id),original);tests++;}}
const research=b.filter(x=>x.section==='research');assert.equal(research.length,73);assert.equal(research.filter(x=>x.topics.includes('ai')).length,48);assert.equal(research.filter(x=>now.topicMatch(x,'ai')).length,49);
for(const x of b){now.location.hash='#read/'+encodeURIComponent(x.id)+'?view=all&topic=operations';assert.equal(now.readRoute().id,x.id);assert.equal(now.readRoute().topic,'operations');tests++;}
const additions=b.filter(x=>!a.some(y=>x.id===y.id));assert.equal(additions.length,2);
assert.equal(now.topicMatch(additions.find(x=>x.id.includes('order-alert')),'ai'),false);
assert.equal(now.topicMatch(additions.find(x=>x.id.includes('reservation-policy')),'ai'),true);
for(const x of additions)for(const id of [x.id,x.id+':section:0','article:'+x.id]){const resolved=now.resolvePortal73Links(x.body+'\n[ledger](sources.md)',id);assert.ok(resolved.includes(new URL('sources.md',x.sourceUrl).href));tests++;}
console.log(JSON.stringify({tests,rawAi:48,effectiveAi:49,alertAi:false,browser:false}));
'''
r=subprocess.run(['node','-e',js,str(o),str(n)],check=True,capture_output=True,text=True)
result={'result':'PASS','originalsPreserved':91,'storiesPreserved':71,'queriesPreserved':146,'unchangedFiles':kept,'sections':sections,'downloads':downloads,'recursiveArchives':archives,'privacyPayloads':scanned,'queryEvidence':query_checks,'archiveInventory':archive_inventory,'actualJsHelpers':json.loads(r.stdout),'htmlBytes':len(html.encode()),'htmlSha256':sha(html.encode()),'inheritedRuntimeLimit':'Protected manifest and hosting configuration preserved byte-for-byte. Historical full-runtime hosting mismatch remains; no retry or alteration. Official installed/prebuilt build is a separate check.','limits':'Offline static and actual pure-JavaScript helpers only. No browser, HTTP, source re-verification, publication, remote history or visual checks.'}
print(json.dumps(result,ensure_ascii=False,indent=2))
