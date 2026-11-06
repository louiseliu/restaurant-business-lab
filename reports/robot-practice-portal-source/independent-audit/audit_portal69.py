"""Independent, local-only static audit. Writes only this audit's JSON result.
Usage: python audit/audit_portal69.py from the production directory.
No browser, network, compilation, archive extraction or historical audit copying.
"""
import base64, hashlib, io, json, re, zipfile, sys, subprocess
from pathlib import Path, PurePosixPath
AUDIT=Path(__file__).resolve().parent
P=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else AUDIT.parent
B=P/'baseline67'; N=P/'portal69'; O=P.parent/'digitalhuman-recipe-portal-production/portal67'
R=N/'src/content/report'; BR=B/'src/content/report'
inputs=[Path(sys.argv[2]).resolve(),Path(sys.argv[3]).resolve()] if len(sys.argv)>3 else [P.parent/'robot-subscription-production/source',P.parent/'ai-practice-production/source']
read=lambda p:json.loads(p.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=[];failures=[]
def ck(value,label):
 checks.append(label)
 if not value:failures.append(label)
a,oa=read(R/'articles.json'),read(BR/'articles.json');s,os=read(R/'illustrated-stories.json'),read(BR/'illustrated-stories.json');d,od=read(N/'src/data.json'),read(B/'src/data.json')
lookup={x['id']:x for x in a['articles']};oldlookup={x['id']:x for x in oa['articles']}
newids=[read(p/'article-entry.json')['id'] for p in inputs]
counts={'research':sum(x['section']=='research' for x in a['articles']),'originals':len(a['articles']),'stories':len(s),'queries':len(d['queries']),'aiResearch':sum(x['section']=='research' and 'ai' in x['topics'] for x in a['articles'])}
ck(counts==dict(research=69,originals=89,stories=69,queries=142,aiResearch=46),'69/89/69/142/46 content counts')
ck((len(oa['articles']),len(os),len(od['queries']))==(87,67,138),'87/67/138 actual baseline counts')
ck(len(lookup)==89 and set(lookup)-set(oldlookup)==set(newids),'Only two unique article additions')
for k,v in oldlookup.items():ck(lookup.get(k)==v,'Preserved original: '+k)
for k,v in os.items():ck(s.get(k)==v,'Preserved story: '+k)
for k,v in od['queries'].items():ck(d['queries'].get(k)==v,'Preserved query: '+k)
ck({k:v for k,v in d.items() if k not in ['queries','generatedAt','buildStatus']}=={k:v for k,v in od.items() if k not in ['queries','generatedAt','buildStatus']},'Preserved report identity, settings, preferences and filters')
ck({k:v for k,v in a.items() if k not in ['articles','sourceCommit','syncNote']}=={k:v for k,v in oa.items() if k not in ['articles','sourceCommit','syncNote']},'Preserved remaining catalog metadata')
ck(d['buildStatus']=='complete','Complete build lifecycle')
ck(set(s)=={x['id'] for x in a['articles'] if x['section']=='research'},'One story per research article')
ck(a['articles']==sorted(a['articles'],key=lambda x:(x['publishedAt'],x['id']),reverse=True),'Chronological first-entry ordering')
frozen=read(P/'baseline67-sha256.json');changed=[]
for rel,h in frozen.items():
 raw=(B/rel).read_bytes();ck(sha(raw)==h,'Frozen baseline: '+rel);ck(raw==(O/rel).read_bytes(),'Original 67 baseline: '+rel) if O.exists() else None
 if raw!=(N/rel).read_bytes():changed.append(rel)
allowed={'src/data.json','src/content/report/articles.json','src/content/report/illustrated-stories.json','src/content/report/IllustratedArticle.jsx','src/content/report/ReportContent.jsx'}
ck(set(changed)==allowed,'Exactly five existing source files changed')
contentOld={str(x.relative_to(BR)) for x in BR.rglob('*') if x.is_file()};contentNew={str(x.relative_to(R)) for x in R.rglob('*') if x.is_file()}
added={'RobotSubscriptionDiagrams.jsx','robotsubscription-diagrams.css','robotsubscription-source-previews.json','AIPracticeDiagrams.jsx','aipractice-diagrams.css','aipractice-source-previews.json'}
ck(contentNew-contentOld==added and not contentOld-contentNew,'Only six content files added; none removed')
reader=(R/'IllustratedArticle.jsx').read_text();oldreader=(BR/'IllustratedArticle.jsx').read_text()
# Remove precisely the independently inspected append-only reader changes.
reverted=reader
for line in ["import RobotSubscriptionSourcePreviews from './robotsubscription-source-previews.json';\n","import {RobotSubscriptionDiagram} from './RobotSubscriptionDiagrams.jsx';\n","import AIPracticeSourcePreviews from './aipractice-source-previews.json';\n","import {AIPracticeDiagram} from './AIPracticeDiagrams.jsx';\n"," if(diagram.layout?.startsWith('robotsubscription-'))return <RobotSubscriptionDiagram diagram={diagram} id={id} rows={diagramRows}/>;\n"," if(diagram.layout?.startsWith('aipractice-'))return <AIPracticeDiagram diagram={diagram} id={id} rows={diagramRows}/>;\n"]:
 ck(reverted.count(line)==1,'One reader insertion: '+line.strip());reverted=reverted.replace(line,'')
preview=f"id.includes('{newids[0]}')?RobotSubscriptionSourcePreviews:id.includes('{newids[1]}')?AIPracticeSourcePreviews:"
ck(reader.count(preview)==1,'Article-scoped preview branches');reverted=reverted.replace(preview,'')
reverted=re.sub(r'^const portal69Sources=.*\n','',reverted,flags=re.M)
reverted=re.sub(r'^function resolvePortal69Links.*\n','',reverted,flags=re.M)
reverted=reverted.replace('value={resolvePortal69Links(children,id)}','value={children}')
ck(reverted==oldreader,'All other reader bytes preserved, including routing, original text and navigation')
newqueries={};bindings=[]
for index,p in enumerate(inputs):
 entry,story,reviewed,fr=[read(p/x) for x in ['article-entry.json','illustrated-story.json','article-reviewed-data.json','frozen.json']];ID=entry['id']
 ck(lookup[ID]==entry and s[ID]==story,'Exact frozen article/story: '+ID)
 ck(entry['body']==(p/'note.md').read_text() and sha(entry['body'].encode())==entry['originalBodySha256']==fr['sha256'],'Complete original body: '+ID)
 ck(entry['firstGit']==fr['commit'] and entry['publishedAt']==entry['updatedAt']==fr['time'],'First commit/time retained: '+ID)
 ck(story['technicalDetails'][0]['body']==(p/'sources.md').read_text() and sha((p/'sources.md').read_bytes())==fr['sourcesSha256'],'Complete source ledger: '+ID)
 expected=[]
 for section in re.split(r'^## ',entry['body'],flags=re.M)[1:]:
  heading,body=section.split('\n',1);expected.append({'title':heading,'body':body.strip().split('\n\n')})
 ck(story['sections']==expected,'Complete original narrative sections: '+ID)
 previews=read(next(p.glob('*source-previews.json')))
 for name in added:
  if (p/name).exists():ck((p/name).read_bytes()==(R/name).read_bytes(),'Frozen added component: '+name)
 for field,suffix in [('diagram',''),('secondDiagram',':second')]:
  qid='diagram-'+ID+suffix;q=d['queries'][qid];diagram=story[field];flow=q['source']['evidenceFlow'][1:]
  ck(q==reviewed['queries'][qid] and q['rows']==diagram['nodes'],'Exact reviewed visual rows: '+qid)
  ck(q['source']['metricDefinitions'][0]['componentIds']==[qid],'Exact visual component binding: '+qid)
  ck([v['title'].split(' · ')[0] for v in flow]==diagram['sourceIds'],'Visual source IDs: '+qid)
  ck(all(v['detail'] in previews for v in flow),'All visual sources have scoped previews: '+qid)
  ck(q['source']['files']==[entry['path']] and q['source']['evidenceFlow'][0]['detail']==entry['sourceUrl'],'Visual fixed-body provenance: '+qid)
  bindings.append({'query':qid,'layout':diagram['layout'],'sourceIds':diagram['sourceIds'],'sourceUrls':[v['detail'] for v in flow]})
 newqueries.update(reviewed['queries'])
ck(set(d['queries'])-set(od['queries'])==set(newqueries) and len(newqueries)==4,'Exactly four new queries')
for names,layout in [('RobotSubscriptionDiagrams.jsx','robotsubscription-timelines'),('AIPracticeDiagrams.jsx','aipractice-evidence')]:
 text=(R/names).read_text();ck('const q=`diagram-${id}`' in text and 'sourceRows={rows} displayRows={rows}' in text and "diagram.layout==='"+layout+"'" in text,'Custom render branch and reviewed data: '+names)
# Every legacy and new visual remains accounted for.
bound={'network','comparison'}
for ID,story in s.items():
 fields=[('diagram','')]
 if story.get('secondDiagram') and not story.get('numericChart'):fields.append(('secondDiagram',':second'))
 if story.get('thirdDiagram'):fields.append(('thirdDiagram',':third'))
 if story.get('revision'):fields.append(('revision',':revision-2026-11-06'))
 for field,suffix in fields:
  qid='diagram-'+ID+suffix;bound.add(qid);nodes=story[field]['diagram']['nodes'] if field=='revision' else story[field]['nodes'];ck(d['queries'][qid]['rows']==nodes,'Global visual row binding: '+qid)
 if story.get('numericChart'):bound.add('visual-'+ID)
ck(bound==set(d['queries']),'All 142 queries accounted for')
htmlpath=P/'timeline69-robot-practice.html';raw=htmlpath.read_bytes();html=raw.decode()
ck(len(raw)==14077756 and sha(raw)=='135406278b0fdd62d3f11bf0c79f6697dfe8c9946ea9a33aeacc108df0a299dc','Exact supplied artifact identity')
ck(raw==(N/'.data-app-offline/exports'/htmlpath.name).read_bytes(),'Official offline export equals delivered HTML')
objects=[]
for literal in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',html):
 try:objects.append(json.loads(json.loads(literal)))
 except (ValueError,TypeError):pass
samples=read(R/'samples.json');ck(samples==read(BR/'samples.json') and len(samples)==2,'Both embedded samples unchanged')
for label,obj in [('catalog',a),('stories',s),('samples',samples)]:ck(sum(v==obj for v in objects)==1,'Compiled complete JSON: '+label)
chunks=re.findall(r'<script type="application/json"(?: id="data-app-reviewed-snapshot"| data-app-snapshot-chunk)>(.*?)</script>',html,re.S);snapshot=''.join(chunks).encode()
ck(snapshot==(N/'src/data.json').read_bytes(),'Every offline snapshot chunk concatenates to exact source bytes')
build=read(N/'dist/data-app-build.json')
for field in ['html','snapshot']:
 item=build[field];value=(N/'dist'/item['path']).read_bytes();ck(sha(value)==item['sha256'] and len(value)==item['bytes'],'Exact build manifest: '+field)
ck(read(N/'dist'/build['snapshot']['path'])==d and sha(snapshot)==build['snapshot']['sha256'],'Split and offline snapshot equivalence')
ck(not re.search(r'(?:src|href)=["\x27]https?://',html),'No statically declared remote assets')
patterns={'private-chat':r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/','local-path':r'/(?:workspace|home/agent|Users)/[A-Za-z0-9]','private-identifier':r'(?:appgprj_|libfile_|Sentinel_|rtc_u\d+_)[A-Za-z0-9_-]{6,}','private-thread':r'codex://threads/','internal-repository':r'https?://git\.chatgpt-team\.site','thread-metadata':r'data-app-local-thread["\x27]\s+content=','private-key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----','credential':r'(?<![A-Za-z0-9_-])(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-(?:proj-)?[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16})'}
stats={'payloads':0,'zipContainers':0,'zipMembers':0,'releaseManifests':0,'downloads':0};hits=[]
def scan(value,label,depth=0):
 ck(depth<=10,'Bounded embedded archive depth: '+label)
 if depth>10:return
 if zipfile.is_zipfile(io.BytesIO(value)):
  stats['zipContainers']+=1
  with zipfile.ZipFile(io.BytesIO(value)) as z:
   ck(z.testzip() is None and len(z.namelist())==len(set(z.namelist())),'ZIP CRC and unique names: '+label)
   contents={n:z.read(n) for n in z.namelist() if not n.endswith('/')}
   for n,b in contents.items():
    stats['zipMembers']+=1;ck(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts,'Bounded ZIP member: '+n);scan(b,label+'!'+n,depth+1)
    if n.endswith('release-manifest.json'):
     stats['releaseManifests']+=1;prefix=n.rsplit('/',1)[0]+'/' if '/' in n else ''
     for entry in json.loads(b)['files']:
      target=prefix+entry['path'];ck(target in contents and len(contents[target])==entry['bytes'] and sha(contents[target])==entry['sha256'],'Nested manifest: '+entry['path'])
 else:
  stats['payloads']+=1;text=value.decode('utf8','replace')
  for kind,pat in patterns.items():
   if re.search(pat,text):hits.append({'payload':label,'kind':kind})
for p in R.rglob('*'):
 if p.is_file():scan(p.read_bytes(),'content/'+str(p.relative_to(R)))
scan(raw,'portable.html');scan(snapshot,'offline-reviewed-snapshot.json');scan((N/'src/data.json').read_bytes(),'reviewed-data.json')
for i,v in enumerate(objects):scan(json.dumps(v,ensure_ascii=False).encode(),'compiled-json-'+str(i))
for ID,sample in samples.items():
 b=sample['html'].encode();ck(sha(b)==sample['sha256'],'Embedded HTML hash: '+ID);scan(b,ID+'/embedded.html')
 for file in sample['files']:
  stats['downloads']+=1;b=base64.b64decode(file['body'],validate=True) if file.get('encoding')=='base64' else file['body'].encode();ck(sha(b)==file['sha256'],'Download hash: '+file['name']);scan(b,ID+'/'+file['name'])
ck(stats['downloads']==5 and stats['zipContainers']==2 and stats['releaseManifests']==1,'All five downloads and nested manifest inspected');ck(not hits,'No privacy-pattern hits')
fp=read(P/'portal-archive-source/input-fingerprints.json');fpcount=0
for p,entries in zip(inputs,fp):
 for name,v in entries.items():
  fpcount+=1;b=(p/name).read_bytes();ck(len(b)==v['bytes'] and sha(b)==v['sha256'],'Input fingerprint: '+p.parent.name+'/'+name)
# Execute actual pure helpers, and ensure the remainder of portal behavior is unchanged.
portal_reader=(R/'ReportContent.jsx').read_text()
reverted_portal=re.sub(r'^function topicMatch.*\n','',portal_reader,flags=re.M).replace('topicMatch(a,r.topic)','a.topics.includes(r.topic)').replace("topicMatch(a,'business-model')","a.topics.includes('business-model')")
ck(reverted_portal==(BR/'ReportContent.jsx').read_text(),'Only scoped topic adapter changes in portal reader')
helper=json.loads(subprocess.check_output(['node',str(AUDIT/'test_scoped_fixes.mjs'),str(P)],text=True))
ck(helper['status']=='passed','Actual scoped helper execution')
report={'scope':'Independent local static audit of exact 69-study offline portal; no publication or browser acceptance claim.','result':'passed-with-explicit-unverified-scope' if not failures else 'needs-revision','artifact':{'name':htmlpath.name,'bytes':len(raw),'sha256':sha(raw)},'counts':counts,'preservation':{'originals':87,'stories':67,'queries':138,'baselineFilesCompared':len(frozen),'changedFiles':sorted(changed),'addedContentFiles':sorted(added),'sourceUserEdits':'Readable 67-story baseline bytes and data only; unavailable original-site edits not verified.'},'newVisualBindings':bindings,'coverage':{'assertions':len(checks),'compiledObjects':len(objects),'snapshotChunks':len(chunks),'snapshotBytes':len(snapshot),'snapshotSha256':sha(snapshot),'inputFingerprints':fpcount,**stats},'privacyPatternHits':hits,'issues':failures,'repairValidation':helper,'resolvedFindings':['Scoped robot business-model topic matching repaired without changing frozen entry.','Scoped frozen-source relative links repaired for two new articles without changing old reader output.'],'notVerified':['Browser rendering, mobile, dark mode, accessibility, popups, editing, history, scrolling, print or export interactions.','Fresh independent compilation or execution of embedded calculators; existing compiled bytes, exact snapshots, and extracted topic/link helpers were inspected.','External primary webpages, restricted PDFs, remote Git provenance or real restaurant effects.','Original-site access, upload, publication or sharing.'],'retainedLimitations':['New robot subscription and AI practice articles preserve inherited root language; existing language attributes unchanged.','Existing Fourth S2 title omits page 19; unchanged and unresolved.','Five historical uncertain audit archives were neither copied nor retried.','Pattern scanning cannot guarantee absence of every possible sensitive datum.']}
(AUDIT/'portal69-static-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(failures))
