"""Apply the reviewed shift revision after checking article, story and both queries.
Usage: python apply_revision.py PROJECT NEW_ARTICLE_SOURCE PREVIOUS_ARTICLE_SOURCE
No remote access or publication. Unexpected edits abort before any write.
"""
import hashlib,json,sys
from pathlib import Path
P,N,B=map(Path,sys.argv[1:]);R=P/'src/content/report'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def canonical(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
a=read(N/'article-entry.json');s=read(N/'illustrated-story.json');q=read(N/'article-reviewed-data.json')['queries']
old_a=read(B/'article-entry.json');old_s=read(B/'illustrated-story.json');old_q=read(B/'article-reviewed-data.json')['queries']
assert canonical(old_a)=='f973e6d7f181811a787524e6f8b62c0bbddfcebdb9b9e11ae544c2ec506f6ed3'
assert canonical(old_s)=='8ea67b7b55783c36663ad1d3cc21e5b22abfc644d2d85348f2be039f36cde533'
expected={'diagram-research-2026-11-01-shift-constraints-note':'2c60b2297e7c8aa7f5eca380286397e9733a8ae068196f0587d2db194289bcb7','diagram-research-2026-11-01-shift-constraints-note:second':'4bcf80bea0a484e5a9e60ea1031e10a80064bbb94510e31362a2d2bfbc1cbef4'}
assert {k:canonical(v) for k,v in old_q.items()}==expected
ID=a['id'];assert ID==s['id']==old_a['id']=='research-2026-11-01-shift-constraints-note'
assert a['publishedAt']==old_a['publishedAt']=='2026-11-01T14:03:18Z'
assert a['firstGit']==old_a['firstGit']=='daa2e94fd3780500f5d3a7e3291e1a3c1df86743'
assert set(q)==set(old_q)
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']
index=read(R/'articles.json');stories=read(R/'illustrated-stories.json');data=read(P/'src/data.json')
matches=[v for v in index['articles'] if v['id']==ID];assert len(matches)==1
present={k:data['queries'][k] for k in q}
if matches[0]==a and stories[ID]==s and present==q:
    print('Already updated; no mutation');raise SystemExit
assert matches[0]==old_a,'Unexpected article edit; no writes'
assert stories[ID]==old_s,'Unexpected story edit; no writes'
assert present==old_q,'Unexpected query edit; no writes'
index['articles']=[a if v['id']==ID else v for v in index['articles']]
stories[ID]=s;data['queries'].update(q);data['generatedAt']=a['updatedAt'];data['buildStatus']='complete'
write(R/'articles.json',index);write(R/'illustrated-stories.json',stories);write(P/'src/data.json',data)
print('Same-ID revision merged; other content and artifact identity preserved.')
