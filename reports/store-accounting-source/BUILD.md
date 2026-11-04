# 小店自建AI经营账：完整独立图文作者源

第43篇，ID为research-2026-11-04-store-accounting-note。首次研究提交69d95a50b4675b000df8b1e6cff146fdb6371e0e，首次入库2026-11-04T21:59:53Z（北京时间2026年11月5日05:59:53）。来源核验日期为11月4日，两者分别保留。冻结正文SHA256为0e27875924c5467065e3d3c655937d51391aa1f4bae8321dfa080bf8c0b13202。

完整五节正文逐段保留，另含完整原文、两条同源链来源和两幅原创React/CSS机制图。第一图是假设两平台套餐分化后的映射核查，不是麦小农事故；第二图是持续维护的四类责任及继续/暂停条件，不是实测工时分布。没有新增成效、费用、准确率或Pro主张。

## 官方复建

用官方Data preparer建立独立report项目，以article-reviewed-data.json为reviewed snapshot。阅读其AGENTS.md及prepare返回的当前组件文档。将本包JSX/CSS放入src/content/report；article-entry.json包为articles数组写articles.json；illustrated-story.json按文章ID映射写illustrated-stories.json。新建项目身份由官方preparer分配；同一成品修订保留其身份。

执行官方helper build --separate-data，再执行export-offline，输出必须位于项目.data-app-offline/exports。将交付副本中的可选data-app-local-thread meta移除；不改受保护运行时、不替换渲染器、不安装依赖。执行python test_article.py HTML路径核验单篇范围、逐段正文、首次时间、图示query、来源及安全。

当前安全HTML为2,923,549字节，SHA256 cf3da98d215a15816e5e3515921aae781e1693f00426fec9d8dc8e7547401d77，静态结果见qa.json。浏览器验收另记；静态验收不证明视觉与交互通过。

## 交付边界

本包是小型可复建作者源，不含大型HTML。附件发送、浏览器验收及原站发布分别以实际回执为准。本轮不重试受限原站、不发布或改权限，不替换历史全站快照、视觉旧附件或重试费用归档。

完整本地门户已独立整合，详见timeline/BUILD.md；独立reader不可覆盖门户reader。

## 本轮实际交付补记

独立文章桌面视觉与交互验收通过，手机未测。独立HTML附件发送请求已接受，不代表用户已打开或下载。门户桌面QA仍在进行，本次小源码归档不提前将其标为通过；本地构建不等于原站发布。

## 门户桌面验收补记

后续独立桌面QA已通过43/63/2计数、AI27筛选、新篇两图及两个来源、全文展开、43↔42相邻导航、旧内容保留和隐私检查。手机未测。详见timeline/visual-qa.json。此前“QA进行中”是本轮早先阶段记录，不代表当前未验收；原站仍未发布。
