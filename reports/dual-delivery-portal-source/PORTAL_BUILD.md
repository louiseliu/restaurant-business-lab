# 两篇增量并入完整62篇门户：本地可复建源码

本轮仅整合已完成的Kotipizza与Fourth单篇，没有新增或改写研究。正文首次入库分别为a9a3137240790b5ef12abe6273adb8e0dd09505b（2026-11-05T23:17:18Z）与cb37b545b6d51d5fba07486b632476a6a117a518（2026-11-05T23:20:56Z）。首次入库时间不是原始来源发布日期。

## 输入和复建

本小型目录包含增量脚本、冻结基线指纹、测试与QA，不含HTML、ZIP、dist、完整运行时、缓存或私人绝对路径。需要可读的完整60篇门户基线，以及兼容的官方Data构建工具。它不是全部历史源码的独立镜像。

1. 从louiseliu/restaurant-business-lab的固定提交ab4fd880e04667a4c8d8fbb71ceeb3d70454aa84取回reports/dynamic-delivery-source与reports/forecast-reimport-source。分别作为KOTIPIZZA_SOURCE与FOURTH_SOURCE参数，只读使用，不依赖单篇standalone工程。
2. 原始正文可分别从首次提交的research/2026-11-05-kotipizza-pricing/note.md、research/2026-11-05-forecast-reimport/note.md取回，各自同目录sources.md提供主张边界。本合并读取冻结article-entry.json与illustrated-story.json，核对全文及sources正文的SHA256，不改写已发送成品。
3. 在新的PRODUCTION_DIR放置本目录为portal-archive-source。运行python portal-archive-source/prepare_portal.py PRODUCTION_DIR EXISTING_PORTAL60。334项基线文件必须与baseline60-sha256.json一致；目标已存在或基线有新编辑时拒绝。先另行保存和审查新编辑，不能强制覆盖。
4. 运行python portal-archive-source/build_portal.py PRODUCTION_DIR KOTIPIZZA_SOURCE FOURTH_SOURCE NODE DATA_APP_MJS SANITIZATION_DIR。NODE为官方Node可执行文件，DATA_APP_MJS为官方scripts/data-app.mjs，SANITIZATION_DIR可用FOURTH_SOURCE/support或仓库reports/public-site-sanitization。
5. 流程实测合并守卫，先预检两篇全部身份、query与文件冲突，再追加两篇及四项query。仅新增六个图文组件/CSS/来源预览文件；作者reader只加入两篇分支。原门户身份、主题、时间线、导出偏好、受保护运行时和全部旧内容保持。
6. 脱敏检查只读运行，buildStatus设为complete后使用官方prepare、build --separate-data、export-offline。子进程不带可选会话标记环境变量。正式build manifest核验HTML和数据sidecar字节数与SHA256。输出PRODUCTION_DIR/timeline62-dual-delivery.html，仅本地保存。
7. test_portal_preservation.py核验旧对象、冻结全文/来源、两图行/组件绑定、编译JSON、样板及五项下载、递归ZIP CRC和内部release manifest、数据载荷与脱敏；test_reader_routes.mjs执行实际路由辅助函数及URL往返、数量、AI筛选和新旧时间排序。它们不代表浏览器交互验证。

## 已核验结果

62篇研究、82份完整原文、62篇图文、2个样板、AI40、127项queries。旧80份原文、60篇图文、123项queries及330项无需改动的基线文件逐项不变。legacy、主门户reader、两份内嵌HTML及五项下载保持。检查161项文本载荷、2个递归ZIP和1份内部release manifest。

完整HTML为13,738,556字节，SHA256：7333bc3064f85e83364dc4602132d0ae141dd4d0d819b7c57247507ad1360fe5。新的无dist/缓存/node_modules目录完成同一小型脚本的prepare→build→export及所有测试，HTML逐字一致。见portal-reproducibility.json。

防覆盖测试验证正文、摘要、图文lead、query来源标签和导出偏好的既有编辑不丢失。重复合并、身份/query冲突、计数异常及第二篇组件/CSS/预览/符号链接冲突全部在写入前拒绝。

Fourth共享S2标题仍遗漏第19页，第二图注释和定义已正确包含第19页；这是不影响研究事实的既有展示缺项。本轮不修正，保留单篇作者源与成品一致，见presentation-status.json。

## 未完成的验证和边界

完整门户视觉、窄屏、深浅主题、来源面板、点击导航/历史/滚动、编辑持久化、下载点击、打印、实际断网及浏览器日志未验。既有HTTP ERR_CONNECTION_REFUSED与file协议拒绝继续记录；未重试、换路、重新托管、修改安全设置或访问受限原站。未上传任何HTML/ZIP、发布站点或改变权限。

只保证本次可读的60篇本地基线完整保留，不等于恢复不可读历史或未归档编辑。原公开站不在本轮操作范围，不能把本地62篇称为线上已更新。小型源码归档、完整门户附件、大文件归档及原站同步由上级任务另行处理；本构建脚本不包含网络或远端写入。
