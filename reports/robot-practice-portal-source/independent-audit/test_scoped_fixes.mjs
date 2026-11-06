import fs from 'node:fs';
import vm from 'node:vm';
import {pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const root=process.argv[2]?pathToFileURL(process.argv[2].replace(/\/$/,'')+'/'):new URL('../',import.meta.url);
const read=(name)=>fs.readFileSync(new URL(name,root),'utf8');
const old=JSON.parse(read('baseline67/src/content/report/articles.json')).articles;
const all=JSON.parse(read('portal69/src/content/report/articles.json')).articles;
const stories=JSON.parse(read('portal69/src/content/report/illustrated-stories.json'));
const r=read('portal69/src/content/report/IllustratedArticle.jsx');
const p=read('portal69/src/content/report/ReportContent.jsx');
const source=r.match(/^const portal69Sources=.*$/m)[0];
const resolver=r.match(/^function resolvePortal69Links.*$/m)[0];
const topic=p.match(/^function topicMatch.*$/m)[0];
const c=vm.createContext({URL});vm.runInContext(source+'\n'+resolver+'\n'+topic,c);
let checks=0,links=0;
for(const a of old){for(const t of ['ai','business','business-model','all','unknown']){assert.equal(c.topicMatch(a,t),a.topics.includes(t));checks++;}for(const id of [a.id,a.id+':lead','article:'+a.id]){assert.equal(c.resolvePortal69Links(a.body,id),a.body);checks++;}}
const ids=['research-2026-11-06-robot-subscription-exit-note','research-2026-11-06-ai-practice-validation-note'];
for(const id of ids){const a=all.find(a=>a.id===id),s=stories[id];const values=[[a.body,'article:'+id],[s.lead,id+':lead'],...s.sections.map((s,i)=>[s.body.join('\n\n'),id+':section:'+i])];
 for(const [text,key] of values){const out=c.resolvePortal69Links(text,key);for(const m of text.matchAll(/\]\((\.\.?\/[^)]+|sources\.md)\)/g)){assert(out.includes(']('+new URL(m[1],a.sourceUrl).href+')'));links++;}assert.equal(c.resolvePortal69Links(out,key),out);checks++;}
 assert.equal(c.resolvePortal69Links('[test](sources.md)','prefix'+id),'[test](sources.md)');checks++;
}
assert(c.topicMatch(all.find(a=>a.id===ids[0]),'business-model'));checks++;
assert(!c.topicMatch(all.find(a=>a.id===ids[1]),'business-model'));checks++;
assert(r.includes('value={resolvePortal69Links(children,id)}'));assert(p.includes("topicMatch(a,'business-model')")&&p.includes('topicMatch(a,r.topic)'));checks+=2;
console.log(JSON.stringify({status:'passed',oldEntries:old.length,checks,resolvedRelativeOccurrences:links,scope:'Actual extracted pure helpers executed in Node; no browser interaction.'}));
