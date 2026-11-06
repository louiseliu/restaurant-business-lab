# 机器人低初付与AI陪练：69篇本地门户

本目录是从可读67篇本地门户追加第68、69篇的增量作者源码与真实核验，不是独立完整历史镜像。原研究正文、来源、已接受发送请求的单篇作者输入保持不变；不可读原站的用户编辑没有被恢复或验证。

## 输入、身份与复建

归档准备读取 main `e6b87b50fefa87d9d059559f31818ec9251da960`，仓库AGENTS、研究Skill、current及两篇状态已读。旧门户小型源码与最新main的19项文件Git blob匹配；两篇note/sources从该head逐字回读并核对本地字节。完整67篇基线经上一轮保留检查复验，357项指纹见 baseline67-sha256.json。它只被复制，不被改写。

两份输入目录为相邻 ../robot-subscription-source 与 ../ai-practice-source。18项实际合并输入见 input-fingerprints.json。机器人首提为 `2c32d8b669ea8cf6c5835e9598325bbddc73297a`，首次时间 `2026-11-06T04:08:54Z`；AI陪练首提为 `10fb03ca2b9cb138818364d019ec5fb7360cd534`，首次时间 `2026-11-06T04:17:21Z`。不把构建时间写成首次入库或来源发布日期。

需要完整可读的67篇本地门户、上述作者输入、Python 3、Node与兼容官方Data工具。不能用不完整历史源码替代基线。

1. 将本目录复制为新的 PRODUCTION_DIR/portal-archive-source。
2. 运行 `python portal-archive-source/prepare_portal.py PRODUCTION_DIR BASELINE67`。先核全部指纹，目标必须不存在，再复制为baseline67与portal69，保护输入。
3. 运行 `python portal-archive-source/build_portal.py PRODUCTION_DIR ROBOT_SOURCE AI_PRACTICE_SOURCE NODE DATA_APP_MJS SANITIZATION_DIR`。SANITIZATION_DIR可用任一单篇的support目录。
4. 所有冲突和冻结输入预检结束才写入；仅新增两篇、四query、六个作者图示/来源预览文件。5个原文件有必要增量：articles.json、illustrated-stories.json、data.json、IllustratedArticle.jsx与ReportContent.jsx。不覆盖单篇reader到门户，不更换运行时或身份。
5. 冻结entry保留robot的business与AI陪练的ai。仅对robot的新ID增加business-model筛选/列表标签兼容；仅两新ID的相对Markdown链接在渲染时解析到各自固定Git首提。原数据与87条旧文章行为不变。既有语言属性保持，两新篇沿用单篇根语言继承，不擅自替换已发附件。
6. 只读脱敏检查后设buildStatus=complete，执行官方prepare、build --separate-data、export-offline。构建子进程不传可选会话标记。输出原字节复制到 timeline69-robot-practice.html，不修改编译HTML。

## 实际核验

完整本地成品为 **69研究/89全文/69图文/2样板、AI46、142项queries**。机器人设备服务研究是商业模式主题，不算AI成效。HTML **14,077,756字节**，SHA256 `135406278b0fdd62d3f11bf0c79f6697dfe8c9946ea9a33aeacc108df0a299dc`，未上传、发送或Git归档。

- 原87全文、67图文、138项query逐对象保持；352项无需变更文件和357项基线指纹复核通过。两篇完整五节叙事、开篇、来源台账、四图及首提保持。
- 33项合并保护通过：用户正文、摘要、图文、query、reader注释和导出偏好保留；数量、身份、query、文件/悬空链接、两reader锚点、重复整合和18项输入字节篡改都在写入前拒绝。只在一次性副本测试。
- 主检查扫描191项文本载荷，核验5项下载、2个递归ZIP、release manifest、编译JSON和分离数据/manifest。路由测试执行真实URL、topicMatch和resolvePortal69Links辅助函数，逐条确认旧文章行为保持，新条目正确筛选与固定来源链接解析；这不是浏览器交互测试。
- 独立初审发现分类筛选和相对链接两处合并缺陷，按上述新ID范围修复后重新官方构建并审计，初审未作为通过证据。独立最终结果与真实断言数见 independent-audit/portal69-static-audit.json。
- 全新无dist、缓存或node_modules目录按相同官方流程复建，HTML逐字一致；执行源码与输入指纹逐项相同。两单篇原静态、各8项防覆盖及各3项脱敏单测重跑通过，原作者源及成品没有改动。

两篇单篇附件请求于 **2026-11-06T04:20:23Z** 被接受，不代表送达、打开或下载。各自成品字节与SHA256见相邻源码的delivery-status.json。本轮没有重发、替换附件或发送完整门户。

## 尚未核验与保留事项

浏览器桌面/窄屏、深浅主题、真实图形、来源面板、点击/历史/滚动、编辑持久化、下载点击、打印、真实断网、日志及屏幕阅读器未验。既有HTTP/file/原站限制没有重试、换路、重托管或改权限。静态与复建不代替浏览器验收；没有重新联网研究来源或复算历史样板内部业务计算。

原站未同步、当前可读性未复核；沿用最后核验v19的20研究/40全文/2样板、AI9。第21—69篇49项新增与三项既有同ID修订，共52项待同步。旧Fourth共享S2标题缺第19页的展示问题不变。历史四项未确认审计写入及一项同字节JSON继续开放，见baseline-known-gaps.json；未重试、同内容改名上传或换接口。

HTML归档、门户附件、旧附件替换、费用原归档、原站编辑保护、旧全站离线快照及既有视觉待办独立保留。本次不上传HTML/ZIP、缓存、完整运行时、私人路径/会话/交付标识或凭据。README.md和state/current.md保持原字节，当前小型状态见 ../../state/2026-11-06-portal69.json。
