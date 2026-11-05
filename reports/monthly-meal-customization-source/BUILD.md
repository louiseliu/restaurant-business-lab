# 月餐定制：完整图文与第45篇门户增量

正文固定提交 `d819c713ba57d611170f531848e33aa15c6e50b9`，首次入库 `2026-11-05T04:05:13Z`，正文SHA256 `2c43f7b73c0314a0b9d68faceb7dfad8e881d03e1872c4d66d66c47aecd6ddd9`。文章ID为 `research-2026-11-05-monthly-meal-customization-note`。

本篇讨论稳定月餐客户增加后，何时值得让AI辅助整理定制要求。研究图文区分媒体报道的业务动作、店主自报和作者提出的验收示意；不把业务转型与收入变化归因为AI，不计算净利润、净节省或回本。

## 基线和保护范围

完整门户以排班同ID修订后的44篇可读作者工程为基线（归档提交 `28a6aa0199867b843445c6b24fdec540c6b4cd8b`；完整离线基线SHA256 `84bd1f2dbce2b6190a679df7ac4ad8b5110d5921a8e89cdd4f2f820193e5052b`），已经包含菜品图同ID修订、盘点第三图及reader修订。该44篇工程从可读22篇基线与固定公开小源重建；保留测试只证明本轮可读基线未受损，不证明缺失的历史44篇工程或未归档编辑已恢复。

在隔离副本中运行 `python integrate45.py PORTAL_SRC ARTICLE_SOURCE`。脚本在写入前校验44/64/2、AI27及91项query，确认新ID和两项query不冲突，验证全文SHA256与两图节点对应。仅追加本篇、两项query及专用图组件，在完整reader增加图组件导入和布局分支，并且只对本篇将完整原文中的相对 `sources.md` 链接展开为固定GitHub提交链接；源正文JSON字节及hash不变；不以独立reader覆盖门户。保留原门户身份、旧全文、图文、queries、共享代码、样板和下载。

## 独立图文

使用当前安装的官方Data `prepare-data-app.mjs --surface report --output NEW_PROJECT --snapshot article-reviewed-data.json` 创建新独立文章身份。读取生成的AGENTS和prepare返回的组件文档。执行 `python prepare_standalone.py NEW_PROJECT`，在 `src/content/report/` 安装本篇JSON、专用图组件和shared中的单篇reader/timeline样式，保留官方壳及源检查能力。正文使用RichNarrative，图中reviewed rows只读；两幅图各有自己的query和来源作用域。reviewed rows使用扁平中文字符串列，与图文节点完全一致，避免来源数据预览出现`[object Object]`。

## 构建与脱敏

1. 运行仓库 `reports/public-site-sanitization/test_sanitization.py`，在文章/样板载荷生成后对两个项目运行脱敏脚本与 `--check`，再检查本篇数据及来源。
2. 对两个项目执行官方 `data-app.mjs prepare --project-dir PROJECT` 解析当前文档；普通构建使用 `build --project-dir PROJECT --separate-data`，不编辑受保护运行时、不安装替代依赖、不切换渲染器。
3. 通过官方 `export-offline` 导出到各项目的 `.data-app-offline/exports/`，再复制完整单文件为 `monthly-meal-customization.html` 和 `timeline45-monthly-meal.html`。交付副本仅清除可选本地线程meta；split HTML本身不是完整离线交付。
4. 运行 `python test_preservation.py WORK_ROOT BASELINE44 NOTE_MD` 和 `node test_reader_routes.mjs PORTAL_REPORT_DIR`。将归档的`baseline44-sha256.json`放到WORK_ROOT下并命名为`baseline-sha256.json`；单篇官方新建后的指纹记录为`standalone-prepared-sha256.json`。逐字保护基线，验证新篇冻结全文、图文/query一一对应、最终HTML解码内容、split构建manifest、递归隐私、5下载载荷及2ZIP。
5. 检查中使用creating/updating状态；内容和必要检查结束后，将两套项目的buildStatus设为complete，再重建、导出和重跑测试。
6. 浏览器验收另记。静态检查、源数据相符和构建成功不等于视觉或交互验收。只报告实际检查的桌面/手机范围。

## 发布边界

本目录仅归档小型作者源、测试和回执，不含大型HTML、dist、凭据或私人附件标识。完整HTML的本地生成、附件发送与原站同步分别记录。未访问此前403原站、未改变权限、未重试或替换任何旧受限附件。原公开站只能引用最后验收v19的20/40/2、AI9；本地新数量不代表线上状态。旧全站离线快照及其他独立待办保持。

## 本轮已执行的检查

- 新篇冻结正文hash与实际首次提交/时间一致，六节叙事和完整原文保留；两图均为原创研究示意，只有两篇主源。未把自报成本或承载量画成效果数据。
- 官方prepare、separate-data build及完整offline export均成功。单篇1/1、2queries；完整门户45篇研究/65份全文/2样板、AI28，93queries。
- 旧64份全文、44篇图文、91项queries以及287个基线文件逐字/逐对象保留。只有数据、文章索引、故事集合和作者reader发生必要改变，另新增两图组件与样式；门户身份和全部受保护文件不变。
- 单篇官方新壳241个非内容文件保持。最终HTML解码的正文/故事与JSON一致，split HTML及snapshot的bytes/SHA256和reviewed data均核对一致。
- 递归隐私检查80项门户文本载荷、13项单篇载荷，保留5下载和2ZIP；全局脱敏测试、来源字符串行检查、路由、AI筛选数量、倒序、合并冲突拒绝及用户编辑保留测试通过。
- 首轮桌面验收发现两图来源预览把嵌套cells显示为对象字符串。已在作者数据/组件层改为扁平中文列，未改受保护运行时。两图数据预览和搜索已独立复测通过；最终范围以`independent-qa.json`为准。
- 两套项目buildStatus已置complete并再次构建、导出、重跑静态验收。最终完整单篇HTML为2,927,091字节，SHA256 `527acaf29fb741515247bb49522f03b8503b2f099cd9cc94e950d2d4166fdb9d`；完整门户为13,032,425字节，SHA256 `bcc4fd1f300c31b0ef216804cc9af5ca9b00191fe340b89445a93844fa96e5b7`。

这些检查不代表原站更新或附件发送成功。手机、真机、打印、实际断网打开、全45篇逐篇视觉与所有下载点击没有因此获得验收。


## 交付状态补记

最终限定桌面验收通过，详见`independent-qa.json`。2026-11-05 04:17 UTC，新篇独立HTML附件发送请求已被接受，不代表已打开或下载。门户仅本地完成，未同步原站；本次新篇使待上站合计增至27项。既有排班/视觉旧附件与其他待办不受影响。
