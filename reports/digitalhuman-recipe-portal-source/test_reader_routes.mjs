import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const root=process.argv[2]||path.resolve(import.meta.dirname,'..');
const source=fs.readFileSync(path.join(root,'ReportContent.jsx'),'utf8');
const helpers=source.slice(source.indexOf('function readRoute()'),source.indexOf('export function ReportContent()'));
const context=vm.createContext({location:{hash:''},URLSearchParams});vm.runInContext(helpers,context);
for(const test of [
 {hash:'#read/research-2026-11-06-digitalhuman-livestream-note',id:'research-2026-11-06-digitalhuman-livestream-note',view:'research',topic:'all',q:''},
 {hash:'',id:'',view:'research',topic:'all',q:''},
 {hash:'#read/research-2026-11-06-ai-recipe-development-note',id:'research-2026-11-06-ai-recipe-development-note',view:'research',topic:'all',q:''},
 {hash:'#read/research-2026-11-06-supplier-alias-mapping-note',id:'research-2026-11-06-supplier-alias-mapping-note',view:'research',topic:'all',q:''},
 {hash:'#read/research-2026-11-05-forecast-reimport-note',id:'research-2026-11-05-forecast-reimport-note',view:'research',topic:'all',q:''},
 {hash:'#read/research-2026-11-05-kotipizza-pricing-note',id:'research-2026-11-05-kotipizza-pricing-note',view:'research',topic:'all',q:''},
 {hash:'#read/research-2026-10-29-ai-food-waste-note',id:'research-2026-10-29-ai-food-waste-note',view:'research',topic:'all',q:''},
 {hash:'#?view=all&topic=ai&q=%20%E5%8E%A8%E6%88%BF%20&section=methods',id:'',view:'all',topic:'ai',q:' 厨房 '},
 {hash:'#read/sample-delivery',id:'sample-delivery',view:'research',topic:'all',q:''}
]){context.location.hash=test.hash;const r=vm.runInContext('readRoute()',context);for(const k of ['id','view','topic','q'])assert.equal(r[k],test[k]);}
context.location.hash='#?view=all&topic=ai&q=%E5%8E%A8%E6%88%BF&section=research';const hash=vm.runInContext('homeHash(readRoute())',context);context.location.hash=hash;assert.equal(vm.runInContext('readRoute().q',context),'厨房');assert.equal(vm.runInContext('readRoute().section',context),'research');
const catalog=JSON.parse(fs.readFileSync(path.join(root,'articles.json'),'utf8'));const stories=JSON.parse(fs.readFileSync(path.join(root,'illustrated-stories.json'),'utf8'));const samples=JSON.parse(fs.readFileSync(path.join(root,'samples.json'),'utf8'));
assert.equal(catalog.articles.length,87);assert.equal(Object.keys(stories).length,67);assert.equal(Object.keys(samples).length,2);
const selected=catalog.articles.filter(a=>a.section==='research');assert.equal(selected.length,67);assert.equal(selected.filter(a=>a.topics.includes('ai')).length,45);assert.equal(selected[0].id,'research-2026-11-06-ai-recipe-development-note');
for(let i=1;i<selected.length;i++)assert.ok(selected[i-1].publishedAt>=selected[i].publishedAt);
assert.ok(!source.includes('还没有 AI 专题文章'));
assert.equal(selected.find(a=>a.id==='research-2026-10-30-qsmart-note').publishedAt,'2026-10-30T07:29:17Z');
console.log('Route parsing/URL round trip, 67/87/2 counts, AI topic and chronological order passed. Browser history/scroll checks are separate.');

