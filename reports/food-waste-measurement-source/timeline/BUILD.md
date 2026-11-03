# 第38篇全量时间线复建与待同步包

本包只准备本地作者内容，没有发布站点或上传大型 HTML。目标为38篇正式图文、58份全文、2个样板、AI23，按首次入库时间倒序。线上仍是最后核验的v19，不可把本地数量称作已上站。

## 复建

以既有第22篇 knowledge-withdrawal 完整官方 Data 作者项目为基线，先保留原件。按 recovery-manifest.json 从固定提交 50b14bf22de124141f5ebf50eb1fd776f8b6ef9a 获取45个小JSON，保存到工作包 recovered/ 下，路径保持仓库相对路径。逐个验证 Git blob SHA：SHA1(“blob ” + UTF8字节数 + NUL + 原始字节)，必须完全一致；不得去除或添加换行后假称原件。

第38篇三个JSON使用本包上级的 `../food-waste-measurement/`，与单篇图文共用，不重复归档。专用组件 `WasteDiagrams.jsx` 与 `waste-diagrams.css` 同样从上级目录读取；本目录的 `IllustratedArticle.jsx` 是保留完整门户路由的版本，不与上级单篇版本混用。把这三个JSON准备为独立目录。在工作包根放 recovery-manifest.json 与 article_topics.json，并建立 source 子目录用于保存测试回执。保留本包及其上级的相对布局。运行：

python reports/food-waste-measurement-source/timeline/restore_timeline.py WORK_PACKAGE COMPLETE_PROJECT/src reports/food-waste-measurement-source/food-waste-measurement

脚本拒绝重复套用组件补丁；不重新生成旧全文，不改受保护运行时。恢复的是23—37，其中第30篇使用 inventory-capture-revision-source 最新同ID修订，不用早期 inventory-capture-source 覆盖。首次入库2026-11-01T13:03:33Z不变，完整正文SHA256为361ddd7a23696f9c32735d44e39051c225ebb8da80ab6085438d911cbb7166b2。第38篇首次提交d6655ef13a9924efa4c6ee6998ed733c06078bd9，首次入库2026-11-03T04:03:57Z。

组件只增添第30篇第三图分支、第38篇两种专用机制图布局与修订原文链接；保留门户路由、上一篇下一篇、返回、全文、Legacy读本、嵌入样板、下载数据及原UI。不要用单篇 ReportContent 替换门户。45个恢复JSON已经原样归档于既有仓库，本包不重复提交它们。

按官方 Data helper prepare 后 build --separate-data，再 export-offline 到项目 .data-app-offline/exports。完整 HTML 仅本地保留；交付副本用既有 sanitize_export.py 移除可选本地线程meta，不修改运行时。大HTML GitHub归档未完成，未尝试上传。

node reports/food-waste-measurement-source/timeline/test_reader_routes.mjs COMPLETE_PROJECT/src/content/report
python reports/food-waste-measurement-source/timeline/test_preservation.py WORK_PACKAGE BASELINE_PROJECT/src COMPLETE_PROJECT/src

## 验证与限制

qa.json记录本次实际结果：38/58/2、AI23、路由和倒序通过；旧42份原文、22篇图文逐对象相同，9个共享文件逐字节相同，旧查询保留；所有实际渲染的机制图有对应reviewed rows，包含第30篇第三图。递归检查66项文本载荷和2个ZIP容器，核验嵌入HTML及下载文件哈希；未发现私人会话链接、本地路径、线程meta或内部通话标识。官方编译和完整离线导出通过，成品SHA256见qa.json。

完整门户本轮未做实际浏览器验收，静态通过不替代视觉、手机布局或点击验证。公开发布前仍需核对远端用户改动，取得可达的匿名验收环境，继续使用原站与原权限，不新建站点。该包不包含私人项目地址、凭据或运行时。
