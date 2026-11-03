"""Static source checks only. Does not compile JSX or claim rendered HTML verification."""
import json,re,hashlib
from pathlib import Path
p=Path(__file__).parent
a=json.loads((p/'order-cancellation/article-entry.json').read_text())
s=json.loads((p/'order-cancellation/illustrated-story.json').read_text())
d=json.loads((p/'order-cancellation/article-reviewed-data.json').read_text())
sha='2ee3e6e5d9034614a32160bfa992d3186860fa2e153164af023273fbc4a7844b'
assert hashlib.sha256(a['body'].encode()).hexdigest()==sha
assert (p/'note.md').read_text()==a['body']
assert a['firstGit']=='49bce5efc9fbf2d69d9fd922480f7690d07eae1f'
assert a['publishedAt']==a['updatedAt']=='2026-11-03T18:00:26Z'
assert a['topics']==['business-model'] and d['buildStatus']=='paused'
assert a['id']==s['id']=='research-2026-11-03-order-cancellation-note'
assert len(s['sections'])==4 and len(s['sources'])==3 and len(d['queries'])==2
for sec in s['sections']:
 assert '## '+sec['title']+'\n\n'+'\n\n'.join(sec['body']) in a['body']
for suffix,key in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix
 assert d['queries'][q]['rows']==s[key]['nodes']
 assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
 assert s[key]['layout'].startswith('cancellation-')
 assert len(d['queries'][q]['rows'])==3
reader=(p/'IllustratedArticle.jsx').read_text(); entry=(p/'ReportContent.jsx').read_text()
assert 'catalog.articles[0]' in entry and 'stories[item.id]' in entry
assert 'when(item.publishedAt)' in reader and "timeZone:'Asia/Shanghai'" in entry
assert "if(el.tagName==='DETAILS')el.open=true" in reader
assert "startsWith('cancellation-')" in reader
assert "import {CancellationDiagram} from './CancellationDiagrams.jsx'" in reader
assert 'Handoff' not in reader and 'unclef.tw' not in reader and 'LINE' not in reader
for src in s['sources']: assert src['url'] in reader
component=(p/'CancellationDiagrams.jsx').read_text()
assert 'sourceRows={rows} displayRows={rows}' in component
assert 'data-reviewed-rows' in component and 'RichNarrative' in component
pattern=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_|Sentinel_|rtc_u\d'
scanned=0
for f in p.rglob('*'):
 if f.is_file() and f.suffix in ['.jsx','.css','.json','.md']:
  assert not re.search(pattern,f.read_text()),f
  scanned+=1
print(json.dumps({'status':'source-static-checks-passed','bodySHA256':sha,'sections':4,'diagrams':2,'queries':2,'sources':3,'scannedFiles':scanned,'build':'not-run-missing-official-helper','html':'not-produced','visual':'not-run','formalCompletedCount':40,'formalAIcount':25},ensure_ascii=False,indent=2))
