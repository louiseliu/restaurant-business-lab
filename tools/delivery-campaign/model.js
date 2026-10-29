/* 外卖活动条件增量模型 v1.0.0 — 无网络、无依赖。HTML 内嵌副本由 build.py 生成。 */
(function (root) {
  'use strict';
  const LIMITS = Object.freeze({ orders: 10000000, contribution: 1000000, fixed: 10000000000 });
  const DEFAULTS = Object.freeze({ N: 1000, alpha: 0.4, cp: 8, cb: 12, F: 2000 });
  function number(value, label) {
    if (value === null || value === undefined || typeof value === 'boolean' || (typeof value === 'string' && value.trim() === '')) throw new Error(label + '不能为空。');
    const n = Number(value);
    if (!Number.isFinite(n)) throw new Error(label + '必须是有限数字。');
    return n;
  }
  function validate(raw) {
    const x = {};
    for (const [key, label] of [['N','活动归因订单数'],['alpha','真实增量比例'],['cp','活动单均贡献'],['cb','原价单均贡献'],['F','固定增量支出']]) x[key] = number(raw[key], label);
    if (!Number.isInteger(x.N) || x.N < 0 || x.N > LIMITS.orders) throw new Error('订单数须为 0–10,000,000 的整数。');
    if (x.alpha < 0 || x.alpha > 1) throw new Error('真实增量比例须在 0%–100% 之间；未知不等于 100%。');
    if (Math.abs(x.cp) > LIMITS.contribution || Math.abs(x.cb) > LIMITS.contribution) throw new Error('单均贡献须在 −1,000,000 至 1,000,000 元之间。');
    if (x.F < 0 || x.F > LIMITS.fixed) throw new Error('固定增量支出须在 0–10,000,000,000 元之间；不能填负数。');
    return x;
  }
  function amount(x, alpha) { return x.N * (x.cp - (1 - alpha) * x.cb) - x.F; }
  function evaluate(raw) {
    const x = validate(raw);
    const incrementalOrders = x.N * x.alpha;
    const replacedOrders = x.N * (1 - x.alpha);
    const promoContribution = x.N * x.cp;
    const displacedContribution = replacedOrders * x.cb;
    const delta = amount(x, x.alpha);
    let threshold = null;
    let thresholdState = 'unsupported';
    if (x.N > 0 && x.cb > 0) {
      // 与 1-cp/cb+F/(N*cb) 代数等价；先合并分子，减少端点的浮点相消误差。
      threshold = (x.F - x.N * (x.cp - x.cb)) / (x.N * x.cb);
      thresholdState = threshold < 0 ? 'all-positive' : threshold === 0 ? 'break-even-at-zero' : threshold < 1 ? 'within-range' : threshold === 1 ? 'break-even-at-one' : 'unreachable';
      if (!Number.isFinite(threshold)) { threshold = null; thresholdState = 'precision-limit'; }
    }
    return { ...x, incrementalOrders, replacedOrders, promoContribution, displacedContribution, delta,
      threshold, thresholdState, atZero: amount(x,0), atOne: amount(x,1),
      scenarios: [0,0.25,0.5,0.75,1].map(alpha => ({alpha, delta: amount(x,alpha)})) };
  }
  function contribution(raw) {
    const fields = ['settlement','food','packaging','commission','delivery','discount','labor','other'];
    const x = {};
    for (const field of fields) {
      x[field] = number(raw[field], '单均构成项 ' + field);
      if (x[field] < 0 || x[field] > 1000000) throw new Error('单均构成项须为 0–1,000,000 元；退款冲正须先按同口径汇总。');
    }
    const c = x.settlement - fields.slice(1).reduce((sum, field) => sum + x[field], 0);
    if (Math.abs(c) > LIMITS.contribution) throw new Error('构成项算出的单均贡献超过支持范围，请检查币种和单位。');
    return c;
  }
  const api = Object.freeze({ LIMITS, DEFAULTS, number, validate, evaluate, contribution });
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.DeliveryModel = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
