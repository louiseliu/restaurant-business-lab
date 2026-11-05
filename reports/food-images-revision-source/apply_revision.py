"""Apply a guarded same-ID article revision and its two scoped query updates.

Usage: python apply_revision.py TARGET_PROJECT BATCH_SOURCE PREVIOUS_FOOD_IMAGE_SOURCE
Use only an isolated current author-project copy. This script does not build or publish.
"""
import hashlib,json,subprocess,sys
from pathlib import Path
target,batch,previous=map(Path,sys.argv[1:]);article=batch/'food-images';report=target/'src/content/report'
def read(p):return json.loads(p.read_text())
def canon(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
data=read(target/'src/data.json');revised=read(article/'article-reviewed-data.json');old=read(previous/'article-reviewed-data.json')
assert set(revised['queries'])==set(old['queries']) and len(old['queries'])==2
for query_id,expected in old['queries'].items():
    assert query_id in data['queries'],'Missing expected query'
    assert data['queries'][query_id] in [expected,revised['queries'][query_id]],'Unexpected query edit; preserve user changes: '+query_id
# The repository's exact updater validates prior body, metadata, story, and first time
# before writing. Do not replace a failed guard with an unconditional merge.
subprocess.run([sys.executable,str(batch/'shared/update_article.py'),str(article),str(report)],check=True)
original_id=data['id'];data['queries'].update(revised['queries']);data['generatedAt']=revised['generatedAt'];data['buildStatus']='complete'
assert data['id']==original_id
content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
if (target/'src/data.json').read_text()!=content:(target/'src/data.json').write_text(content)
print('Same ID, first time, artifact identity and unrelated queries preserved. Run sanitizer, official build and QA next.')
