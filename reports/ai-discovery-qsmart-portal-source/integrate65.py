"""Merge one frozen article and one same-ID revision only after all preflight checks."""
import copy,hashlib,json,shutil,sys
from pathlib import Path
from reader_patch import patch_reader,ID,QID
S,A,Q=[Path(v) for v in sys.argv[1:]];R=S/'content/report'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
expected=read(Path(__file__).with_name('input-fingerprints.json'))
for key,folder in [('aiDiscovery',A),('qsmartRevision',Q)]:
    for name,record in expected[key].items():
        data=(folder/name).read_bytes();assert len(data)==record['bytes'] and sha(data)==record['sha256'],'Frozen input changed: '+name
a=read(R/'articles.json');s=read(R/'illustrated-stories.json');d=read(S/'data.json')
assert (len(a['articles']),len(s),len(d['queries']))==(84,64,131),'Unexpected baseline counts'
lookup={v['id']:v for v in a['articles']};assert len(lookup)==84
assert ID not in lookup and ID not in s
n=read(A/'article-entry.json');st=read(A/'illustrated-story.json');q=read(A/'article-reviewed-data.json')['queries'];f=read(A/'frozen.json')
assert n['id']==st['id']==ID
assert f['editorialFrozen'] is True and n['firstGit']==f['commit']=='40e158a2766f7edd8e3d684b66436dd197624ecb'
assert n['publishedAt']==n['updatedAt']==f['time']=='2026-11-06T02:15:50Z'
assert n['topics']==['ai'] and n['originalBodySha256']==f['sha256']==sha(n['body'].encode())==sha((A/'note.md').read_bytes())
assert sha((A/'sources.md').read_bytes())==f['sourcesSha256']
assert len(q)==2 and not set(q)&set(d['queries'])
for key,suffix in [('diagram',''),('secondDiagram',':second')]:
    query='diagram-'+ID+suffix
    assert q[query]['rows']==st[key]['nodes'] and q[query]['source']['metricDefinitions'][0]['componentIds']==[query]
original=read(Q/'original-article-entry.json');originalStory=read(Q/'original-illustrated-story.json');originalQueries=read(Q/'original-reviewed-queries.json')
assert lookup.get(QID)==original,'Q-Smart was edited; preserve and reconcile rather than overwrite'
assert s.get(QID)==originalStory,'Q-Smart story was edited; preserve and reconcile'
assert all(d['queries'].get(k)==v for k,v in originalQueries.items()),'Original Q-Smart queries changed'
revised=read(Q/'article-entry.json');revisedStory=read(Q/'illustrated-story.json');revisedQueries=read(Q/'article-reviewed-data.json')['queries'];rf=read(Q/'frozen.json')
assert rf['editorialFrozen'] is True and rf['remoteReadbackVerified'] is True
assert revised['id']==revisedStory['id']==QID and revised['publishedAt']==original['publishedAt']=='2026-10-30T07:29:17Z'
assert revised['firstGit']=='2d35d3947a51ebafdf8097d393ce49d6db457411' and revised['firstSourceUrl']==original['sourceUrl']
assert revised['revisionGit']==rf['revisionCommit']=='8770ddeefaa8ace5dd3fe1f9e4f68d7abbc4e760' and revised['updatedAt']==rf['revisionTime']=='2026-11-06T02:12:43Z'
assert revised['body'].startswith(original['body']) and revised['originalBodySha256']==original['originalBodySha256']
assert revised['revisedBodySha256']==rf['bodySha256']==sha(revised['body'].encode())==sha((Q/'note.md').read_bytes())
assert rf['sourcesSha256']==sha((Q/'sources-update-2026-11-06.md').read_bytes())==sha(revisedStory['revision']['sourceLedger'].encode())
assert {k:v for k,v in revisedStory.items() if k!='revision'}==originalStory
assert all(revisedQueries.get(k)==v for k,v in originalQueries.items())
newRevisionQueries={k:v for k,v in revisedQueries.items() if k not in originalQueries};rq='diagram-'+QID+':revision-2026-11-06'
assert set(newRevisionQueries)=={rq} and rq not in d['queries']
assert newRevisionQueries[rq]['rows']==revisedStory['revision']['diagram']['nodes'] and newRevisionQueries[rq]['source']['metricDefinitions'][0]['componentIds']==[rq]
additions=[]
for folder,names in [(A,['AIDiscoveryDiagrams.jsx','ai-discovery-value-diagrams.css','ai-discovery-value-source-previews.json']),(Q,['QSmartRevision.jsx','qsmart-revision.css'])]:
    for name in names:
        assert (folder/name).is_file() and not (R/name).exists() and not (R/name).is_symlink(),'File conflict: '+name
        additions.append((folder/name,R/name))
reader=patch_reader((R/'IllustratedArticle.jsx').read_text())
# Nothing above this line writes. Preserve every unrelated object and file.
a['articles']=[revised if v['id']==QID else v for v in a['articles']]+[n]
a['articles'].sort(key=lambda v:(v['publishedAt'],v['id']),reverse=True)
a['sourceCommit']=f['commit'];a['syncNote']='本地待同步65篇图文及Q-Smart同篇补充；未发布站点。'
s[ID]=st;s[QID]=revisedStory;d['queries'].update(q);d['queries'].update(newRevisionQueries);d['buildStatus']='updating';d['generatedAt']=f['time']
write(R/'articles.json',a);write(R/'illustrated-stories.json',s);write(S/'data.json',d);(R/'IllustratedArticle.jsx').write_text(reader)
for src,dst in additions:shutil.copyfile(src,dst)
print('Added one article and two queries; appended one Q-Smart revision query without changing its original identity, diagrams or queries.')
