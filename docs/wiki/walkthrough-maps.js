/* Walkthrough maps and encounters reuse the owner's manually pinned wiki snapshot. */
"use strict";
window.LegendsWalkthroughMaps=(()=>{
 let pending,renderToken=0;
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function load(){return pending||(pending=Promise.all(['walkthrough-maps.json','dex-data.json'].map(url=>fetch(url).then(r=>{if(!r.ok)throw Error('Map data unavailable');return r.json();}))).catch(e=>{pending=null;throw e;}));}
 function speciesRow(e,species){
  const p=species.get(e.id);if(!p)return '';
  const pos=window.LegendsSpriteAtlas?.icons[p.sprite];
  const icon=pos?'<span class="walkthrough-pokemon-icon" aria-hidden="true" style="--icon-x:'+(-pos[0])+';--icon-y:'+(-pos[1])+'"></span>':'';
  const level=e.min===e.max?e.min:e.min+'–'+e.max;
  return '<li><a href="dex.html?view=species&amp;pokemon='+encodeURIComponent(e.id)+'">'+icon+'<span><strong>'+esc(p.name)+'</strong><small>Lv. '+level+'</small></span></a><span class="walkthrough-rate">'+e.rate+'%</span></li>';
 }
 function encounterList(place,maps,species){
  const route=maps.get(place.mapId);if(!route)return '';
  const land=route.methods.filter(m=>m.id==='land'),later=route.methods.filter(m=>m.id!=='land');
  const method=m=>'<div class="walkthrough-method"><strong>'+esc(m.id==='land'?'Grass / walking':m.label)+'</strong><ul>'+m.entries.map(e=>speciesRow(e,species)).join('')+'</ul></div>';
  return '<section class="walkthrough-route" data-route="'+esc(route.id)+'"><div class="walkthrough-route-heading"><strong>'+esc(route.name)+' encounters</strong><a href="dex.html?map='+encodeURIComponent(route.id)+'">Open in LegendsDex →</a></div>'+land.map(method).join('')+(later.length?'<details class="walkthrough-later"><summary>Later: fishing and Surf encounters</summary><p>You need the matching fishing rod or Surf access before using these methods.</p>'+later.map(method).join('')+'</details>':'')+'</section>';
 }
 async function decorate(root,page){
  const token=++renderToken;
  try{
   const [guide,data]=await load();if(token!==renderToken||root.dataset.walkthroughPage!==page)return;
   if(guide.sourceCommit!==data.sourceCommit||window.LegendsSpriteAtlas?.sourceCommit!==data.sourceCommit)throw Error('Snapshot mismatch');
   const species=new Map(data.species.map(p=>[p.id,p])),maps=new Map(data.maps.map(m=>[m.id,m]));
   for(const block of guide.chapters[page]||[]){
    const heading=root.querySelector('#'+block.section);if(!heading)continue;
    const places=block.places.map(id=>guide.places[id]),cells=new Map();for(const p of places)for(const c of p.cells)cells.set(c.join(','),c);
    const label=places.map(p=>p.name).join(', ');
    const figure='<figure class="walkthrough-map"><figcaption>Where you are: '+esc(label)+'</figcaption><svg viewBox="0 0 224 120" role="img" aria-label="Hoenn map highlighting '+esc(label)+'"><title>'+esc(label)+'</title><image href="'+esc(guide.image)+'" width="224" height="120"/>'+[...cells.values()].map(([x,y])=>'<rect class="walkthrough-map-highlight" x="'+x+'" y="'+y+'" width="8" height="8"/>').join('')+'</svg><p class="walkthrough-map-key"><span aria-hidden="true"></span> Highlighted: '+esc(label)+'</p></figure>';
    const encounters=block.encounters.map(id=>encounterList(guide.places[id],maps,species)).join('');
    const html='<aside class="walkthrough-field-guide" data-walkthrough-section="'+esc(block.section)+'" aria-label="Map and encounters for '+esc(heading.textContent)+'">'+figure+(block.note?'<p class="walkthrough-field-note">'+esc(block.note)+'</p>':'')+(encounters?'<p class="walkthrough-encounter-note">Standard wild encounters. Percentages are the share within each method, not the chance per step. Tap a Pokémon for its LegendsDex details.</p>'+encounters:'')+'</aside>';
    // Place the field guide after this section's instructions, before the next heading.
    let next=heading.nextElementSibling;while(next&&!/^H[23]$/.test(next.tagName))next=next.nextElementSibling;
    if(next)next.insertAdjacentHTML('beforebegin',html);else heading.parentElement.insertAdjacentHTML('beforeend',html);
   }
   // Town deep links retain their section position when the maps finish loading above them.
   const anchor=location.hash.slice(1);if(/^section-[a-z0-9-]+$/.test(anchor)&&root.querySelector('#'+anchor))root.querySelector('#'+anchor).scrollIntoView({block:'start',behavior:'instant'});
  }catch{if(token===renderToken&&root.dataset.walkthroughPage===page){const nav=root.querySelector('.walkthrough-navigation');nav?.insertAdjacentHTML('afterend','<p class="walkthrough-map-error">Maps and encounters could not load. You can keep reading the instructions, or refresh to try again.</p>');}}
 }
 return {decorate};
})();
