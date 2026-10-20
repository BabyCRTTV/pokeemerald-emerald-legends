// Reader navigation and lazy sprite-audio regression checks without a browser dependency.
const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
const base=__dirname+'/../docs/wiki/';
class Node {
 constructor(){this.listeners={};this.dataset={};this.value='';this.innerHTML='';this.textContent='';this.hidden=false;this.classList={add(){},remove(){},toggle(){}};}
 addEventListener(name,f){const previous=this.listeners[name];this.listeners[name]=previous?(...args)=>{previous(...args);f(...args);}:f;} getBoundingClientRect(){return {top:0};} setAttribute(){} focus(){} showModal(){this.open=true;} close(){this.open=false;this.listeners.close?.();}
}
function boot(file,data,url='https://example.test/wiki/'){
 const nodes=new Map(),listeners={},windowListeners={},stack=[url];let index=0;
 const get=id=>{if(!nodes.has(id))nodes.set(id,new Node());return nodes.get(id);};
 let location=new URL(url);
 const ctx={URL,URLSearchParams,Map,Set,console,setTimeout,clearTimeout,HTMLImageElement:class{},navigator:{userAgent:'LegendsWikiAndroid/5'},document:{documentElement:get('html'),title:'',hidden:false,activeElement:null,getElementById:get,querySelector:s=>get(s.replace(/^#/,'')),querySelectorAll:()=>[],addEventListener:(n,f)=>listeners[n]=f},window:{scrollY:0,scrollTo(){},matchMedia:()=>({matches:false}),addEventListener:(n,f)=>windowListeners[n]=f},LegendsSprites:{markup:()=>'<span class="thumb"></span>',hydrate(){},preload:async()=>{}},fetch:async()=>({ok:true,json:async()=>data})};
 Object.defineProperty(ctx,'location',{get:()=>location});
 ctx.history={pushState(a,b,u){location=new URL(u,location);stack.splice(++index);stack.push(location.href);},replaceState(a,b,u){location=new URL(u,location);stack[index]=location.href;}};
 const sounds=[];
 ctx.Audio=class {constructor(url){this.url=url;this.events={};sounds.push(this);}pause(){this.paused=true;}addEventListener(n,f){this.events[n]=f;}play(){this.played=true;return this.fail?Promise.reject(Error()):Promise.resolve();}};
 vm.runInNewContext(fs.readFileSync(base+'cry-forms.js','utf8'),ctx);
 vm.runInNewContext(fs.readFileSync(base+'dex-profiles.js','utf8'),ctx);
 vm.runInNewContext(fs.readFileSync(base+file,'utf8'),ctx);
 const click=(kind,value)=>{const target=get('clicked');target.dataset={[kind]:value};listeners.click({target:{closest:s=>s==='[data-'+kind+']'?target:null},preventDefault(){}});};
 return {ctx,get,click,sounds,back(){location=new URL(stack[--index]);windowListeners.popstate();},listeners};
}
const settle=()=>new Promise(r=>setImmediate(r));
(async()=>{
 const articles=JSON.parse(fs.readFileSync(base+'articles.json'));
 const w=boot('wiki.js',articles);await settle();
 assert.equal((w.get('cards').innerHTML.match(/data-category=/g)||[]).length,8);
 assert(!w.get('cards').innerHTML.includes('data-page='),'home must not dump every article');
 w.click('category','Customization');assert.match(w.ctx.location.search,/category=Customization/);assert.match(w.get('content').innerHTML,/Trainer Card customization/);
 w.click('page','wardrobe');assert.match(w.ctx.location.search,/page=wardrobe/);
 w.back();assert.match(w.get('content').innerHTML,/<h1>Customization<\/h1>/);
 w.back();assert.match(w.get('content').innerHTML,/alt="Pokémon Emerald: Legends"/);
 w.get('search').value='boots';w.get('search').listeners.input();assert.match(w.get('cards').innerHTML,/wardrobe/);
 w.click('category','all');assert.equal((w.get('content').innerHTML.match(/data-page=/g)||[]).length,articles.articles.length);
 const chapters=articles.articles.filter(p=>Number.isInteger(p.chapter)).sort((a,b)=>a.chapter-b.chapter);
 assert(chapters.every(p=>!p.content.includes('## Your goal')&&!p.content.includes('First time playing?')));
 assert.deepEqual(chapters.map(p=>p.chapter),Array.from({length:25},(_,i)=>i+1));
 w.click('page',chapters[0].id);assert.match(w.get('content').innerHTML,/Next chapter/);assert(!w.get('content').innerHTML.includes('Previous chapter'));
 w.click('page',chapters[17].id);assert.match(w.get('content').innerHTML,/Next chapter/);
 w.click('page',chapters[24].id);assert.match(w.get('content').innerHTML,/Previous chapter/);assert(!w.get('content').innerHTML.includes('Next chapter'));
 const deep=boot('wiki.js',articles,'https://example.test/wiki/?category=Kanto%20postgame');await settle();assert.match(deep.get('content').innerHTML,/<h1>Kanto postgame/);
 const data=JSON.parse(fs.readFileSync(base+'dex-data.json'));
 const maps=JSON.parse(fs.readFileSync(base+'walkthrough-maps.json'));assert.equal(maps.sourceCommit,data.sourceCommit);
 const stats=JSON.parse(fs.readFileSync(base+'town-stat-sources.json'));assert.equal(stats.sourceCommit,maps.townStatsSourceCommit);
 for(const region of Object.values(maps.regions))for(const town of region.towns){const source=stats.towns[town.name];assert.equal(town.population,Object.values(source.npcPlacements).reduce((a,b)=>a+b,0));assert.equal(town.buildings,source.buildingCount);assert(town.population>=0&&town.buildings>=0);}
 for(const [page,blocks] of Object.entries(maps.chapters)){
  const content=articles.articles.find(p=>p.id===page).content;
  const headings=new Set([...content.matchAll(/^#{2,3} (.+)$/gm)].map(m=>'section-'+m[1].toLowerCase().replace(/[^a-z0-9 ]/g,'').trim().replace(/\s+/g,'-')));
  for(const block of blocks){assert(block.section==='chapter-overview'||headings.has(block.section),block.section);for(const id of block.places){assert(maps.places[id]);for(const [x,y] of maps.places[id].cells)assert(x>=0&&x<224&&y>=0&&y<120);}for(const id of block.encounters)assert(data.maps.some(m=>m.id===maps.places[id].mapId));}
 }

 const portraits=JSON.parse(fs.readFileSync(base+'dex-portrait-sources.json'));assert.equal(portraits.sourceCommit,data.sourceCommit);assert.equal(portraits.count,data.species.length);
 for(const [name,hash] of Object.entries(portraits.files))assert.equal(require('node:crypto').createHash('sha256').update(fs.readFileSync(base+name)).digest('hex'),hash,'portrait file integrity');
 // Changed source pins must request fresh metadata together with no-store JSON.
 const dexHTML=fs.readFileSync(base+'dex.html','utf8');
 for(const script of ['dex-profiles.js','dex-sprite-atlas.js']){
  const src=dexHTML.match(new RegExp('src="('+script.replaceAll('.','\\.')+'[^" ]*)"'))?.[1];
  assert(src?.includes(data.sourceCommit.slice(0,8)),script+' cache key must match pinned source');
 }
 const guideHTML=fs.readFileSync(base+'index.html','utf8');
 for(const script of ['dex-sprite-atlas.js','walkthrough-maps.js']){
  const src=guideHTML.match(new RegExp('src="('+script.replaceAll('.','\\.')+'[^" ]*)"'))?.[1];
  assert(src?.includes(data.sourceCommit.slice(0,8)),script+' guide cache key must match pinned source');
 }
 const atlas={window:{}};vm.runInNewContext(fs.readFileSync(base+'dex-sprite-atlas.js','utf8'),atlas);
 assert.equal(atlas.window.LegendsSpriteAtlas.sourceCommit,data.sourceCommit);
 for(const p of data.species)assert(atlas.window.LegendsSpriteAtlas.icons[p.sprite],p.id+' missing from preloaded atlas');
 const profiles={window:{}};vm.runInNewContext(fs.readFileSync(base+'dex-profiles.js','utf8'),profiles);
 assert.equal(profiles.window.LegendsProfiles.sourceCommit,data.sourceCommit);
 for(const p of data.species)assert(profiles.window.LegendsProfiles.entries[p.id],p.id+' missing entry');
 for(const m of data.maps){const loc=profiles.window.LegendsProfiles.locations[m.id];assert.equal(loc.region,m.region);if(m.region==='Sevii'){assert.equal(loc.cells.length,0,'Sevii must not use mainland coordinates');assert.match(loc.note,/expedition/);}else assert(loc.cells.length,m.id+' missing map marker');for(const [x,y] of loc.cells)assert(x>=0&&x<224&&y>=0&&y<120);}
 assert.deepEqual(JSON.parse(JSON.stringify(profiles.window.LegendsProfiles.locations.MAP_ROUTE101.cells)),[[32,80]]);
 const seasonalMethods=data.maps.flatMap(m=>m.methods.filter(x=>x.seasonalVariants?.length).map(x=>[m.id.replace('MAP_ROUTE',''),x.id]));
 for(const [route,method] of seasonalMethods){
  const u=boot('dex.js',data);await settle();u.get('method').listeners.change({target:{value:method}});u.get('search').value='Route '+route;u.get('search').listeners.input();
  assert.equal(u.get('seasonal-preview-note').hidden,data.seasonalStatus!=='preview');
  const m=data.maps.find(m=>m.id==='MAP_ROUTE'+route).methods.find(m=>m.id===method);
  const resident=m.seasonalVariants[0].entries.filter(e=>m.seasonalVariants.every(v=>v.entries.some(x=>x.id===e.id)));
  for(const season of ['spring','summer','autumn','winter']){
   u.get('season').listeners.change({target:{value:season}});
   const h=u.get('results').innerHTML,v=m.seasonalVariants.find(v=>v.season===season).entries;
   assert.equal((h.match(/class="encounter"/g)||[]).length,v.length);
   assert.equal((h.match(/season--all/g)||[]).length,resident.length);
   assert.equal((h.match(new RegExp('season--'+season,'g'))||[]).length,2);
   assert.equal((h.match(/time--all-day/g)||[]).length,v.length);
   for(const e of v)assert(h.includes('data-species="'+e.id+'"'),route+' '+season+' '+e.id);
   assert.equal([...h.matchAll(/class="rate">(\d+)%/g)].reduce((n,x)=>n+Number(x[1]),0),100);
  }
 }
 // All Seasons is a union, preserving each tuple's own rate and availability.
 for(const [route,method] of seasonalMethods){
  const u=boot('dex.js',data,'https://example.test/wiki/dex.html?season=all');await settle();
  assert.equal(u.get('season').value,'all');u.get('method').listeners.change({target:{value:method}});u.get('search').value='Route '+route;u.get('search').listeners.input();
  const m=data.maps.find(m=>m.id==='MAP_ROUTE'+route).methods.find(m=>m.id===method),expected=new Map();
  for(const v of m.seasonalVariants)for(const e of v.entries)expected.set([e.id,e.min,e.max,e.rate,e.time||'all-day'].join(':'),e);
  const rows=u.get('results').innerHTML.split('<div class="encounter">').slice(1);
  assert.equal(rows.length,expected.size,route+' union count');assert.match(u.get('results').innerHTML,/Shares apply in the seasons shown/);
  for(const e of expected.values()){
   const row=rows.find(row=>row.includes('data-species="'+e.id+'"')&&row.includes('class="rate">'+e.rate+'%'));
   assert(row,route+' all '+e.id);assert(row.includes('time--'+(e.time||'all-day')));
   if(e.seasons.length===4)assert(row.includes('season--all'));
   else assert(row.includes(e.seasons.map(x=>x[0].toUpperCase()+x.slice(1)).join(' / ')));
  }
  u.get('season').listeners.change({target:{value:'winter'}});assert.equal(u.ctx.location.search.includes('season=winter'),true);
  u.get('season').listeners.change({target:{value:'all'}});assert.equal(u.ctx.location.search.includes('season=all'),true);
  assert.equal(u.get('results').innerHTML.split('<div class="encounter">').length-1,expected.size);
 }
 // Different levels/rates/times for one species stay separate, with variant-derived badges.
 const fixture={...data,species:data.species.filter(p=>['BULBASAUR','PIKACHU'].includes(p.id)),maps:[{id:'MAP_ROUTE101',name:'Route 101',region:'Hoenn',methods:[{id:'land',label:'Land / grass',entries:[{id:'PIKACHU',min:4,max:4,rate:100}],seasonalVariants:[{season:'spring',entries:[{id:'BULBASAUR',min:2,max:2,rate:30,time:'nighttime'}]},{season:'summer',entries:[{id:'BULBASAUR',min:3,max:3,rate:10,time:'daytime'}]},{season:'autumn',entries:[{id:'BULBASAUR',min:2,max:2,rate:30,time:'nighttime'}]},{season:'winter',entries:[{id:'BULBASAUR',min:2,max:2,rate:30,time:'nighttime'}]}]}]}]};
 // Importer metadata describes species-wide availability, even when its tuples differ.
 for(const variant of fixture.maps[0].methods[0].seasonalVariants)for(const entry of variant.entries)entry.seasons=['spring','summer','autumn','winter'];
 const original=JSON.stringify(fixture),u=boot('dex.js',fixture,'https://example.test/wiki/dex.html?season=all');await settle();
 const html=u.get('results').innerHTML;assert.equal(html.split('<div class="encounter">').length-1,2);assert(!html.includes('data-species="PIKACHU"'));
 assert.match(html,/Spring \/ Autumn \/ Winter/);assert.match(html,/season--summer/);assert.match(html,/time--nighttime/);assert.match(html,/time--daytime/);
 assert.match(html,/Lv. 2/);assert.match(html,/Lv. 3/);assert.match(html,/class="rate">30%/);assert.match(html,/class="rate">10%/);assert(!html.includes('class="rate">40%'));
 u.click('species','BULBASAUR');assert.equal((u.get('detail-content').innerHTML.match(/class="location-row"/g)||[]).length,2);assert.equal(JSON.stringify(fixture),original);
 const fallback=JSON.parse(original);fallback.maps[0].methods[0].seasonalVariants=[];
 const empty=boot('dex.js',fallback,'https://example.test/wiki/dex.html?season=all');await settle();assert.match(empty.get('results').innerHTML,/data-species="PIKACHU"/);empty.click('species','PIKACHU');assert.match(empty.get('detail-content').innerHTML,/class="location-row"/);
 const invalid=boot('dex.js',data,'https://example.test/wiki/dex.html?season=invalid');await settle();assert.equal(invalid.get('season').value,'autumn');
 assert.match(dexHTML,/<option value="all">All Seasons<\/option>/);assert.match(dexHTML,/dex\.js\?v=legendsdex-1\.4\.0/);
 console.log('PASS: '+seasonalMethods.length*4+' individual-season views and '+seasonalMethods.length+' All Seasons unions, exact shares/badges, URL round trips, tuple identity, fallbacks and no source mutation');
 const d=boot('dex.js',data);await settle();assert.equal(d.sounds.length,0,'audio must not preload all cries');
 assert.match(d.get('results').innerHTML,/data-cry=/);assert.match(d.get('results').innerHTML,/class="pokemon-link"/);
 const species=boot('dex.js',data,'https://example.test/wiki/dex.html?view=species');await settle();assert.match(species.get('results').innerHTML,/<div class="dex-card">/);assert.match(species.get('results').innerHTML,/<button type="button" class="pokemon-link" data-species="BULBASAUR"/);
 assert.equal((species.get('results').innerHTML.match(/class="dex-card"/g)||[]).length,data.species.length);assert(species.get('more').hidden);
 d.click('cry','BULBASAUR');await settle();assert(d.sounds[0].url.endsWith('/cries/bulbasaur.wav'));assert(d.sounds[0].played);assert(!d.get('detail').open);
 d.click('cry','DA_BUG');await settle();assert(d.sounds[0].paused);assert(d.sounds[1].url.endsWith('/cries/da_bug.wav'));
 d.click('species','BULBASAUR');assert(d.get('detail').open);assert.match(d.get('detail-content').innerHTML,/Play Bulbasaur cry/);
 d.get('detail').close();assert(d.sounds[1].paused);
 d.ctx.document.hidden=true;d.listeners.visibilitychange();
 console.log('PASS: topic home, category/article deep links, Back navigation, full index, search, lazy cries, exclusive playback, sprite/detail separation, dialog audio cleanup');
})().catch(e=>{console.error(e);process.exit(1);});
