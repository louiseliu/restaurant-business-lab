# AI更新预测，店长昨天的修改该留下吗：小型作者源码

本目录保留逐字冻结正文和来源台账、两幅原创定性图、生成器、作者阅读界面及静态核查。首次正文提交和时间见 frozen.json。note.md 与 sources.md 的早期研究状态不作事后改写；图文制作、附件发送及归档状态另记交付记录。

图1区分锁定、覆盖与重新施加，对照新信息和人工判断。图2独立检查修改理由有效性、信息是否已进入新基线，并将已承诺执行计划分开。两图均为定性分析，版本机制、未知、事件和促销覆盖边界就近说明，不声称实测事故、经营效果或完整软件工作流。

## 兼容官方工具复建

需要 Python 3、Node 和兼容官方 Data analytics 插件；完整运行时不随作者增量源归档，不安装替代渲染器。

1. 将本目录作者文件复制到生产目录的 source/。运行 `python source/make_article.py source/note.md source/frozen.json`，原稿和来源哈希须与 frozen.json 一致。也可从固定Git提交读取 research/2026-11-05-forecast-reimport/note.md 和同目录 sources.md 后核验。
2. 在已安装官方插件根目录调用 `node scripts/prepare-data-app.mjs --surface report --output PROJECT --snapshot PRODUCTION/source/article-reviewed-data.json`。PROJECT 必须是新目录；阅读生成工程的 AGENTS.md 及返回的组件文档。记录全部准备后文件的相对路径与SHA256，保存为 PRODUCTION/standalone-prepared-sha256.json，再运行 `python source/prepare_standalone.py PROJECT`。复建时用自己的新基线，不覆盖历史检查指纹；准备器为新报告创建新的稳定身份。
3. 调用 `python source/support/test_sanitization.py`，再以 `source/support/sanitize_site_content.py PROJECT/src/content/report` 和同命令追加 `--check` 核查公开内容。完成内容后将 PROJECT/src/data.json 中 buildStatus 设置为 complete。调用官方 `data-app.mjs prepare --project-dir PROJECT` 及 `data-app.mjs build --project-dir PROJECT --separate-data`，保留受保护运行时。构建环境不要注入本地线程身份。
4. 调用官方 `data-app.mjs export-offline --project-dir PROJECT --output PROJECT/.data-app-offline/exports/forecast-reimport.html`，将生成文件复制到 PRODUCTION/forecast-reimport.html。使用兼容官方工具提供的导出路径；不得伪造输出或覆盖保护检查。若导出携带本地线程标签，最终交付副本须去除该身份标签并重新做隐私和字节核查，不改受保护运行时。
5. PROJECT 对应 PRODUCTION/standalone，运行 `python source/test_standalone.py PRODUCTION source/note.md`；运行 `python source/test_authoring_guard.py PROJECT` 在一次性副本验证防覆盖。新构建的随机报告身份和官方运行时可能使HTML hash不同，不能以本文历史HTML hash代替新结果验证。

## 已执行检查和限制

build-qa.json：官方构建、正文完整性、来源作用域、隐私扫描、编译内嵌数据和构建清单字节验证；241个官方文件未改动。authoring-guard-qa.json：8项一致与变更场景均保护现有文件。generator-reproducibility.json：干净临时目录重新生成三个JSON，与交付作者输入逐字一致。

visual-qa-status.json 明确记录未做浏览器视觉、窄屏、暗色和交互验收。静态通过不等于渲染验收。未上站、整合门户、上传或远端写入，未重试受限来源。交付状态另记，不以入库代替发送成功。

不归档大型HTML、PDF、ZIP、缓存、机器专用运行脚本或完整运行时。manifest.json记录本目录其他文件的字节和哈希，供小型源码归档核验。
