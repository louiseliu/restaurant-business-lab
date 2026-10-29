# 餐饮研究阅读门户：UI/UX 作者源增量

本包只更新既有站点的阅读界面；没有研究事实、数据快照或私有配置。保留9篇图文研究、29份原文、两个独立实战样板与原蜜雪读本。旧独立HTML和全站HTML是其各自导出时的快照，本包不会追溯改写它们。

## 文件与应用
将本包5个作者组件/样式文件与现有项目 `src/content/report/` 对比后合并：ReportContent.jsx、IllustratedArticle.jsx、Samples.jsx、timeline.css、illustrated.css。保留现有 articles.json、illustrated-stories.json、samples.json、LegacyReport.jsx，以及reviewed data和用户presentation。不要覆盖用户后续编辑。

需要既有兼容Data app API 1项目；不包含受保护runtime，不可独立npm构建。通过官方Data build验证和编译；同一站点的标准发布负责源码身份、数据快照和访问控制。本包不含发布凭证、不自动发布、不创建新站点。

## 阅读行为
- 首页优先最新研究；研究、实战样板、全部资料三频道。历史读本保留轻量入口，不占据研究首屏。
- 列表URL使用 `#?view=all&topic=ai&q=关键词&section=research`（默认值可省略）；搜索覆盖标题、实际展示摘要与全文，trim后不区分大小写。
- 旧 `#read/<id>` 深链接继续有效。界面把自己的列表位置与路由记录在浏览器history state的restaurantReader命名空间，保留其他history state字段；不写云端、不使用账号收藏。
- 返回列表恢复筛选、搜索和位置；浏览器Back/Forward恢复对应页面。直接打开新深链接没有先前列表状态时返回默认列表。列表筛选可从URL刷新恢复。
- 文章目录使用本组件唯一ID的受控滚动，不写目录hash，避免破坏文章路由；原文目录项会展开原文。上一篇/下一篇按原首次入库时间排序，不按更新日重排。
- 样板继续沙盒allow-scripts；未添加same-origin或任何模型/数据上传权限。

## 校验
`node test_reader_routes.mjs <project>/src/content/report` 验证解析、URL roundtrip、9/29/2及AI分类/倒序；既有图文覆盖与样板hash校验继续执行。

发布前还需实际浏览器验证：搜索/主题→文章→返回位置；原生Back/Forward；目录与原文展开；邻篇边界；样板返回与下载。手机窄窗、原生放大和键盘焦点属于独立视觉/交互验收，不能以编译或源码测试冒充真机测试。
