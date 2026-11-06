# 67篇门户独立静态审计

原审计在完整本地生产目录执行，仅向新audit目录写脚本和JSON。实际运行1,476项断言，未发现新增阻断问题。报告绑定HTML SHA256 `a33e32b064a67577873677001382f747e0e7d1b9b1e0b7745b73a1cb312521e0`，完整范围与未验项见portal67-static-audit.json。

## 复跑布局

本目录内的原审计脚本保持受审时原字节。脚本按当时生产布局解析输入；如需复跑，应将audit_portal67.py复制到 `PRODUCTION_DIR/audit/`，并保留：

- `PRODUCTION_DIR/baseline65`、`PRODUCTION_DIR/portal67`、`PRODUCTION_DIR/baseline65-sha256.json`、`PRODUCTION_DIR/portal-archive-source/input-fingerprints.json`。
- `PRODUCTION_DIR/timeline67-digitalhuman-recipe.html`。
- 与PRODUCTION_DIR同级的 `ai-discovery-portal-production/portal65`、`digitalhuman-production/source` 和 `ai-recipe-production/source`，分别为原始65篇基线及两份冻结输入。

执行 `python PRODUCTION_DIR/audit/audit_portal67.py`。不要直接在本归档目录运行后将缺失完整基线误称产物失败；本增量源码不是完整历史镜像。脚本只写新audit结果，不改正文、源码、产物，不启动浏览器、服务器、网络、编译或发布。

该审计不重做外部原始来源研究或内嵌业务计算，也不核远端Git权限/交付。浏览器渲染、交互及真正离线操作均未验。数字人语言继承、旧Fourth来源标题缺页码及历史五项不确定归档保持限制，不是本轮关闭项。
