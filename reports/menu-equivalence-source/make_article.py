"""Build the full frozen narrative and two explicitly illustrative comparisons."""
from pathlib import Path
import hashlib,json,re,sys
A=Path(__file__).resolve().parent;body=Path(sys.argv[1]).read_text();meta=json.loads(Path(sys.argv[2]).read_text());ID='research-2026-11-05-menu-equivalence-note';P='research/2026-11-05-menu-equivalence/note.md';U=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['commit']}/{P}"
assert hashlib.sha256(body.encode()).hexdigest()==meta['sha256']
def write(n,v):(A/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:];lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1);sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=[]
for label,url in re.findall(r'\[([^\]]+)\]\((https://[^\s)]+)\)',body):
 if url not in {s['url'] for s in sources}:sources.append({'title':label,'url':url})
dg={'kind':'compare','layout':'menu-equivalence-structure','label':'看起来都能多选，商品结构却不同','scope':'商品选项与套餐子项的机制比较。以下“锅物、肉片”仅为作者构造示例，不是案例店的真实菜单或迁移方案。','nodes':[
{'决定':'商品 + 加料选项','结构示意':'锅物 → 肉片选项 → 希望同一种加两份','来源支持的边界':'iCHEF整合概览写明：同一商品内不能重复选择相同选项。台湾范围来自该概览。','待验证的问题':'顾客原有加购数量能否表达？同步是否改变原来可卖的组合？不推及所有Uber Eats接入方式。'},
{'决定':'套餐 + 子商品','结构示意':'套餐 → 可选子商品 → 按套餐规则多选及重复','来源支持的边界':'套餐子项说明描述子商品可按规则多选及重复，并同步到包括Uber Eats的平台。','待验证的问题':'能否保留本店原加料的选择上下限、加价及每份归属？套餐能力不能直接证明商品选项已经恢复。'}
],'completion':'历史投诉与当前帮助页不能拼成“已经修复”的时间线。只有在实际地区、账号版本和商品结构下演示完整购买与制作过程，才能判断原组合是否保留。','note':'图1｜原创结构示意。经营者自述与供应商功能说明分别使用；没有独立重现、最终迁移结果或经营成效验证。'}
second={'kind':'compare','layout':'menu-equivalence-kitchen','label':'同样三份肉，备料合计与逐份装配需要的信息不同','scope':'作者模拟订单：第一份锅物加两份同种肉，第二份锅物加一份；不设售价，不代表案例门店真实订单或曾经发生错单。','nodes':[
{'决定':'全部套餐的子项合计','输出示意':'两份锅物｜肉片合计：3份','适合回答':'集中备料岗位要准备多少份肉。','仍需保留':'装配岗位若只看到合计，仍需其他可靠信息确认哪份锅配两份、哪份配一份。'},
{'决定':'每份套餐的子项数量','输出示意':'第一份锅物 → 肉片2份；第二份锅物 → 肉片1份','适合回答':'逐份装配岗位如何分配已经准备的肉片。','仍需保留':'顾客选择、数量与价格记录能对应；名称及打印格式不必逐字相同。'}
],'completion':'官方厨房联设置有前提：先将商品数量显示设为“相同商品显示总数”，才出现子项数量设置，选择全部套餐合计或每份套餐个别数量。子项集中/分开排列是另一项选择；不可混为同一开关。','note':'图2｜原创信息取舍示意，不是产品界面截图。具体配置与每份归属仍须验收，不保证默认模板适合所有门店，也不证明鍋美美打印错误。'}
story={'id':ID,'headline':title,'lead':lead,'findings':['重复加料是重要购买方式时，先验收组合、计价和每份制作信息；固定菜单可更优先考虑统一维护。','套餐子项支持重复选择，不直接证明原商品加料已恢复；改建需要核对数量边界、加价和归属。','整合、独立维护与主动简化，应比较真实需求和持续维护负担，不以少一个后台代替成本判断。'],'diagram':dg,'secondDiagram':second,'sections':sections,'meaning':'采购菜单同步，验收的应是一份仍能购买、正确收费并做出来的餐。保留重要组合且维护可承受时采用整合；关键组合缺失时比较经核实可用的替代方案。','unknowns':['未独立重现经营者经历，没有该门店最终迁移选择或效果数据。','帮助页完整版本沿革、实际地区与账号适用性未核实，不能推断当前版本已修复。','没有交易、费用和维护工时证据，不估算损失、利润或回本；未新增Pro咨询或门店实验。'],'actions':['选出不能丢失的真实购买方式，用脱敏或模拟样本表达数量、加价和每份归属。','在获授权的测试环境或供应商演示中核对顾客选择、价格记录和厨房输出，未验证环节不据此放行。','能够保留且可持续维护就继续整合；关键组合缺失则比较替代；主动简化须明确批准商品变化。'],'sources':sources}
entry={'id':ID,'path':P,'title':title,'section':'research','topics':['business-model'],'publishedAt':meta['time'],'updatedAt':meta['time'],'excerpt':'从重复加料到逐份厨房表达，菜单同步需要保留哪些商品含义？比较整合、改建与主动简化的经营取舍。','body':body,'originalBodySha256':meta['sha256'],'sourceUrl':U,'firstGit':meta['commit']}
queries={}
for diagram,suffix in [(dg,''),(second,':second')]:
 q='diagram-'+ID+suffix;queries[q]={'rows':diagram['nodes'],'source':{'label':diagram['label'],'files':[P],'metricDefinitions':[{'label':'菜单结构与制作信息的条件比较','definition':diagram['scope']+' '+diagram['note'],'componentIds':[q]}],'evidenceFlow':[{'title':s['title'],'detail':s['url']} for s in sources if suffix=='' or 'p=36376' in s['url']]+[{'title':'作者机制分析与模拟验收情景','detail':U}],'caveats':[diagram['completion'],diagram['note']]}}
previews={
'https://vocus.cc/article/6a0083d7fd89780001622651':'经营者自述熟客无法重复加购肉片，以及调整后再次同步又受限的经历。未经独立重现，不能据此确定接口责任或当前功能。',
'https://www.4force.com.tw/':'4force将鍋美美食豔室列为旗下火锅品牌；同主体材料用于确认品牌关系，不增加独立效果证据。',
'https://case.4force.com.tw/':'同主体案例页记录说明补充及阶段性商业对话封卷；不证明功能修复或原组合恢复。',
'https://support.ichefpos.com/?p=16450':'整合概览列明台湾范围、整合菜单覆盖平台原菜单及同一商品内相同选项不可重复选择；不推及所有平台接入方式。',
'https://support.ichefpos.com/?lang=zh-yue&p=65591':'套餐子商品可按规则多选及重复选择，并同步到包括Uber Eats的平台；不能等同所有商品加料选项。',
'https://support.ichefpos.com/?lang=zh-yue&p=36376':'厨房联先设置相同商品显示总数，才出现子项数量选项：全部套餐合计或每份套餐个别数量。集中或分开排列另行选择；不是默认配置适用性证明。'}
write('menu-equivalence-source-previews.json',{s['url']:{'title':s['title'],'summary':previews[s['url']],'source':'2026-11-05公开资料核验；事实范围与限制见正文','approvedForReport':True} for s in sources})
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',{'surface':'report','title':title,'generatedAt':meta['time'],'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries})
print(meta['sha256'],len(sections),'complete sections; two original diagrams')
