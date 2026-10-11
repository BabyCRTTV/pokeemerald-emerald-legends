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
 w.back();assert.match(w.get('content').innerHTML,/Your Legends guide/);
 w.get('search').value='boots';w.get('search').listeners.input();assert.match(w.get('cards').innerHTML,/wardrobe/);
 w.click('category','all');assert.equal((w.get('content').innerHTML.match(/data-page=/g)||[]).length,articles.articles.length);
 const chapters=articles.articles.filter(p=>Number.isInteger(p.chapter)).sort((a,b)=>a.chapter-b.chapter);
 assert(chapters.every(p=>!p.content.includes('## Your goal')&&!p.content.includes('First time playing?')));
 assert.deepEqual(chapters.map(p=>p.chapter),Array.from({length:14},(_,i)=>i+1));
 w.click('page',chapters[0].id);assert.match(w.get('content').innerHTML,/Next chapter/);assert(!w.get('content').innerHTML.includes('Previous chapter'));
 w.click('page',chapters[13].id);assert.match(w.get('content').innerHTML,/Previous chapter/);assert(!w.get('content').innerHTML.includes('Next chapter'));
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
 const atlas={window:{}};vm.runInNewContext(fs.readFileSync(base+'dex-sprite-atlas.js','utf8'),atlas);
 assert.equal(atlas.window.LegendsSpriteAtlas.sourceCommit,data.sourceCommit);
 for(const p of data.species)assert(atlas.window.LegendsSpriteAtlas.icons[p.sprite],p.id+' missing from preloaded atlas');
 const profiles={window:{}};vm.runInNewContext(fs.readFileSync(base+'dex-profiles.js','utf8'),profiles);
 assert.equal(profiles.window.LegendsProfiles.sourceCommit,data.sourceCommit);
 for(const p of data.species)assert(profiles.window.LegendsProfiles.entries[p.id],p.id+' missing entry');
 for(const m of data.maps){const loc=profiles.window.LegendsProfiles.locations[m.id];assert.equal(loc.region,m.region);assert(loc.cells.length,m.id+' missing map marker');for(const [x,y] of loc.cells)assert(x>=0&&x<224&&y>=0&&y<120);}
 assert.deepEqual(JSON.parse(JSON.stringify(profiles.window.LegendsProfiles.locations.MAP_ROUTE101.cells)),[[32,80]]);
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
