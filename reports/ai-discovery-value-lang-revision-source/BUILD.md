# 中文文章语言标记修订（未发送）

已发送请求接受的原版本保持不动，SHA256与时间见 `revision.json`。本目录只记录一次无障碍改动：给作者文章节点增加 `lang="zh-CN"`，不修改官方HTML、运行时、正文、图文、两项query、来源、首次入库时间或稳定报告ID。

`shared/IllustratedArticle.jsx` 是修订后作者reader，`article-language.patch` 是精确差异。以原单篇小源码为基准应用这一差异，再运行原官方构建脚本。若reader已有其他修改，应审查合并，不能直接用整份reader覆盖用户更改。后续门户只按它的现有reader采纳这个属性，不应将单篇reader直接覆盖门户。

本次已重新运行官方prepare、separate-data build、export-offline、完整单篇静态检查和8项防覆盖检查。同一报告身份重复构建得到相同HTML；正文、图文、数据及metadata逐字保持，只有作者文章语言属性改变。官方240受保护文件检查及241准备基线文件保持仍适用。

新HTML只留本地，未发送、未替换原附件、未发布或并入门户。浏览器、屏幕阅读器、视觉与交互未验，既有HTTP/file/原站访问限制未重试或绕过。这是静态语义修正，不声称屏幕阅读器实测成功。
