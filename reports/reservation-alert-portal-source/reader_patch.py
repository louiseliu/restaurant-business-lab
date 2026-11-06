"""Scoped additions for the two new frozen articles. Never replace an existing reader."""
import json
IDS=['research-2026-11-06-reservation-policy-note','research-2026-11-06-order-alert-note']
NAMES=[['ReservationPolicyDiagrams.jsx','reservation-policy-diagrams.css','reservation-policy-source-previews.json'],['OrderAlertDiagrams.jsx','order-alert-diagrams.css','order-alert-source-previews.json']]
URLS=['https://github.com/louiseliu/restaurant-business-lab/blob/fdb6fd9e3c9e34d4afc772a14bd82dc8e6a8d349/research/2026-11-06-reservation-policy/note.md','https://github.com/louiseliu/restaurant-business-lab/blob/40d7d709015ed753668b52e22c0dd8d49ff96db9/research/2026-11-06-order-alert/note.md']
def patch_reader(text):
 def replace(old,new,count=1):
  nonlocal text
  assert text.count(old)==count,'Reader anchor changed; preserve edits: '+old[:70]
  text=text.replace(old,new)
 replace("import React from 'react';","import React from 'react';\nimport ReservationPolicySourcePreviews from './reservation-policy-source-previews.json';\nimport {ReservationPolicyDiagram} from './ReservationPolicyDiagrams.jsx';\nimport OrderAlertSourcePreviews from './order-alert-source-previews.json';\nimport {OrderAlertDiagram} from './OrderAlertDiagrams.jsx';")
 replace('const diagramRows=reviewedRows(diagramId);',"const diagramRows=reviewedRows(diagramId);\n if(diagram.layout?.startsWith('reservation-policy-'))return <ReservationPolicyDiagram diagram={diagram} id={id} rows={diagramRows}/>;\n if(diagram.layout?.startsWith('order-alert-'))return <OrderAlertDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
 replace('sourcePreviews={',f"sourcePreviews={{id.includes('{IDS[0]}')?ReservationPolicySourcePreviews:id.includes('{IDS[1]}')?OrderAlertSourcePreviews:")
 helper='const portal73Sources='+json.dumps(dict(zip(IDS,URLS)))+';\nfunction resolvePortal73Links(text,id){const entry=Object.entries(portal73Sources).find(([key])=>id===key||id.startsWith(key+\':\')||id===\'article:\'+key);return entry&&typeof text===\'string\'?text.replace(/\\]\\((\\.\\.?\\/[^)]+|sources\\.md)\\)/g,(_,url)=>`](${new URL(url,entry[1]).href})`):text;}\n'
 replace('const R=({id,children,className})=>',helper+'const R=({id,children,className})=>')
 replace('value={resolvePortal71Links(resolvePortal69Links(children,id),id)}','value={resolvePortal73Links(resolvePortal71Links(resolvePortal69Links(children,id),id),id)}')
 replace("lang={['research-2026-11-06-site-selection-rent-note'",f"lang={{['{IDS[0]}','{IDS[1]}','research-2026-11-06-site-selection-rent-note'")
 replace('Object.hasOwn(portal71Sources,item.id)','(Object.hasOwn(portal71Sources,item.id)||Object.hasOwn(portal73Sources,item.id))',2)
 return text

def patch_catalog_reader(text):
 # No catalog behavior change is needed. Fail early on an unexpected structure.
 assert text.count('function topicMatch(')==1,'Catalog reader anchor changed; preserve edits'
 return text
