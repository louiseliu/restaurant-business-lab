"""Apply reviewed same-ID revision only against the expected prior body/story.
Usage: python update_article.py ARTICLE_DIRECTORY EXISTING_PROJECT/src/content/report
Stops on unexpected user changes; preserves original publication and all other entries.
"""
import json,hashlib,sys
from pathlib import Path
src,root=map(Path,sys.argv[1:]);a=json.loads((src/'article-entry.json').read_text());s=json.loads((src/'illustrated-story.json').read_text());g=json.loads((src/'update-guard.json').read_text());id=a['id'];assert id==s['id']==g['id']
index=json.loads((root/'articles.json').read_text());stories=json.loads((root/'illustrated-stories.json').read_text());old=next(x for x in index['articles'] if x['id']==id)
assert old['publishedAt']==a['publishedAt'],'Cannot alter first publication'
if old==a and stories[id]==s:print('Already updated; no mutation');raise SystemExit
assert old['originalBodySha256']==g['previousOriginalBodySha256'],'Unexpected original body; preserve edits'
assert hashlib.sha256(json.dumps(old,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==g['previousEntryCanonicalSha256'],'Unexpected article metadata; preserve edits'
canonical=json.dumps(stories[id],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
assert hashlib.sha256(canonical).hexdigest()==g['previousStoryCanonicalSha256'],'Unexpected story; preserve edits'
index['articles']=[a if x['id']==id else x for x in index['articles']];stories[id]=s
(root/'articles.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n');(root/'illustrated-stories.json').write_text(json.dumps(stories,ensure_ascii=False,indent=2)+'\n')
print('Same-ID revision merged; run query sync, sanitization, official build and QA')
