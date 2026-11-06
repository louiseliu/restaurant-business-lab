"""Fresh independent rebuild. Args: PRODUCTION BASELINE71 RESERVATION_SOURCE ALERT_SOURCE NODE DATA_APP_MJS."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
p,baseline,res,alert,node,tool=map(Path,sys.argv[1:]);p=p.resolve();target=p/'independent-rebuild'
assert not target.exists(),'Use a fresh target; preserve previous builds'
shutil.copytree(p/'portal-archive-source',target/'portal-archive-source',ignore=shutil.ignore_patterns('__pycache__','independent-audit'))
author=target/'portal-archive-source'
subprocess.run([sys.executable,str(author/'prepare_portal.py'),str(target),str(baseline)],check=True)
subprocess.run([sys.executable,str(author/'build_portal.py'),str(target),str(res),str(alert),str(node),str(tool),str(res/'support')],check=True)
m=json.loads((p/'portal73/dist/data-app-build.json').read_text());files=['timeline73-reservation-alert.html','portal73/dist/data-app-build.json']+['portal73/dist/'+m[k]['path'] for k in ['html','snapshot']]
results=[]
for rel in files:
 data=(p/rel).read_bytes();assert data==(target/rel).read_bytes(),rel;results.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
print(json.dumps({'result':'PASS','freshBuild':True,'officialPrepareBuildExport':True,'identicalOutputs':results},indent=2))
