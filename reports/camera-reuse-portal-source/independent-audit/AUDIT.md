# 第64篇门户独立静态审计

新执行36项检查全部通过。全文84、图文64、研究64、样板2、AI42、queries131。旧83全文与顺序、63图文、129查询对象逐项不变；仅4项预期整合文件改变，旧UI、legacy与样板代码逐字不变。两样板5下载逐一核验摘要，递归检查45个ZIP文件成员，共扫描50个去重对象。

双图分别绑定独立query，行数据与冻结输入相同；原文首提交与时间、来源元数据、组件/预览/样式均核对。split构建manifest的HTML与snapshot字节数及SHA256匹配；离线HTML全部JSON分片重建后等于完整src/data.json。离线HTML含新增标题和两图布局。

隐私签名扫描未发现实际凭据、私人工作路径或具体私人下载链接。首次扫描命中官方运行时通用codex线程链接模板，逐字检查后确认无线程ID；最终测试仅将实际含ID的链接列为命中。扫描不能证明不存在所有类型私人信息。

未进行浏览器、视觉渲染、交互、HTTP/file预览、原站访问、上传或远端写入。既有视觉未验及HTTP/file限制不被本静态结果解除。历史四份审计/日志及同字节JSON未改写或用作本轮成功证据。

## 复跑

从本目录运行：python independent_audit.py --baseline BASELINE63 --production PRODUCTION_DIR --frozen-source CAMERA_REUSE_SOURCE --output NEW_AUDIT_OUTPUT_DIR

支持 --baseline、--production、--frozen-source、--output；参数均为本地目录。新审计不执行受审代码，不接触浏览器或网络。JSON结果列出每项判断与下载递归记录。
