"""Rebuild samples.json from versioned public sample files, never fetch or publish.
Run: python generate_samples.py --repo <repository-checkout> --output <report-authoring>/samples.json
"""
import argparse,base64,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--output',required=True);a=p.parse_args();repo=Path(a.repo);data=json.loads(Path(__file__).with_name('samples-metadata.json').read_text())
for sample in data.values():
 folder=repo/sample.pop('repositoryDirectory');html=(folder/sample.pop('entrypoint')).read_bytes()
 assert hashlib.sha256(html).hexdigest()==sample['sha256'],sample['id']+' entrypoint differs from reviewed version'
 sample['html']=html.decode()
 for file in sample['files']:
  raw=(folder/file['name']).read_bytes();assert hashlib.sha256(raw).hexdigest()==file['sha256'],file['name']+' differs from reviewed version'
  file['body']=base64.b64encode(raw).decode()
Path(a.output).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Generated 2 verified sample entries; no network, upload or deployment.')
