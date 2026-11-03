"""Static standalone route targets. Actual directory/original clicks are separate QA."""
import json
from pathlib import Path
p=Path(__file__).parent
a=json.loads((p/'service-handoff/article-entry.json').read_text())
s=json.loads((p/'service-handoff/illustrated-story.json').read_text())
reader=(p/'IllustratedArticle.jsx').read_text()
entry=(p/'ReportContent.jsx').read_text()
assert 'catalog.articles[0]' in entry and 'stories[item.id]' in entry
assert 'when(item.publishedAt)' in reader and "timeZone:'Asia/Shanghai'" in entry
assert "if(el.tagName==='DETAILS')el.open=true" in reader
assert "el.scrollIntoView({behavior:'instant',block:'start'})" in reader
for key in ['top','answer','evidence','meaning','limits','sources','original']:
 assert f"anchor('{key}')" in reader
assert "anchor('section-'+i)" in reader and "['section-'+i,s.title]" in reader
assert 'onClick={()=>jump(id)}' in reader and "jump('top')" in reader
assert len(s['sections'])==4 and a['id']==s['id']
assert 'restaurant-portal service-handoff-article' in entry
assert "startsWith('handoff-')" in reader
print('Standalone default target, 11 unique anchor targets, directory jump, original disclosure, fixed source and Beijing first-Git rendering passed static checks.')
