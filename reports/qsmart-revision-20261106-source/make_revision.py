"""Append a verified same-ID revision; retain original article identity and diagrams."""
from pathlib import Path
import copy,hashlib,json,re,sys

A=Path(__file__).resolve().parent
NOTE=Path(sys.argv[1]); META=Path(sys.argv[2]); ID='research-2026-10-30-qsmart-note'
PATH='research/2026-10-30-qsmart/note.md'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def write(name,value):(A/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
meta=read(META);body=NOTE.read_text();ledger=NOTE.with_name('sources-update-2026-11-06.md').read_text()
assert meta.get('editorialFrozen') is True and meta.get('remoteReadbackVerified') is True
assert re.fullmatch(r'[a-f0-9]{40}',meta['revisionCommit'])
assert re.fullmatch(r'2026-11-06T[0-9:]{8}Z',meta['revisionTime'])
assert sha(NOTE.read_bytes())==meta['bodySha256']
assert sha(NOTE.with_name('sources-update-2026-11-06.md').read_bytes())==meta['sourcesSha256']
original=read(A/'original-article-entry.json');story=read(A/'original-illustrated-story.json');queries=read(A/'original-reviewed-queries.json')
assert original['id']==ID and original['publishedAt']=='2026-10-30T07:29:17Z'
assert original['body']==(A/'original-note.md').read_text()
assert body.startswith(original['body']) and body!=original['body']
appendix=body[len(original['body']):].strip(); title,rest=appendix.split('\n',1)
assert title.startswith('## ') and '2026年11月6日' in title
parts=rest.strip().split('\n\n');assert parts[-1].startswith('补充研究说明：')
url=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['revisionCommit']}/{PATH}"
ledger_url=url.replace('note.md','sources-update-2026-11-06.md')
def links(text):return text.replace('(sources-update-2026-11-06.md)',f'({ledger_url})')
dg=read(A/'revision-diagram-copy.json')
revision={'id':'revision-2026-11-06','title':title[3:],'intro':parts[0],
 'paragraphs':[links(p) for p in parts[1:-1]],'researchNote':links(parts[-1]),
 'diagram':dg,'sourceLedger':ledger,
 'ledgerContext':f"以下来源台账保留修订稿冻结时的原文字节，其中“尚未提交”等是当时状态。正文与来源补充已于{meta['revisionTime']}入库；较新状态见[同ID修订记录]({url.replace('note.md','revision-status-2026-11-06.json')})。本图文保留首次入库时间，不重新计为一篇研究。",
 'sources':[{'title':'百胜中国2026年第三季度业绩会文字稿｜2026-11-03，印刷第3页；读取与403限制见补充说明','url':'https://ir.yumchina.com/static-files/d8dac412-3927-4243-951e-fe7b71065ec8'},
 {'title':'小食代同场电话会报道｜2026-11-03；非独立成效证据，作者访问超时与审校读取状态分别保留','url':'https://www.foodinc.com.cn/2026/11/03/20261103001/'}]}
story['revision']=revision
entry=copy.deepcopy(original)
entry.update({'body':body,'updatedAt':meta['revisionTime'],'sourceUrl':url,
 'firstSourceUrl':original['sourceUrl'],'firstGit':'2d35d3947a51ebafdf8097d393ce49d6db457411',
 'revisionGit':meta['revisionCommit'],'revisedBodySha256':meta['bodySha256']})
q=f'diagram-{ID}:revision-2026-11-06'
queries[q]={'rows':dg['nodes'],'source':{'label':dg['label'],
 'files':[PATH,'research/2026-10-30-qsmart/sources-update-2026-11-06.md'],
 'metricDefinitions':[{'label':dg['label'],'definition':dg['scope']+' '+dg['completion']+' '+dg['note'],'componentIds':[q]}],
 'evidenceFlow':[{'title':'同ID修订固定公开版本','detail':url},{'title':'作者比较框架','detail':'三种选择和成本边界为作者分析，不是公司产品架构、流程验证或经营实验。'}]+[{'title':s['title'],'detail':s['url']} for s in revision['sources']]+[{'title':'读取边界与不能推出的结论','detail':ledger_url}],
 'caveats':['营运支持中心与Q-Smart具体关系未知。','没有AI独立成效、分项成本或总工作量下降的证据。','该PDF曾返回可读解析，随后定位请求403；未重试受限请求，未截图核验。']}}
write('article-entry.json',entry);write('illustrated-story.json',story)
write('article-reviewed-data.json',{'surface':'report','title':entry['title'],'generatedAt':meta['revisionTime'],
 'status':'reviewed','buildStatus':'updating','exportPreferences':{'selected':None,'destinations':[]},
 'filters':[],'report':{'asOf':'2026-11-06'},'queries':queries})
write('frozen.json',meta)
(A/'note.md').write_text(body);(A/'sources-update-2026-11-06.md').write_text(ledger)
print('Verified original prefix, original ID/time and frozen revision; retained both original queries.')
