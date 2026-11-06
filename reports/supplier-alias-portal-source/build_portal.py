"""Local-only official build. Args: PRODUCTION_DIR SUPPLIER_ALIAS_SOURCE NODE DATA_APP_MJS SANITIZATION_DIR."""
import json,os,re,subprocess,sys
from pathlib import Path
P,A,NODE,TOOL,SAN=[Path(v).resolve() for v in sys.argv[1:]];T=Path(__file__).resolve().parent;ROOT=P/'portal63'
assert not (ROOT/'dist').exists(),'Preserve existing build; use fresh isolated directory'
env=dict(os.environ)
for key in ['CODEX_SESSION_ID','CODEX_THREAD_ID']:env.pop(key,None)
def run(*args):subprocess.run([str(a) for a in args],check=True,env=env)
run(sys.executable,T/'test_portal_merge_guard.py',A,P/'baseline62')
run(sys.executable,T/'integrate63.py',ROOT/'src',A)
run(sys.executable,SAN/'test_sanitization.py')
# Read-only check: never rewrite frozen article inputs or unrelated baseline content.
run(sys.executable,SAN/'sanitize_site_content.py',ROOT/'src/content/report','--check')
d=json.loads((ROOT/'src/data.json').read_text());d['buildStatus']='complete';(ROOT/'src/data.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
run(NODE,TOOL,'prepare','--project-dir',ROOT)
run(NODE,TOOL,'build','--project-dir',ROOT,'--separate-data')
output=ROOT/'.data-app-offline/exports/timeline63-supplier-alias.html'
run(NODE,TOOL,'export-offline','--project-dir',ROOT,'--output',output)
html=re.sub(r'<meta\s+name="data-app-local-thread"[^>]*>','',output.read_text());(P/'timeline63-supplier-alias.html').write_text(html)
run(sys.executable,T/'test_portal_preservation.py',P,A)
run(NODE,T/'test_reader_routes.mjs',ROOT/'src/content/report')
