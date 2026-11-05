"""Generate full illustrated content from the hash-checked frozen public note."""
import hashlib,json,re,sys
from pathlib import Path
A=Path(__file__).resolve().parent;body=Path(sys.argv[1]).read_text();meta=json.loads(Path(sys.argv[2]).read_text());ID='research-2026-11-05-site-fitout-note';P='research/2026-11-05-site-fitout/note.md';U=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['commit']}/{P}"
assert hashlib.sha256(body.encode()).hexdigest()==meta['sha256']
def write(n,v):(A/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:];lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1);sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=[{'title':'潇湘晨报原报道｜长沙门店采访与现场对照','url':'https://k.sina.cn/article_1655444627_62ac1493020031u48.html'},{'title':'生态环境部公布｜生态环境法典第二百五十条','url':'https://www.mee.gov.cn/ywgz/fgbz/fl/202603/t20260313_1146496.shtml'},{'title':'市场监管总局｜食品经营许可和备案管理办法第十二、十三及六十四条','url':'https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/fgs/art/2023/art_91a91c26ae464a2f898952d5b84f62c6.html'}]
dg={'kind':'flow','layout':'fitout-gates','label':'先排除会让投入失效的条件，再决定下一笔钱','scope':'本文提出的核验顺序，不是长沙门店实际执行流程。每一步都保留停止或修改方案的选择；不能把全部问题都留到施工以后。','nodes':[
{'决定':'继续谈这个地址？','先核对':'拟经营品类、具体建筑条件、项目适用要求，以及可追溯的市场线索。','暂不付款的信号':'硬条件无法确认，或必要改造已改变原经营前提。','仍可选择':'暂停签约，补核验或比较其他铺位。'},
{'决定':'让方案进入施工？','先核对':'实测尺寸、设备条件、备餐与取餐路径、交付范围及报价。','暂不付款的信号':'效果图与现场有冲突，或新增工程尚未重新定价。','仍可选择':'先放样、改图、更新报价，再决定相应付款。'},
{'决定':'删去哪项专业服务？','先核对':'AI实际替代的交付、验收责任、工程判断是否仍有人承担。','暂不付款的信号':'仅取消“设计费”名目，却没有明确工作和责任归属。','仍可选择':'按相同交付范围比较，保留项目必要的专业核验。'}
],'completion':'判断改变时，允许退回前一步。核验也有成本：先查不成立就必须换址或重做工程的前提，不追求无限补齐资料。','note':'图1｜原创经营决策示意。现行法规示例须同时核对建筑位置、项目行为与排放特征，按所在地及具体项目确认；不评价报道门店合规，也不是法律或工程意见。'}
second={'kind':'compare','layout':'fitout-delivery','label':'同一张效果图，四种尚未回答的施工问题','scope':'以下为作者构造的交付差距分析。取餐台冲突是假设情景，不是案例事故；没有复刻真实门店平面、测量值或施工报价。','nodes':[
{'决定':'尺寸：看着放得下 → 实测放得下','效果图能表达':'空间感、视觉比例与风格意图。','施工前补什么':'实测尺寸、设备尺寸、操作及维护空间。','晚确认可能牵动':'柜体定做、设备位置与相邻工种返工。'},
{'决定':'动线：画面宽敞 → 动作走得通','效果图能表达':'柜台和取餐区的大致关系。','施工前补什么':'按实际尺寸放样，走一遍备餐、打包、取餐动作。','晚确认可能牵动':'取餐台和设备操作位置相互挤占，需重新布置。'},
{'决定':'工程：外观完整 → 条件可执行','效果图能表达':'门头、墙面与设备外观。','施工前补什么':'安装、清洁维修及拟改造条件；按实际要求确认专业专项工作。','晚确认可能牵动':'管线与设备适配、是否允许改造、费用及开业时间。'},
{'决定':'报价：总价好看 → 交付可核对','效果图能表达':'希望达到的视觉结果。','施工前补什么':'尺寸材料、设备条件、报价项目与交付责任。','晚确认可能牵动':'增项争议、协调工作和原预算以外的支出。'}
],'completion':'没有单列设计费 ≠ 项目净节省。比较相同交付范围，还要考虑增项、设备适配、开业前租金与周转资金。','note':'图2｜原创机制示意，不提供发生概率、成本估计或回本期。长沙报道的现场相似仅支持视觉方案被采用；AI选址准确性和净节省仍缺少证据。'}
story={'id':ID,'headline':title,'lead':lead,'findings':['熟悉品类、房屋条件清楚且改动容易调整时，AI适合先生成可讨论的视觉方案。','第一次经营、改造较大或关键条件未核实时，应先补现场和专业判断，再决定签约及施工付款。','实景像效果图不证明选址准确；没有单列设计费，也不能推出净节省或更快回本。'],'diagram':dg,'secondDiagram':second,'sections':sections,'meaning':'把生成方案的速度用来多比较一次，把资金承诺的速度交给现场事实。先查会迫使老板换址或重做工程的前提，才能在钱难以收回之前保留退出选择。','unknowns':['长沙案例的投入和未付设计费为经营者自述；报道未披露对完整成本、未选铺位表现或后续收益的核验。','媒体页面显示05.01、正文记4月27日实访，本次摘录未明确年份；不据此推定适用现行法的个案结论。','两图为作者机制分析，不是实测流程、真实平面、事故记录或经验证的收益方案。'],'actions':['签约前先核对房屋和拟经营项目的硬条件，再将AI市场判断追溯到同口径资料。','付款前让效果图对应实测布置、报价与责任，对冲突路径先做现场放样。','取消费用项时，同时核对谁继续承担测量、工程判断和验收；条件不清先补核验或换方案。'],'sources':sources}
entry={'id':ID,'path':P,'title':title,'section':'research','topics':['ai','business-model'],'publishedAt':meta['time'],'updatedAt':meta['time'],'excerpt':'长沙小店的现场对照支持AI视觉方案被采用，但签约、施工与省设计费，需要分别核对地址硬条件、交付边界和完整成本。','body':body,'originalBodySha256':meta['sha256'],'sourceUrl':U,'firstGit':meta['commit']}
queries={}
for diagram,suffix in [(dg,''),(second,':second')]:
 q='diagram-'+ID+suffix
 queries[q]={'rows':diagram['nodes'],'source':{'label':diagram['label'],'files':[P],'metricDefinitions':[{'label':'作者提出的核验与交付边界','definition':diagram['scope']+' '+diagram['note'],'componentIds':[q]}],'evidenceFlow':[{'title':x['title'],'detail':x['url']} for x in sources]+[{'title':'研究分析','detail':U}],'caveats':[diagram['completion'],diagram['note']]}}
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',{'surface':'report','title':title,'generatedAt':meta['time'],'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries})
write('fitout-source-previews.json',{
 sources[0]['url']:{'title':sources[0]['title'],'summary':'记者对照聊天记录与门店，观察到效果图和实景相似。投入4万多元、没有支付设计费是店主自述；报道未披露对完整成本、选址预测或经营收益的核验。页面05.01及实访4月27日未明确年份。','source':'潇湘晨报官方账号，2026-11-05核验','approvedForReport':True},
 sources[1]['url']:{'title':sources[1]['title'],'summary':'第二百五十条对指定建筑位置内新建、改建、扩建产生油烟、异味、废气的餐饮项目规定禁止性要求。用于当前项目核验示例，不是对报道门店的合规判断，须按具体项目和所在地确认。','source':'生态环境部公布的法律文本，2026-11-05核验','approvedForReport':True},
 sources[2]['url']:{'title':sources[2]['title'],'summary':'第十二、十三条涉及与食品经营相适应的场所、设备设施、合理布局与工艺流程及相关申请材料。第六十四条说明省级已对小餐饮监督管理作出规定的，依其规定执行。具体项目须向所在地市场监管部门确认适用要求。','source':'市场监管总局规章原文，2026-11-05核验','approvedForReport':True}
})
print(meta['sha256'],len(sections),'sections; two original mechanism diagrams')
