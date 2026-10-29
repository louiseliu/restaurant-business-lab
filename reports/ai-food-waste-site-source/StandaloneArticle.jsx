import React from 'react';
import {IllustratedArticle} from './IllustratedArticle.jsx';
import catalog from './articles.json';
import stories from './illustrated-stories.json';
import './timeline.css';
const when=t=>new Intl.DateTimeFormat('zh-CN',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hour12:false}).format(new Date(t));
export function ReportContent(){const item=catalog.articles[0];return <IllustratedArticle item={item} story={stories[item.id]} when={when} back={<a className="timeline-back" href={item.sourceUrl} target="_blank" rel="noreferrer">查看固定版本研究原文 ↗</a>}/>;}
