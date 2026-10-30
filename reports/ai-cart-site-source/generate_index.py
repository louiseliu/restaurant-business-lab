"""Generate a static reading index from a verified public-repository manifest or checkout.
Usage: python3 generate_index.py --inventory manifest.json --output articles.json
       python3 generate_index.py --repo public-repo-checkout --output articles.json
No network fetch, publication or credentials; review new article classification before release.
"""
import argparse,json,re,subprocess,posixpath,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--inventory');p.add_argument('--repo');p.add_argument('--output',required=True);p.add_argument('--topics',default=str(Path(__file__).with_name('article_topics.json')));a=p.parse_args()
topic_overrides=json.loads(Path(a.topics).read_text()) if Path(a.topics).exists() else {}
repo_name='louiseliu/restaurant-business-lab'
def classify(path):
 if path.startswith('logs/'):return 'log'
 if path.startswith('methods/') or path.startswith('.agents/skills/'):return 'method'
 if path.startswith('research/'):
  if Path(path).name in ['provisional-research.md','pro-prompt-pending.md']:return 'historical-draft'
  if Path(path).name in ['QA.md','bounds-check-findings.md','judgment-revision.md','pro-collaboration.md']:return 'supporting'
  return 'research'
 return 'reference'
if a.inventory:
 raw=json.loads(Path(a.inventory).read_text());ref=raw['ref'];docs=[d for d in raw['documents'] if d['path'].endswith('.md')]
else:
 root=Path(a.repo).resolve()
 def git(*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
 ref=git('rev-parse','HEAD');docs=[]
 for path in git('ls-tree','-r','--name-only',ref).splitlines():
  if not path.endswith('.md'):continue
  if not (path.startswith(('research/','methods/','logs/','.agents/skills/')) or path in ['README.md','AGENTS.md','CHANGELOG.md','state/current.md','reports/README.md','reports/owner-report-source/BUILD.md']):continue
  body=git('show',f'{ref}:{path}');dates=git('log','--follow','--format=%cI','--',path).splitlines();title=next((l[2:].strip() for l in body.splitlines() if l.startswith('# ')),Path(path).stem)
  docs.append(dict(path=path,body=body,title=title,type=classify(path),firstCommittedAt=dates[-1],updatedAt=dates[0]))
sections={'research':'research','supporting':'support','historical-draft':'history','method':'methods','log':'logs','reference':'about'}
ids={d['path']:re.sub('[^a-zA-Z0-9]+','-',d['path'].removesuffix('.md')).strip('-').lower() for d in docs}
articles=[]
for d in docs:
 path=d['path'];body=d['body']
 def link(m):
  label,target=m.group(1),m.group(2)
  if target.startswith(('http:','https:','mailto:','#')):return m.group(0)
  clean=target.split('#')[0];resolved=posixpath.normpath(posixpath.join(posixpath.dirname(path),clean))
  url='#read/'+ids[resolved] if resolved in ids else f'https://github.com/{repo_name}/blob/{ref}/{resolved}'
  if resolved=='reports/restaurant-owner-report.html':url='#read/illustrated-report'
  return f'[{label}]({url})'
 body=re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)',link,body)
 paragraphs=[l.strip() for l in d['body'].splitlines() if l.strip() and not l.startswith(('#','---','|','name:','description:','研究日期','核验日期','更新：'))]
 excerpt=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',paragraphs[0] if paragraphs else d['title']).replace('**','')[:155]
 topics=['business-model'] if sections[d['type']] in ['research','support','history'] else []
 # AI is opt-in evidence-based metadata, never inferred from the word automation.
 if d.get('topics'):topics=d['topics']
 if path in topic_overrides:topics=topic_overrides[path]
 articles.append(dict(id=ids[path],path=path,title=d['title'],section=sections[d['type']],topics=topics,publishedAt=d['firstCommittedAt'],updatedAt=d['updatedAt'],excerpt=excerpt,body=body,sourceUrl=f'https://github.com/{repo_name}/blob/{ref}/{path}',originalBodySha256=hashlib.sha256(d['body'].encode()).hexdigest()))
articles.sort(key=lambda x:(x['publishedAt'],x['id']),reverse=True)
assert len(set(x['id'] for x in articles))==len(articles)
Path(a.output).write_text(json.dumps(dict(sourceCommit=ref,dateBasis='Git first commit (not original publication time)',articles=articles),ensure_ascii=False,indent=2))
print(json.dumps({'documents':len(articles),'research':sum(x['section']=='research' for x in articles),'sourceCommit':ref}))
