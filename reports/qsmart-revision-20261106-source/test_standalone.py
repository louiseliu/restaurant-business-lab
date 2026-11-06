"""Static preservation, scoped source, compiled payload and privacy checks; no browser claim."""
from pathlib import Path
import copy,hashlib,json,re,sys
A=Path(__file__).resolve().parent;P=Path(sys.argv[1]);ROOT=P/'standalone';R=ROOT/'src/content/report';ID='research-2026-10-30-qsmart-note'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
checks={}
def check(name,value):
 assert value,name
 checks[name]=True
original=read(A/'original-article-entry.json');old_story=read(A/'original-illustrated-story.json');old_queries=read(A/'original-reviewed-queries.json')
entry=read(A/'article-entry.json');story=read(A/'illustrated-story.json');reviewed=read(A/'article-reviewed-data.json');meta=read(A/'frozen.json')
check('same_article_id',entry['id']==ID)
check('same_first_time',entry['publishedAt']==original['publishedAt']=='2026-10-30T07:29:17Z')
check('same_first_commit',entry['firstGit']=='2d35d3947a51ebafdf8097d393ce49d6db457411')
check('revision_time_not_first_time',entry['updatedAt']==meta['revisionTime'] and entry['publishedAt']!=entry['updatedAt'])
check('same_title_topics_excerpt',all(entry[k]==original[k] for k in ['title','topics','excerpt','path','section']))
check('original_body_unchanged_prefix',entry['body'].startswith(original['body']) and original['body']==(A/'original-note.md').read_text())
check('original_body_hash_retained',entry['originalBodySha256']==original['originalBodySha256']==sha(original['body'].encode()))
check('full_revised_body_hash',entry['body']==(A/'note.md').read_text() and entry['revisedBodySha256']==meta['bodySha256']==sha(entry['body'].encode()))
check('frozen_revision_remote_binding',entry['revisionGit']==meta['revisionCommit'] and meta['revisionCommit'] in entry['sourceUrl'] and meta['remoteReadbackVerified'] is True)
check('original_source_link_retained',entry['firstSourceUrl']==original['sourceUrl'])
base=copy.deepcopy(story);revision=base.pop('revision')
check('all_original_story_fields_unchanged',base==old_story)
check('both_original_queries_unchanged',all(reviewed['queries'][q]==v for q,v in old_queries.items()))
q=f'diagram-{ID}:revision-2026-11-06';new=reviewed['queries'][q];dg=revision['diagram']
check('exactly_one_added_query',len(reviewed['queries'])==3 and set(reviewed['queries'])==set(old_queries)|{q})
check('new_diagram_rows_and_scope',new['rows']==dg['nodes'] and new['source']['metricDefinitions'][0]['componentIds']==[q] and new['source']['metricDefinitions'][0]['label']==dg['label'])
check('new_diagram_qualitative_not_numeric',all(isinstance(v,str) for row in new['rows'] for v in row.values()) and [r['方案'] for r in new['rows']]==['纯软件','有人接手的托管服务','现有人工流程'])
check('relationship_unknown_explicit','关系未知' in dg['scope'] and '不是公司产品架构' in new['source']['evidenceFlow'][1]['detail'])
check('no_independent_ai_effect_claim','没有AI独立成效' in new['source']['caveats'][1])
check('original_queries_exclude_new_source',all('d8dac412' not in json.dumps(v) for v in old_queries.values()))
check('new_source_ordinary_link_only','d8dac412' in json.dumps(revision) and not list(R.glob('*source-preview*')))
check('403_no_retry_disclosed','403' in revision['researchNote'] and '未重试' in revision['researchNote'])
check('full_supplemental_ledger',revision['sourceLedger']==(A/'sources-update-2026-11-06.md').read_text() and sha(revision['sourceLedger'].encode())==meta['sourcesSha256'])
actual_a=read(R/'articles.json');actual_s=read(R/'illustrated-stories.json');d=read(ROOT/'src/data.json')
check('exactly_one_complete_article',actual_a=={'articles':[entry]} and actual_s=={ID:story})
check('complete_official_snapshot',d['surface']=='report' and d['buildStatus']=='complete' and d['queries']==reviewed['queries'] and bool(d['id']))
unchanged=0
for rel,expected in read(P/'standalone-prepared-sha256.json').items():
 if rel.startswith('src/content/') or rel in ('src/data.json','src/theme.css'):continue
 check('official:'+rel,sha((ROOT/rel).read_bytes())==expected);unchanged+=1
for name,expected in read(A/'original-preservation.json')['files'].items():check('original-input:'+name,sha((A/name).read_bytes())==expected)
html=(P/'qsmart-revised.html').read_text();parsed=[]
for raw in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)',html):
 try:parsed.append(json.loads(json.loads(raw)))
 except (ValueError,TypeError):pass
catalogs=[v for v in parsed if isinstance(v,dict) and 'articles' in v];stories=[v for v in parsed if isinstance(v,dict) and ID in v]
check('compiled_full_article',len(catalogs)==1 and catalogs[0]==actual_a)
check('compiled_full_story',len(stories)==1 and stories[0]==actual_s)
check('offline_assets_no_external_fetch',not re.search(r'(?:src|href)=["\x27]https?://',html))
manifest=read(ROOT/'dist/data-app-build.json')
for key in ['html','snapshot']:
 b=(ROOT/'dist'/manifest[key]['path']).read_bytes();check('build_manifest_'+key,len(b)==manifest[key]['bytes'] and sha(b)==manifest[key]['sha256'])
built=read(ROOT/'dist'/manifest['snapshot']['path']);check('compiled_queries_and_identity',built['queries']==d['queries'] and built['id']==d['id'])
patterns=[r'appgprj_[A-Za-z0-9]{6,}',r'libfile_[A-Za-z0-9]{6,}',r'Sentinel_[A-Za-z0-9]{6,}',r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/',r'codex://threads/',r'data-app-local-thread["\x27]\s+content=',r'/workspace/[A-Za-z0-9]',r'/home/agent/[A-Za-z0-9]',r'rtc_u\d+_',r'https?://git\.chatgpt-team\.site']
payloads=[(str(p.relative_to(R)),p.read_bytes()) for p in R.rglob('*') if p.is_file()]+[('data.json',(ROOT/'src/data.json').read_bytes()),('offline',(P/'qsmart-revised.html').read_bytes())]+[(f'decoded-{i}',json.dumps(v,ensure_ascii=False).encode()) for i,v in enumerate(parsed)]
for name,b in payloads:
 for pat in patterns:assert not re.search(pat,b.decode('utf8','replace')),name+': '+pat
qa={'checks':{k:v for k,v in checks.items() if not k.startswith('official:')},'unchangedOfficialFiles':unchanged,'privacyPayloads':len(payloads),
 'articleId':ID,'firstCommit':entry['firstGit'],'publishedAt':entry['publishedAt'],'revisionCommit':entry['revisionGit'],'updatedAt':entry['updatedAt'],
 'counts':{'articles':1,'originalDiagramsPreserved':2,'addedDiagrams':1,'queries':3},'runtimeSha256':manifest['runtimeSha256'],
 'html':{'bytes':(P/'qsmart-revised.html').stat().st_size,'sha256':sha((P/'qsmart-revised.html').read_bytes())},
 'notPerformed':['Browser visual and interaction QA','Large HTML or ZIP archival','Portal integration','Site publication or permission changes','New source PDF retry or screenshot verification']}
(P/'build-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa,ensure_ascii=False,indent=2))
