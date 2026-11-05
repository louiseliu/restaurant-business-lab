"""Static same-ID checks. Optional argument: directory of the exact prior three JSONs.

The optional prior source can be read from commit
90a2cc6e90e87dd84294840e4e00dfbb6e7b4a43. No network or publication is performed.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

here = Path(__file__).resolve().parent
batch = here.parent
root = batch.parent.parent

def read(path):
    return json.loads(path.read_text())

def canonical(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

entry = read(here / 'article-entry.json')
story = read(here / 'illustrated-story.json')
data = read(here / 'article-reviewed-data.json')
guard = read(here / 'update-guard.json')
manifest = read(batch / 'manifest.json')
revision = manifest['sourceRevisions']['food-images']
assert entry['id'] == story['id'] == guard['id'] == 'research-2026-10-30-food-images-note'
assert entry['publishedAt'] == '2026-10-30T04:06:26Z'
assert entry['updatedAt'] == revision['updatedAt']
assert '/' + revision['sourceCommit'] + '/' in entry['sourceUrl']
assert entry['body'] == (root / entry['path']).read_text()
assert hashlib.sha256(entry['body'].encode()).hexdigest() == entry['originalBodySha256']
assert len(data['queries']) == 2
assert '过去每年的代运营和摄影两项支出合计超过6万元' in entry['body']
assert '无法认作AI带来的年净节省' in entry['body']
assert '也不能当作单店金额' in entry['body']
assert any(s['url'] == 'https://www.chinanews.com.cn/cj/2026/06-26/10647834.shtml' for s in story['sources'])
for key, diagram in [('diagram', 'diagram-' + entry['id']), ('secondDiagram', 'diagram-' + entry['id'] + ':second')]:
    assert story[key]['nodes'] == data['queries'][diagram]['rows']
    assert any(x['detail'] == entry['sourceUrl'] for x in data['queries'][diagram]['source']['evidenceFlow'])

if len(sys.argv) > 1:
    old_dir = Path(sys.argv[1])
    old_entry = read(old_dir / 'article-entry.json')
    old_story = read(old_dir / 'illustrated-story.json')
    assert canonical(old_entry) == guard['previousEntryCanonicalSha256']
    assert canonical(old_story) == guard['previousStoryCanonicalSha256']
    assert old_entry['originalBodySha256'] == guard['previousOriginalBodySha256']
    for k in ['id', 'path', 'title', 'section', 'topics', 'publishedAt', 'excerpt']:
        assert entry[k] == old_entry[k], k
    for k in ['diagram', 'secondDiagram']:
        assert story[k] == old_story[k], k
    assert entry['body'].split('## 决策边界：')[0] == old_entry['body'].split('## 决策边界：')[0]

    with tempfile.TemporaryDirectory() as temp:
        target = Path(temp)
        unrelated = {'id': 'untouched', 'body': '用户已有内容'}
        unrelated_story = {'lead': '用户已有图文'}

        def seed(e, s):
            (target / 'articles.json').write_text(json.dumps({'articles': [e, unrelated], 'other': 'kept'}, ensure_ascii=False))
            (target / 'illustrated-stories.json').write_text(json.dumps({e['id']: s, 'untouched': unrelated_story}, ensure_ascii=False))

        def run():
            return subprocess.run([sys.executable, str(batch / 'shared/update_article.py'), str(here), str(target)], capture_output=True, text=True)

        def snapshot():
            return tuple((target / f).read_bytes() for f in ['articles.json', 'illustrated-stories.json'])

        seed(old_entry, old_story)
        assert run().returncode == 0
        after = snapshot()
        assert read(target / 'articles.json')['articles'] == [entry, unrelated]
        assert read(target / 'articles.json')['other'] == 'kept'
        assert read(target / 'illustrated-stories.json') == {entry['id']: story, 'untouched': unrelated_story}
        assert run().returncode == 0 and snapshot() == after
        for kind in ['body', 'metadata', 'story']:
            e, s = copy.deepcopy(old_entry), copy.deepcopy(old_story)
            if kind == 'body':
                e['body'] += '\n用户追加内容\n'
                e['originalBodySha256'] = hashlib.sha256(e['body'].encode()).hexdigest()
            elif kind == 'metadata':
                e['excerpt'] += ' 用户修改'
            else:
                s['lead'] += ' 用户修改'
            seed(e, s)
            before = snapshot()
            assert run().returncode != 0 and snapshot() == before, kind
    print('Same-ID/body/first-time/two-diagram/source binding, guarded merge, unrelated-content preservation, idempotence and three user-edit rejection cases passed.')
else:
    print('Current-source checks passed; prior-source guard scenarios not run (provide prior JSON directory).')
