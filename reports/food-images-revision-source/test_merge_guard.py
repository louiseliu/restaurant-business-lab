"""Run isolated merge, idempotence and query-edit rejection checks.
Usage: python test_merge_guard.py CURRENT_BATCH_SOURCE PREVIOUS_FOOD_IMAGE_SOURCE
"""
import copy,json,subprocess,sys,tempfile
from pathlib import Path
here=Path(__file__).resolve().parent;batch,prior=map(Path,sys.argv[1:])
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
old=read(prior/'article-entry.json');old_story=read(prior/'illustrated-story.json');old_data=read(prior/'article-reviewed-data.json')
new=read(batch/'food-images/article-entry.json');new_story=read(batch/'food-images/illustrated-story.json')
with tempfile.TemporaryDirectory() as tmp:
    target=Path(tmp);report=target/'src/content/report';report.mkdir(parents=True)
    def seed(data):
        write(report/'articles.json',{'articles':[old,{'id':'unrelated','body':'已有内容'}]})
        write(report/'illustrated-stories.json',{old['id']:old_story,'unrelated':{'lead':'已有图文'}})
        write(target/'src/data.json',data)
    def snapshot():return [(p,p.read_bytes()) for p in sorted((target/'src').rglob('*.json'))]
    def run():return subprocess.run([sys.executable,str(here/'apply_revision.py'),str(target),str(batch),str(prior)],capture_output=True,text=True)
    data=copy.deepcopy(old_data);data['id']='report:guard-test';data['queries']['unrelated']={'rows':[{'value':'retain'}]}
    seed(data);result=run();assert result.returncode==0,result.stderr
    assert read(report/'articles.json')['articles']==[new,{'id':'unrelated','body':'已有内容'}]
    assert read(report/'illustrated-stories.json')=={old['id']:new_story,'unrelated':{'lead':'已有图文'}}
    after=read(target/'src/data.json');assert after['id']=='report:guard-test' and after['queries']['unrelated']==data['queries']['unrelated']
    frozen=snapshot();assert run().returncode==0 and snapshot()==frozen
    changed=copy.deepcopy(data);qid=next(iter(old_data['queries']));changed['queries'][qid]['source']['label']+=' 用户修改'
    seed(changed);before=snapshot();result=run();assert result.returncode!=0 and snapshot()==before
print('Guarded merge, same identity, unrelated query/content preservation, idempotence and query-edit rejection passed.')
