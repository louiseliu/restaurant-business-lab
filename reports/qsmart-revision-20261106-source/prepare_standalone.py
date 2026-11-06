"""Install one same-ID Q-Smart revision into a new prepared report, with no-overwrite guards."""
from pathlib import Path
import hashlib,json,shutil,sys
A=Path(__file__).resolve().parent;PROJECT=Path(sys.argv[1]);R=PROJECT/'src/content/report'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(A/'article-entry.json');s=read(A/'illustrated-story.json');d=read(A/'article-reviewed-data.json');current=read(PROJECT/'src/data.json')
assert current.get('id') and current['surface']=='report'
assert len(current.get('queries',{}))==3,'Do not replace a multi-article portal'
assert current['queries']==d['queries'],'Prepared snapshot differs; preserve it'
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['revisedBodySha256']
files=[(f,f.name) for f in (A/'shared').iterdir() if f.is_file()]+[(A/n,n) for n in ['QSmartRevision.jsx','qsmart-revision.css']]
if (R/'articles.json').exists():
 assert read(R/'articles.json')=={'articles':[a]},'Article changed; preserve edits'
 assert read(R/'illustrated-stories.json')=={a['id']:s},'Story changed; preserve edits'
 assert current['queries']==d['queries'],'Reviewed queries changed; preserve edits'
 for src,name in files:assert (R/name).read_bytes()==src.read_bytes(),'Authored reader changed; preserve edits'
 print('Identical frozen revision; no writes.');sys.exit(0)
for src,name in files:
 target=R/name
 assert not target.is_symlink(),'Do not replace a symlink'
 # Official new report includes only its two starter content files.
 if target.exists() and name not in ['ReportContent.jsx','report.css']:
  raise AssertionError('Unexpected pre-existing authored file: '+name)
for src,name in files:shutil.copyfile(src,R/name)
write(R/'articles.json',{'articles':[a]});write(R/'illustrated-stories.json',{a['id']:s});write(R/'samples.json',{})
d['id']=current['id'];write(PROJECT/'src/data.json',d)
print('Installed three scoped diagrams in a new standalone extraction; original article ID retained.')
