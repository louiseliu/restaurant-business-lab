# 第60篇平台AI申诉：完整门户本地增量复建

固定正文提交：dc3c37fbf9a84e8f7de9dc13e5f9046d63fca91e。文章首次入库2026-11-05T22:15:13Z，不作为原始来源发布日期。正文和sources.md的SHA256见同级platform-appeals-source/frozen.json，未改写原文或首次入库时间。

## 输入与复建

本目录仅含门户增量脚本、测试和QA，正文、图文组件及reviewed queries复用同级platform-appeals-source。完整复建需要可读的59篇门户源、冻结公开note.md及同目录sources.md、兼容官方Data工具和仓库reports/public-site-sanitization工具。不含HTML、ZIP、dist、完整运行时、缓存或私人元数据。

1. 从公开仓库取回reports/platform-appeals-portal-source和reports/platform-appeals-source，在新的PRODUCTION_DIR分别放为portal-archive-source、archive-source。无需单篇standalone工程。
2. 运行python portal-archive-source/prepare_portal.py PRODUCTION_DIR EXISTING_PORTAL59。它核对baseline59-sha256.json的331项指纹，拒绝基线差异和已存在目标，再建立baseline59与portal60。新用户编辑必须先保存并重新审查，不强行覆盖。
3. 运行python portal-archive-source/build_portal.py PRODUCTION_DIR NOTE_MD NODE DATA_APP_MJS SANITIZATION_DIR。后三项为官方Node、data-app.mjs及公开脱敏工具目录。脚本不含网络、上传、提交或发布操作。
4. 流程先测试合并守卫，再新增一篇、两项query及三个本篇图文文件，只在作者reader加入本篇分支。保留门户身份、原UI、时间线、主题、导出偏好及受保护运行时。原文、故事、来源、图表行、queries和旧文件逐项核验。
5. 脱敏检查后设置buildStatus=complete，运行官方prepare、build --separate-data与export-offline。构建子进程不带可选会话环境变量，保留并核验官方manifest、HTML和sidecar大小与SHA256。离线输出timeline60-platform-appeals.html。
6. test_portal_preservation.py检查冻结全文和来源、编译JSON、旧数据和文件、两项嵌入样板、五个下载、递归ZIP的CRC和内部manifest、数据载荷及脱敏。test_reader_routes.mjs执行实际路由辅助函数、URL往返、数量和排序，不声称浏览器点击已验。test_portal_merge_guard.py实测保留用户正文、摘要、故事、query及导出偏好，重复和身份、query、文件、符号链接冲突在写入前拒绝。

## 本轮结果与范围

本地完整门户60研究/80全文/2样板、AI39、123项queries。原79份全文、59篇图文、121项queries及327项无需变更的基线文件保持不变。全文HTML为13,645,958字节，SHA256为250ba17437c63dd0b866b987ca35cb17633940b3334fa93843bc46716a8157a3。

官方构建和离线导出、静态完整性、实际路由辅助函数、153项文本载荷、5项下载、2个递归ZIP容器和1份内部release-manifest检查通过。脱敏工具未改动已有内容。全文、legacy、嵌入样板和下载内容均纳入检查。

独立审校发现单篇第二图来源定义标签复用第一图。门户导入仅将该标签改为“留证投入取舍”，详见presentation-correction.json；定义、行、来源、正文和时间不变。已发送单篇及其作者源保留，不重发附件，不将此展示标注差异记作新研究。

最终小型源码在不含单篇工程、缓存、旧dist或node_modules的干净目录完成prepare→build→export复建，HTML逐字及SHA256一致，见portal-reproducibility.json。独立静态核查见portal-independent-qa.json。

完整门户视觉、窄屏、深浅主题、来源面板、点击导航/历史/滚动、编辑持久化、下载点击、打印、实际断网和浏览器错误日志未验。既有HTTP预览ERR_CONNECTION_REFUSED及历史file协议拒绝仍保留；本轮未重试、换路、重新托管或修改安全设置。未访问受限原站、发布或改权限，也未重新判断原站当前可读性。

仅保证本次可读59篇本地基线完整保留，不等于恢复不可读历史或未归档用户编辑。原公开站仍只引用最后核验v19的20/40/2、AI9，当前可读性未复核，42项待同步。大HTML/ZIP归档、门户附件、原站同步、历史附件替换、费用原归档、旧离线快照及既有视觉待办独立保留。
