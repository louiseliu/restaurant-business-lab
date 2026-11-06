import json,hashlib,pathlib,re,sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
for idx,name in enumerate(['robot-subscription','ai-practice']):
 p=pathlib.Path(sys.argv[idx+1]) if len(sys.argv)>3 else ROOT/(name+'-production')/'source';m=read(p/'manifest.json');fs=m['files'];fs=fs if isinstance(fs,list) else [dict(v,path=k) for k,v in fs.items()]
 for f in fs:
  assert sha(p/f['path'])==f['sha256'];assert (p/f['path']).stat().st_size==f['bytes']
 e=read(p/'article-entry.json');s=read(p/'illustrated-story.json');d=read(p/'article-reviewed-data.json');f=read(p/'frozen.json')
 assert e['body']==(p/'note.md').read_text()
 assert e['originalBodySha256']==f['sha256']==sha(p/'note.md')
 assert f['sourcesSha256']==sha(p/'sources.md')
 assert e['firstGit']==f['commit'] and e['publishedAt']==f['time']==e['updatedAt']
 assert '/blob/'+f['commit']+'/' in e['sourceUrl']
 assert s['technicalDetails'][0]['body']==(p/'sources.md').read_text()
 parts=re.split(r'^## ',e['body'],flags=re.M)
 assert s['sections']==[{'title':part.split('\n',1)[0],'body':part.split('\n',1)[1].strip().split('\n\n')} for part in parts[1:]]
 for key,suffix in [('diagram',''),('secondDiagram',':second')]:
  q='diagram-'+e['id']+suffix;query=d['queries'][q];assert query['rows']==s[key]['nodes']
  assert query['source']['metricDefinitions'][0]['componentIds']==[q]
  assert [a['title'].split(' · ')[0] for a in query['source']['evidenceFlow'][1:]]==s[key]['sourceIds']
  assert all(isinstance(v,str) for row in query['rows'] for v in row.values())
 # Scan actual author payload only; scripts intentionally contain privacy test patterns.
 patterns=[r'appgprj_[A-Za-z0-9]{6,}',r'libfile_[A-Za-z0-9]{6,}',r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/',r'codex://threads/',r'/workspace/[A-Za-z0-9]',r'/home/agent/[A-Za-z0-9]',r'rtc_u\d+_',r'https?://git\.chatgpt-team\.site',r'gh[pousr]_[A-Za-z0-9]{25,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
 for file in ['article-entry.json','illustrated-story.json','article-reviewed-data.json','note.md','sources.md','reviewed-illustration-copy.json']:
  for pat in patterns:assert not re.search(pat,(p/file).read_text()),(name,file,pat)
 results.append({'article':e['id'],'manifestFiles':len(fs),'commit':f['commit'],'time':f['time'],'manifest':True,'bodyLedgerFrozenMetadata':True,'queriesAndSourceScope':True,'privacyPatternScan':True,'diagramRows':[len(s[k]['nodes']) for k in ['diagram','secondDiagram']]})
p=(pathlib.Path(sys.argv[3]) if len(sys.argv)>3 else ROOT/'digitalhuman-recipe-portal-production/portal67')/'src';a=read(p/'content/report/articles.json')['articles'];s=read(p/'content/report/illustrated-stories.json');d=read(p/'data.json')
assert len(a)==87 and len(s)==67;ids=[a['id'] for a in a];assert len(set(ids))==87
assert not set(ids)&{r['article'] for r in results}
newq=set()
for idx,name in enumerate(['robot-subscription','ai-practice']):
 source=pathlib.Path(sys.argv[idx+1]) if len(sys.argv)>3 else ROOT/(name+'-production')/'source'
 q=read(source/'article-reviewed-data.json')['queries'];assert not set(q)&(set(d['queries'])|newq);newq.update(q)
report={'status':'pass_local_static_inputs','articles':results,'base':{'articles':len(a),'stories':len(s),'queries':len(d['queries'])},'addition':{'articles':2,'queries':len(newq)},'limits':['No external access or independent remote readback.','No browser, visual or interaction testing.','Credential/privacy scanning is pattern based, not an absolute privacy guarantee.','No source files modified.']}
(pathlib.Path(__file__).parent/'input-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
