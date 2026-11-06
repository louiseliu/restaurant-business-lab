"""Scoped additions only: new diagrams, previews, frozen relative links, language and ledger note."""
import json
IDS=['research-2026-11-06-site-selection-rent-note','research-2026-11-06-supplier-recommendation-note']
NAMES=[['SiteSelectionDiagrams.jsx','siteselection-diagrams.css','siteselection-source-previews.json'],['SupplierRecommendationDiagrams.jsx','supplier-recommendation-diagrams.css','supplier-recommendation-source-previews.json']]
URLS=['https://github.com/louiseliu/restaurant-business-lab/blob/c905ca1df6c8587d76b5f7e66dae7c57d5a342ce/research/2026-11-06-site-selection-rent/note.md','https://github.com/louiseliu/restaurant-business-lab/blob/1496fce49b261cb108102b83dec501cea82cd5b4/research/2026-11-06-supplier-recommendation/note.md']
def patch_reader(text):
 def replace(old,new):
  nonlocal text
  assert text.count(old)==1,'Reader anchor changed; preserve edits: '+old[:70]
  text=text.replace(old,new)
 replace("import React from 'react';","import React from 'react';\nimport SiteSelectionSourcePreviews from './siteselection-source-previews.json';\nimport {SiteSelectionDiagram} from './SiteSelectionDiagrams.jsx';\nimport SupplierRecommendationSourcePreviews from './supplier-recommendation-source-previews.json';\nimport {SupplierRecommendationDiagram} from './SupplierRecommendationDiagrams.jsx';")
 replace('const diagramRows=reviewedRows(diagramId);',"const diagramRows=reviewedRows(diagramId);\n if(diagram.layout?.startsWith('siteselection-'))return <SiteSelectionDiagram diagram={diagram} id={id} rows={diagramRows}/>;\n if(diagram.layout?.startsWith('supplier-recommendation-'))return <SupplierRecommendationDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
 replace('sourcePreviews={',f"sourcePreviews={{id.includes('{IDS[0]}')?SiteSelectionSourcePreviews:id.includes('{IDS[1]}')?SupplierRecommendationSourcePreviews:")
 helper='const portal71Sources='+json.dumps(dict(zip(IDS,URLS)))+';\nfunction resolvePortal71Links(text,id){const entry=Object.entries(portal71Sources).find(([key])=>id===key||id.startsWith(key+\':\')||id===\'article:\'+key);return entry&&typeof text===\'string\'?text.replace(/\\]\\((\\.\\.?\\/[^)]+|sources\\.md|calculations\\.py|calculation-results\\.json)\\)/g,(_,url)=>`](${new URL(url,entry[1]).href})`):text;}\n'
 replace('const R=({id,children,className})=>',helper+'const R=({id,children,className})=>')
 replace('value={resolvePortal69Links(children,id)}','value={resolvePortal71Links(resolvePortal69Links(children,id),id)}')
 replace("lang={['research-2026-11-06-ai-discovery-value-note'",f"lang={{['{IDS[0]}','research-2026-11-06-ai-discovery-value-note'")
 replace('<summary>深入看：计算口径与推论边界</summary><div>{story.technicalDetails.map', '<summary>{Object.hasOwn(portal71Sources,item.id)?\'首次研究台账，历史状态保留\':\'深入看：计算口径与推论边界\'}</summary><div>{Object.hasOwn(portal71Sources,item.id)&&<R id={`${item.id}:ledger-status`}>{`以下台账保留定稿时的文字，其中“未提交”等描述属于当时状态。当前固定研究版本见[研究原文](${item.sourceUrl})。`}</R>}{story.technicalDetails.map')
 replace("{item.topics.includes('ai')?'AI 在餐饮'","{(item.id==='research-2026-11-06-site-selection-rent-note'||item.topics.includes('ai'))?'AI 在餐饮'")
 return text


def patch_catalog_reader(text):
 def replace(old,new):
  nonlocal text
  assert text.count(old)==1,'Catalog reader anchor changed; preserve edits: '+old[:70]
  text=text.replace(old,new)
 replace("function topicMatch(article,topic){return article.topics.includes(topic)","function topicMatch(article,topic){return (article.id==='research-2026-11-06-site-selection-rent-note'&&['ai','business-model'].includes(topic))||article.topics.includes(topic)")
 replace("a.topics.includes('ai')?'AI 在餐饮'","topicMatch(a,'ai')?'AI 在餐饮'")
 return text
