"""Prepare reviewed single-article authored content in a NEW official Data project copy.
Usage: python prepare_standalone.py <export-project>/src
Do not run on the live site's authoring checkout. Uses no network or credentials.
"""
import json,shutil,sys
from pathlib import Path
src=Path(__file__).parent;dst=Path(sys.argv[1]);r=dst/'content/report';r.mkdir(parents=True,exist_ok=True)
a=json.loads((src/'article-entry.json').read_text());s=json.loads((src/'illustrated-story.json').read_text())
(r/'articles.json').write_text(json.dumps({'articles':[a]},ensure_ascii=False));(r/'illustrated-stories.json').write_text(json.dumps({a['id']:s},ensure_ascii=False))
for f in ['illustrated.css','timeline.css']:shutil.copyfile(src/f,r/f)
shutil.copyfile(src/'StandaloneReader.jsx',r/'IllustratedArticle.jsx');shutil.copyfile(src/'StandaloneArticle.jsx',r/'ReportContent.jsx');shutil.copyfile(src/'article-reviewed-data.json',dst/'data.json')
print('Single-article authored export prepared; use official Data build/export-offline. No Site publication.')
