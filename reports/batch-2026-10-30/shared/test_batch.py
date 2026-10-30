"""Offline entry/diagram/provenance checks; optional target report directory regression."""
import hashlib,json,subprocess,sys,tempfile
from pathlib import Path
base=Path(__file__).resolve().parent.parent
entries=list(base.glob('*/article-entry.json'));assert len(entries)==3
for file in entries:
 a=json.loads(file.read_text());s=json.loads((file.parent/'illustrated-story.json').read_text());d=json.loads((file.parent/'article-reviewed-data.json').read_text())
 assert a['id']==s['id'];assert a['publishedAt']=='2026-10-30T04:06:26Z'
 assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']
 expected='e6f524b36e3efd43e7c7d43ee43439852030412c' if file.parent.name=='voice-receptionist' else 'e7575c5632a6bd4e1fd1752ff4e954fee29f615c'
 assert '/'+expected+'/' in a['sourceUrl']
 for diagram in ['diagram','secondDiagram']:assert len(s[diagram]['nodes'])>=3
 assert len(d['queries'])==2
 if file.parent.name=='restocking-controls':assert a['topics']==['business-model']
 assert d['buildStatus']=='complete'
# Additive merge and second-run idempotence against an empty synthetic catalog.
with tempfile.TemporaryDirectory() as temp:
 target=Path(temp);(target/'articles.json').write_text('{"articles": []}');(target/'illustrated-stories.json').write_text('{}')
 command=[sys.executable,str(base/'shared/apply_batch.py'),str(base),str(target)]
 subprocess.run(command,check=True,capture_output=True);one=(target/'articles.json').read_bytes();subprocess.run(command,check=True,capture_output=True)
 assert (target/'articles.json').read_bytes()==one
 assert len(json.loads(one)['articles'])==3
print('3 approved entries, original hashes, exact first-commit timestamps, 6 diagrams, independent snapshots and idempotent merge passed')
