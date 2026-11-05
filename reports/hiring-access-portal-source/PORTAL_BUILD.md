# 第59篇招聘入口：完整门户本地增量复建

固定正文提交：fc02d8ca4db8a14ab86572d1d936fcdd6eaa8cb8。文章首次入库时间2026-11-05T21:05:54Z，不作为来源发布日期。正文与sources.md的SHA256见同级hiring-access-source/frozen.json。

## 输入与复建

本目录仅包含门户增量脚本、测试与QA。正文、图文组件、reviewed queries及frozen.json复用同级hiring-access-source，不重复单篇作者源。不含门户HTML、ZIP、dist、完整运行时或私人元数据。完整复建需要可读的58篇门户源、固定公开note.md及同目录sources.md、兼容官方Data工具和仓库reports/public-site-sanitization工具。保留用户工作副本，不覆盖它。

1. 从公开仓库取回reports/hiring-access-portal-source和reports/hiring-access-source。在新的PRODUCTION_DIR下分别放为portal-archive-source、archive-source。门户复建不依赖单篇standalone工程。
2. 运行python portal-archive-source/prepare_portal.py PRODUCTION_DIR EXISTING_PORTAL58。它核对baseline58-sha256.json的328项指纹，拒绝基线差异及已存在目标，再创建baseline58与portal59。若输入存在新用户编辑，先保存并重新审查，不得强行覆盖。
3. 运行python portal-archive-source/build_portal.py PRODUCTION_DIR NOTE_MD NODE DATA_APP_MJS SANITIZATION_DIR。后三项分别为官方Node、官方data-app.mjs及公开脱敏工具目录。脚本无网络、上传、提交或发布调用。
4. 流程先运行合并守卫，再新增1篇、2项query和3个本篇图文文件。只在作者reader新增本篇分支，不改受保护运行时、门户身份、主题或用户偏好。原标题、正文、故事、来源、图表行、旧queries及旧文件都逐项核验。
5. 脱敏检查后设置buildStatus=complete，运行官方prepare、build --separate-data及export-offline。构建子进程不带可选会话环境变量；保留官方manifest，核验实际HTML与sidecar的大小、SHA256。离线HTML输出timeline59-hiring-access.html。
6. test_portal_preservation.py核验冻结全文/台账、完整旧数据与文件、编译JSON、两项样板、五个下载、递归ZIP的CRC与内部manifest及公开载荷脱敏。test_reader_routes.mjs执行实际路由辅助函数、URL往返、计数/排序，不声称浏览器交互已验。test_portal_merge_guard.py验证用户正文、摘要、故事、query及导出偏好保留；重复与身份、query、文件、符号链接冲突均零写入拒绝。

## 本轮结果与范围

本地门户59研究/79全文/2样板、AI38、121项queries。原78份全文、58篇图文、119项queries和324项无需变更的基线文件保持不变。全文HTML为13,598,336字节，SHA256为95770ea71d5776cf622546449f33eed8d1494ed21dff6ece93821cda86dbe4e0。

官方构建、离线导出、静态完整性、路由辅助函数、149项文本载荷、5项下载、2个递归ZIP容器及1份内部release-manifest检查通过。脱敏工具未改动任何已有内容。图解采用定性流程及采购取舍，未对真实候选人评分、排序或作录用决定。

完整门户视觉、窄屏、深浅主题、点击导航/历史/滚动、编辑持久化、下载点击、打印、实际断网与浏览器错误日志未验。最近单篇HTTP预览返回ERR_CONNECTION_REFUSED，历史file协议访问被拒绝；本轮没有重试、换路或重新托管绕过。没有发布、上传或重发原站，也未重新判断原站当前可读性。

仅保证本次可读58篇本地基线完整保留，不等于恢复不可读历史或未归档用户编辑。大HTML入库、门户附件发送、站点同步和其他历史附件待办独立保留。

最终小源码已在不含单篇工程、缓存或旧dist的干净目录完成prepare→build→export复建，HTML逐字及SHA256一致，见portal-reproducibility.json。独立审计结果见portal-independent-qa.json。
