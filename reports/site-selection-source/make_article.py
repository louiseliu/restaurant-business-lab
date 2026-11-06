"""Generate one frozen narrative, a decision diagram and a synthetic contribution chart."""
from pathlib import Path
import hashlib,json,re,sys
A=Path(__file__).resolve().parent
NOTE=Path(sys.argv[1]);body=NOTE.read_text();meta=json.loads(Path(sys.argv[2]).read_text())
ID='research-2026-11-06-site-selection-rent-note';P='research/2026-11-06-site-selection-rent/note.md'
U=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['commit']}/{P}"
assert re.fullmatch(r'[a-f0-9]{40}',meta['commit']), 'Require verified first commit'
assert re.fullmatch(r'2026-11-06T[0-9:]{8}Z',meta['time']), 'Require actual first commit timestamp'
assert meta.get('editorialFrozen') is True and meta.get('remoteReadbackVerified') is True
assert hashlib.sha256(body.encode()).hexdigest()==meta['sha256']
source_body=NOTE.with_name('sources.md').read_text()
assert hashlib.sha256(source_body.encode()).hexdigest()==meta['sourcesSha256']
calculations=json.loads(NOTE.with_name('calculation-results.json').read_text())
assert calculations['data_status']=='author_constructed_synthetic_examples_only'
assert calculations['required_average_incremental_orders_per_day']=='20'
def write(n,v):(A/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:]
lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1);sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=[]
for label,url in re.findall(r'\[([^\]]+)\]\((https://[^\s)]+)\)',body):
 if url not in {s['url'] for s in sources}:sources.append({'title':f'S{len(sources)+1} · {label}','url':url})
config=json.loads((A/'reviewed-illustration-copy.json').read_text());dg=config.pop('diagram');chart=config.pop('numericChart')
story={'id':ID,'headline':title,'lead':lead,**config,'diagram':dg,'numericChart':chart,'sections':sections,'sources':sources,'technicalDetails':[{'title':'首次研究台账，历史状态保留','body':source_body}]}
entry={'id':ID,'path':P,'title':title,'section':'research','topics':['business'],'publishedAt':meta['time'],'updatedAt':meta['time'],'excerpt':'排名先用于筛选，租金溢价要靠本店新增贡献证明','body':body,'originalBodySha256':meta['sha256'],'sourceUrl':U,'firstGit':meta['commit']}
q='diagram-'+ID
queries={q:{'rows':dg['nodes'],'source':{'label':dg['label'],'files':[P],'metricDefinitions':[{'label':dg['label'],'definition':dg['scope']+' '+dg['note'],'componentIds':[q]}],'evidenceFlow':[{'title':'作者决策框架，不是产品内部算法','detail':U}]+[{'title':s['title'],'detail':s['url']} for s in sources],'caveats':[dg['completion'],dg['note']]}}}
labels=['预期情景','贡献降低','产能受限'];rows=[]
for label,s in zip(labels,calculations['scenarios']):
 orders=s['realized_incremental_orders_per_day'];contribution=s['contribution_per_order'];gross=s['monthly_incremental_contribution'];net=s['net_difference_after_rent_premium']
 assert gross==30*orders*contribution and net==gross-6000
 rows.append({'label':label,'value':net,'fullLabel':f'{label}（每日多{orders}单，每单{contribution}元）','display':f'{net:+,}元/月','incrementalOrdersPerDay':orders,'contributionPerOrderCny':contribution,'operatingDays':30,'grossContributionCny':gross,'rentPremiumCny':6000,'otherCostDifferenceCny':0,'dataStatus':'作者构造的模拟假设，非实测'})
q='visual-'+ID;calculation_path=P.replace('note.md','calculations.py');result_path=P.replace('note.md','calculation-results.json')
queries[q]={'rows':rows,'source':{'label':'租金溢价模拟：新增贡献减去租金差额','files':[P,calculation_path,result_path],'metricDefinitions':[{'label':'每月净差额（元）','definition':'每日净新增订单 × 每单贡献 × 30天 − 6,000元租金溢价。其他成本差额假设为0；仅为两铺位的差额，不是整店利润。','formula':'incrementalOrdersPerDay * contributionPerOrderCny * operatingDays - rentPremiumCny - otherCostDifferenceCny','componentIds':[q]},{'label':'基准盈亏平衡订单量','definition':'每单贡献10元时，6,000 ÷ 30 ÷ 10 = 每日20单。只抵消租金差额，不覆盖整店成本。','componentIds':[q]}],'evidenceFlow':[{'title':'作者构造情景，无实测或厂商报价含义','detail':U},{'title':'可运行计算脚本','detail':U.replace('note.md','calculations.py')},{'title':'已运行结果','detail':U.replace('note.md','calculation-results.json')}],'caveats':['所有输入均为作者假设，不是美团预测或门店数据。','新增整班人力、物业、保底、原有订单折扣损失等如有差异须另扣。押金、装修与开业前资金另行检查。']},'methods':[{'language':'python','code':NOTE.with_name('calculations.py').read_text()}]}
write('article-entry.json',entry);write('illustrated-story.json',story)
write('article-reviewed-data.json',{'surface':'report','title':title,'generatedAt':meta['time'],'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-06'},'queries':queries})
print(meta['sha256'],len(sections),'complete sections; decision diagram and synthetic contribution chart')
