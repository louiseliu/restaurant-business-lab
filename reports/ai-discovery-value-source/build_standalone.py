"""Official local-only build from frozen evidence; never upload or publish."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
A=Path(__file__).resolve().parent
P=Path(sys.argv[1]).resolve();NODE=Path(sys.argv[2]).resolve();PLUGIN=Path(sys.argv[3]).resolve()
assert A==P/'source','Place this archive at PRODUCTION_DIR/source before rebuilding'
ENV={k:v for k,v in os.environ.items() if k not in ['CODEX_SESSION_ID','CODEX_THREAD_ID']}
def run(*args):subprocess.run([str(a) for a in args],check=True,env=ENV)
run(sys.executable,A/'make_article.py',A/'note.md',A/'frozen.json')
root=P/'standalone'
if not root.exists():
 run(NODE,PLUGIN/'scripts/prepare-data-app.mjs','--surface','report','--output',root,'--snapshot',A/'article-reviewed-data.json')
 hashes={str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in root.rglob('*') if f.is_file()}
 (P/'standalone-prepared-sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
run(sys.executable,A/'prepare_standalone.py',root)
run(sys.executable,A/'support/test_sanitization.py')
run(sys.executable,A/'support/sanitize_site_content.py',root/'src/content/report','--check')
d=json.loads((root/'src/data.json').read_text());d['buildStatus']='complete';(root/'src/data.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
run(NODE,PLUGIN/'scripts/data-app.mjs','prepare','--project-dir',root)
run(NODE,PLUGIN/'scripts/data-app.mjs','build','--project-dir',root,'--separate-data')
out=root/'.data-app-offline/exports/ai-discovery-value.html'
run(NODE,PLUGIN/'scripts/data-app.mjs','export-offline','--project-dir',root,'--output',out)
shutil.copyfile(out,P/'ai-discovery-value.html')
run(sys.executable,A/'test_standalone.py',P,A/'note.md')
