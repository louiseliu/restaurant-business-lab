# 第58篇呷哺退出现金：完整门户本地增量复建

固定正文提交：5387f063f8624ff03d2c38cf097d3c5f5ab538f5。文章首次入库时间2026-11-05T20:15:51Z，不作为来源发布日期。正文与sources.md哈希见frozen.json。

## 输入与复建

本目录仅为门户增量脚本/测试/QA；正文、图文组件、reviewed queries、frozen.json复用同级archive-source，不重复单篇作者源。本目录是小型作者源码，不含门户HTML、ZIP、dist、完整运行时或私人元数据。完整复建需要可读的57篇门户源、对应公开note.md及同目录sources.md、当前官方Data工具和公开仓库reports/public-site-sanitization工具。保留用户工作副本，不能覆盖它。

1. 从公开仓库取回 reports/xiabu-exit-portal-source（本目录）及 reports/xiabu-exit-source（单篇作者源）。在新的PRODUCTION_DIR下分别放为portal-archive-source、同级archive-source，并保留已验证单篇standalone（只用于核验门户与单篇身份不同）。
2. 运行 python portal-archive-source/prepare_portal.py PRODUCTION_DIR EXISTING_PORTAL57。它核对baseline57-sha256.json，拒绝基线差异及已存在目标，再创建baseline57和portal58。遇到新用户编辑应先保存和重新审查，不得强行覆盖。
3. 运行 python portal-archive-source/build_portal.py PRODUCTION_DIR NOTE_MD NODE DATA_APP_MJS SANITIZATION_DIR。后三项为官方Node、官方data-app.mjs、公开脱敏工具目录。脚本无网络、上传、提交或发布调用。
4. 流程先进行合并守卫测试，再添加1篇、2个query和3个本篇图文文件。只对作者reader增加本篇分支，不改受保护运行时、站点身份、旧文、主题或用户偏好。正文、故事、来源、图表行、旧queries及旧文件均做字节/对象级核验。
5. 通过脱敏测试后，设置buildStatus=complete，执行官方prepare、build --separate-data和export-offline。构建子进程不带可选会话环境变量；保留原始官方manifest，核验实际HTML及sidecar的大小、SHA256。离线HTML输出timeline58-xiabu-exit.html。
6. test_portal_preservation.py检查冻结全文/来源、完整旧数据、旧文件、编译JSON、样板、五个下载、递归ZIP的CRC与内部manifest、公开内容及离线产物脱敏。test_reader_routes.mjs执行实际路由辅助函数、URL往返、计数/排序；不声称浏览器交互已验。test_portal_merge_guard.py验证用户正文、摘要、故事、query及导出偏好保留，重复与身份/query/文件/符号链接冲突均零写入拒绝。

## 本轮结果

本地门户58研究 / 78全文 / 2样板 / AI37 / 119queries。保留77篇原文、57篇故事、117个queries及321项非必要变更基线文件。新增呷哺研究属于商业模式，不错误计入AI专题。全文HTML 13,550,513字节，SHA256：5d71863953492fa7b28c7d9a516a6810aae8967def61b30a332ebfdeefa906e3。

官方构建/离线导出、静态完整性、脱敏和路由辅助函数检查通过。完整门户视觉、窄屏、深浅主题、点击导航/历史/滚动、编辑持久化、下载点击、打印、实际断网与浏览器错误日志未验。此前单篇HTTP预览ERR_CONNECTION_REFUSED，file协议被拒绝；本轮没有重试、换路绕过或修改安全配置。没有发布、上传或重发原站，也没有对原站可读性作新判断。

仅保证本次可读57篇基线得到完整保留，不等于恢复不可读历史或未归档用户编辑。大HTML入库、站点同步、其他历史附件均是独立事项。

最终小源码已在新目录执行完整prepare_portal.py → build_portal.py复建，输出HTML逐字及SHA256一致；见portal-reproducibility.json。未沿用原dist、离线导出或缓存。
