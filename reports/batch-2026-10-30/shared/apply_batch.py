"""Add approved entries without overwriting existing articles or user edits.
Usage: python apply_batch.py BATCH_DIRECTORY EXISTING_PROJECT/src/content/report
Each child directory containing article-entry.json also requires illustrated-story.json.
Run reviewed query synchronization and public sanitization after all source generation.
"""
import json,sys
from pathlib import Path
source=Path(sys.argv[1]);root=Path(sys.argv[2]);index=json.loads((root/'articles.json').read_text());stories=json.loads((root/'illustrated-stories.json').read_text())
entries=sorted(source.glob('*/article-entry.json'));assert entries,'No approved article entries'
for file in entries:
 entry=json.loads(file.read_text());story=json.loads((file.parent/'illustrated-story.json').read_text());id=entry['id'];assert story['id']==id
 existing=next((a for a in index['articles'] if a['id']==id),None)
 assert existing is None or existing==entry,'Existing article differs; preserve edits and review'
 assert id not in stories or stories[id]==story,'Existing illustrated story differs; review before merge'
 assert entry['publishedAt'] and entry['sourceUrl']
 if existing is None:index['articles'].append(entry)
 stories[id]=story
index['articles'].sort(key=lambda a:(a['publishedAt'],a['id']),reverse=True)
index['syncNote']='增量研究同步；各篇固定sourceUrl及真实首次入库时间保留，非全部行政资料同步。'
(root/'articles.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n');(root/'illustrated-stories.json').write_text(json.dumps(stories,ensure_ascii=False,indent=2)+'\n')
print('Merged',len(entries),'entries. Existing content preserved; review/query sync/sanitize/build/QA still required.')
