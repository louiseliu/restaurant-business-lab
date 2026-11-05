"""Check safe merge, repeat application and rejection of user edits before writes.
Usage: python test_merge_guard.py NEW_ARTICLE_SOURCE PREVIOUS_ARTICLE_SOURCE
"""
import copy,json,subprocess,sys,tempfile
from pathlib import Path
here=Path(__file__).resolve().parent;new,prior=map(Path,sys.argv[1:])
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
old=read(prior/'article-entry.json');story=read(prior/'illustrated-story.json');data=read(prior/'article-reviewed-data.json');ID=old['id']
with tempfile.TemporaryDirectory() as tmp:
    target=Path(tmp);report=target/'src/content/report';report.mkdir(parents=True)
    def seed():
        write(report/'articles.json',{'articles':[old,{'id':'unrelated','body':'Existing user content'}]})
        write(report/'illustrated-stories.json',{ID:story,'unrelated':{'lead':'Existing user story'}})
        d=copy.deepcopy(data);d['id']='report:existing-user-artifact';d['queries']['unrelated']={'rows':[{'value':'preserve'}]};write(target/'src/data.json',d)
    def snapshot():return [(str(p),p.read_bytes()) for p in sorted((target/'src').rglob('*.json'))]
    def run():return subprocess.run([sys.executable,str(here/'apply_revision.py'),str(target),str(new),str(prior)],capture_output=True,text=True)
    seed();r=run();assert r.returncode==0,r.stderr
    a=read(report/'articles.json');s=read(report/'illustrated-stories.json');d=read(target/'src/data.json')
    assert a['articles']==[read(new/'article-entry.json'),{'id':'unrelated','body':'Existing user content'}]
    assert s=={ID:read(new/'illustrated-story.json'),'unrelated':{'lead':'Existing user story'}}
    assert d['id']=='report:existing-user-artifact' and d['queries']['unrelated']=={'rows':[{'value':'preserve'}]}
    frozen=snapshot();assert run().returncode==0 and snapshot()==frozen
    for kind in ['body','metadata','story','query']:
        seed()
        if kind in ['body','metadata']:
            p=report/'articles.json';v=read(p);v['articles'][0]['body' if kind=='body' else 'title']+=' User edit';write(p,v)
        elif kind=='story':
            p=report/'illustrated-stories.json';v=read(p);v[ID]['lead']+=' User edit';write(p,v)
        else:
            p=target/'src/data.json';v=read(p);v['queries'][next(iter(data['queries']))]['source']['label']+=' User edit';write(p,v)
        before=snapshot();r=run();assert r.returncode!=0 and snapshot()==before,kind
print('Passed: same ID, unrelated content preservation, idempotence, body/metadata/story/query edit rejection before writes.')
