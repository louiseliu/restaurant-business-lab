# 餐饮老板 HTML 报告：可公开作者源

HTML 成品为官方 Data app runtime 的自包含离线导出。无需外部 CDN；需要现代浏览器及 JavaScript。GitHub 文件页可能显示源代码，下载后用浏览器打开。报告不是纯静态无 JS 页面。

## 文件
- ReportContent.jsx：中文报告、图解、ChartRenderer 封装 EvidenceChart、来源和折叠方法附录。
- report.css：作者内容样式，响应式与打印规则。
- reviewed-data.json：已复核的公开资料输入和计算值；无账号凭证或原始私人会话。

## 重建
需要已安装 Data Analytics 插件的官方 `prepare-data-app.mjs` / `data-app.mjs`，不是单凭这三个源文件即可运行。
1. `node <plugin>/scripts/prepare-data-app.mjs --surface report --output <new-project> --snapshot <reviewed-data.json>`
2. 阅读新项目 AGENTS.md，将 JSX/CSS 放到 `src/content/report/`。保留 preparer 创建的公共组件与 `ReportDisclosure.jsx`。
3. `node <plugin>/scripts/data-app.mjs build --project-dir <project> --separate-data`
4. `node <plugin>/scripts/data-app.mjs export-offline --project-dir <project> --output <project>/.data-app-offline/exports/restaurant-owner-report.html`

本次 runtime SHA256：b1771584910da746d0cf1b967a4889fee226053d841596104b457a04a2dd3d91

本文件没有提供 Site 发布配置、账号 ID、部署令牌或私人对话原文。研究来源与固定提交在报告中可查。
