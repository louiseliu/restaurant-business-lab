# HTML 源码与构建说明

成品 `case-demo.html` 已包含运行所需 JS/CSS 和全部模拟展示数据；读取成品不需要安装依赖、CDN、模型服务或 Python。交互用于浏览预计算结果，不是站内计算/模型系统。

可编辑作者文件保留在 `html-source/ReportContent.jsx` 与 `html-source/report.css`；`reviewed-snapshot.json` 保存已计算模拟结果和来源。它们是标准 Data report 内容，不替换或篡改公共运行时。**公开包不包含完整 app runtime、node_modules、宿主配置、私人路径或登录资料。**

需要重新构建 HTML 时，先完成分析和文稿复核，使用已安装且兼容的 Data 插件（本次 1.1.0-exp-baseline，API v1）及 Node。`DATA_PLUGIN_ROOT` 指向使用者本机安装位置；不要将个人路径写入发布文件。依次：

```sh
python src/prepare_snapshot.py
node "$DATA_PLUGIN_ROOT/scripts/prepare-data-app.mjs" --surface report --output "$PWD/app" --snapshot "$PWD/reviewed-snapshot.json"
# 首次创建后阅读 app/AGENTS.md；不要覆盖已有 app，已有项目应在原项目更新。
cp html-source/ReportContent.jsx app/src/content/report/ReportContent.jsx
cp html-source/report.css app/src/content/report/report.css
# 完成作者内容后，将 app/src/data.json 的 buildStatus 设为 complete。
node "$DATA_PLUGIN_ROOT/scripts/data-app.mjs" build --project-dir "$PWD/app" --separate-data
node "$DATA_PLUGIN_ROOT/scripts/data-app.mjs" export-offline --project-dir "$PWD/app" --output "$PWD/app/.data-app-offline/exports/case-demo.html"
cp app/.data-app-offline/exports/case-demo.html case-demo.html
```

构建使用插件已有离线打包运行时，无 CDN。不要编辑受保护运行时或跳过边界检查。没有该插件也可以运行全部 Python 分析和测试、阅读现成 HTML；不宣称只靠 Python 就能重新编译 JSX。

复算数据不代表旧文稿自动正确：更新结果后需重写/复核 `docs/weekly_report.md`、冻结断言、图表和叙述。无新授权不得发布或写入真实业务系统。
