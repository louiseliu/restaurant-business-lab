#!/usr/bin/env python3
"""Independent local-only additive portal audit. Does not execute app/browser or alter production."""
from pathlib import Path
import json,hashlib,re,base64,zipfile,io,argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--baseline',type=Path,default=Path('research-work/supplier-alias-portal-production/portal63'))
parser.add_argument('--production',type=Path,default=Path('research-work/camera-reuse-portal-production'))
parser.add_argument('--frozen-source',type=Path,default=Path('research-work/camera-reuse-production/source'))
parser.add_argument('--output',type=Path,default=Path(__file__).parent)
args=parser.parse_args()
BASE=args.baseline;PROD=args.production;NEW=PROD/'portal64';SRC=args.frozen_source;OUT=args.output
OUT.mkdir(parents=True,exist_ok=True);checks=[]
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def check(name,condition,detail=None):checks.append({'test':name,'pass':bool(condition),'detail':detail})
def report(p):return p/'src/content/report'
b=report(BASE);n=report(NEW)
ba=read(b/'articles.json')['articles'];na=read(n/'articles.json')['articles'];bs=read(b/'illustrated-stories.json');ns=read(n/'illustrated-stories.json');bd=read(BASE/'src/data.json');nd=read(NEW/'src/data.json');sample=read(n/'samples.json')
id='research-2026-11-06-camera-reuse-note'; q='diagram-'+id
check('counts', [len(na),len(ns),sum(a['section']=='research' for a in na),len(sample),sum('ai' in a.get('topics',[]) for a in na),len(nd['queries'])]==[84,64,64,2,42,131])
check('unique article IDs',len({a['id'] for a in na})==84)
check('old article objects and order unchanged',[a for a in na if a['id']!=id]==ba)
check('old story objects unchanged',{k:ns[k] for k in bs}==bs)
check('old reviewed queries unchanged',{k:nd['queries'][k] for k in bd['queries']}==bd['queries'])
check('exact new query scope',set(nd['queries'])-set(bd['queries'])=={q,q+':second'})
check('samples byte-identical',(n/'samples.json').read_bytes()==(b/'samples.json').read_bytes())
oldfiles={str(p.relative_to(BASE)):sha(p.read_bytes()) for p in BASE.rglob('*') if p.is_file() and not str(p.relative_to(BASE)).startswith(('dist/','.data-app-offline/'))}
changed=[p for p,h in oldfiles.items() if not (NEW/p).is_file() or sha((NEW/p).read_bytes())!=h]
allowed={'src/data.json','src/content/report/articles.json','src/content/report/illustrated-stories.json','src/content/report/IllustratedArticle.jsx'}
check('only authorized additive integration changes to baseline',set(changed)==allowed,changed)
check('frozen article exact',next(a for a in na if a['id']==id)==read(SRC/'article-entry.json'))
check('frozen story exact',ns[id]==read(SRC/'illustrated-story.json'))
frozen=read(SRC/'frozen.json');a=next(a for a in na if a['id']==id)
check('first-body commit and time',frozen['commit']=='eaf8d57c523197ca67a04662f5d48dc45a201c22' and a['publishedAt']=='2026-11-06T01:10:58Z' and frozen['commit'] in a['sourceUrl'])
check('frozen body hash',sha(a['body'].encode())==frozen['sha256'])
check('new reviewed queries exact',all(nd['queries'][k]==v for k,v in read(SRC/'article-reviewed-data.json')['queries'].items()))
for suffix,key in [('', 'diagram'),(':second','secondDiagram')]:
 query=nd['queries'][q+suffix];diag=ns[id][key]
 check('diagram rows '+key,query['rows']==diag['nodes'])
 check('component evidence '+key,any(q+suffix in x['componentIds'] for x in query['source']['metricDefinitions']))
 check('fixed source '+key,any(frozen['commit'] in x['detail'] for x in query['source']['evidenceFlow']))
