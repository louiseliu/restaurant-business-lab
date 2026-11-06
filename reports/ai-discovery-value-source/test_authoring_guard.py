"""Exercise no-overwrite guards using disposable copies of a finished article."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile

A=Path(__file__).resolve().parent
SOURCE=Path(sys.argv[1]).resolve()
def hashes(root):
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
def read(root,path):return json.loads((root/path).read_text())
def write(root,path,value):(root/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def change_article(root):
 path='src/content/report/articles.json';v=read(root,path);v['articles'][0]['body']+='\nUser edit';write(root,path,v)
def change_story(root):
 path='src/content/report/illustrated-stories.json';v=read(root,path);next(iter(v.values()))['lead']+=' User edit';write(root,path,v)
def change_query(root):
 path='src/data.json';v=read(root,path);next(iter(v['queries'].values()))['rows'][0]['User edit']='Keep this';write(root,path,v)
def change_reader(root):
 p=root/'src/content/report/IllustratedArticle.jsx';p.write_text(p.read_text()+'\n// User edit\n')
def change_css(root):
 p=root/'src/content/report/ai-discovery-value-diagrams.css';p.write_text(p.read_text()+'\n/* User edit */\n')
def add_query(root):
 path='src/data.json';v=read(root,path);v['queries']['other-article']={'rows':[]};write(root,path,v)
def remove_identity(root):
 path='src/data.json';v=read(root,path);v.pop('id',None);write(root,path,v)

checks=[]
with tempfile.TemporaryDirectory(prefix='ai-discovery-value-guard-') as tmp:
 for name,mutate in [('identical',None),('changed-original',change_article),('changed-story',change_story),('changed-query',change_query),('changed-reader',change_reader),('changed-style',change_css),('multi-article-query',add_query),('missing-report-identity',remove_identity)]:
  root=Path(tmp)/name
  shutil.copytree(SOURCE,root,ignore=shutil.ignore_patterns('dist','.data-app-offline','node_modules'))
  if mutate:mutate(root)
  before=hashes(root)
  result=subprocess.run([sys.executable,str(A/'prepare_standalone.py'),str(root)],capture_output=True,text=True)
  assert (result.returncode==0)==(mutate is None),name
  assert before==hashes(root),name+' changed files before rejecting or confirming'
  checks.append({'case':name,'result':'no-op' if mutate is None else 'rejected before writes','filesPreserved':True})
print(json.dumps({'checks':checks,'scope':'Disposable local copies only; no external writes or browser claims.'},ensure_ascii=False,indent=2))
