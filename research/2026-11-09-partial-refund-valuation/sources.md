# 来源与核验边界

核验日期：2026-11-09；以下访问状态仅代表本轮实测。正文为产品机制研究，非因果利润估计。

1. Grab 官方署名实施文章，2026-08-14： https://www.grab.com/inside-grab/stories/how-we-taught-llms-to-solve-the-missing-muffins-mystery/
   - 正文可读。作者为 Grab Support 产品与工程负责人。支持先人工验证部分缺失入口，再用 LLM 分类、匹配菜单单价、无精确项时寻找类似品、关键部分缺失全额和食安/质量转人工的公开机制。
   - 已上线多数市场是平台自报，完整国家名单未列。公开“约20%”缺少样本/观察期；“每月少约32,000人工工单”无单店成本/独立对照。正文不采用这两项数字，不能推出公平准确率或商家净收益。
   - 折扣、赠品、税费、多项漏送、估值公式、人工改判和实施成本未公开。
2. Grab 新加坡商家教育： https://merchant.grab.com/en-sg/guides/all/getting-orders-right-and-managing-refunds
   - 正文可读，发布日期未确认。支持平台代处理履约退款可能从商家结算扣除、Finance查看。另节 GrabPay 90天期限未用于本文，不能混作 GrabFood售后期限。
3. Grab 新加坡商家直接处理说明： https://merchant.grab.com/en-sg/blog/resolve-order-issues-directly-with-your-consumers
   - 正文可读，发布日期未确认。支持商家联系、补送/退款及三小时后转客服；补送费用、门店实际资格未知。不把该路径与第一项模型自动处理拼成已核实的端到端统一部署。1—3同机构，不算独立成效证据。
4. 美团外卖平台商家责任场景赔付管理规范： https://rules-center.meituan.com/m/detail/guize/334001?activeRule=1
   - 正文可读；页首及第八条均标2026-05-06修订，首发2025-11-14。第二条限卖家责任明确场景，保留特别规则；第四条第九项包含协商套餐部分退款；第七条区分退款和额外赔付扣款；备注保留依法赔付边界。
   - 未将第五条自配送少送1—5元赔付写成通用退款上限。未登录后台验证个店适用情况，非法律意见。

# 查重

实际读取 README.md、state/current.md、AGENTS.md、项目 SKILL、编辑规范及来源发现方法。2026-11-09本轮实际目录列出102个研究目录，不以过时README的65篇为当前计数，也不自动把全部目录当正式文章计数。

实读：
- research/2026-11-03-order-cancellation/note.md：取消后停制作与配送，非套餐部分漏送估值。
- research/2026-11-05-platform-appeals/note.md：识假、履约举证与申诉，非部分履约退款估值。
- research/2026-11-01-inventory-capture/note.md 与 model-update-acceptance：排除已写星巴克停盘点工具的重复选题。

本篇独立经营问题是“部分漏餐时应先购买自动估值还是先整理套餐及处理依据”，不是把已有申诉篇拆分凑数。

# 执行状态

未新增 Pro 请求，未验证本轮实际 Pro 模型。未操作真实订单、客户数据、权限、购买或外部联络。研究子线程命令工具两次返回无可用执行环境；正文和来源通过连接器准备。图文由主线程继续制作验收，未完成前不称正式交付。GitHub大HTML归档未执行；原站未同步；不触发或绕过历史确认。