comp=(n/'CameraReuseDiagrams.jsx').read_text();reader=(n/'IllustratedArticle.jsx').read_text()
check('component uses real reviewed rows and public source wrapper',all(x in comp for x in ['DataComponent','queryId={q}','sourceRows={rows}','displayRows={rows}','data-reviewed-rows','sourcePreviews={previews}']))
check('reader binds second diagram independently',"id={`${item.id}:second`}" in reader and 'camera-reuse-' in reader)
check('new component/copy source bytes',all((n/x).read_bytes()==(SRC/x).read_bytes() for x in ['CameraReuseDiagrams.jsx','camera-reuse-diagrams.css','camera-reuse-source-previews.json']))
check('UI routes/styles/legacy/download code unchanged',all((n/x).read_bytes()==(b/x).read_bytes() for x in ['ReportContent.jsx','timeline.css','Samples.jsx','samples.css','LegacyReport.jsx']))
check('status complete identity unchanged',nd['buildStatus']=='complete' and nd['id']==bd['id'])
manifest=read(NEW/'dist/data-app-build.json')
for name in ['html','snapshot']:
 x=manifest[name]; data=(NEW/'dist'/x['path']).read_bytes();check('build manifest '+name,len(data)==x['bytes'] and sha(data)==x['sha256'])
check('split reviewed data exact',read(NEW/'dist'/manifest['snapshot']['path'])==nd)
html=PROD/'timeline64-camera-reuse.html'; raw=html.read_text(); scripts=re.findall(r'<script([^>]*)>(.*?)</script>',raw,re.S)
joined=''.join(s for attrs,s in scripts if 'application/json' in attrs)
check('offline JSON chunks reconstruct full reviewed snapshot',json.loads(joined)==nd)
check('compiled new title and two layouts',all(x in raw for x in [a['title'],'camera-reuse-chain','camera-reuse-options',q]))
# Scan exported text and recursively decoded attachment ZIP members without contacting a source.
patterns={
 'private_workspace':r'(?:/workspace/(?:scratch|shared)|/home/agent/|/[a-z]+_notes/)',
 'secret_token':r'(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-(?:proj-)?[A-Za-z0-9_-]{30,}|AKIA[0-9A-Z]{16})',
 'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
 'private_download':r'(?:sediment://|sandbox:/|codex://threads/[0-9a-f-]{20,}|chatgpt\.com/(?:c|g)/[0-9a-f-]{20,})'
}
seen=set(); scans=[];hits=[]; zip_entries=[]
def scan(name,data,depth=0):
 digest=sha(data)
 if digest in seen:return
 seen.add(digest);scans.append({'name':name,'bytes':len(data),'sha256':digest})
 if data[:2]==b'PK':
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   for f in z.infolist():
    if not f.is_dir():zip_entries.append(name+'!'+f.filename);scan(name+'!'+f.filename,z.read(f),depth+1)
  return
 text=data.decode('utf-8',errors='replace')
 for key,p in patterns.items():
  if re.search(p,text):hits.append({'file':name,'pattern':key})
 for i,m in enumerate(re.finditer(r'data:[^\s\"\'<>]*?;base64,([A-Za-z0-9+/=]{32,})',text)):
  try:scan(name+f'::base64-{i}',base64.b64decode(m[1],validate=True),depth+1)
  except ValueError:pass
scan(html.name,html.read_bytes())
files=[]
for sid,s in sample.items():
 scan(sid+'::html',s['html'].encode())
 for f in s['files']:
  data=base64.b64decode(f['body']) if f['encoding']=='base64' else f['body'].encode()
  files.append(sid+'/'+f['name']);check('download digest '+files[-1],sha(data)==f['sha256']);scan(files[-1],data)
check('five sample downloads',len(files)==5,files)
check('recursive privacy signatures',not hits,{'hits':hits,'scanned_objects':len(scans),'zip_entries':len(zip_entries),'scope':'Signature scan only; not a proof that every kind of private information is absent.'})
result={'audit':'independent newly executed local static tests','tests':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'artifact_sha256':sha(html.read_bytes()),'recursive_scans':scans,'zip_entries':zip_entries,'limitations':['No browser, visual rendering, interactions, HTTP/file preview, original-site visits, uploads or remote writes were performed.','Existing historical audit/log files were not modified or reissued as fresh verification.','Privacy scan is signature-based and covers offline HTML, inline base64 runtime and all five sample downloads including ZIP members.']}
(OUT/'independent-audit-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':result['passed'],'failed':result['failed'],'failed_tests':[c for c in checks if not c['pass']]},ensure_ascii=False,indent=2))
raise SystemExit(bool(result['failed']))
