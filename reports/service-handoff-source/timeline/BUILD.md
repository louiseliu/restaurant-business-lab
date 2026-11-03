# 第40篇完整门户整合与验收

本包把「店员接手以后，AI客服什么时候才能再开口」加入完整第39篇门户。目标为本地40篇研究、60份全文、2个样板、AI25；不是上线回执，不新增大型HTML或ZIP归档。

## 恢复基线

先按 reports/food-waste-measurement-source/timeline/BUILD.md 从完整第22篇官方Data作者项目恢复38篇，再按 reports/customer-agent-entry-source/timeline/BUILD.md 恢复39篇。保持原22篇及恢复后的39篇基线不变，复制39篇项目为本轮待更新作者项目。

verified-source-manifest.json列出基线恢复的51份JSON。前45份来自固定提交50b14bf22de124141f5ebf50eb1fd776f8b6ef9a，最后六份来自d6ac21a3f1fd3e10a9eb76eafc16075d331f87f1。将它们以原始字节放在WORK_PACKAGE/recovered/下，保留仓库相对路径；不可调整换行后声称原件一致。把本目录的清单、脚本和测试放在WORK_PACKAGE/source/下。

## 整合

本包上级service-handoff/三JSON及HandoffDiagrams.jsx、handoff-diagrams.css是唯一新增输入。integration-inputs.json记录这些作者文件的SHA256，不将本地作者输入误称为已提交Git文件。第40篇首次研究提交98fa4044144f56ec5d6b22bf25ea5bef5e6fee74，首次入库2026-11-03T11:10:36Z，正文SHA256为a0f7b6d072401409a1383388da56058901667426f8d71d8571a3dfd2afdb3332。

python reports/service-handoff-source/timeline/integrate40.py COMPLETE_PROJECT/src reports/service-handoff-source

脚本先验证输入、基线数量、正文及首次入库信息，再合并三JSON，排序按首次入库倒序。门户IllustratedArticle只增加专用组件导入及handoff-布局分支，保留第39篇标题语义断行、key={item.id}、第30篇第三图、目录、全文与相邻阅读。不得用单篇ReportContent或IllustratedArticle覆盖门户，不修改受保护运行时。

运行当前官方Data helper prepare、build --separate-data。若需要执行完整HTML一致性测试，再用export-offline导出至作者项目.data-app-offline/exports/timeline40.html，复制到WORK_PACKAGE/timeline40.html，并运行本包sanitize_export.py移除可选本地线程meta。完整HTML只在本地测试保留，不上传GitHub。

node reports/service-handoff-source/timeline/test_reader_routes.mjs COMPLETE_PROJECT/src/content/report

python reports/service-handoff-source/timeline/test_preservation.py WORK_PACKAGE BASELINE39_PROJECT/src COMPLETE_PROJECT/src

## 验收范围

测试覆盖40/60/2与AI25、首次入库倒序、旧39篇图文和59份全文逐对象不变、旧queries、9个共享文件及其他旧源文件逐字保留、原门户reader仅两处预期增加、两个样板和5项下载载荷、2个ZIP容器内载荷、递归隐私检查、最终HTML解码的全部60份原文和40篇图文逐对象一致。第40篇两张图的reviewed rows及来源作用域须一致。

qa.json记录静态验收结果，visual-qa.json单独记录随后完成的许可官方静态预览。实际通过：桌面40/60/2首页、新篇标题与两图、AI25筛选及重置、目录到完整原文自动展开、40→39相邻阅读、浏览器前进后退的标题/正文一致及返回筛选列表。手机、打印、全40篇逐篇视觉、下载点击及本轮门户来源面板未测；来源面板另在本篇独立图文实际验收。既有第30/34—37篇视觉待办不因此关闭。预览已停止。

最终安全门户HTML为12,876,671字节，SHA256为478cd100712d1d717ce72d9961226b70eb74142e3bd2d0f23ae3ae450e6d95d8。

保留原站、原权限与既有待同步状态。本包不发布，不重试受限原站，不新增站点、Pro调用、业务调用或门店实验。
