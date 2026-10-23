'use client';
import {useState} from 'react';
import {Artifact} from '../../../lib/api';
import {SaveButton} from '../../saved-components';
import {ExhibitContent} from './content';
type Tab='story'|'making'|'details'|'look';
export function ArtifactExperience({a,content}:{a:Artifact;content:ExhibitContent}) {
 const [tab,setTab]=useState<Tab>('story'),[copied,setCopied]=useState(false);
 async function share(){try{await navigator.clipboard.writeText(window.location.href);setCopied(true);window.setTimeout(()=>setCopied(false),1800)}catch{setCopied(false)}}
 const tabs:Tab[]=['story','making','details','look'];
 const labels:Record<Tab,string>={story:'The story',making:'Making & use',details:'Object file',look:'Look closer'};
 return <section className="exhibit">
  <div className="exhibit-media">{a.image_url?<img className="exhibit-photo" src={a.image_url} alt={a.name}/>:<div className="photo-unavailable photo-unavailable-large">Photograph unavailable</div>}<div className="photo-caption"><span>OBJECT IN FOCUS</span><span>{a.image_attribution||'Collection photograph'}</span></div></div>
  <div className="exhibit-copy"><div className="eyebrow">{a.category.name} <span className="dot">•</span> {a.historical_period}</div><h1>{a.name}</h1><p className="exhibit-lead">{content.lead}</p>
   <div className="object-actions"><SaveButton item={{slug:a.slug,name:a.name,category:a.category.name,period:a.historical_period,image:a.image_url}}/><button className="button light" onClick={share}>{copied?'Link copied ✓':'Share object ↗'}</button></div>
   <div className="exhibit-tabs" role="tablist" aria-label="Explore this object">{tabs.map(x=><button key={x} role="tab" aria-selected={tab===x} className={tab===x?'active':''} onClick={()=>setTab(x)}>{labels[x]}</button>)}</div>
   {tab==='story'&&<div className="tab-panel" role="tabpanel"><div className="reading-copy"><p>{content.story}</p></div><div className="context-note"><span className="eyebrow">A wider world</span><p>{content.history}</p></div></div>}
   {tab==='making'&&<div className="tab-panel" role="tabpanel"><div className="making-section"><span className="eyebrow">How it works</span><p>{content.how}</p></div><div className="making-section"><span className="eyebrow">In people’s hands</span><p>{content.inUse}</p></div><div className="process-callout"><span>FROM MATERIAL</span><b>{a.materials.join(' · ')}</b><span>TO MEANING</span></div></div>}
   {tab==='details'&&<div className="tab-panel" role="tabpanel"><div className="fact-grid"><div><span>Period</span><b>{a.historical_period}</b></div><div><span>Place</span><b>{a.origin}</b></div><div><span>Materials</span><b>{a.materials.join(', ')}</b></div><div><span>Subject</span><b>{a.category.name}</b></div></div><p className="significance">{a.historical_significance}</p><div className="context-note"><span className="eyebrow">Reading the record</span><p>{content.context}</p></div>{a.source_url&&<a className="source-link" href={a.source_url} target="_blank" rel="noreferrer">Open the collection record ↗</a>}</div>}
   {tab==='look'&&<div className="tab-panel" role="tabpanel"><div className="look-list">{content.look.map((x,i)=><div className="look-item" key={x}><span>0{i+1}</span><p>{x}</p></div>)}</div><div className="context-note"><span className="eyebrow">A question to carry</span><p>What can the materials and the way this object was made tell you about its maker, owner, or moment in history?</p></div></div>}
  </div></section>
}

