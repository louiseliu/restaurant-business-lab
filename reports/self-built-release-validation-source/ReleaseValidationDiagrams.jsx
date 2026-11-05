import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './release-validation-diagrams.css';
export function ReleaseValidationDiagram({diagram,id,rows}){
 const q=`diagram-${id}`;const auth=diagram.layout==='release-auth';
 const Stage=({row,index})=><section className="release-stage" key={row['验收环节']}><header><span className="release-index">{String(index+1).padStart(2,'0')}</span><div><p className="release-tag">{row['性质']}</p><h3>{row['验收环节']}</h3></div></header><div className="release-cells">{Object.entries(row).filter(([key])=>!['验收环节','性质'].includes(key)).map(([label,text])=><div className="release-cell" key={label}><h4>{label}</h4><p>{text}</p></div>)}</div></section>;
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className={`release-validation ${diagram.layout}`}>
   <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
   {auth?<div className="release-table-wrap" data-reviewed-rows><table className="release-table"><thead><tr><th>测试身份</th><th>实际权限约定</th><th>预期检查</th><th>谁来解释</th></tr></thead><tbody>{rows.map(row=><tr key={row['验收环节']}><th scope="row">{row['验收环节']}<small>{row['性质']}</small></th>{['权限约定','预期检查','谁来解释'].map(k=><td key={k} data-label={k}>{row[k]}</td>)}</tr>)}</tbody></table></div>:<><div className="release-stages" data-reviewed-rows>{rows.slice(0,4).map((row,index)=><Stage row={row} index={index} key={row['验收环节']}/>)}</div><div className="release-cases" data-reviewed-rows>{rows.slice(4).map((row,index)=><Stage row={row} index={index} key={row['验收环节']}/>)}</div></>}
   <RichNarrative id={`${id}:completion`} value={diagram.completion} className="release-completion"/>
   <RichNarrative id={`${id}:note`} value={diagram.note} className="study-figure-note"/>
  </figure>
 </DataComponent>;
}
