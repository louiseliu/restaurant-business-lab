"""Append the two frozen diagram/preview branches to the existing portal reader."""
IDS=['research-2026-11-06-robot-subscription-exit-note','research-2026-11-06-ai-practice-validation-note']
NAMES=[['RobotSubscriptionDiagrams.jsx','robotsubscription-diagrams.css','robotsubscription-source-previews.json'],['AIPracticeDiagrams.jsx','aipractice-diagrams.css','aipractice-source-previews.json']]
def patch_reader(text):
 def replace(old,new):
  nonlocal text
  assert text.count(old)==1,'Reader anchor changed; preserve edits: '+old[:70]
  text=text.replace(old,new)
 replace("import React from 'react';","import React from 'react';\nimport RobotSubscriptionSourcePreviews from './robotsubscription-source-previews.json';\nimport {RobotSubscriptionDiagram} from './RobotSubscriptionDiagrams.jsx';\nimport AIPracticeSourcePreviews from './aipractice-source-previews.json';\nimport {AIPracticeDiagram} from './AIPracticeDiagrams.jsx';")
 replace('const diagramRows=reviewedRows(diagramId);',"const diagramRows=reviewedRows(diagramId);\n if(diagram.layout?.startsWith('robotsubscription-'))return <RobotSubscriptionDiagram diagram={diagram} id={id} rows={diagramRows}/>;\n if(diagram.layout?.startsWith('aipractice-'))return <AIPracticeDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
 replace('sourcePreviews={',f"sourcePreviews={{id.includes('{IDS[0]}')?RobotSubscriptionSourcePreviews:id.includes('{IDS[1]}')?AIPracticeSourcePreviews:")
 replace('const R=({id,children,className})=>','const portal69Sources={"research-2026-11-06-robot-subscription-exit-note": "https://github.com/louiseliu/restaurant-business-lab/blob/2c32d8b669ea8cf6c5835e9598325bbddc73297a/research/2026-11-06-robot-subscription-exit/note.md", "research-2026-11-06-ai-practice-validation-note": "https://github.com/louiseliu/restaurant-business-lab/blob/10fb03ca2b9cb138818364d019ec5fb7360cd534/research/2026-11-06-ai-practice-validation/note.md"};\nfunction resolvePortal69Links(text,id){const entry=Object.entries(portal69Sources).find(([key])=>id===key||id.startsWith(key+\':\')||id===\'article:\'+key);return entry&&typeof text===\'string\'?text.replace(/\\]\\((\\.\\.?\\/[^)]+|sources\\.md)\\)/g,(_,url)=>`](${new URL(url,entry[1]).href})`):text;}\nconst R=({id,children,className})=>')
 replace('value={children} className={className}', 'value={resolvePortal69Links(children,id)} className={className}')
 return text

def patch_catalog_reader(text):
 def replace(old,new):
  nonlocal text
  assert text.count(old)==1,'Catalog reader anchor changed; preserve edits: '+old[:70]
  text=text.replace(old,new)
 helper="function topicMatch(article,topic){return article.topics.includes(topic)||(article.id==='research-2026-11-06-robot-subscription-exit-note'&&topic==='business-model'&&article.topics.includes('business'));}\n"
 replace('function readRoute()',helper+'function readRoute()')
 replace('a.topics.includes(r.topic)','topicMatch(a,r.topic)')
 replace("a.topics.includes('business-model')","topicMatch(a,'business-model')")
 return text
