"""Exercise additive merge refusal and preservation using temporary copies only."""
import json,subprocess,sys,tempfile,shutil,hashlib
from pathlib import Path
A=Path(sys.argv[1]); BASE=Path(sys.argv[2]); SCRIPT=A/'integrate54.py'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def snap(root):return {str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
with tempfile.TemporaryDirectory() as temp:
 root=Path(temp)/'src';shutil.copytree(BASE/'src',root);R=root/'content/report'
 def run():return subprocess.run([sys.executable,str(SCRIPT),str(root),str(A)],capture_output=True,text=True)
 # Additive integration must retain an existing user edit rather than replace it.
 p=R/'articles.json';a=read(p);a['articles'][0]['excerpt']+=' Existing user edit';a['articles'][0]['body']+='\nExisting user paragraph';write(p,a)
 s=read(R/'illustrated-stories.json');k=next(iter(s));s[k]['lead']+=' Existing user edit';write(R/'illustrated-stories.json',s)
 d=read(root/'data.json');q=next(iter(d['queries']));d['queries'][q]['source']['label']+=' Existing user edit';write(root/'data.json',d)
 before=snap(root);r=run();assert r.returncode==0,r.stderr
 after=read(R/'articles.json');lookup={v['id']:v for v in after['articles']}
 assert all(lookup[v['id']]==v for v in a['articles']);assert all(read(R/'illustrated-stories.json')[k]==v for k,v in s.items())
 assert all(read(root/'data.json')['queries'][k]==v for k,v in d['queries'].items())
 frozen=snap(root);r=run();assert r.returncode!=0 and snap(root)==frozen,'Repeat merge must refuse before writing'
 # Conflicting incoming identity/query or unexpected article count must stop without writes.
 for kind in ['id','query','count']:
  shutil.rmtree(root);shutil.copytree(BASE/'src',root);R=root/'content/report'
  if kind=='id':
   p=R/'articles.json';v=read(p);v['articles'][0]['id']=read(A/'article-entry.json')['id'];write(p,v)
  elif kind=='query':
   p=root/'data.json';v=read(p);v['queries'][next(iter(read(A/'article-reviewed-data.json')['queries']))]=v['queries'].pop(next(iter(v['queries'])));write(p,v)
  else:
   p=R/'articles.json';v=read(p);v['articles'].pop();write(p,v)
  frozen=snap(root);r=run();assert r.returncode!=0 and snap(root)==frozen,kind
print('Passed: existing user body metadata/story/query edits preserved; repeated, identity, query and count conflicts refused before writes.')

