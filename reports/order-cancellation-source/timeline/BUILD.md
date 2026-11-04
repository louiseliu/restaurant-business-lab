# 第41篇本地完整门户增量

先按reports/service-handoff-source/timeline/BUILD.md恢复完整40/60/2、AI25基线。51份固定JSON逐Git blob校验，恢复后的安全HTML SHA256应为478cd100712d1d717ce72d9961226b70eb74142e3bd2d0f23ae3ae450e6d95d8，本轮实际完全一致。保留基线及用户改动，另建独立作者副本。

运行integrate41.py COMPLETE_PROJECT/src reports/order-cancellation-source。只合并本篇三JSON、增加两query和取消图组件，门户reader仅增加组件import与cancellation布局分支。保留原门户ReportContent、既有标题修复、key、第三图、全文、样板、下载、路由及主题筛选，不用单篇reader替换门户。

使用官方helper build --separate-data和export-offline，输出到项目.data-app-offline/exports，再复制为WORK_PACKAGE/timeline41.html并运行sanitize_export.py。WORK_PACKAGE/source放verified-source-manifest.json，WORK_PACKAGE/recovered保持51份原始JSON路径；运行test_preservation.py WORK_PACKAGE BASELINE40_PROJECT/src COMPLETE_PROJECT/src及test_reader_routes.mjs COMPLETE_PROJECT/src/content/report。

本轮实际41研究/61全文/2样板、AI25。旧60全文、40图文、83queries、9共享与252其他源文件保留；5下载和2ZIP完整，72文本载荷隐私检查通过。完整离线HTML 12900507字节，SHA256 71f488ff4529b36fa90a448151ea8056c82194a16aaf255130324be266ec88f8。浏览器验收另记，不以静态测试替代。

仅本地待同步源；没有访问、发布或改变受限原站权限，没有大型HTML GitHub归档。上线前仍须核对原站用户编辑和许可状态。


## 完成本轮交付与验收

单篇HTML附件发送请求已被接受。完整门户桌面验收通过，手机未测；此结果不代表原站已同步。正式研究41篇、AI25，原站22项待同步。详细验收范围另附visual-qa.json。
