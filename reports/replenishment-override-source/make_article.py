"""Build the illustrated narrative from a frozen, hash-checked public note."""
import hashlib,json,re,sys
from pathlib import Path
A=Path(__file__).resolve().parent; body=Path(sys.argv[1]).read_text(); meta=json.loads(Path(sys.argv[2]).read_text());ID='research-2026-11-05-replenishment-override-note';P='research/2026-11-05-replenishment-override/note.md';U=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['commit']}/{P}"
assert hashlib.sha256(body.encode()).hexdigest()==meta['sha256']
def write(n,v):(A/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:];lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1);sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=[{'title':'预印本§3.3｜随机分组与权限安排','url':'https://arxiv.org/html/2607.00420v2#S3.SS3'},{'title':'预印本§4、表2｜库存与销量结果','url':'https://arxiv.org/html/2607.00420v2#S4'}]
sources += [{'title':'arXiv版本入口｜v2与修订日期','url':'https://arxiv.org/abs/2607.00420'},{'title':'作者官网｜当前发表状态线索','url':'https://minda-zhao.github.io/Personal-Website/'}]
dg={'kind':'compare','layout':'override-experiment','label':'允许下调，降低库存的同时要看销售机会','scope':'企业合作预印本的现场试验：2023年5月4日起，553名全职补货员随机分组，试验46天。下表仅复述论文结果方向与统计判断，没有把系数换算成原始百分比。','nodes':[
{'试验政策':'禁止下调','可修改范围':'不能下调；仍可上调，保留仓库缺货等业务例外。','库存结果':'作为比较基准','销量结果':'作为比较基准','怎样读':'比较对象不是完全无人工参与。'},
{'试验政策':'自由下调','可修改范围':'可自由下调，不设SKU种类数上限；仍可上调，保留仓库缺货等运营例外。','库存结果':'相对禁止组，显著下降','销量结果':'相对禁止组，显著下降','怎样读':'库存下降不能单独证明经营改善。'},
{'试验政策':'有限下调','可修改范围':'每台机器每次补货，最多下调两个SKU种类；仍可上调，保留仓库缺货等业务例外。','库存结果':'相对禁止组，显著下降','销量结果':'相对禁止组，变化未达统计显著','怎样读':'未达显著不等于证明销售无损。'}
],'completion':'“两个”约束可改的商品种类数，不约束每种少补多少件。两组的显著性不同，也不等于两种政策彼此差异显著。','note':'图1｜原创证据整理。三组来自同一企业合作预印本，不是三份独立证据；现场为智能售货业务，不能直接转成厨房原料的额度或利润结论。'}
second={'kind':'flow','layout':'override-decision','label':'从少订一项，到复核它影响的整段经营','scope':'本文为餐饮构造的分析路径，不是试验企业的实测记录，也不是已经验证的门店规则。名额、下调幅度、异常接管分别处理。','nodes':[
{'判断环节':'先辨认修改理由','要留下什么':'算法原建议、实际执行量、修改理由；新增预订变化是否可核对。','继续的条件':'有系统之外的有效信息，值得纳入判断。','收窄或修复':'多数调整都修补同一错误，先回到数据维护。'},
{'判断环节':'沿共享原料找影响','要留下什么':'受影响菜品、主打菜、已接预订与堂食/外卖/套餐。','继续的条件':'影响范围可辨认，改后可供份数可核对。','收窄或修复':'无法看清断供范围，先不扩大自动执行。'},
{'判断环节':'把补救负担算进去','要留下什么':'报损、紧急采购、额外复核；停售开始与恢复、替代选择。','继续的条件':'库存压力缓解，停售和补货负担没有出现需处理的恶化。','收窄或修复':'主打菜可售时间缩短，或临时采购反复增加。'},
{'判断环节':'按预先约定决定去留','要留下什么':'完整补货周期的记录；促销、停业、改菜单和配送变化另记。','继续的条件':'保留可比基线，先继续观察而非立刻全店放开。','收窄或修复':'收回有问题的品项范围，先解决原因。'}
],'completion':'食品安全、已接订单或明确供货异常 → 沿既有责任流程接管，不能因为“名额用完”而强迫照单执行。','note':'图2｜原创经营分析。未成交需求通常观察不全，停售时间不直接等于确定丢单金额；库存下降也不自动等于原料成本、现金或利润改善。'}
story={'id':ID,'headline':title,'lead':lead,'findings':['建议量基本可用且门店有额外信息时，有限下调权值得小范围验证；数据或配送失常时，先修复输入和异常流程。','同时看库存、报损、可售时段与补货负担。销量变化未达显著不能写成销售无损，更不能写成利润改善。','厨房共享原料牵连多道菜，不照搬售货机每次两个SKU的上限。'],'diagram':dg,'secondDiagram':second,'sections':sections,'meaning':'决定下调权时，把有效本地信息、共享原料影响和补救能力放在一起。短期报损风险高且补货可靠时，更多空间可能有价值；主打菜缺货影响整单、供货周期长时，则应更谨慎。','unknowns':['现场证据来自智能售货业务的企业合作预印本，不证明餐厅已复现，也不认定为生成式AI应用。','没有本地门店利润增量、回本期或已经执行的餐饮试验；情景、成本判断与权限安排均为作者分析。','论文中的库存与销量结果不能直接转换为原料节省或销售无损，也不能由两个显著性判断推断政策之间差异显著。'],'actions':['选择记录完整、影响范围清楚的一组品项，保留原建议、执行量和理由，观察完整补货周期。','在看结果前写清继续与停止条件，同时记录停售、报损、紧急补货及营业环境变化。','有效本地信息可持续核对时再观察；反复数据错误或关键菜断供时，先收窄范围并修复原因。'],'sources':sources}
entry={'id':ID,'path':P,'title':title,'section':'research','topics':['ai','business-model'],'publishedAt':meta['time'],'updatedAt':meta['time'],'excerpt':'智能售货随机试验提示有限下调权值得检验，但厨房共享原料、缺货后果与补救成本，决定小店能否借用这条思路。','body':body,'originalBodySha256':meta['sha256'],'sourceUrl':U,'firstGit':meta['commit']}
queries={}
for diagram,suffix in [(dg,''),(second,':second')]:
 q='diagram-'+ID+suffix
 queries[q]={'rows':diagram['nodes'],'source':{'label':diagram['label'],'files':[P],'metricDefinitions':[{'label':'实验结果方向及餐饮迁移边界','definition':diagram['scope']+' '+diagram['note'],'componentIds':[q]}],'evidenceFlow':[{'title':x['title'],'detail':x['url']} for x in sources]+[{'title':'研究分析','detail':U}],'caveats':[diagram['completion'],diagram['note']]}}
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',{'surface':'report','title':title,'generatedAt':meta['time'],'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries})
write('override-source-previews.json',{
sources[0]['url']:{'title':sources[0]['title'],'summary':'丰宜智能售货业务的553名全职补货员随机分组，试验始于2023年5月4日、持续46天。有限组每机每次最多下调两个SKU种类，不是下调件数；仍可上调并保留仓库缺货等运营例外。','source':'企业合作预印本 arXiv v2，2026-10-17修订','approvedForReport':True},
sources[1]['url']:{'title':sources[1]['title'],'summary':'相对禁止组，两种允许下调的政策库存均显著下降；自由组销量显著下降，有限组销量变化未达显著。后者不等于销售无损，显著性不同也不证明两政策彼此差异显著。','source':'同一预印本表2；非餐饮实测或独立第三方验证','approvedForReport':True},
sources[2]['url']:{'title':sources[2]['title'],'summary':'当前研究采用v2预印本，修订日期为2026年10月17日。版本状态不等于正式发表确认。','source':'arXiv版本记录，2026-11-05核验','approvedForReport':True},
sources[3]['url']:{'title':sources[3]['title'],'summary':'作者官网将本文列为预印本，标注在Manufacturing & Service Operations Management大修中。本轮未核验到正式发表版；不能写成从未接受同行评议。','source':'作者官网状态线索，2026-11-05核验','approvedForReport':True}
})
print(meta['sha256'],len(sections),'sections; two original diagrams')
