"""Build an isolated, pre-copied 59-story portal using the installed official tools.
Arguments: PRODUCTION_DIR NOTE_MD NODE DATA_APP_MJS SANITIZATION_DIR
Never uploads, archives, publishes or changes the baseline.
"""
import json,os,re,subprocess,sys
from pathlib import Path
P=Path(sys.argv[1]).resolve(); NOTE=Path(sys.argv[2]).resolve()
NODE=Path(sys.argv[3]).resolve(); TOOL=Path(sys.argv[4]).resolve(); SAN=Path(sys.argv[5]).resolve()
T=P/'portal-archive-source'; A=P/'archive-source'; ROOT=P/'portal60'
assert not (ROOT/'dist').exists(), 'Use an isolated source copy without prior dist; preserve any existing build separately.'
env=dict(os.environ)
for key in ['CODEX_SESSION_ID','CODEX_THREAD_ID']: env.pop(key,None)
def run(*args): subprocess.run([str(a) for a in args],check=True,env=env)
run(sys.executable,T/'test_portal_merge_guard.py',A,P/'baseline59')
run(sys.executable,T/'integrate60.py',ROOT/'src',A)
run(sys.executable,SAN/'test_sanitization.py')
run(sys.executable,SAN/'sanitize_site_content.py',ROOT/'src/content/report')
run(sys.executable,SAN/'sanitize_site_content.py',ROOT/'src/content/report','--check')
data=json.loads((ROOT/'src/data.json').read_text()); data['buildStatus']='complete'
(ROOT/'src/data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
run(NODE,TOOL,'prepare','--project-dir',ROOT)
run(NODE,TOOL,'build','--project-dir',ROOT,'--separate-data')
output=ROOT/'.data-app-offline/exports/timeline60-platform-appeals.html'
run(NODE,TOOL,'export-offline','--project-dir',ROOT,'--output',output)
html=re.sub(r'<meta\s+name="data-app-local-thread"[^>]*>','',output.read_text())
(P/'timeline60-platform-appeals.html').write_text(html)
run(sys.executable,T/'test_portal_preservation.py',P,P/'baseline59',NOTE)
run(NODE,T/'test_reader_routes.mjs',ROOT/'src/content/report')
