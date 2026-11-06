"""Exercise preservation and refusal before any write, using temporary copies only."""
import copy,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
from reader_patch import IDS,NAMES
A,Q,B=[Path(v).resolve() for v in sys.argv[1:]];T=Path(__file__).parent.resolve();checks=[]
def hashes(p):return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file()}
def jsonedit(p,fn):
 v=json.loads(p.read_text());fn(v);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def run_case(name,edit,passExpected=False,after=None):
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp)/'src';shutil.copytree(B/'src',root);r=root/'content/report';inputs=[A,Q];edit(root,r)
  before=hashes(root);result=subprocess.run([sys.executable,T/'integrate67.py',root,*inputs],capture_output=True,text=True)
  assert (result.returncode==0)==passExpected,(name,result.stderr)
  if not passExpected:assert hashes(root)==before,name+' wrote before refusing'
  if after:after(root,r)
  checks.append({'case':name,'passed':True,'noPartialWrite':not passExpected})
def edits(root,r):
 jsonedit(r/'articles.json',lambda x:x['articles'][0].update({'summary':'User edited summary','body':x['articles'][0]['body']+'\nUser note'}))
 jsonedit(r/'illustrated-stories.json',lambda x:next(iter(x.values())).update({'userEdit':'keep'}))
 jsonedit(root/'data.json',lambda x:(x['queries'][next(iter(x['queries']))].update({'userEdit':'keep'}),x.update({'exportPreferences':{'keep':True}})))
def after(root,r):
 assert any(x.get('summary')=='User edited summary' and x['body'].endswith('User note') for x in json.loads((r/'articles.json').read_text())['articles'])
 assert any(x.get('userEdit')=='keep' for x in json.loads((r/'illustrated-stories.json').read_text()).values())
 assert json.loads((root/'data.json').read_text())['exportPreferences']=={'keep':True}
run_case('Preserve user prose, summary, story, query and export preferences',edits,True,after)
run_case('Reject unexpected counts',lambda s,r:jsonedit(r/'articles.json',lambda x:x['articles'].pop()))
run_case('Reject duplicate article identity',lambda s,r:jsonedit(r/'articles.json',lambda x:x['articles'][0].update({'id':IDS[0]})))
run_case('Reject new query collision',lambda s,r:jsonedit(s/'data.json',lambda x:x['queries'].update({'diagram-'+IDS[0]:x['queries'].pop(next(iter(x['queries'])))})))
run_case('Reject missing report identity',lambda s,r:jsonedit(s/'data.json',lambda x:x.pop('id')))
run_case('Reject changed reader anchor',lambda s,r:(r/'IllustratedArticle.jsx').write_text((r/'IllustratedArticle.jsx').read_text().replace("import React from 'react';", "import React from 'react'")))
for name in sum(NAMES,[]):
 run_case('Reject existing file '+name,lambda s,r,n=name:(r/n).write_text('User owned'))
run_case('Reject dangling destination symlink',lambda s,r:(r/NAMES[0][0]).symlink_to('missing-user-file'))
def repeat(s,r):
 subprocess.run([sys.executable,T/'integrate67.py',s,A,Q],check=True,capture_output=True)
run_case('Reject repeated integration',repeat)
# Frozen source rejection: each actual input byte mutation must fail before writes.
fp=json.loads((T/'input-fingerprints.json').read_text())
for i,records in enumerate(fp):
 for name in records:
  with tempfile.TemporaryDirectory() as tmp:
   temp=Path(tmp);src=temp/'input';shutil.copytree([A,Q][i],src,ignore=shutil.ignore_patterns('__pycache__'))
   f=src/name;f.write_bytes(f.read_bytes()+b'\n')
   root=temp/'src';shutil.copytree(B/'src',root);before=hashes(root);inputs=[A,Q];inputs[i]=src
   result=subprocess.run([sys.executable,T/'integrate67.py',root,*inputs],capture_output=True,text=True)
   assert result.returncode and hashes(root)==before,name
   checks.append({'case':'Reject frozen input '+str(i)+'/'+name,'passed':True,'noPartialWrite':True})
print(json.dumps({'passed':len(checks),'cases':checks,'browserTests':False},ensure_ascii=False,indent=2))
