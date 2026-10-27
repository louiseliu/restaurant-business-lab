# 餐饮商业模式研究院

以可验证证据推进餐饮商业问题研究，持续维护研究成果、商业分析方法、研究记录与 `restaurant-business-model-lab` Skill。

## 当前状态

初始化日期：2026-10-27。

- 已接收并检查上传的 Skill v0.3：仅含四个 Markdown 文件，无可执行脚本、二进制或依赖。
- 仓库级 Skill 位于 [`.agents/skills/restaurant-business-model-lab/`](.agents/skills/restaurant-business-model-lab/SKILL.md)。这是版本化的项目配置，不等同于宿主全局注册或已启动后台进程。
- 首次实际研究已由通用口径边界推进到[蜜雪商品收入与加盟网络店日的条件性检验](research/2026-10-27-franchise-evidence/final-report.md)：构造指标至少下降约 4.55%，不能推断终端需求或加盟商利润下降。
- 两轮真实 Pro 回复、公开原始资料回查、独立计算和措辞纠错已完成，详见[协作记录](research/2026-10-27-franchise-evidence/pro-collaboration.md)与[判断修订](research/2026-10-27-franchise-evidence/judgment-revision.md)。最终成果发布仍以实际远端提交核验为准。
- GitHub 内容写入已恢复，[首轮公开证据包提交](https://github.com/louiseliu/restaurant-business-lab/commit/204eb60c727f7d9fa1ebdd35e96f47b44c35aa0a)已核实；本版本在其上补充实际 Pro 往返及新的边界检验。
- 已配置自 2026-10-28 起每日早间研究检查（Asia/Shanghai），尚未完成首次定时运行验证。按证据价值和可用额度选择 Pro，不是 24 小时后台进程。没有新增付费资源。

## 工作原则

1. 先提出值得解决的商业问题，再按证据选择调查、计算、Pro 协作和验证动作，不机械套用固定流程。
2. 事实、计算、假设和建议分开记录；公开原始资料优先，重复转载不算独立证据。
3. 总部收入、利润、终端交易额与加盟商单店收益分别分析，不能相互替代。
4. Pro 是共同思考伙伴，其回答不是事实证明。核验来源和计算，并保留分歧与判断修订。
5. 外部操作只在明确授权范围内进行；本公开仓库不得存放凭据、私有经营资料或个人敏感信息。

## 目录

- [给餐饮老板的图文 HTML 报告](reports/README.md)：下载后浏览器打开，含图解、经营问题与证据边界。

- [Skill 与参考文件](.agents/skills/restaurant-business-model-lab/SKILL.md)
- [研究规范](methods/research-standard.md)
- [当前进度](state/current.md)
- [研究日志](logs/2026-10-27-initialization.md)
- [本轮研究结论](research/2026-10-27-franchise-evidence/final-report.md)：条件性边界结果、反例、经营意义与未解问题。
- [原始初查稿](research/2026-10-27-franchise-evidence/provisional-research.md)：历史初始判断，保留其写作时状态；不要将其中尚未咨询的描述当作当前状态。
- [独立边界复核](research/2026-10-27-franchise-evidence/bounds-check-findings.md)、[来源补充](research/2026-10-27-franchise-evidence/source-additions.json)、[可运行代码](research/2026-10-27-franchise-evidence/bounds-check.py)。

## 首次闭环验收

必须能够提供：真实研究问题与来源、实际执行的验证、真实 GPT Pro 模型及会话使用证据、因核验而保留或修订的判断，以及已在远端核实的 GitHub 提交。任一环节未完成都应明确标注，不以计划或模拟代替成功。

## 使用 Skill

将仓库的 `.agents/skills/restaurant-business-model-lab/` 作为项目级 Skill 交给支持相应目录约定的宿主；应以宿主实际发现结果为准。本文件不承诺跨宿主自动加载。需要全局安装时，使用宿主支持的安装方式，并另外核验发现结果。

