/* Walkthrough maps and encounters reuse the owner's manually pinned wiki snapshot. */
"use strict";
window.LegendsWalkthroughMaps=(()=>{
 let pending,renderToken=0;
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function load(){return pending||(pending=Promise.all(['walkthrough-maps.json','dex-data.json'].map(url=>fetch(url+'?layout=2',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('Map data unavailable');return r.json();}))).catch(e=>{pending=null;throw e;}));}
 function regionExplorer(root,guide){
  const host=root.querySelector('#section-your-first-adventure');if(!host)return;
  if(!guide.regions?.Hoenn?.towns||!guide.regions?.Kanto?.towns)throw Error('Region maps need refreshed data');
  const panel=document.createElement('section');panel.className='region-map-explorer';panel.setAttribute('aria-label','Explore the region maps');
  panel.innerHTML='<div class="region-map-tabs"><button type="button" data-region-map="Hoenn" aria-pressed="true">Hoenn</button><button type="button" data-region-map="Kanto" aria-pressed="false">Kanto</button></div><div class="region-map-canvas"></div><p>Town and city symbols mark settlements; the connecting paths show routes, and blue areas show the sea. Tap a town symbol to see its name. Switch between Hoenn and Kanto above, or choose a town from the list below.</p><label class="map-town-picker">Find a town <select aria-label="Choose a town on the map"></select></label><output class="map-town-name" aria-live="polite">Tap a town to see its name.</output>';
  let next=host.nextElementSibling;while(next&&!/^H[23]$/.test(next.tagName))next=next.nextElementSibling;if(next)next.before(panel);else host.parentElement.append(panel);
  let region='Hoenn';const canvas=panel.querySelector('.region-map-canvas'),picker=panel.querySelector('select'),name=panel.querySelector('output');
  const choose=i=>{const town=guide.regions[region].towns[Number(i)];if(!town)return;picker.value=String(i);name.textContent=town.name+' · '+region;};
  function draw(selected){region=selected;const map=guide.regions[region];
   panel.querySelectorAll('[data-region-map]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.regionMap===region)));
   canvas.innerHTML='<svg width="224" height="120" viewBox="0 0 224 120" role="group" aria-label="'+region+' town map"><image href="'+esc(map.image)+'" width="224" height="120"/>'+map.towns.map((t,i)=>'<rect class="map-town-hit" x="'+Math.max(0,t.x-2)+'" y="'+Math.max(0,t.y-2)+'" width="'+Math.min(224-Math.max(0,t.x-2),t.width+4)+'" height="'+Math.min(120-Math.max(0,t.y-2),t.height+4)+'" role="button" tabindex="0" data-town="'+i+'" aria-label="'+esc(t.name)+'"><title>'+esc(t.name)+'</title></rect>').join('')+'</svg>';
   picker.innerHTML='<option value="">Choose a town…</option>'+map.towns.map((t,i)=>'<option value="'+i+'">'+esc(t.name)+'</option>').join('');name.textContent='Tap a town to see its name.';
  }
  panel.addEventListener('click',e=>{const tab=e.target.closest('[data-region-map]'),town=e.target.closest('[data-town]');if(tab)draw(tab.dataset.regionMap);else if(town)choose(town.dataset.town);});
  panel.addEventListener('keydown',e=>{const town=e.target.closest('[data-town]');if(town&&(e.key==='Enter'||e.key===' ')){e.preventDefault();choose(town.dataset.town);}});
  picker.addEventListener('change',()=>{if(picker.value!=='')choose(picker.value);});draw('Hoenn');
 }
 function speciesRow(e,species){
  const p=species.get(e.id);if(!p)return '';
  const pos=window.LegendsSpriteAtlas?.icons[p.sprite];
  const icon=pos?'<span class="walkthrough-pokemon-icon" aria-hidden="true" style="--icon-x:'+(-pos[0])+';--icon-y:'+(-pos[1])+'"></span>':'';
  const level=e.min===e.max?e.min:e.min+'–'+e.max;
  return '<li><a href="dex.html?view=species&amp;pokemon='+encodeURIComponent(e.id)+'">'+icon+'<span><strong>'+esc(p.name)+'</strong><small>Lv. '+level+'</small></span></a><span class="walkthrough-rate">'+e.rate+'%</span></li>';
 }
 function encounterList(place,maps,species,available=["land"]){
  const route=maps.get(place.mapId);if(!route)return '';
  const land=route.methods.filter(m=>available.includes(m.id)),later=route.methods.filter(m=>!available.includes(m.id));
  const method=m=>'<div class="walkthrough-method"><strong>'+esc(m.id==='land'?'Walking encounters':m.label)+'</strong><ul>'+m.entries.map(e=>speciesRow(e,species)).join('')+'</ul></div>';
  return '<section class="walkthrough-route" data-route="'+esc(route.id)+'"><div class="walkthrough-route-heading"><strong>'+esc(route.name)+' encounters</strong><a href="dex.html?map='+encodeURIComponent(route.id)+'">Open in LegendsDex →</a></div>'+land.map(method).join('')+(later.length?'<details class="walkthrough-later"><summary>Other methods to revisit</summary><p>These methods need the matching rod or field utility. Return once you have it.</p>'+later.map(method).join('')+'</details>':'')+'</section>';
 }
 async function decorate(root,page){
  const token=++renderToken;
  try{
   const [guide,data]=await load();if(token!==renderToken||root.dataset.walkthroughPage!==page)return;
   if(guide.sourceCommit!==data.sourceCommit||window.LegendsSpriteAtlas?.sourceCommit!==data.sourceCommit)throw Error('Snapshot mismatch');
   const species=new Map(data.species.map(p=>[p.id,p])),maps=new Map(data.maps.map(m=>[m.id,m]));
   if(page==='walkthrough')regionExplorer(root,guide);
   for(const block of guide.chapters[page]||[]){
    const heading=block.section==='chapter-overview'?root.querySelector('.chapter-intro-tip'):root.querySelector('#'+block.section);if(!heading)continue;
    const places=block.places.map(id=>guide.places[id]),cells=new Map();for(const p of places)for(const c of p.cells)cells.set(c.join(','),c);
    const label=places.map(p=>p.name).join(', ');
    const figure='<figure class="walkthrough-map"><figcaption>Where you are: '+esc(label)+'</figcaption><svg viewBox="0 0 224 120" role="img" aria-label="Hoenn map highlighting '+esc(label)+'"><title>'+esc(label)+'</title><image href="'+esc(guide.image)+'" width="224" height="120"/>'+[...cells.values()].map(([x,y])=>'<rect class="walkthrough-map-highlight" x="'+x+'" y="'+y+'" width="8" height="8"/>').join('')+'</svg><p class="walkthrough-map-key"><span aria-hidden="true"></span> Highlighted: '+esc(label)+'</p></figure>';
    const encounters=block.encounters.map(id=>encounterList(guide.places[id],maps,species,block.availableMethods)).join('');
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
