import json, hashlib, re, sys
from pathlib import Path
root = Path(__file__).parent
p = root / 'shift-constraints'
a = json.loads((p / 'article-entry.json').read_text())
s = json.loads((p / 'illustrated-story.json').read_text())
d = json.loads((p / 'article-reviewed-data.json').read_text())
g = json.loads((p / 'update-guard.json').read_text())
assert a['id'] == s['id'] == g['id'] == 'research-2026-11-01-shift-constraints-note'
assert a['publishedAt'] == '2026-11-01T14:03:18Z'
assert a['updatedAt'] == '2026-11-05T03:09:32Z'
assert a['firstGit'] == 'daa2e94fd3780500f5d3a7e3291e1a3c1df86743'
assert g['preserveFirstGit'] == a['firstGit'] and g['preservePublishedAt'] == a['publishedAt']
assert '2b466f57a0176f05386b4e0915443e2a28d3b2e8' in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest() == a['originalBodySha256'] == '7042c61fbb7377d3a37a84b0375cb6d19b814f3440b291c3b7c88506e15c0b89'
note = root.parents[1] / a['path']
if note.exists():
    assert note.read_text() == a['body'], 'Frozen source body differs'
assert a['topics'] == ['ai', 'business-model']
assert len(s['sources']) == 4
assert len(s['diagram']['nodes']) == 4 and len(s['secondDiagram']['nodes']) == 2
assert '任务遗漏' in s['diagram']['nodes'][0]['title']
assert '不证明产品会自动学习' in s['diagram']['scope']
assert '非收益测算' in s['secondDiagram']['scope']
assert '员工自述' in a['body'] and '同一版本' in a['body'] and '库存系统' in a['body']
for suffix, key in [('', 'diagram'), (':second', 'secondDiagram')]:
    q = 'diagram-' + a['id'] + suffix
    assert d['queries'][q]['rows'] == s[key]['nodes']
    src = d['queries'][q]['source']
    assert src['metricDefinitions'][0]['componentIds'] == [q]
    assert src['evidenceFlow'][0]['detail'] == a['sourceUrl']
    assert q in g['previousQueriesCanonicalSha256']
pattern = r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'):
    assert not re.search(pattern, f.read_text())
if len(sys.argv) > 1:
    h = Path(sys.argv[1]).read_text()
    assert not re.search(pattern, h) and 'data-app-local-thread' not in h
print('Passed revised full body/hash, unchanged ID and first time, four source roles, two diagram bindings and privacy; no build or browser claim')
