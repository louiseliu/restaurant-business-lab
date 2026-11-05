"""Install this article into its official prepared report without modifying infrastructure."""
import hashlib,json,shutil,sys
from pathlib import Path
PROJECT=Path(sys.argv[1]);A=Path(__file__).resolve().parent;R=PROJECT/'src/content/report'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(A/'article-entry.json');st=read(A/'illustrated-story.json');d=read(A/'article-reviewed-data.json');prepared=read(PROJECT/'src/data.json')
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']
assert prepared['surface']=='report' and prepared.get('id'),'Use the official report preparer first'
# Current identity must already be the recorded artifact or a newly prepared one, never a portal.
assert len(prepared.get('queries',{}))==2,'Do not replace a multi-article portal'
if (R/'articles.json').exists():
 old=read(R/'articles.json');assert len(old['articles'])==1 and old['articles'][0]['id']==a['id']
 assert old['articles'][0]==a,'Existing article differs; preserve it and reconcile before editing'
 assert read(R/'illustrated-stories.json')=={a['id']:st},'Existing story differs; preserve user edits'
 assert prepared['queries']==d['queries'],'Existing reviewed queries differ; preserve them'
 for f in (A/'shared').iterdir():
  if f.is_file():assert (R/f.name).read_bytes()==f.read_bytes(),'Existing reader differs; reconcile edits'
 for name in ['OverrideDiagrams.jsx','override-diagrams.css','override-source-previews.json']:assert (R/name).read_bytes()==(A/name).read_bytes()
 print('Existing article matches the frozen source; no writes made.');sys.exit(0)
for f in (A/'shared').iterdir():
 if f.is_file():shutil.copyfile(f,R/f.name)
for name in ['OverrideDiagrams.jsx','override-diagrams.css','override-source-previews.json']:shutil.copyfile(A/name,R/name)
write(R/'articles.json',{'articles':[a]});write(R/'illustrated-stories.json',{a['id']:st});write(R/'samples.json',{})
d['id']=prepared['id'];d['buildStatus']='creating';write(PROJECT/'src/data.json',d)
print('Installed one frozen article; retained official prepared report identity.')

