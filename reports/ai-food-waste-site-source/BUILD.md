# 首篇AI机制研究：站点增量源

原文固定提交：327353e38ea3b8981bd2ea8937e9d1aaa0ad28e2。首次Git入库时间2026-10-29T06:10:06Z；不是来源发布时间或现场实验日期。

这是现有私有站点的作者源增量，不含完整保护runtime、站点身份、用户presentation、凭证或样板大载荷。

1. 在保留现有文章、图文、两样板和用户编辑的既有项目执行 `python apply_article.py <project>/src/content/report`。如同ID已有不同内容会停止，不能强盖。
2. 对比并合并ReportContent.jsx的同步说明、IllustratedArticle.jsx的动态主题页眉；不要覆盖用户另行修改。
3. 将生成/校验脚本和article_topics.json置于原timeline-tools目录。AI主题为显式元数据，不通过‘自动化’等关键词猜测。
4. `python sync_illustrated_queries.py <project>/src`，再执行覆盖校验、官方Data编译。原文可展开，来源固定版本，两图明确机制示意与证据边界。
5. 桌面/窄屏验证最新倒序、AI筛选、新文两图和完整原文；旧8篇图文、28全文、两个实战样板与原蜜雪读本不得丢失。
6. 沿原Site标准发布，重读/保留实际线上snapshot、presentation和私有权限，不新建站点。部署回读及浏览器验收后再声称完成。

本增量不包含新的全站HTML，也不假称旧归档HTML已更新。没有新增Pro咨询、真实门店试验或私人经营数据。60%指FY25相对FY17生产食物浪费克/客餐的公司披露变化，不是AI独立贡献；现有有限保证不能直接外推为该AI效果的审计结论。

## 本篇独立HTML
`report.html` 是本篇独立自包含离线图文（两图、完整原文、来源），需要JavaScript、无外部CDN，不含站点身份。不是新全站快照。

复建时在**独立的官方Data导出项目副本**执行 `python prepare_standalone.py <export-project>/src`，再用官方Data build/export-offline。它将StandaloneArticle.jsx作为导出入口，并绑定本篇article-entry、story与公开generic ID快照。不要在正式站authoring执行此单篇准备脚本，否则会把入口改成单篇。不会携带旧私人会话或样板载荷。
