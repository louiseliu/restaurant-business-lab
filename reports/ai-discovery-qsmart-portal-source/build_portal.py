"""Local-only official build. Args: PRODUCTION_DIR AI_DISCOVERY_SOURCE QSMART_SOURCE NODE DATA_APP_MJS SANITIZATION_DIR."""
import json,os,re,subprocess,sys
from pathlib import Path
P,A,Q,NODE,TOOL,SAN=[Path(v).resolve() for v in sys.argv[1:]];T=Path(__file__).resolve().parent;ROOT=P/'portal65'
assert not (ROOT/'dist').exists(),'Preserve existing build; use fresh isolated directory'
env=dict(os.environ)
for key in ['CODEX_SESSION_ID','CODEX_THREAD_ID']:env.pop(key,None)
def run(*args):subprocess.run([str(a) for a in args],check=True,env=env)
run(sys.executable,T/'test_portal_merge_guard.py',A,Q,P/'baseline64')
run(sys.executable,T/'integrate65.py',ROOT/'src',A,Q)
run(sys.executable,SAN/'test_sanitization.py')
# Read-only check: never rewrite frozen article inputs or unrelated baseline content.
run(sys.executable,SAN/'sanitize_site_content.py',ROOT/'src/content/report','--check')
d=json.loads((ROOT/'src/data.json').read_text());d['buildStatus']='complete';(ROOT/'src/data.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
run(NODE,TOOL,'prepare','--project-dir',ROOT)
run(NODE,TOOL,'build','--project-dir',ROOT,'--separate-data')
output=ROOT/'.data-app-offline/exports/timeline65-discovery-qsmart.html'
run(NODE,TOOL,'export-offline','--project-dir',ROOT,'--output',output)
assert 'name="data-app-local-thread"' not in output.read_text();(P/'timeline65-discovery-qsmart.html').write_bytes(output.read_bytes())
run(sys.executable,T/'test_portal_preservation.py',P,A,Q)
run(NODE,T/'test_reader_routes.mjs',ROOT/'src/content/report')
