"""Prepare one approved article in a separate official Data authoring project.
Usage: python prepare_article.py ARTICLE_DIRECTORY EXPORT_PROJECT/src
ARTICLE_DIRECTORY contains article-entry.json, illustrated-story.json and article-reviewed-data.json.
No fetching, publication, Site identity or live-project mutation. Do not target the live portal.
"""
import json,shutil,sys
from pathlib import Path
source=Path(sys.argv[1]);target=Path(sys.argv[2]);common=Path(__file__).parent;report=target/'content/report'
report.mkdir(parents=True,exist_ok=True)
entry=json.loads((source/'article-entry.json').read_text());story=json.loads((source/'illustrated-story.json').read_text());data=json.loads((source/'article-reviewed-data.json').read_text())
assert story['id']==entry['id']
assert entry['publishedAt'] and entry['sourceUrl'],'Requires actual repository first publication'
(report/'articles.json').write_text(json.dumps({'articles':[entry]},ensure_ascii=False,indent=2)+'\n')
(report/'illustrated-stories.json').write_text(json.dumps({entry['id']:story},ensure_ascii=False,indent=2)+'\n')
for f in ['illustrated.css','timeline.css']:shutil.copyfile(common/f,report/f)
shutil.copyfile(common/'StandaloneReader.jsx',report/'IllustratedArticle.jsx')
shutil.copyfile(common/'StandaloneArticle.jsx',report/'ReportContent.jsx')
(target/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Prepared independent article. Build/export with official Data workflow next.')
