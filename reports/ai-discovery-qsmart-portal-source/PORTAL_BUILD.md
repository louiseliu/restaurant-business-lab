# 第65篇AI搜索与Q-Smart同篇补充合批门户

本目录只保存小型增量源码、冻结指纹和本轮静态核验。第65篇正文首次提交为 `40e158a2766f7edd8e3d684b66436dd197624ecb`，首次时间 `2026-11-06T02:15:50Z`。Q-Smart仍为 `research-2026-10-30-qsmart-note`，首次提交 `2d35d3947a51ebafdf8097d393ce49d6db457411`、首次时间 `2026-10-30T07:29:17Z`；修订为 `8770ddeefaa8ace5dd3fe1f9e4f68d7abbc4e760`、`2026-11-06T02:12:43Z`。修订不新增文章、不改变首次时间排序，也不把公开来源日期当入库日期。

## 固定输入和范围

需要完整、可读的64篇本地门户。其小型增量源归档为 `42da422322ff0e6332161fb079fb1090eb50e320`，本轮在较新仓库头 `d7c47b97d6f63175fa7498c464b5e3d5a01aa8d8` 读取最新README和仓库Skill，并逐字核对19项基线归档文件及Git blob哈希。最终归档曾修正审计说明中的公共相对路径，旧本地审计说明与归档字节不同；门户内容和运行时不受影响。346项基线文件指纹及此前64篇保留测试均已核验。本轮只基于这一可读本地版本，不代表恢复原站用户编辑或不可读历史。

输入是 `reports/ai-discovery-value-source` 的已送出单篇作者源和 `reports/qsmart-revision-20261106-source` 的同篇修订源。20项实际输入的字节数和SHA256冻结在 `input-fingerprints.json`，本轮还从 `bd4c6cd60bac9ddbbb165867b0e02f1fca58011b` 逐字回读全部20项并核对Git blob哈希，见 `input-remote-verification.json`。Q-Smart源归档提交为 `66b75aec61c23a1be6ce2b4ea4753eedd4e06a6f`。GEO两版本小源码归档提交为 `bd4c6cd60bac9ddbbb165867b0e02f1fca58011b`；独立语言修订目录为 `reports/ai-discovery-value-lang-revision-source`。GEO语言属性差异另列于 `language-provenance.json`，只为本篇作者article添加中文语言标记，绝不用单篇reader替换门户reader。

GEO已发送版HTML为 `24b43ab696c30b868f8ed7c733a60d129ee12b74443636b9ea2b0f20a0dba6ea`；后续未发送单篇语言修订为 `93daa0501e82a1f39ad0116703230688da0f7be799c1b2e6d91eb55519233bfe`。两版保持分开，本门户不是再次发送或替换附件。本目录不包含完整HTML、ZIP、dist、缓存或运行时镜像，也不是完整历史源码镜像。

## 在新的目录复建

1. 将本目录放为 `PRODUCTION_DIR/portal-archive-source`，准备完整64篇基线 `BASELINE64`、上述GEO和Q-Smart作者源，以及兼容官方Data工具。
2. 执行 `python portal-archive-source/prepare_portal.py PRODUCTION_DIR BASELINE64`。脚本核对346项指纹，拒绝基线变更及已存在目标，不覆盖输入或用户修改。
3. 执行 `python portal-archive-source/build_portal.py PRODUCTION_DIR AI_DISCOVERY_SOURCE QSMART_SOURCE NODE DATA_APP_MJS SANITIZATION_DIR`。`NODE`为官方Node，`DATA_APP_MJS`为官方Data脚本；脱敏检查目录可用Q-Smart作者源中的 `support`。
4. 合并前核对输入文件指纹、篇数、身份、正文/来源哈希、首次与修订时间、原两图及queries、增量query和目标文件冲突。Q-Smart已有编辑时拒绝写入并保留，不用冻结副本覆盖。其他既有正文、摘要、故事、query和导出偏好原样保留。所有预检结束后才写入。
5. 只追加GEO全文/图文/两项query，对Q-Smart原对象附加修订段及一项query。主时间线reader、legacy、受保护运行时、主题、稳定身份、样板和下载不变。作者图文reader增加GEO分支、仅该篇的 `lang`、Q-Smart补充目录/附段/来源及相对来源链接解析；保留所有旧分支、相邻导航和编辑ID。
6. 使用只读脱敏检查，内容完成后设 `buildStatus=complete`，执行官方prepare、`build --separate-data` 和 `export-offline`。构建子进程不携带可选会话标记；离线HTML按字节复制，不改写编译输出。最终为 `PRODUCTION_DIR/timeline65-discovery-qsmart.html`，只留本地。

## 本轮检查

结果为65篇研究、85份全文、65篇图文、2项样板、AI43、134项queries。83份其他全文、63篇其他故事、131项旧queries及342项无需变更的基线文件逐项保持。Q-Smart原正文是修订正文的逐字前缀，原图文所有字段与两幅图、两项query不变，新增内容独立列在revision。主reader及legacy字节不变，原两份内嵌HTML和5项下载不变。

防覆盖回归含17项检查：保留其他用户编辑和导出偏好，拒绝重复合并、身份/query/数量冲突、五项新文件及悬空链接冲突、Q-Smart正文/摘要/故事/query编辑和预期reader锚点变化。另运行 `test_frozen_input_guards.py AI_DISCOVERY_SOURCE QSMART_SOURCE BASELINE64`，逐一改变20项输入，20项均在任何门户写入前拒绝，原输入不变。

主测试检查175项文本载荷、2个递归ZIP和内部release manifest、内嵌样板、5项下载、编译JSON、分离数据与构建manifest，未发现所列私人标识模式。隐私模式扫描不等于所有私人信息类型的绝对证明。路由测试实际运行URL辅助函数、往返、数量、AI分类与首次时间排序；这些不是浏览器测试。

HTML为13,892,324字节，SHA256 `f033d638d659037cb96f0e062784c55c5451622c90a8793ed4c3244b97b97305`。无dist、缓存或node_modules的新目录按相同官方流程复建，逐字结果见 `portal-reproducibility.json`。独立审计另执行1,432项检查，确认134项query绑定及6段离线内嵌reviewed data拼接后与源数据逐字相同，单独检查174项载荷和45个ZIP成员。其扫描计数口径与主测试不同，均未发现新增阻断项；未重编译或重算样板内部业务计算。范围、结果、复跑依赖及未验项目见 `independent-audit/`。

## 未验和保留待办

未进行桌面/窄屏、深浅主题、实际图形、来源面板、导航/历史/滚动、编辑持久化、下载点击、打印、真实断网或浏览器日志验收。此前HTTP连接拒绝、file协议拒绝及原站权限限制没有重试、换路、重新托管或改安全设置。构建通过不等于这些项目通过。

原站未同步、当前可读性未复核；仅可引用最后验收v19的20研究/40全文/2样板、AI9。第21—65篇45项新增、两项旧修订和本次Q-Smart修订共48项待同步。没有上传、发送或Git归档完整门户HTML/ZIP，也没有发布或改权限。

历史四项审计写入未获可核验成功及一项同字节JSON继续保留为缺件，见 `baseline-known-gaps.json`。本轮没有重试、改名同内容上传或换接口。旧Fourth共享S2标题缺第19页的展示问题仍在，第二图注释/定义含正确范围；未改写旧图文或已发送单篇。历史附件与归档待办没有借本次完成关闭。
