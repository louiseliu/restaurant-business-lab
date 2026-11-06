"""Copy a supplied verified 71-story baseline into new isolated working directories.
Arguments: PRODUCTION_DIR EXISTING_PORTAL71
Does not modify its input, upload or publish. Requires the complete baseline.
"""
import hashlib,json,shutil,sys
from pathlib import Path
P=Path(sys.argv[1]).resolve();BASE=Path(sys.argv[2]).resolve();A=Path(__file__).resolve().parent
expected=json.loads((A/'baseline71-sha256.json').read_text())
exclude={'dist','.data-app-offline','node_modules','__pycache__'}
actual={str(f.relative_to(BASE)):hashlib.sha256(f.read_bytes()).hexdigest() for f in BASE.rglob('*') if f.is_file() and not exclude.intersection(f.relative_to(BASE).parts)}
assert actual==expected,'Baseline differs; preserve edits and reconcile instead of overwriting'
assert not (P/'baseline71').exists() and not (P/'portal73').exists(),'Use a fresh production directory'
for name in ['baseline71','portal73']:shutil.copytree(BASE,P/name,ignore=shutil.ignore_patterns(*exclude))
(P/'baseline71-sha256.json').write_text(json.dumps(expected,indent=2)+'\n')
print('Copied verified baseline into two isolated directories; original unchanged.')
