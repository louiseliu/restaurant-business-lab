## 同篇电话研究的编辑升级

电话篇后续修订固定 `e6f524b36e3efd43e7c7d43ee43439852030412c`，修订时间 `2026-10-30T04:23:39Z`，原首次入库时间不变。正文与图文均以服务瓶颈、碎片工时、任务价值、人工接手和增量贡献连贯展开，不是第 14 篇。

若项目已含旧版电话篇，不用 append 脚本强覆盖：

```sh
python shared/update_article.py voice-receptionist "$REPORT_DIR"
python shared/sync_illustrated_queries.py "$PROJECT_DIR/src"
```

更新脚本校验旧 entry/story 的完整 canonical hash 和正文 hash；若用户修改过会停止，不移除保护继续覆盖。已是同一新版则无改动。新项目从零应用当前全部条目，仍可用 `apply_batch.py`。随后仍须脱敏、官方 build、QA。原稿时间与本次修订时间分别保留。
