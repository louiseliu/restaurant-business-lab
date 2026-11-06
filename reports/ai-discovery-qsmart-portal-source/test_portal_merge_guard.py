"""Test preservation and preflight refusal on temporary copies, without external writes."""
import json,subprocess,sys,tempfile,shutil
from pathlib import Path
A,Q,BASE=[Path(v).resolve() for v in sys.argv[1:]];SCRIPT=Path(__file__).with_name('integrate65.py').resolve();QID='research-2026-10-30-qsmart-note'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def snap(root):return {str(p.relative_to(root)):('symlink',str(p.readlink())) if p.is_symlink() else p.read_bytes() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
passed=[]
with tempfile.TemporaryDirectory() as temp:
 root=Path(temp)/'src';shutil.copytree(BASE/'src',root);R=root/'content/report'
 def run():return subprocess.run([sys.executable,str(SCRIPT),str(root),str(A),str(Q)],capture_output=True,text=True)
 a=read(R/'articles.json');target=next(v for v in a['articles'] if v['id']!=QID);target['excerpt']+=' Existing user edit';target['body']+='\nExisting user paragraph';write(R/'articles.json',a)
 s=read(R/'illustrated-stories.json');k=next(k for k in s if k!=QID);s[k]['lead']+=' Existing user edit';write(R/'illustrated-stories.json',s)
 d=read(root/'data.json');q=next(k for k in d['queries'] if QID not in k);d['queries'][q]['source']['label']+=' Existing user edit';d['exportPreferences']={'selected':['pdf'],'destinations':[]};write(root/'data.json',d)
 result=run();assert result.returncode==0,result.stderr
 lookup={v['id']:v for v in read(R/'articles.json')['articles']}
 assert all(lookup[v['id']]==v for v in a['articles'] if v['id']!=QID)
 assert all(read(R/'illustrated-stories.json')[k]==v for k,v in s.items() if k!=QID)
 assert all(read(root/'data.json')['queries'][k]==v for k,v in d['queries'].items())
 assert read(root/'data.json')['exportPreferences']==d['exportPreferences'];passed.append('Unrelated user body, excerpt, story, query and export policy edits preserved')
 frozen=snap(root);r=run();assert r.returncode!=0 and snap(root)==frozen;passed.append('Repeated merge refused before writes')
 for kind in ['id','query','revision-query','count','component','stylesheet','preview','revision-component','revision-style','symlink','qsmart-body','qsmart-metadata','qsmart-story','qsmart-query','reader']:
  shutil.rmtree(root);shutil.copytree(BASE/'src',root);R=root/'content/report'
  if kind=='id':
   p=R/'articles.json';v=read(p);v['articles'][0]['id']=read(A/'article-entry.json')['id'];write(p,v)
  elif kind in ['query','revision-query']:
   p=root/'data.json';v=read(p);key=next(iter(read(A/'article-reviewed-data.json')['queries'])) if kind=='query' else 'diagram-'+QID+':revision-2026-11-06';v['queries'][key]=v['queries'].pop(next(iter(v['queries'])));write(p,v)
  elif kind=='symlink':(R/'QSmartRevision.jsx').symlink_to('missing-user-file.jsx')
  elif kind in ['component','stylesheet','preview','revision-component','revision-style']:
   name={'component':'AIDiscoveryDiagrams.jsx','stylesheet':'ai-discovery-value-diagrams.css','preview':'ai-discovery-value-source-previews.json','revision-component':'QSmartRevision.jsx','revision-style':'qsmart-revision.css'}[kind];(R/name).write_text('Existing user file\n')
  elif kind.startswith('qsmart-'):
   if kind in ['qsmart-body','qsmart-metadata']:
    p=R/'articles.json';v=read(p);obj=next(x for x in v['articles'] if x['id']==QID);obj['body' if kind=='qsmart-body' else 'excerpt']+=' User edit';write(p,v)
   elif kind=='qsmart-story':
    p=R/'illustrated-stories.json';v=read(p);v[QID]['lead']+=' User edit';write(p,v)
   else:
    p=root/'data.json';v=read(p);v['queries']['diagram-'+QID]['source']['label']+=' User edit';write(p,v)
  elif kind=='reader':
   p=R/'IllustratedArticle.jsx';p.write_text(p.read_text().replace("['limits','未知与核查']","['limits','User label']"))
  else:
   p=R/'articles.json';v=read(p);v['articles'].pop();write(p,v)
  frozen=snap(root);r=run();assert r.returncode!=0 and snap(root)==frozen,kind;passed.append(kind+' conflict refused before writes')
report={'checksPassed':len(passed),'checks':passed,'scope':'Temporary local copies only; edited Q-Smart content is refused rather than overwritten.'}
(Path(__file__).parent/'merge-guard-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
