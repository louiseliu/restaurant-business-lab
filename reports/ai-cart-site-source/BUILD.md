# AI加购机制研究：v7阅读门户的可复建增量

原文固定提交：5c14b9b034b8ecab34fbae4c38523126b0c4cb6c。首次Git入库2026-10-29T22:00:41Z，即北京时间2026-10-30 06:00:41；目录与核验日期2026-10-29不能代替首次入库日期。

## 原站增量
1. 以最新v7门户作者源为基准，保留现有UI/UX、9篇旧图文、29份旧全文、两个实战样板、原蜜雪读本及用户编辑。不要拿早期v6组件覆盖最新界面。
2. 执行 `python apply_article.py <project>/src/content/report`，将本篇article-entry.json和illustrated-story.json增量合并。已有同ID不同内容会停止，不强盖。
3. 合并article_topics.json的显式AI主题，保留其他主题映射；更新相应generate_index、sync_illustrated_queries、覆盖校验及路由测试脚本。
4. 运行 `python sync_illustrated_queries.py <project>/src` 后用官方Data build。结果应为10篇图文/30份全文/2个样板，AI筛选2篇，新文按真实首次时间居首。
5. 实际浏览器验证两图、全文/来源、目录/返回/历史状态和窄屏；比对旧内容未改。既有site/presentation/私有权限不能重置。本包不含身份、凭证、配置或自动发布动作。

## 独立HTML
report.html为本篇自包含离线图文，含两个信息图、完整原文和固定来源，需JavaScript，无外部CDN。不是新全站快照；本轮不重发旧完整站点HTML。

在独立官方Data导出项目副本中运行 `python prepare_standalone.py <export-project>/src`，再标准build/export-offline。StandaloneReader.jsx保留v7阅读排版和受控目录，只移除不适用于单篇文件的邻篇导航。不要将它覆盖到原站；原站继续使用既有IllustratedArticle.jsx。公共快照使用无账号关联的generic报告ID，只含本篇两图的审定数据。

## 内容边界
第一图是实验基线与指标分母对照：ABV+1%、Order Share+8%为作者报告相对变化，后者不是总订单增长。第二图是原创门店验证建议，不是已执行结果，没有模拟利润或回本期。原始资料为2023和2021历史来源，本轮核验不代表2026新实验；未使用Pro。
