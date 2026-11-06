# 后厨旧摄像头利旧单篇图文复建

本目录仅含小型作者源码和检查记录，不含大HTML、ZIP、官方运行时或任何私人环境路径。固定正文首提为 `eaf8d57c523197ca67a04662f5d48dc45a201c22`，真实首次时间 `2026-11-06T01:10:58Z`。原文与来源的SHA256见 `frozen.json`，不得用生成时间覆盖首次入库时间。

## 输入与内容

`note.md`和`sources.md`逐字保留冻结材料；来源台账中“待提交/待制作”等是冻结阶段快照，不代表后续构建状态；展开标题已明确标记“首次研究台账，历史状态保留”。正文6节，两幅作者原创定性图，分别说明资产核验链与条件投入分支。历史学校视频项目数据不制成AI失败率，不外推小店故障概率。湖北制度路径不等于任意摄像头兼容保证。

## 官方构建

需要 Python 3、Node，以及当前已安装的 Data analytics 插件。按插件本身的安装定位获取根目录，不在仓库保存个人绝对路径。下面的变量由操作者设置到其获准环境。

1. `python make_article.py note.md frozen.json`。生成器先验证冻结与两个文件哈希，然后生成正文入口、图文叙事和两项受检数据。
2. `node "$DATA_PLUGIN_ROOT/scripts/prepare-data-app.mjs" --surface report --output "$PROJECT" --snapshot "$PWD/article-reviewed-data.json"`。仅为新项目运行，保留准备器赋予的稳定报告ID。记录准备目录哈希，再阅读生成的AGENTS与当前组件参考。
3. `python prepare_standalone.py "$PROJECT"`。只安装作者内容与数据，不修改受保护运行时。已有正文、图、query、读本或样式与输入不一致时会停止，禁止覆盖用户改动。
4. 运行 `python support/test_sanitization.py`，然后用 `support/sanitize_site_content.py` 对作者内容目录执行检查。正文和两图确认完成时，将src/data.json的buildStatus设为complete。
5. 通过官方 `data-app.mjs prepare --project-dir "$PROJECT"` 解析当前组件参考，再 `data-app.mjs build --project-dir "$PROJECT" --separate-data`。不用源码模式或替代运行时。
6. 用官方 `data-app.mjs export-offline --project-dir "$PROJECT" --output "$PROJECT/.data-app-offline/exports/camera-reuse.html"` 生成自包含交付文件。构建前清除本任务临时路由环境变量，交付件检查不包含私有路径或会话标识。大HTML/ZIP不属于本作者源码归档。

本次官方运行时SHA256：`b1771584910da746d0cf1b967a4889fee226053d841596104b457a04a2dd3d91`。同一准备目录第二次生成和构建的HTML逐字一致；全新准备器会分配新报告ID，不能据本记录宣称新身份构建的字节也相同。

## 已做与未做

通过：冻结正文及来源一致、6节叙事完整、两图各自query和指标定义一致、来源作用域、编译内嵌数据一致、官方manifest文件字节/哈希、241项官方文件未改、14项文本载荷脱敏、8项防覆盖测试、相同身份重复构建字节一致。

未做：浏览器视觉、窄屏、深色、交互、打印、浏览器真实断网验收。未尝试受限预览，也未切换协议或重新托管绕过限制。静态通过不等于视觉验收。未上传大HTML/ZIP、未发布或同步原站、未并入完整门户。后续交付及远端归档状态应独立记录。


## 小源码归档与交付记录

本归档保留两个独立审校范围：`independent-qa.json`是完整独立静态审计，包含远端原稿核验、官方重复构建、八项防覆盖与三项脱敏测试；`independent-scoped-qa.json`保留较窄的最终标题/条件修订复核，不把两份记录的范围混同。独立审计所记边界CSS强调样式未命中属于可选样式问题，未改写已发送HTML，也不声称实看了浏览器渲染。

归档前重跑静态完整性、防覆盖、脱敏单元测试，三份生成器JSON在临时目录逐字复算，并完成语法、清单与私有标识检查，见`archive-qa.json`。单篇附件请求于 **2026-11-06T01:16:27Z** 被接受，不代表送达、打开或下载；交付件为2,938,211字节，SHA256 `00f519c429b409cad0b843c11f5a76d96a9a488929eb4704ca853dfd713a22ee`。详见`delivery-status.json`。

本篇完整门户增量尚未完成，原站未同步；浏览器视觉/交互、HTML归档与历史待办均保留。完整门户最近记录仍63/83/2、AI41、129项queries，其历史审计缺件不因本次单篇归档而关闭。
