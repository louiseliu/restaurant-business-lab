# 第64篇旧摄像头复用研究并入完整门户

本轮只将冻结的 `camera-reuse` 文章、两幅定性图和来源纳入完整63篇本地门户，不新增或改写研究。正文首次入库为 `eaf8d57c523197ca67a04662f5d48dc45a201c22`，真实时间为 `2026-11-06T01:10:58Z`；该时间不是公开资料的发布日期。正文与来源仍对应首次提交中的 `research/2026-11-06-camera-reuse/`。

## 范围与输入

本目录只保存小型增量脚本、343项冻结基线指纹、真实测试结果与复建说明；不包含完整HTML、ZIP、dist、运行时镜像、缓存或私人环境路径。需要完整且可读的63篇本地门户基线及兼容的官方Data构建工具，本目录不是所有历史源码的独立镜像。不可读的旧版本和原站用户编辑没有恢复。

相应单篇输入为 `reports/camera-reuse-source`，精确输入提交见 `manifest.json`。读取 `article-entry.json`、`illustrated-story.json`、`article-reviewed-data.json`、`frozen.json` 及三项图文组件文件，全部保持冻结输入。63篇基线对应小源码归档 `8fa22f5d558819eea2eddba01bbb38e271f015f7`；该归档的27项可读文件已逐字和Git blob哈希核验，上一轮门户保留测试也已复跑通过。

## 本地复建

1. 在新的 `PRODUCTION_DIR` 放置本目录为 `portal-archive-source`。运行 `python portal-archive-source/prepare_portal.py PRODUCTION_DIR EXISTING_PORTAL63`。脚本先验证343项基线文件指纹，拒绝基线变化或既有目标目录，不覆盖用户修改。先保存、审查新编辑，再另行合并。
2. 运行 `python portal-archive-source/build_portal.py PRODUCTION_DIR CAMERA_REUSE_SOURCE NODE DATA_APP_MJS SANITIZATION_DIR`。`NODE` 为官方Node，`DATA_APP_MJS` 为官方 `scripts/data-app.mjs`，脱敏检查目录可用单篇输入中的 `support`。
3. 合并先核对篇数、文章和query身份、首次提交及时间、正文哈希、双图数据行、组件/样式/预览文件冲突。全部通过后，仅追加一篇、两项query及三项图文源码，并为作者图文reader新增本篇分支。主门户reader、时间线、主题、稳定身份、导出偏好、legacy、受保护运行时和旧文章不变。
4. 脱敏扫描只读执行。内容完成后将 `buildStatus` 设为 `complete`，运行官方 `prepare`、`build --separate-data` 和 `export-offline`。子进程移除可选会话标记环境变量。输出 `PRODUCTION_DIR/timeline64-camera-reuse.html` 只留本地。
5. `test_portal_preservation.py` 检查所有旧对象、冻结正文/来源、两图、编译JSON、数据快照、两样板及五项下载、递归ZIP CRC与内部release manifest和隐私模式。`test_reader_routes.mjs` 实际执行路由辅助函数、URL往返、数量、AI分类和按真实时间排序。这些是静态及函数检查，不是浏览器验收。

独立审计可在主构建后另行复跑：`python portal-archive-source/independent-audit/independent_audit.py --baseline PRODUCTION_DIR/baseline63 --production PRODUCTION_DIR --frozen-source CAMERA_REUSE_SOURCE --output AUDIT_OUTPUT_DIR`。使用新的结果目录，不改写历史审计。

## 已完成验证

64篇研究、84份完整原文、64篇图文、2项样板、AI42、131项queries。原83份全文、63篇图文、129项queries和339项无需变化的基线文件逐项保持；原基线343文件在构建后再次哈希核验，源目录未改。全文、legacy、主reader、两份内嵌HTML及五项下载完整保留。主测试扫描169项文本载荷，检查两个递归ZIP和一份内部release manifest，分离构建HTML/数据文件与manifest逐字核验。

防覆盖回归验证既有正文、摘要、图文lead、query来源标签和导出偏好编辑均获保留；重复合并、身份/query/数量冲突，以及组件、样式、来源预览和悬空符号链接冲突都在写入前拒绝。新执行的独立审计36项全部通过，另核验45个ZIP成员和50个去重对象、双图绑定及离线JSON重建。隐私签名未发现实际私人路径、凭据或具体私人链接；这不是对所有类型私人信息的绝对证明。独立审计范围与结果见 `independent-audit/`，不把其静态通过称为视觉通过。

完整本地HTML为 **13,825,087字节**，SHA256为 `0cdc4b54271bc29fbdd3762de2b527c61ae74d6e72e46333dd4746086e5f813a`。新的无dist、缓存或node_modules目录经同一官方流程和测试重建，得到逐字相同的HTML，见 `portal-reproducibility.json`。

## 继续保留的限制

浏览器桌面/窄屏、深浅主题、来源面板、导航/历史/滚动、编辑持久化、下载点击、打印、真实断网和浏览器日志均未验。既有本地HTTP连接拒绝、file协议拒绝及原站权限限制继续保留；本轮未重试、换路、重新托管、修改安全设置或访问受限原站。

旧Fourth图文共享S2标题缺第19页，第二图注释及定义包含正确页码。本轮不更改旧内容，也不改写已发送单篇。历史视觉与附件替换等待办不关闭。

63篇归档的四项审计文件写入未获可核验成功，与其中一项字节相同的JSON也未上传。完整本地文件及哈希仍保留，本轮没有重试、改名重复上传或换接口。见 `baseline-known-gaps.json` 与原 `reports/supplier-alias-portal-source/archive-status.json`。本轮新增小源码不代表这些历史缺件已补齐。

本轮未上传、发送或归档完整门户HTML/ZIP，未发布站点或改权限。原站仍只能引用最后验收的v19，20研究/40全文/2样板、AI9，当前可读性未复核；46项待同步。本地64篇完成不能称为线上更新。单篇附件状态另见 `reports/camera-reuse-source/delivery-status.json`，请求接受不代表送达、打开或下载。
