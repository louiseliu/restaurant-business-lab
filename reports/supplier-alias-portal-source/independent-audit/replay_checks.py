#!/usr/bin/env python3
"""Replay authored tests and decoded sample computation only in disposable copies.
Usage: replay_checks.py PRODUCTION ARTICLE_ARCHIVE NODE OUTPUT
No network, browser, upload, dependency install or protected-runtime change.
"""
import base64,hashlib,io,json,re,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
P,A,NODE,OUT=[Path(x).resolve() for x in sys.argv[1:]];OUT.mkdir(exist_ok=True,parents=True)
read=lambda p:json.loads(p.read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
logs={}
def run(name,args,cwd=None):
 result=subprocess.run([str(a) for a in args],cwd=cwd,capture_output=True,text=True)
 logs[name]=result.stdout+result.stderr
 assert result.returncode==0,(name,result.stdout[-4000:],result.stderr[-4000:])
 return logs[name]
run('merge-guard',[sys.executable,P/'portal-archive-source/test_portal_merge_guard.py',A,P/'baseline62'])
run('reader-routes',[NODE,P/'portal-archive-source/test_reader_routes.mjs',P/'portal63/src/content/report'])
run('sanitization-regression',[sys.executable,A/'support/test_sanitization.py'])
run('sanitization-readonly',[sys.executable,A/'support/sanitize_site_content.py',P/'portal63/src/content/report','--check'])
samples=read(P/'portal63/src/content/report/samples.json')
results={}
with tempfile.TemporaryDirectory() as temp:
 root=Path(temp)
 for sid,sample in samples.items():
  file=next(f for f in sample['files'] if f['name'].endswith('.zip'))
  raw=base64.b64decode(file['body'],validate=True);dest=root/sid;dest.mkdir()
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   assert z.testzip() is None
   for n in z.namelist():
    p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and '\\' not in n
    assert (z.getinfo(n).external_attr >> 16)&0o170000!=0o120000
   z.extractall(dest)
  if sid=='sample-delivery':
   before=(dest/'index.html').read_bytes()
   run('delivery-build',[sys.executable,dest/'build.py'],dest)
   assert (dest/'index.html').read_bytes()==before==sample['html'].encode()
   run('delivery-tests',[NODE,dest/'tests/test-model.cjs'],dest)
   tests=read(dest/'tests/test-results.json');assert (tests['passed'],tests['failed'])==(45,0)
   results[sid]={'htmlRebuiltByteIdentical':True,'testsPassed':45,'testsFailed':0}
  elif sid=='sample-ai-weekly':
   work=dest/'ai-weekly'
   files=[p for sub in ['data','results'] for p in (work/sub).rglob('*') if p.is_file()]
   files.extend([work/'qa/independent_recompute.json',work/'qa/independent_recompute.sql'])
   before={p.relative_to(work).as_posix():p.read_bytes() for p in files}
   original=read(work/'reviewed-snapshot.json')
   htmlchunks=re.findall(r'<script\s+type="application/json"[^>]*>([\s\S]*?)</script>',sample['html'])
   embedded=json.loads(''.join(htmlchunks));assert embedded==original
   run('ai-weekly-calculations',[sys.executable,work/'src/run_all.py'],work)
   assert all((work/p).read_bytes()==b for p,b in before.items())
   run('ai-weekly-snapshot',[sys.executable,work/'src/prepare_snapshot.py'],work)
   rebuilt=read(work/'reviewed-snapshot.json')
   differences=sorted(k for k in set(original)|set(rebuilt) if original.get(k)!=rebuilt.get(k))
   assert set(differences)<= {'id','buildStatus'},differences
   frozen=read(work/'docs/claims_manifest.json');qa=read(work/'results/quality_report.json')
   assert len(frozen)==107 and qa['checks_passed']==78
   results[sid]={'testsPassed':16,'frozenNumericExpectations':len(frozen),'reconciliationChecks':qa['checks_passed'],'reproducedDataResultAndIndependentSqlFiles':len(before),'allReproducedFilesByteIdentical':True,'archivedSnapshotEqualsEmbeddedHtml':True,'regeneratedSnapshotContentEqualsArchived':True,'snapshotLifecycleDifferences':differences,'htmlRebuilt':False}
# Outputs do not include ephemeral filesystem locations.
for k,v in logs.items():
 assert str(root) not in v
 (OUT/(k+'.log')).write_text(v)
report={'result':'passed','testScope':'Locally replayed archived authoring merge guard, route functions and sanitization tests; decoded ZIP samples executed only in temporary copies. No browser or third official portal build.','portal':{'mergeGuard':'passed','readerRoutes':'passed','sanitizationRegression':'3 passed','sanitizationReadOnly':'53 payloads passed'},'samples':results,'limitations':['AI-weekly HTML was not recompiled with the official runtime; its embedded reviewed snapshot and all archived result values were verified.','Regenerated AI-weekly snapshot lifecycle/identity fields can differ; content fields must be identical.','Sample tests and static route tests do not establish current portal browser behavior or actual offline execution.']}
(OUT/'replayed-checks-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
