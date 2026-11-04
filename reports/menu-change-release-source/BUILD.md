# AI 菜单更新：独立图文作者源

研究ID：research-2026-11-04-menu-change-release-note。首次研究提交2099f57b263929a283a34c63871923441a824836，首次时间2026-11-04T21:08:17Z，冻结正文SHA256 fe7cf3baeca717e24bf87239c0911b63dbfbd30f6010d8f7c7f7751a7d09a6c0。核验日期与首次Git时间分别保留。

单篇基于官方Data运行时构建。两幅原创React/CSS机制图分别比较各处完成依据及两类配置任务的工作构成；文档机制与研究建议分开，不代表经实测的AI自动部署链。四节正文逐段保留，另附完整冻结原文及三条同供应商来源。无虚构耗时、收益、准确率、门店结果或Pro咨询。

## 复建

在独立官方Data作者项目src/content/report放本包六个JSX/CSS文件。article-entry.json包装为articles数组写articles.json，illustrated-story.json按文章ID映射写illustrated-stories.json，article-reviewed-data.json写src/data.json。勿将独立reader覆盖完整门户。

先运行官方helper prepare，按返回的组件文档核查。再运行build --separate-data，并将export-offline输出写至项目.data-app-offline/exports内的绝对路径。交付副本按既有sanitize_export.py清除可选本地线程meta。不改受保护运行时、不改用替代渲染器、不安装依赖。

运行python test_article.py HTML路径，检查最终HTML解码结果、仅含目标文章、完整原文、两图两query三来源、首次时间、段落完整性与隐私。qa.json为实际静态结果，浏览器验收须单独记录，不以构建代替视觉验证。

## 范围

本包只生成独立文章，不改41篇门户基线。门户整合未执行；原站未访问、发布或改权限。大型HTML没有GitHub归档。历史附件、费用原归档与旧整站快照不变。附件是否发送由发送回执确定，不由本包推断。

## 交付补记

独立图文已通过独立桌面验收，手机未测。附件发送请求已接受，不代表已打开或下载。门户整合仍待完成，不把独立验收当作整站验收。

## 完整门户整合补记

随后已恢复历史41篇基线并完成第42篇本地增量构建与静态验收，详见timeline/BUILD.md。此前未整合的记录保留为阶段状态；浏览器验收与原站发布各自独立判断。
