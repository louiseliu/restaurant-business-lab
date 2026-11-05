# AI会员营销：完整图文与第53篇本地门户增量

正文固定在frozen.json所列首次提交24d9ca5b470ba665628923ed01bf2a5ca4e28235，首次UTC为2026-11-05T15:20:09Z。正文SHA256 c5f6833e81a428ec09a7f7a4b197ce2c6bdfff8409110672cb1c2ab2f284debc。保留五节论证、研究说明与完整原文，不把首次入库时间冒充案例实施时间。

图一分别比较普通CRM生日规则、智能生日营销和意向客户托管，保留2026年3月企助与商城双版本条件，不把托管选券或短信问答套给智能生日。图二为作者提出的保留、有限试用及扩大采购路径，强调授权信息、可控制优惠与触达、整组合格顾客和增量总成本。两图均为原创研究示意，不采用供应商收益数字，不构造报价、净利润或回本。六源均来自同一厂商，不是六项独立效果证据。

## 复建步骤

1. 取得固定提交的note.md，运行 `python make_article.py NOTE_MD frozen.json`，校验冻结正文并生成完整叙事、六来源预览及两项reviewed queries。
2. 用官方prepare-data-app.mjs创建单篇report工程，以article-reviewed-data.json作为snapshot。保存新工程准备后的文件指纹为standalone-prepared-sha256.json；运行prepare_standalone.py，保留官方稳定身份和受保护运行时。
3. 复制完整52篇已归档门户为隔离基线及工作副本，保存基线指纹为baseline-sha256.json；原完整HTML应匹配dbd7daf6abca3227f3560c6280a18584ebadf49a845026228f2d056b1ac1c689。运行 `python integrate53.py PORTAL/src SOURCE`，基线须为52篇、72全文、AI34、107queries。仅追加一篇、两项query和必要渲染分支。身份、数量或query冲突在写入前拒绝；旧文章、图文和用户编辑不覆盖。
4. 运行仓库既有公共脱敏补丁及其测试，生成全部载荷后、构建前执行sanitize_site_content.py及--check。设buildStatus为complete，再走官方data-app.mjs prepare、build --separate-data、export-offline。导出路径在工程.data-app-offline/exports下；交付副本只移除可选本地thread元数据。
5. 运行test_preservation.py（制作目录、基线、冻结正文三个参数）、test_merge_guard.py（源码及基线）、test_reader_routes.mjs（门户report目录）。完整HTML、dist、下载包均不归档到GitHub；只有最小公开源码和回执进入仓库。

## 已执行检查

官方构建、完整离线导出、五节与研究说明逐字保留、六源绑定及query一致性、构建manifest、递归隐私检查通过。单篇两个图均使用独立query，行字段为可读中文。门户结果为53篇研究、73份全文、2样板、AI35、109queries。旧72份全文、52篇图文、107queries和306个非必要变更文件保持；单篇241项非内容官方文件保持。5下载载荷与2ZIP内容校验和隐私检查通过，不代表浏览器点击下载验收。

合并保护测试覆盖保留已有正文、摘要、图文、query用户编辑，重复合并及ID/query/数量冲突无写入拒绝；路由解析、URL往返、顺序与AI筛选函数测试通过。

桌面视觉、浏览器交互、手机、打印及真实断网未验。不能用静态检查替代视觉或交互验收，历史视觉待办不因此关闭。保留检查仅针对可读归档52篇基线，不证明更早缺失或未归档编辑已恢复。附件保存与发送由后续真实回执确认，本说明不预先声称已交付。

原公开站仅引用最后核验v19的20/40/2、AI9；未访问受限原站、发布或改变权限。第21—53篇33项新增，加视觉收银与菜品图两项同ID修订，共35项待同步；其他历史待办保持。不是新的全站离线公开版本，也不是自动同步。
