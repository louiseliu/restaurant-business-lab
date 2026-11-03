# 第39篇完整门户整合与验收

本包在完整第38篇基线上加入顾客自有AI入口研究。结果为本地39篇研究、59份全文、2个样板、AI24；不是上线回执，不新增大型HTML或附件。

## 恢复与整合

先按 reports/food-waste-measurement-source/timeline/BUILD.md 从完整第22篇官方Data作者项目恢复38/58/2基线，包含第30篇同ID修订、第三图与固定修订链接。保留此38篇项目不变，另复制为待更新作者项目。三个JSON与专用组件均使用本包上级已有文件，不复制单篇ReportContent或整份单篇IllustratedArticle覆盖门户。

在工作包中放置 source/ 下的本包测试和清单，并将 verified-source-manifest.json 中的51份JSON以原始字节放在 recovered/ 下，保留仓库相对路径。前45份来自固定提交50b14bf22de124141f5ebf50eb1fd776f8b6ef9a，最后六份来自d6ac21a3f1fd3e10a9eb76eafc16075d331f87f1。脚本计算Git blob SHA，不能调整换行后当作原件。

执行：

python reports/customer-agent-entry-source/timeline/integrate39.py COMPLETE_PROJECT/src reports/customer-agent-entry-source

脚本只合并本篇三JSON、新增专用组件导入与agent-entry分支，沿用首次提交90a3b9b65e399b3df0169092f1685adb857658f9及首次入库2026-11-03T07:05:31Z。排序按首次入库倒序。正文SHA256为4096e9ea61b55452e68d4d79a07201324ac4ce83963c05f8f4531b39c5d66c91。

本轮桌面发现39→38→浏览器后退时标题可能残留前一篇，虽然URL和正文已恢复。作者article节点增加key={item.id}后重新构建并实际复验后退/前进、列表返回及筛选恢复，标题与正文一致；未改受保护运行时。第39篇标题按语义逗号断行，避免桌面末字独占一行，其他文章标题不变。

使用官方Data helper prepare、build --separate-data、export-offline，离线导出只放项目.data-app-offline/exports，再将副本置于工作包timeline39.html并运行既有sanitize_export.py移除可选本地线程meta。完整HTML仅本地留存，不上传GitHub。

node reports/customer-agent-entry-source/timeline/test_reader_routes.mjs COMPLETE_PROJECT/src/content/report
python reports/customer-agent-entry-source/timeline/test_preservation.py WORK_PACKAGE BASELINE38_PROJECT/src COMPLETE_PROJECT/src

## 实际验收

qa.json记录最终静态结果：51份JSON的Git blob一致；38篇旧图文、58份旧全文、全部旧queries逐对象不变；9个共享文件及其他所有源文件逐字不变。最终HTML解码的59份完整正文与39篇图文逐对象匹配。第30篇第三图、原UI、Legacy、2个样板和5项下载载荷保留。递归隐私检查68项文本载荷及2个ZIP容器，包括嵌入HTML和下载内容哈希。

原38篇基线重新执行恢复、官方构建与原测试通过；从该基线重新运行本包脚本，254个src文件与最终作者项目逐字一致。最终安全HTML为12,851,583字节，SHA256为3a4f18848b1170792c936c10ab0890b71cd595ebf2a506189b7edc9791e88035。

许可官方静态预览中实际检查39/59/2首页、AI24筛选和重置、新篇标题及两图、目录跳到完整原文并展开、图解来源面板关闭、相邻38篇、浏览器前进后退与返回筛选列表。visual-qa.json记录范围。未开展手机、打印、全39篇逐篇浏览或下载点击实测，既有第30/34—37篇视觉待办不关闭。预览结束后已停止。

原公开站最后核验仍v19 20/40/2、AI9；本轮未复测受限站点、未发布、未改权限。20项上站待同步仍保留。第39篇原独立附件不重复发送，视觉旧附件替换、费用原归档待办和旧全站快照均不变。未新增Pro、业务调用或门店实验。
