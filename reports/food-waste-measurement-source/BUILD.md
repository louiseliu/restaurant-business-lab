# 剩食来源识别：第38篇完整图文

正文首次提交 d6655ef13a9924efa4c6ee6998ed733c06078bd9，首次入库2026-11-03T04:03:57Z。food-waste-measurement三份JSON包含完整冻结正文、两幅原创机制图及对应reviewed queries。正文SHA256：f308fc35fbe0eb64c59a86e1119aa70a3a9e55e4d38b1c7dba31e588e6602a7b。

图一拆分备料、餐台未取用和顾客餐后三种来源，以及不同的优先核查；图二比较人工基线与AI辅助，合流到可追溯记录和人工核查。规划中的LLM建议独立标注，不接入既有流程，不提供虚构识别率、减废率或利润数字。四个论证章节保留全部段落，文末可展开完整冻结原文和三条原始来源。

## 独立文章重建

复用研究院 reports/batch-2026-10-30/shared/prepare_article.py；第一个参数为本包 food-waste-measurement 目录，第二个参数必须为独立官方Data项目的 src 目录，不能传项目根。再将本包 ReportContent.jsx、IllustratedArticle.jsx、WasteDiagrams.jsx、illustrated.css、timeline.css、waste-diagrams.css 复制到 src/content/report。官方Data工作流 prepare、build --separate-data、export-offline；导出到项目 .data-app-offline/exports 内，再对交付副本用既有 sanitize_export.py 去除可选本地线程meta。不得编辑受保护运行时。

## 待同步门户集成

只合并本篇三JSON到现有articles、stories和queries，并按首次入库时间排序。门户原IllustratedArticle只新增WasteDiagram导入，以及Diagram中命中diagram.layout以waste-开头时的独立分支；复制附加组件和CSS。不要用本包独立ReportContent覆盖门户，不覆盖旧图解组件。需同时保留#30修订的三个图、全部旧文章、Legacy与样板、原文与下载载荷。完整门户恢复及验收见 [timeline/BUILD.md](timeline/BUILD.md)，恢复清单、测试与门户版组件位于该子目录，专用图组件与本包共用。

## 本轮验收

最终HTML 2,919,466字节，SHA256：534bc3d47bfb44ec2888547f7de504b850d40e2bb4e3e13112d1a581bf6b2571。test_article.py 解码最终编译JSON，断言仅本篇、全文逐字相同、首次Git和时间、两图两query、四节论证、三来源及私人定位脱敏。不是旧22篇门户导出，也没有用摘要替代全文。

许可浏览器本轮实际检查了桌面首页、两幅完整机制图、目录跳转、完整原文展开与图解来源面板，均可用。手机窄屏未完成实测：当前浏览器未提供视口尺寸设置，快捷键未改变CSS视口，未冒充真机验证。响应式断点有静态检查，但不能替代手机验收。

## 可复用的官方静态预览流程

当作者项目的dev依赖不可用，不能为预览修改受保护项目。完成官方separate-data构建后，把完整dist复制到一个独立临时静态预览目录，并配置该目录的 .openai/hosting.json 为 {"static":{"directory":"dist"}}。不复制package.json，不新增Site身份。使用 sites-preview stop 后，以 sites-preview start <静态预览目录> 启动官方预览；仅打开命令返回的准确地址，按许可CUA检查实际渲染，结束后 sites-preview stop。若预览失败，读取start错误及status，遇网络或权限限制停止，不换浏览器路线绕过。

本次仅本地预览成功，不代表原公开站点访问限制解除。未发布站点、未修改权限。大型HTML GitHub归档未完成且未发起；小作者源码保留在本包。完整独立附件的发送请求于2026-11-03T04:10:12.484570Z被接受，不代表已打开或下载；私人附件定位与回执不纳入公开仓库。
