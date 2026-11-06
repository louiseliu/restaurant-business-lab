import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const root=path.resolve(process.argv[2]);
const baseline=path.resolve(root,'../../../..','baseline69/src/content/report');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const source=fs.readFileSync(path.join(root,'ReportContent.jsx'),'utf8');
const oldSource=fs.readFileSync(path.join(baseline,'ReportContent.jsx'),'utf8');
assert.equal(source.replace("(article.id==='research-2026-11-06-site-selection-rent-note'&&['ai','business-model'].includes(topic))||",'').replace("topicMatch(a,'ai')?'AI 在餐饮'","a.topics.includes('ai')?'AI 在餐饮'"),oldSource);
const helpers=source.slice(source.indexOf('function topicMatch('),source.indexOf('export function ReportContent()'));
const ctx=vm.createContext({location:{hash:''},URLSearchParams});vm.runInContext(helpers,ctx);
const a=read(path.join(root,'articles.json')),old=read(path.join(baseline,'articles.json'));
assert.equal(a.articles.length,91);assert.equal(Object.keys(read(path.join(root,'illustrated-stories.json'))).length,71);
assert.equal(Object.keys(read(path.join(root,'samples.json'))).length,2);
const research=a.articles.filter(x=>x.section==='research');assert.equal(research.length,71);assert.equal(research.filter(x=>x.topics.includes('ai')).length,47);
assert.equal(research.filter(x=>{ctx.article=x;return vm.runInContext("topicMatch(article,'ai')",ctx)}).length,48);
let checks=0;
for(const x of a.articles){ctx.location.hash='#read/'+x.id;const r=vm.runInContext('readRoute()',ctx);assert.equal(r.id,x.id);checks++;}
ctx.location.hash='#?view=all&topic=ai&q=%E5%8E%A8%E6%88%BF&section=research';const h=vm.runInContext('homeHash(readRoute())',ctx);ctx.location.hash=h;assert.equal(vm.runInContext('readRoute().q',ctx),'厨房');assert.equal(vm.runInContext('readRoute().section',ctx),'research');checks+=2;
for(const x of research){ctx.article=x;for(const topic of ['ai','business','business-model','other']){ctx.topic=topic;assert.equal(vm.runInContext('topicMatch(article,topic)',ctx),x.topics.includes(topic)||(x.id==='research-2026-11-06-site-selection-rent-note'&&['ai','business-model'].includes(topic))||(x.id==='research-2026-11-06-robot-subscription-exit-note'&&topic==='business-model'&&x.topics.includes('business')));checks++;}}
const extract=(p,start,end)=>{const s=fs.readFileSync(p,'utf8');return s.slice(s.indexOf(start),s.indexOf(end));};
const currentCtx=vm.createContext({URL});vm.runInContext(extract(path.join(root,'IllustratedArticle.jsx'),'const portal69Sources=','const R='),currentCtx);
const oldCtx=vm.createContext({URL});vm.runInContext(extract(path.join(baseline,'IllustratedArticle.jsx'),'const portal69Sources=','const R='),oldCtx);
for(const x of old.articles){for(const id of [x.id+':lead',x.id+':section:0','article:'+x.id]){currentCtx.text=oldCtx.text=x.body;currentCtx.id=oldCtx.id=id;assert.equal(vm.runInContext('resolvePortal71Links(resolvePortal69Links(text,id),id)',currentCtx),vm.runInContext('resolvePortal69Links(text,id)',oldCtx));checks++;}}
for(const x of research.slice(0,2)){for(const id of [x.id+':lead',x.id+':technical:0','article:'+x.id]){currentCtx.text=x.body;currentCtx.id=id;const resolved=vm.runInContext('resolvePortal71Links(resolvePortal69Links(text,id),id)',currentCtx);for(const [,relative] of x.body.matchAll(/\]\((\.\.?\/[^)]+|sources\.md|calculations\.py|calculation-results\.json)\)/g)){assert.ok(resolved.includes(new URL(relative,x.sourceUrl).href));checks++;}assert.ok(!/\]\((\.\.?\/|sources\.md|calculations\.py|calculation-results\.json)/.test(resolved));checks++;}}
console.log(JSON.stringify({actualHelperChecks:checks,routeParsing:true,topicFilters:true,previousBehaviorPreserved:true,newRelativeLinksResolved:true,browserTests:false}));
