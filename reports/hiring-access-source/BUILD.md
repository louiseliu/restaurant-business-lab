# AI招聘入口与行政辅助：单篇图文作者源

本目录为第59篇研究的作者增量源。正文与来源台账按 frozen.json 指定的首次提交及SHA256冻结；两幅原创图解解释招聘工作流和采购取舍，不还原品牌后台，不对真实个人作筛选或录用决定。

图解保留关键边界：海纳只说明人才池内候选人可二面，不能推成所有拒绝均被复核；专项图文与模型适配不等于公平性已获验证。Chipotle预期、自报与供应商宣传分开解释，不合并不同时间口径，不计算小店回本期。

## 本地复建

1. 从 frozen.json 的固定提交取回 research/2026-11-05-hiring-access/note.md 与 sources.md。运行 `python make_article.py NOTE_MD frozen.json`。生成器先核验两文件哈希，保留全部章节与台账，再生成两个定性图解查询。
2. 用兼容官方 Data `prepare-data-app.mjs --surface report` 和 article-reviewed-data.json 准备新工程，记录准备后的文件哈希；运行 `python prepare_standalone.py PROJECT`。仅安装作者内容，保留官方报告身份，不覆盖不一致已有内容或多篇门户。
3. 使用仓库 reports/public-site-sanitization 流程检查，设置 buildStatus 为 complete，再运行官方 `data-app.mjs prepare`、`build --separate-data` 和 `export-offline`。不要将本地线程环境标识注入输出。导出先放在 `.data-app-offline/exports/` 下，再复制为交付件。
4. 检查脚本采用制作目录布局：将本目录内容放在 `PRODUCTION_DIR/source/`，官方工程放在 `PRODUCTION_DIR/standalone/`，准备阶段指纹放在 `PRODUCTION_DIR/standalone-prepared-sha256.json`，独立HTML放在 `PRODUCTION_DIR/ai-hiring.html`。运行 `python test_standalone.py PRODUCTION_DIR NOTE_MD`，核验完整正文与台账、图文段落、图源范围、查询绑定、官方非内容文件、编译内容、构建manifest、隐私和离线静态资产。

完整官方运行时不包含在作者增量源内。复建需要兼容的官方准备、构建与导出工具；新准备工程要重新记录保护文件指纹，不能把运行时版本变化误认成篡改。

本轮仅本地单篇制作：不发布、不改变访问权限、不修改既有门户、不提交HTML或大型blob。HTML、dist、缓存、私人路径与运行身份不进入小型作者源。

## 检查范围

结果以 build-qa.json 和 visual-qa-status.json 为准。成功构建与静态检查不替代浏览器视觉及交互验收；不可把未运行项目写为通过。来源台账的编辑状态按首次提交原样保留，图文制作状态由本目录另记。

## 归档时的交付与独立审校状态

单篇HTML为2,940,902字节，SHA256 `b73bfac8e714f660b8e1bb715d3606a162e00700e7417701a2c2564f92ced7b2`。附件发送请求于2026-11-05 21:09 UTC被接受，时间精度为分钟，不代表用户已收到、打开或下载。见 delivery-status.json。

independent-qa.json记录固定提交原文与来源的独立回读、内容及静态检查；本次归档再运行单篇检查、Python语法解析与新目录正文生成器复算通过。原审校中的相对路径说明问题为记录位置问题，归档的 visual-qa-status.json 与 build-qa.json 同目录，独立审校字段已作包装路径修正，不改变文章或HTML。

浏览器预览连接被拒绝，未渲染文章；视觉与交互仍未验，未换路访问、重新托管或修改安全设置。第59篇尚未纳入完整门户，原公开站未同步。HTML归档待办保留，本目录不包含HTML、ZIP或完整官方运行时。
