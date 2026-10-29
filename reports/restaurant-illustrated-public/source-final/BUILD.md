# 餐饮研究院：全量图文阅读站维护

## 内容与口径
- 固定公开仓库 `louiseliu/restaurant-business-lab` 的受审快照；不是实时 GitHub 同步。
- 当前 8 篇研究图文读本、28 份 Markdown 全文；原蜜雪老板版另作历史精选阅读形式，不重复计算为研究。
- 按首次 Git 入库时间倒序，不把历史文章的核验更新伪装成新发布。页面展示北京时间。
- 商业模式与 AI 在餐饮是两条主题线；无已验证 AI 专文时显示空状态。AI 标签须人工确认。
- 公开安全导出隐藏私人协作会话地址；不改变公开仓库旧历史，原文中的相应链接以“私人协作会话，未公开”代替。

## 每次更新流程
1. 获取公开仓库完整 Git 历史，确认目标提交；运行 `python generate_index.py --repo <checkout> --output <authored>/articles.json`。仅更新本地索引，不联网发布。
2. 人工复核新文分类；正式研究须在 `illustrated-stories.json` 以稳定文章 ID 增加读本。至少提供：lead、findings、diagram、secondDiagram 或 numericChart、sections、meaning、unknowns、actions、公开来源。
3. 两幅图必须解释不同信息：机制/流程与数据/证据边界。不能为了图形虚构数据、把假设当事实，或给未知量补数。numericChart rows 保留精度；display 可四舍五入，note 必须说明样本、单位、期间和条件。
4. 运行 `python validate_illustrated.py <authored>`，检查全部正式研究图文覆盖、全文链接、倒序和图表数值。
5. 在既有 Data 项目保留保护 runtime、站点配置和用户编辑，仅更新 authored 内容与经核验的数据。运行 `python sync_illustrated_queries.py <project>/src` 绑定图解到 reviewed queries；官方 Data build 和 export-offline 编译。
6. 实际浏览器检查桌面和窄屏：8 篇/新增篇至少两图、关键标签、来源、完整原文折叠与返回列表；不能用静态编译通过冒充视觉验收。
7. 同一已授权站点走标准 Data publication 流程更新，保留访问权限；检查部署与完整资产回读。此源码包不包含发布配置、账号、凭证，也不会自动部署。
8. 公共归档前运行 `python sanitize_public.py <authoring-project> <new-safe-output>`。把安全 authored 内容及 reviewed-data.json 放入一个独立导出副本，经官方编译导出安全 HTML；再扫描私人链接/内部标识。不要把私有站编译件直接提交公开仓库。

## 文件与依赖
- `ReportContent.jsx`：首页/时间线/分类和阅读路由。
- `IllustratedArticle.jsx` + `illustrated.css`：8 篇图文的统一可访问组件；`illustrated-stories.json`：逐篇人工审定叙事和图形配置。
- `articles.json`：原文全文、稳定 ID、固定提交来源及首次入库时间。
- `LegacyReport.jsx` + `report.css`：原老板报告；`timeline.css`：导航与列表。
- `reviewed-data.json`：公开安全快照；渲染图表与来源查看所用数据。
- HTML 是自包含离线导出，无外部 CDN，**需要 JavaScript**。公开 JSX 是作者源码，不含受保护 Data runtime，不能单独 `npm install` 后构建。需要兼容的官方 Data app runtime（此版本 API 1），通过官方脚手架/编译器构建；或直接打开 HTML 阅读。

后续研究仍需先完成真实证据核验，再更新图文；本流程不声称实时自动同步，不新增定时任务。
