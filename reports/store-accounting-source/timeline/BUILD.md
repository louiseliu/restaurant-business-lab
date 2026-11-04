# 第43篇完整门户增量

以reports/menu-change-release-source/timeline/BUILD.md恢复的已验收42篇门户为基线。当前main的第42篇article-entry、illustrated-story、article-reviewed-data三个文件Git blob SHA与本地原始文件一致；既有安全HTML SHA256为5da4fa6178dfbc360ef592ee5c2825ec965c57a6b4d6451a1f1b7acf60f4cd05。先复制独立作者项目，保留原基线。

运行python integrate43.py COMPLETE_PROJECT/src reports/store-accounting-source。仅合并三个JSON，新增两个query与AccountingDiagrams专用组件；门户reader只增加一个import及一个accounting布局分支，不覆盖共享阅读器。保留旧42图文、62全文、87queries、9共享文件和256其他源文件。

运行官方helper prepare、build --separate-data及export-offline；离线输出放项目.data-app-offline/exports。交付副本仅清除可选data-app-local-thread meta。工作包根放安全timeline43.html，执行python test_preservation.py WORK_PACKAGE BASELINE42_PROJECT/src COMPLETE_PROJECT/src，以及node test_reader_routes.mjs COMPLETE_PROJECT/src/content/report。

实际43研究/63全文/2样板、AI27。最终HTML解码目录和图文与源JSON逐对象一致，正文、倒序、路由、图示来源作用域均通过；第30篇第三图与同ID修订保留。5项下载和2个ZIP完整，递归扫描76项文本载荷。安全HTML为12,957,419字节，SHA256 04743bccf3fc8fc18da3cda4f2282ec4387a010b93dadb35628574c8fd596f92。详见qa.json。

这是本地静态验收，不代表门户浏览器验收、原站发布或受限访问恢复。浏览器实际检查须另记；本轮未重试受限原站、发布或修改权限。大型HTML未向GitHub上传，旧独立附件与全站离线快照不变。

## 实际桌面验收

独立桌面QA已通过43/63/2、AI27筛选、新篇两图及两个来源、完整原文展开与43↔42导航，旧内容及隐私检查通过，详见visual-qa.json。手机未测；这只完成本地门户验收，不代表原站403解除或已经发布。
