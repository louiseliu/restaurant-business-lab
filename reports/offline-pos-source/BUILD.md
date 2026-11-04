# 离线收银与复网核对：第44篇完整图文作者源

正文首次提交 b0f0dd59974e4b507be9dbe38bd5d0e00012c4ab，首次入库2026-11-04T23:00:25Z（北京时间2026年11月5日07:00:25）。来源复核日期为2026年11月4日。冻结正文SHA256：f1c6c12ffa391db1083f41316731ddda937f64e344cac9d9f9ac1470a06d9c2e。

四节完整论证逐段保留，研究说明在完整原文保留。两幅原创React/CSS图：第一幅依据CakeDock说明区分现场收款交付、后台接受和后厨收到，核验建议清楚标注为作者设计；第二幅说明有限营业、异常交接与逐笔对账，不把银豹和CakeDock拼接为共同部署。银豹旧安卓切换网络、PC失败转人工边界保留。没有新增产品实测、收益数字、AI或Pro主张。

## 复建

1. 使用官方Data preparer建立独立report项目，以article-reviewed-data.json为snapshot，并读取项目AGENTS.md及prepare返回的当前组件文档。新项目使用preparer分配的新身份，修订同一成品保留原身份。
2. 将本目录JSX/CSS复制到src/content/report。article-entry.json包装为articles数组写articles.json；illustrated-story.json按文章ID映射写illustrated-stories.json。保留官方src/data.json及其新项目ID。
3. 使用官方helper build --separate-data，再export-offline，输出在项目.data-app-offline/exports内。交付副本移除可选data-app-local-thread元数据，不改受保护运行时。
4. python test_article.py 安全HTML路径。检查冻结正文、四节论证、两图、两来源、首次时间、单篇范围及隐私。静态通过不代替视觉验收。

完整门户另见timeline/BUILD.md。独立reader不能覆盖完整门户reader。

## 交付与安全边界

本包不含大型HTML。独立HTML、门户HTML、浏览器验收、附件发送和原站发布是不同状态，分别按实际回执记录。本次官方构建和静态QA通过；浏览器QA尚待独立记录。未访问此前403的站点、发布、改权限或上传大型HTML；不替换视觉旧附件、不重试费用原归档，旧全站快照保留。

## 后续实际验收与交付

独立HTML附件发送请求已接受，不代表用户已打开或下载。独立核验已检查正文、隐私与桌面阅读。门户44/64/2、AI27和旧内容静态保留核验通过；浏览器transport随后断开，44↔43相邻点击未完成，手机未测。不得把本轮记录写成完整门户交互验收通过。原站未访问、发布或改权限。
