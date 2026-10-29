"""Add reviewed AI article without deleting old articles, stories or samples.
Usage: python apply_article.py <existing-project>/src/content/report
"""
import json,sys
from pathlib import Path
root=Path(sys.argv[1]);here=Path(__file__).parent;entry=json.loads((here/'article-entry.json').read_text());story=json.loads((here/'illustrated-story.json').read_text());index=json.loads((root/'articles.json').read_text());stories=json.loads((root/'illustrated-stories.json').read_text());id=entry['id'];existing=next((a for a in index['articles'] if a['id']==id),None)
assert existing is None or existing==entry,'Existing article differs; review edits before merging'
assert id not in stories or stories[id]==story,'Existing story differs; preserve user changes'
if existing is None:index['articles'].append(entry)
index['articles'].sort(key=lambda a:(a['publishedAt'],a['id']),reverse=True);index['sourceCommit']='327353e38ea3b8981bd2ea8937e9d1aaa0ad28e2';index['syncNote']='增量研究同步；各篇固定sourceUrl保留原版本，非全部行政资料同步。';stories[id]=story
(root/'articles.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n');(root/'illustrated-stories.json').write_text(json.dumps(stories,ensure_ascii=False,indent=2)+'\n')
print('Article merged. Existing entries preserved; run reviewed-query sync, build and browser QA next.')
