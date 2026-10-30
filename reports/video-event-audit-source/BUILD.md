# 视频与POS事件核查：独立图文源码

正文首次入库：`9ba2df51078bbd601df171b7025dbbd851529f96`，`2026-10-30T18:06:06Z`。本篇独立HTML已生成，正文与两个原创机制图均保留；不是全站快照，也尚未加入公开站时间线。本目录只含小型源码，不含HTML、运行时、私人元数据或发布凭据。

`video-event-audit/`中的entry保留完整正文与固定来源；story区分案例披露和研究建议；reviewed-data为两图提供独立来源绑定。第二图是连接可靠性×人工承接能力的四格建议，不是门店观测数据。未复制人员截图，不把告警当违规事实。

复用已归档的`reports/batch-2026-10-30/shared/`模板。另建独立官方Data report工程，勿指向线上或完整站作者源：

```sh
python test_article.py
python "$REPO_ROOT/reports/batch-2026-10-30/shared/prepare_article.py" video-event-audit "$EXPORT_PROJECT/src"
```

按官方Data流程执行separate-data构建及export-offline，再使用shared/sanitize_export.py去掉导出副本可选本地线程meta。可传最终HTML路径给test_article.py追加安全检查；完整原文展开、两图及来源须实际可读。

独立HTML需要JavaScript；不调用外部模型，未上传门店数据，不声称新Pro、现场试用或经营收益。HTML仅通过Library交付，本轮不创建大HTML GitHub blob。公开站仍保留原v15；此前视觉收银同步和费用证据归档各自待办不因此关闭。后续合站须另行核对最新实际基线、用户编辑及公开安全检查，不从本目录自动发布。
