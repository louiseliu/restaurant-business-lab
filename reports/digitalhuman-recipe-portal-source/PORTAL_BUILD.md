# 数字人直播与AI新品研发合批门户

本目录是从可读65篇本地门户追加第66、67篇的增量源码与真实核验，不是完整历史运行时镜像。两篇冻结正文、来源及已发送单篇作者输入未改；用户现有本地内容按原对象/字节保留，不声称恢复不可读原站编辑。

## 固定基线与输入

归档前读取 main `0df6ef177aee33cc61518e8cfe9a65e3bd81135e`，完整树1511个文件；仓库AGENTS、研究Skill、current及两篇状态已读。此前完整门户源码归档为 `397040b1a0def6f673d79f47ef185fb215c5f045`；25项公开源码Git blob与本地归档逐项一致。完整65篇本地基线351项指纹见 baseline65-sha256.json，基线不被改写。

两份作者源为相邻目录 ../digitalhuman-source 与 ../ai-recipe-source。实际18项整合输入由 input-fingerprints.json 冻结。四份原文/来源另从最新main逐字回读并核Git blob，见 input-remote-verification.json。数字人首提 `e8a30863c44caf6b8f50dc62d4414352a332b088`，实际首次时间 `2026-11-06T03:12:41Z`；新品研发首提 `dd45f0e85ae903ac64732e62fa90f929cb5917fc`，实际时间 `2026-11-06T03:16:45Z`。不把图文构建时间替换首次入库或来源发布日期。

## 复建

需要完整、可读的65篇本地门户、上述两份作者源、Python 3及兼容官方Data工具。不得用缺失历史的局部源码冒充完整基线。

1. 将本目录放为新的 `PRODUCTION_DIR/portal-archive-source`。
2. `python portal-archive-source/prepare_portal.py PRODUCTION_DIR BASELINE65`：核对全部351项指纹，目标须不存在；复制到隔离 baseline65 与 portal67，不覆盖源基线或用户修改。
3. `python portal-archive-source/build_portal.py PRODUCTION_DIR DIGITALHUMAN_SOURCE AI_RECIPE_SOURCE NODE DATA_APP_MJS SANITIZATION_DIR`。最后参数可用任一单篇源码的 support 目录。
4. 合并前验证冻结输入、篇数、身份、query绑定、正文来源哈希、首次时间、六项新文件与链接冲突和reader锚点。所有预检结束后才写入；已有文章、故事、query与导出偏好保持，不使用单篇reader覆盖门户。
5. 只新增两篇、四项query及六项作者图示/预览文件，在既有图文reader追加分支。保留新品article的zh-CN及GEO既有中文属性；数字人保持其发送版根语言继承，不擅自修订或替换附件。主reader、legacy、运行时、样板、主题与稳定报告身份保持。
6. 只读脱敏检查后设 buildStatus=complete，运行官方prepare、build --separate-data和export-offline。构建子进程不传可选会话标记。导出原字节复制为 timeline67-digitalhuman-recipe.html，不改编译HTML。

## 本轮实际结果

本地成品为 **67研究/87全文/67图文/2样板、AI45、138项queries**。HTML **13,982,641字节**，SHA256 `a33e32b064a67577873677001382f747e0e7d1b9b1e0b7745b73a1cb312521e0`。它只保存在本地，未上传、发送或Git归档。

- 85份旧全文、65篇旧图文、134项旧query逐对象保持；347项无需改动文件及源基线351项指纹复核通过。两篇完整六节叙事、来源台账、四图与固定首提保留。
- 合并保护32项通过：用户正文/摘要/图文/query/导出偏好保持，篇数/身份/query冲突、六项文件及悬空链接冲突、reader锚点变化、重复合并和18项冻结输入字节篡改均在写入前拒绝。临时副本用于测试，无正式数据破坏。
- 主测试检查183项文本载荷、5项下载、2个递归ZIP、内部release manifest、编译JSON和分离数据/manifest；路由测试运行实际URL辅助函数与往返、数量、分类和首次时间排序。
- 全新无dist、缓存和node_modules目录按相同官方流程复建，HTML逐字一致，九项执行源/输入文件与复建副本一致。
- 独立静态审计1,476项检查通过，26个编译JSON、6段离线snapshot与365,001字节源数据逐字一致，182项载荷、45个ZIP成员、5项下载和四图rows/来源作用域核对通过。独立与主测试载荷计数口径不同。详见 independent-audit/。
- 两单篇的原静态、防覆盖与三项脱敏单测重跑通过，作者源原字节保持。归档目录不是Data成品目录，误将成品扫描器用于源码目录时因缺少samples.json报错，没有改文件；随后对两个实际单篇及门户正确路径运行扫描通过，源码目录另做清单/语法/隐私模式扫描。

两单篇合批附件请求于 **2026-11-06T03:23:00Z** 被接受，不代表送达、打开或下载。各自字节和SHA256见相邻源码目录的 delivery-status.json。未重发或替换原附件，也未发送完整门户。

## 未完成范围

浏览器桌面/窄屏、深浅主题、实际图形、来源面板、点击/历史/滚动、编辑持久化、下载、打印、真实断网、浏览器日志与屏幕阅读器均未验。既有HTTP/file/原站限制未重试、换路、重新托管或修改权限。静态与复建不代替浏览器验收；未重新联网验证研究来源或复算样板内部业务计算。

原站未同步、当前可读性未复核；只引用最后核验v19的20研究/40全文/2样板、AI9。第21—67篇47项新增及三项既有同ID修订，共50项待同步。已有Fourth共享S2标题缺第19页的展示问题保留。历史四项未确认审计写入及一项同字节JSON仍开放，见baseline-known-gaps.json；没有重试、改名同内容上传或换接口。

HTML归档、门户附件、旧附件替换、费用原归档、原站编辑保护、旧全站离线快照及既有视觉待办继续独立保留。本轮不上传HTML/ZIP、缓存、完整运行时、私人路径、私人会话、交付标识或凭据。大型README/current保留历史，最新小型状态见 ../../state/2026-11-06-portal67.json。
