# 餐饮商业模式研究院

以可验证证据推进餐饮商业问题研究，持续维护研究成果、商业分析方法、研究记录与 `restaurant-business-model-lab` Skill。

## 研究重点

在餐饮商业模式研究之外，重点增加 **AI 在餐饮中的实际应用**：优先核验真实使用场景、实施与持续运营成本、经营效果及可复制条件。区分供应商宣称、试点结果与独立验证；普通自动化、广告实验或流程优化不因新方向而改标为 AI，不补造尚无证据的文章。

## 当前状态

初始化日期：2026-10-27。

- 已接收并检查上传的 Skill v0.3：仅含四个 Markdown 文件，无可执行脚本、二进制或依赖。
- 仓库级 Skill 位于 [`.agents/skills/restaurant-business-model-lab/`](.agents/skills/restaurant-business-model-lab/SKILL.md)。这是版本化的项目配置，不等同于宿主全局注册或已启动后台进程。
- 首次实际研究已由通用口径边界推进到[蜜雪商品收入与加盟网络店日的条件性检验](research/2026-10-27-franchise-evidence/final-report.md)：构造指标至少下降约 4.55%，不能推断终端需求或加盟商利润下降。
- 两轮真实 Pro 回复、公开原始资料回查、独立计算和措辞纠错已完成，详见[协作记录](research/2026-10-27-franchise-evidence/pro-collaboration.md)与[判断修订](research/2026-10-27-franchise-evidence/judgment-revision.md)。[最终研究提交](https://github.com/louiseliu/restaurant-business-lab/commit/e855c67e53e80165f968efed9ef7ba91029cdc1a)已在远端核验。
- [老板版图文 HTML 归档提交](https://github.com/louiseliu/restaurant-business-lab/commit/b9150cb2369b2d6add851a112ae5256b4b43cfb1)已在远端核验，原研究与离线报告均保留。
- 2026-10-28 首次每日早间定时研究已实际执行（Asia/Shanghai）：完成蜜雪证据缺口的有界复查，以及[古茗盈亏平衡与加盟回本口径研究](research/2026-10-28-franchise-payback-definitions/research-note.md)。这是历史招股书核验，不是当天新闻；本轮没有新的 Pro 请求或回复。
- 按用户要求，研究检查现已改为每小时；2026-10-28 05:00 UTC（上海时间 13:00）的首轮小时研究已实际执行，完成[古茗后续加盟商人数桥与留存辨识核验](research/2026-10-28-franchise-payback-definitions/continuation-note.md)。本轮未新增 Pro 请求或回复。
- 按证据价值和可用额度选择 Pro，不是 24 小时后台进程。首次执行不等于未来每次运行均已验证。没有新增付费资源。

## 工作原则

1. 先提出值得解决的商业问题，再按证据选择调查、计算、Pro 协作和验证动作，不机械套用固定流程。
2. 事实、计算、假设和建议分开记录；公开原始资料优先，重复转载不算独立证据。
3. 总部收入、利润、终端交易额与加盟商单店收益分别分析，不能相互替代。
4. Pro 是共同思考伙伴，其回答不是事实证明。核验来源和计算，并保留分歧与判断修订。
5. 外部操作只在明确授权范围内进行；本公开仓库不得存放凭据、私有经营资料或个人敏感信息。

## 全文与图文时间线

原站当前为公开 v15：17 篇研究有独立图文读本（每篇至少两幅有信息价值的图），同时保留 37 份 Markdown 全文、方法及历史记录和原蜜雪老板版。当前原站研究内容基准为 `0df8d429a648e6d64383879ac900110dc5898bff`；按首次 Git 提交时间倒序、显示北京时间，不冒充来源发布日期。

[下载公共安全图文 HTML](reports/restaurant-illustrated-public/restaurant-research-illustrated.html)，用启用 JavaScript 的现代浏览器打开；无需外部 CDN。[作者源码与维护流程](reports/restaurant-illustrated-public/source-final/BUILD.md)。这是静态同步，不是实时抓取，不新增定时任务；AI 专题已有首篇[食物减损机制研究](research/2026-10-29-ai-food-waste/note.md)，[独立离线图文](research/2026-10-29-ai-food-waste/report.html)与[作者增量源](reports/ai-food-waste-site-source/BUILD.md)已归档；原站 v6 已发布验收。后续研究须先核验证据，再制作逐篇图文与来源/未知/行动说明，不能用装饰图或虚构数字替代分析。

公共导出将私人协作链接替换为“私人协作会话，未公开”，不改写既有仓库历史。原文字段 `originalBodySha256` 仅标识脱敏前来源；[脱敏正文校验清单](reports/restaurant-illustrated-public/rendered-article-manifest.json)另记录导出正文哈希，不能将两者混同。已做桌面与窄屏浏览器检查，未宣称 iPhone 真机或打印实测。

## 实战样板（研究者示范，非经营成效实测）

- [外卖活动条件计算器](tools/delivery-campaign/README.md)：可离线替换假设、查看贡献情景；默认值仅演示，活动归因订单不自动等于增量。
- [AI 辅助经营周报](examples/ai-weekly-report/README.md)：完整模拟输入、实际执行的 Python 清洗/分析、AI 辅助文稿及逐记录追溯；不是客户实测，没有外部模型 API、真实数据上传或节时/准确率收益测量。
- [站内样板承载源码与复建说明](reports/samples-site-source/BUILD.md)：从本仓库相对路径读取已核验 HTML/ZIP，检查哈希后生成站内载荷，不自动发布。

两个样板可在原站阅读并下载各自完整包，单独计为示范，不增加公开站 17 篇研究的计数。样板包中的“local-only／未发布”描述保留其制作冻结时状态；当前公开归档以提交历史为准。此前整站离线 HTML 仍是 **v4 固定快照**，不含 v5 样板入口或 v6 新文章；后续分别归档两份独立样板、可复建承载源及新文章独立 HTML/增量源，不声称另有最新整站离线包。v5 的连接与发布仍须官方 Data runtime 和实际验收。

新增第 10 篇 [AI 加购研究](research/2026-10-29-ai-cart-recommendations/note.md)，附[独立离线图文](research/2026-10-29-ai-cart-recommendations/report.html)与[作者增量源](reports/ai-cart-site-source/BUILD.md)。原站 v8 已发布并验收，10 篇研究/30 份全文/2 项样板，保留 v7 阅读体验。历史平台 A/B 是作者报告，不是本项目门店实测；不能将客单提升视为小店利润提升。当前更新是静态增量，不是自动同步；旧 v4 整站离线 HTML 快照保持不变，也不含本篇。

## 新增案例与实施短篇

原站 v10 发布验收时为 **13 篇研究、33 份全文、2 项样板**：新增 [AI 电话接待](research/2026-10-30-voice-receptionist/report.html)、[AI 菜品图](research/2026-10-30-food-images/report.html)、[自动订货验收](research/2026-10-30-restocking-controls/report.html)三篇独立图文。[共用作者增量与复建说明](reports/batch-2026-10-30/BUILD.md)保留原 UI、旧研究及公开脱敏流程；订货篇是规则/流程核验，不标成 AI 成功案例。并行深研与有核验价值的案例/实施短篇，不以每日两篇为上限，也不降低来源、安全及事实边界要求。当前为静态增量，旧 v4 全站离线快照不更新；三篇 HTML 可各自离线阅读。

新增第 14 篇[炒菜机器人与整条出餐线研究](research/2026-10-30-robot-kitchen/note.md)，附[独立图文 HTML](research/2026-10-30-robot-kitchen/report.html)及[最小作者增量](reports/robot-kitchen-site-source/BUILD.md)。公开原站 v12 发布验收时为 **14 篇研究/34 份全文/2 项样板**，AI 分类仍为 4 篇；机器人篇只归商业模式，不把机械自动化当已验证 AI 效果。保留电话研究院修订、既有界面、公开脱敏及下载；不是新全站离线快照或自动实时同步。

新增第 15 篇[餐饮软件退出与数据接续研究](research/2026-10-30-software-exit/note.md)，附[独立图文 HTML](research/2026-10-30-software-exit/report.html)与[最小作者增量](reports/software-exit-site-source/BUILD.md)。公开原站 v13 发布验收时为 **15 篇研究/35 份全文/2 项样板**，AI 分类仍为 4 篇。该篇是采购机制分析，区分正常导出与终止安排，不是产品实测、AI 成效或法律意见；旧内容、公开访问与脱敏规范继续保留。

新增第 16 篇[Q-Smart 与店务任务兑现研究](research/2026-10-30-qsmart/note.md)，附[独立图文 HTML](research/2026-10-30-qsmart/report.html)及[最小作者增量](reports/qsmart-site-source/BUILD.md)。公开原站 v14 已发布验收，当前为 **16 篇研究/36 份全文/2 项样板，AI 研究 5 篇**。区分已披露的发现缺员、建议替补、发起电话与尚无成效数据的确认/到岗；任务验收框架是研究建议，不是已实现闭环或新 Pro 审阅。静态增量不更新旧全站离线快照。

## 公开站点与安全复建

用户已授权原站公开访问，v9 脱敏版本已发布；匿名访问首页、数据与 5 项下载均返回成功，公开端不可编辑。v9 发布时为 10 篇研究、30 份全文、2 项样板，UI 和经营数据保持不变；后续 v10 内容增量及当前数量见上节，公开访问与脱敏要求继续保留。

后续从历史作者源复建时，必须在生成文章与样板载荷后、构建前执行[公开内容脱敏补丁与测试](reports/public-site-sanitization/BUILD.md)，再检查构建产物和下载。该补丁通用清除私人协作链接及本地线程元数据，并更新派生内容校验值；不改既有历史文件、不改变访问权限、不自动发布，也不替代完整公开前审查。旧整站离线快照不是 v9 发布物。


## 2026-10-30 15:00 UTC：视觉收银新篇与待同步状态

第 18 篇[视觉收银研究](research/2026-10-30-vision-checkout/note.md)已完成正文核验，附[独立离线图文 HTML](research/2026-10-30-vision-checkout/report.html)与[最小作者增量](reports/vision-checkout-site-source/BUILD.md)。首次入库为 `98b377faa73538f6fd0168ceba7e7ec2f53faf8d`，时间 `2026-10-30T15:02:15Z`。文章比较认菜与认盘计价的维护责任、例外处理与岗位安排，不采用供应商准确率、排队改善或财务效果数字；未开展门店实测或新增 Pro 咨询。

**本篇尚未上站。** v16 发布尝试的数据资产上传返回 HTTP 400，未通过完整回读；已恢复并核验原公开 v15，当前线上仍为 **17 篇研究/37 份全文/2 项样板，AI 研究 6 篇**。本地增量的 18/38/2/7 是目标计数，不是线上状态。后续需修复上传并重新核验；本次不声称站点同步完成。

费用证据第 17 篇已在 v15 公开可读，但其独立 HTML/源码的最终 GitHub 归档仍等待原操作结果，与本篇的资产上传待办分别记录。本次不补交、不重试该批文件，也不把其待办标为完成。旧 v4 整站离线快照不变。

## 阅读界面维护

原站 v7 阅读体验更新已发布并验收：研究、实战样板、全部资料分区；搜索与主题筛选、文章目录、邻篇导航、返回列表和浏览器前进/后退状态恢复。正式站核验了 AI＋厨房筛选及返回查询状态，保留 9 篇研究、29 份全文、2 项样板与原访问范围。

[UI/UX 作者源与路由测试](reports/restaurant-ux-source/BUILD.md)仅为界面增量，依赖既有 Data runtime 与现有正文/样板数据；不自动发布。原文事实、数据与既有独立/整站 HTML 快照均未追溯改写，不把源码测试当成手机真机验证。

## 目录

- [给餐饮老板的图文 HTML 报告](reports/README.md)：下载后浏览器打开，含图解、经营问题与证据边界。

- [Skill 与参考文件](.agents/skills/restaurant-business-model-lab/SKILL.md)
- [研究规范](methods/research-standard.md)
- [来源发现方法与16主体扩充登记](methods/source-discovery.md)：中文中小餐饮与AI线索，逐项标明本轮可读范围、利益和证据边界。
- [当前进度](state/current.md)
- [研究日志](logs/2026-10-27-initialization.md)
- [本轮研究结论](research/2026-10-27-franchise-evidence/final-report.md)：条件性边界结果、反例、经营意义与未解问题。
- [原始初查稿](research/2026-10-27-franchise-evidence/provisional-research.md)：历史初始判断，保留其写作时状态；不要将其中尚未咨询的描述当作当前状态。
- [独立边界复核](research/2026-10-27-franchise-evidence/bounds-check-findings.md)、[来源补充](research/2026-10-27-franchise-evidence/source-additions.json)、[可运行代码](research/2026-10-27-franchise-evidence/bounds-check.py)。

## 首次闭环验收

必须能够提供：真实研究问题与来源、实际执行的验证、真实 GPT Pro 模型及会话使用证据、因核验而保留或修订的判断，以及已在远端核实的 GitHub 提交。任一环节未完成都应明确标注，不以计划或模拟代替成功。

## 使用 Skill

将仓库的 `.agents/skills/restaurant-business-model-lab/` 作为项目级 Skill 交给支持相应目录约定的宿主；应以宿主实际发现结果为准。本文件不承诺跨宿主自动加载。需要全局安装时，使用宿主支持的安装方式，并另外核验发现结果。





