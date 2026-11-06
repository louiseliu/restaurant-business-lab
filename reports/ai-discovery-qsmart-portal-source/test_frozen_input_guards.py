"""Alter each consumed frozen input in a temporary copy; require no portal writes."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
A,Q,BASE=[Path(v).resolve() for v in sys.argv[1:]];T=Path(__file__).resolve().parent
fingerprints=json.loads((T/'input-fingerprints.json').read_text())
def snap(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
checks=[]
with tempfile.TemporaryDirectory() as temp:
 W=Path(temp);shutil.copytree(BASE/'src',W/'src')
 for label,folder in [('aiDiscovery',A),('qsmartRevision',Q)]:
  target=W/label;target.mkdir()
  for name in fingerprints[label]:shutil.copyfile(folder/name,target/name)
 before=snap(W/'src')
 for label in fingerprints:
  for name in fingerprints[label]:
   p=W/label/name;original=p.read_bytes();p.write_bytes(original+b'\n')
   r=subprocess.run([sys.executable,str(T/'integrate65.py'),str(W/'src'),str(W/'aiDiscovery'),str(W/'qsmartRevision')],capture_output=True,text=True)
   assert r.returncode!=0 and 'Frozen input changed: '+name in r.stderr
   assert snap(W/'src')==before,'Portal changed after input refusal'
   p.write_bytes(original);checks.append(label+'/'+name)
report={'checksPassed':len(checks),'checks':checks,'result':'Every modified frozen input was refused before any portal writes. Only temporary copies were changed.'}
(T/'frozen-input-guard-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
