import React from 'react';
import samples from './samples.json';
import './samples.css';
function download(file){
 const bytes=file.encoding==='base64'?Uint8Array.from(atob(file.body),c=>c.charCodeAt(0)):file.body;
 const url=URL.createObjectURL(new Blob([bytes],{type:file.mime}));const a=document.createElement('a');a.href=url;a.download=file.name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
export function SampleCards(){return <section className="sample-cards" aria-label="实战样板"><div className="sample-section-head"><h2>实战样板</h2><p>把研究方法用起来；以下是条件测算或模拟演示，不是新增实测研究。</p></div><div className="sample-card-grid">{Object.values(samples).map(s=><article key={s.id}><span className="sample-badge">{s.label}</span><h3>{s.title}</h3><p>{s.summary}</p>{s.html?<a href={`#read/${s.id}`}>打开样板 →</a>:<span>核验完成后开放</span>}</article>)}</div></section>}
export function SampleReader({id,back}){const s=samples[id];if(!s)return null;return <article className="sample-reader">{back||<a className="timeline-back" href="#">← 返回文章与样板</a>}<header><span className="sample-badge">{s.label}</span><h1>{s.title}</h1><p>{s.summary}</p><p className="sample-boundary">{s.boundary}</p></header><div className="sample-downloads" aria-label="下载样板原件">{s.files.map(f=><button key={f.name} onClick={()=>download(f)}>下载 {f.label||f.name}</button>)}</div><p className="sample-local-note">下方为隔离的本地样板。计算不上传；没有接入模型 API。手机可在样板内部上下滚动，也可下载独立 HTML 后离线打开。</p>{s.html?<iframe title={s.title} srcDoc={s.html} sandbox="allow-scripts" referrerPolicy="no-referrer" className="sample-frame"/>:<p>此样板仍在核验，尚未开放。</p>}<footer>{back||<a href="#">← 返回文章与样板</a>}<details><summary>版本与文件核验</summary><p>样板版本 {s.version} · 原件 SHA256</p><code>{s.sha256||'待冻结'}</code><p>下载文件与该版本原件一致；模拟或条件输入不构成实际经营结果。</p></details></footer></article>}
export const sampleIds=Object.keys(samples);
