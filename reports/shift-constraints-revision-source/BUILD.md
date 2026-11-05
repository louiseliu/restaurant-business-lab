# 排班研究同ID修订：完整图文与44篇门户

研究正文固定提交 `2b466f57a0176f05386b4e0915443e2a28d3b2e8`，小型图文源固定提交 `91dc53aa9fc10a34468e607b3efad0849799ef03`，正文SHA256为 `7042c61fbb7377d3a37a84b0375cb6d19b814f3440b291c3b7c88506e15c0b89`。沿用文章 `research-2026-11-01-shift-constraints-note`、首次提交 `daa2e94fd3780500f5d3a7e3291e1a3c1df86743` 与首次入库 `2026-11-01T14:03:18Z`；修订时间为 `2026-11-05T03:09:32Z`，不新增文章或AI计数。

正文与两图增加任务工时和临时调班的验收问题。图1区分任务遗漏、新信息、重复问题和需求冲突；图2保留固定表与建议表的条件取舍。金豬食堂仍为主案例。界面新闻员工采访仅支持自述线索，瑞幸20-F仅支持公司披露排班机制；不互证同一版本、不判定普遍缺陷或违法、不计算人效或收益。

## 作者基线与恢复边界

既有44篇完整作者目录在本轮执行环境中缺失。本次从现存22篇官方Data作者项目和固定GitHub提交 `378db871b914bf2f6cb1e29c814e15c3c03d85cd` 的公开小源重建44篇。`recovery-sha-receipts.json`记录112份输入的固定版本、Git blob SHA与字节校验；`recovery-qa.json`记录恢复检查。恢复依次采用 food-waste-measurement-source/timeline 的38篇恢复、customer-agent-entry、service-handoff、order-cancellation、menu-change-release、store-accounting、offline-pos 的39—44增量，最后使用 food-images-revision-source 的有界修订。

原22篇工程逐字未改；当前可读的既有编辑、归档增量、菜品图修订、盘点第三图、reader标题与key修复、UI、Legacy和下载均保留。**这是依据归档证据重建，不声称与缺失原44篇工程逐字相同，也不能证明未归档编辑已经找回。** 未读取受限原站或旧附件，不以恢复工作改变访问范围。

独立文章使用既有官方Data作者壳与归档shared/prepare_article.py恢复原篇，采用原 `article-reviewed-data.json` 中的 `report:shift-constraints-20261101` 身份。完整门户保留原门户身份。两者都只在隔离工作副本应用同ID修订；不把单篇reader覆盖到完整门户。

## 复建与安全合并

1. 保留完整44篇恢复基线和单篇恢复基线。取排班修订前的三JSON作为PREVIOUS_ARTICLE_SOURCE，取修订后的三JSON作为NEW_ARTICLE_SOURCE。文件来自 `reports/shift-constraints-source/shift-constraints/`；旧源以 `378db871b914bf2f6cb1e29c814e15c3c03d85cd` 为准。按小源修订回执确认新版本，不追随未核验的可变内容。
2. 分别复制两套基线到工作根目录下的 `portal44` 与 `standalone`。可保存 `baseline-sha256.json`，顶层键为这两个模式，内层为各基线相对路径和SHA256；测试用它确认基线本身未变。
3. 执行 `python apply_revision.py PROJECT NEW_ARTICLE_SOURCE PREVIOUS_ARTICLE_SOURCE`。该程序在任何写入前核对旧entry、story和两项query的固定canonical hash，拒绝用户意外改动；再次执行应幂等。仅替换同ID文章、图文、两项query与构建/更新时间字段，保留原始首发、全部其他内容和artifact身份。
4. 执行 `python test_merge_guard.py NEW_ARTICLE_SOURCE PREVIOUS_ARTICLE_SOURCE`，覆盖正文、元数据、图文和query改动的无写入拒绝场景。旧query不能因正文保护通过而被无条件覆盖。对完整门户执行 `python patch_reader_label.py PORTAL_REPORT_DIR`，仅对本篇把来源文案中的“首次固定版本”改为“固定版本”；所有其他篇的文案、链接和reader字节保持。补丁检查唯一旧文案并支持幂等，无法识别的改动会停止。单篇文案原本准确，无需补丁。
5. 使用仓库 `reports/public-site-sanitization` 的测试与内容检查。调用当前安装官方Data helper的 `prepare --project-dir` 解析文档，再 `build --project-dir ... --separate-data`；不修改受保护运行时、安装替代依赖或更换渲染器。
6. 官方 `export-offline` 导出到各项目 `.data-app-offline/exports/`。将完成的单文件复制到工作根目录，分别命名 `shift-constraints-revised.html` 与 `timeline44-shift-revised.html`，使用归档shared/sanitize_export.py仅移除可选本地线程meta。split HTML单独不是完整离线交付。
7. 执行 `python test_preservation.py WORK_ROOT BASE_PORTAL BASE_STANDALONE NEW_ARTICLE_SOURCE NOTE_MD` 与 `node test_reader_routes.mjs PORTAL_REPORT_DIR`。测试只比较本轮可验证的恢复基线，不把缺失原件冒称为已经逐字核对。

## 本轮实际静态验收

- 官方prepare、separate-data构建及完整离线导出成功，runtime与所有受保护文件保持。
- 门户仍为44篇研究、64份全文、2样板、AI27、91项queries。除排班同ID外的63全文、43图文、89queries和260个其他src文件保持恢复基线原样。reader仅增加本篇来源文案的条件分支，测试逐字验证没有其他修改。
- 单篇保留原artifact及文章身份，只包含1篇、2项query；两幅图的reviewed rows、作用域与图文节点完全一致。
- 编译后的全部全文与图文对象等于作者JSON，冻结正文hash和固定来源一致；倒序、AI筛选数量及路由往返通过。
- 5项下载、2个ZIP和递归隐私检查通过。门户扫描78项、单篇64项文本载荷。guard幂等及四类编辑拒绝均通过。
- 具体成品字节数和SHA256见 `build-qa.json`。浏览器视觉与交互由独立验收另记，静态成功不冒充浏览器验收。

## 发布与交付边界

本目录只包含可复建小源、测试与回执，没有大型HTML。两份完整HTML已本地制作，不代表已替换或交付任何旧附件。未发布、未访问受限原站、未修改权限。原站状态仍只引用最后验收v19的20/40/2、AI9；本地44/64/2不等于线上状态。排班第31篇本已在待同步新增范围内，本次修订并入原篇，不新增同步项；菜品图、视觉、费用原归档及旧附件各自的状态保持，不能因本地重建而关闭。

旧排班附件读取因当前访问范围返回403，未更新、未替换，未另建附件或改变权限绕过。桌面独立验收已检查单篇、完整门户和净化单篇离线文件的重点阅读与交互；具体范围与来源文案修后复测见 `independent-qa.json`。手机视口及真机未测，不声称全站逐篇、所有下载、打印或断网打开均通过。
