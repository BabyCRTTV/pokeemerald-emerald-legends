"use strict";
(() => {
  const $ = (s,scope=document)=>scope.querySelector(s);
  const esc = text => String(text??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  let data=null, bySpecies=new Map(), view="routes", region="all", method="all", availability="all", type="all", query="", pokemonMap=new Map();
  const results=$("#results"), more=$("#more"), search=$("#search"), modal=$("#detail");
  const METHODS=["land","surf","rock","old_rod","good_rod","super_rod"];
  function sprite(p,size="small"){
    const image=LegendsSprites.markup(p,size);
    return '<button type="button" class="cry-sprite" data-cry="'+esc(p.id)+'" aria-label="Play '+esc(p.name)+' cry" title="Play '+esc(p.name)+' cry">'+image+'</button>';
  }
  function prettyLevel(a,b){return a===b?"Lv. "+a:"Lv. "+a+"–"+b}
  function chips(p){return '<div class="types">'+(p.types||[]).map(x=>'<span class="type type--'+x.toLowerCase()+'">'+esc(x.toLowerCase())+'</span>').join("")+'</div>'}
  function speciesListRows(){
    let visible=data.species.filter(p=>{
      let hitsQuery=!query||p.name.toLowerCase().includes(query)||String(p.num??"").padStart(4,"0").includes(query)||p.id.toLowerCase().replaceAll("_"," ").includes(query);
      let matched=(pokemonMap.get(p.id)||[]).filter(loc=>region==="all"||loc.region===region);
      let hasAny=(pokemonMap.get(p.id)||[]).length>0;
      return hitsQuery&& (type==="all"||p.types.includes(type)) && (availability==="all"||(availability==="wild"&&matched.length>0)||(availability==="unknown"&&!hasAny)) && (region==="all"||matched.length>0||availability==="unknown");
    });
    return visible;
  }
  function filteredRoutes(){
    return data.maps.map(map=>{
      if(region!=="all"&&map.region!==region)return null;
      const mapMatch=map.name.toLowerCase().includes(query)||map.id.toLowerCase().includes(query);
      const methods=map.methods.map(m=>{
        if(method!=="all"&&m.id!==method)return null;
        let entries=m.entries.filter(e=>mapMatch||!query||bySpecies.get(e.id)?.name.toLowerCase().includes(query)||e.id.toLowerCase().replaceAll("_"," ").includes(query));
        return entries.length?{...m,entries}:null;
      }).filter(Boolean);
      return methods.length?{...map,methods}:null;
    }).filter(Boolean);
  }
  function encounterCard(e){
    const p=bySpecies.get(e.id);if(!p)return "";
    return '<div class="encounter">'+sprite(p)+'<button type="button" class="pokemon-link" data-species="'+esc(e.id)+'" aria-label="'+esc(p.name+' '+prettyLevel(e.min,e.max)+' '+e.rate+' percent encounter share')+'"><span class="species-copy"><strong>'+esc(p.name)+'</strong><span class="enc-meta">'+prettyLevel(e.min,e.max)+'</span></span><span class="rate">'+e.rate+'%<small>SPAWN</small></span></button></div>';
  }
  function routeCard(map){
    let count=new Set(map.methods.flatMap(m=>m.entries.map(e=>e.id))).size;
    return '<section class="route-card"><div class="route-head"><div><div class="route-name">'+esc(map.name)+'</div><div class="route-sub">'+count+' Pokémon · '+map.methods.length+' encounter '+(map.methods.length===1?"method":"methods")+'</div></div><span class="region-tag">'+esc(map.region)+'</span></div>'
     +map.methods.map(m=>'<div class="method-section"><div class="method-heading"><span>'+esc(m.label)+'</span>'+m.entries.length+' species <small>· Relative encounter share</small></div><div class="enc-grid">'+m.entries.map(encounterCard).join('')+'</div></div>').join('')+'</section>';
  }
  function dexCard(p){
    const n=(pokemonMap.get(p.id)||[]).length;
    return '<div class="dex-card">'+sprite(p)+'<button type="button" class="pokemon-link" data-species="'+esc(p.id)+'"><span><span class="dex-num">'+(p.num?"#"+String(p.num).padStart(4,"0"):"Special form")+'</span><strong>'+esc(p.name)+'</strong><span class="dex-sub">'+(n?n+" wild location"+(n===1?"":"s"):"No listed wild location")+'</span>'+chips(p)+'</span></button></div>';
  }
  function updateControls(){
    document.querySelectorAll("[data-view]").forEach(b=>{let active=b.dataset.view===view;b.classList.toggle("selected",active);b.setAttribute("aria-selected",String(active))});
    document.querySelectorAll("[data-mobileview]").forEach(b=>b.classList.toggle("active",b.dataset.mobileview===view));
    $("#method-box").hidden=view!=="routes";$("#availability-box").hidden=view!=="species";$("#type-box").hidden=view!=="species";
    document.querySelectorAll("[data-region]").forEach(b=>{let active=b.dataset.region===region;b.classList.toggle("active",active);b.setAttribute("aria-pressed",String(active))});
    search.placeholder=view==="routes"?"Search a route or Pokémon…":"Search a Pokémon or Dex number…";
    $("#clear-search").hidden=!search.value;
  }
  function render(){
    if(!data)return;
    updateControls();
    let collection=view==="routes"?filteredRoutes():speciesListRows(),total=collection.length;

    $("#results-heading").textContent=view==="routes"?"Wild encounters":"National Pokédex";
    $("#results-count").textContent=view==="routes"?total+" locations with matching encounters":total+" Pokémon matching your filters";
    results.className=view==="routes"?"":"dex-grid";
    if(total===0){
      results.innerHTML='<div class="empty"><strong>No matches found</strong><p>Try another Pokémon, region, or encounter method.</p></div>';
    }else results.innerHTML=collection.map(x=>view==="routes"?routeCard(x):dexCard(x)).join("");
    LegendsSprites.hydrate(results,data.sourceCommit);
    more.hidden=true;
  }
  function changeView(next){
    const position=window.scrollY;
    if(next!==view){view=next;query="";search.value="";const url=new URL(location.href);url.searchParams.set("view",next);url.searchParams.delete("pokemon");history.replaceState(null,"",url);document.title=(view==="routes"?"Wild encounters":"National Pokédex")+" · Emerald: Legends Wiki";render();}
    window.scrollTo({top:position,behavior:"instant"});
    updateReturnArrow();
  }
  const searchAnchor=$("#search-anchor"), returnArrow=$("#return-to-search");
  const flightDuration=1100, flightCooldown=1000;
  let arrowActive=false, flying=false, cooldownUntil=0, flightTimer=null, revealTimer=null;
  function setArrowVisible(visible){
    arrowActive=visible;
    returnArrow.classList.toggle("is-visible",visible);
    returnArrow.disabled=!visible;
    returnArrow.setAttribute("aria-hidden",String(!visible));
  }
  function flyAway(){
    setArrowVisible(false);
    cooldownUntil=Date.now()+flightDuration+flightCooldown;
    const reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if(!reduce){
      flying=true;returnArrow.classList.add("is-flying");
      flightTimer=setTimeout(()=>{
        flying=false;returnArrow.classList.remove("is-flying");flightTimer=null;
        updateReturnArrow();
      },flightDuration);
    }
    clearTimeout(revealTimer);
    revealTimer=setTimeout(()=>{revealTimer=null;updateReturnArrow();},flightDuration+flightCooldown);
  }
  function updateReturnArrow(){
    const anchorTop=searchAnchor.getBoundingClientRect().top;
    // A little hysteresis prevents tiny movements around the anchor from retriggering.
    const below=anchorTop < (arrowActive?-8:-40);
    if(!below && arrowActive && !flying){flyAway();return;}
    if(flying || Date.now()<cooldownUntil){setArrowVisible(false);return;}
    setArrowVisible(below);
  }
  window.addEventListener("scroll",updateReturnArrow,{passive:true});
  window.addEventListener("resize",updateReturnArrow);
  returnArrow.addEventListener("click",()=>{
    const top=Math.max(0,window.scrollY+searchAnchor.getBoundingClientRect().top-12);
    const reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    window.scrollTo({top,behavior:reduce?"instant":"smooth"});
    searchAnchor.focus({preventScroll:true});
  });
  updateReturnArrow();
  function openPokemon(id,share=true){
    const p=bySpecies.get(id);if(!p)return;
    const linked=(pokemonMap.get(id)||[]).filter(loc=>(region==="all"||loc.region===region));
    const all=pokemonMap.get(id)||[];
    let selected=[...(linked.length?linked:all)];
    selected.sort((a,b)=>a.region.localeCompare(b.region)||a.map.localeCompare(b.map));
    const stats=p.stats?.length===6&&p.stats.every(x=>Number.isFinite(x))?
      '<h3>Base stats</h3><div class="stat-table">'+["HP","Attack","Defense","Sp. Atk","Sp. Def","Speed"].map((name,i)=>'<span>'+name+'</span><div class="stat-track"><i style="width:'+Math.max(1,Math.min(100,p.stats[i]/2.55))+'%"></i></div><span>'+p.stats[i]+'</span>').join("")+'</div>':"";
    const links=selected.length?selected.map(loc=>'<div class="location-row"><div><strong>'+esc(loc.map)+'</strong><small>'+esc(loc.region)+' · '+esc(loc.label)+' · '+prettyLevel(loc.min,loc.max)+'</small></div><span class="rate">'+loc.rate+'%<small>SPAWN</small></span></div>').join(""):'<p>No standard wild encounter is listed in the currently indexed and accessible route tables. It might be obtainable through other methods, or not yet obtainable. This does not establish that the Pokémon is unavailable everywhere.</p>';
    $("#detail-content").innerHTML='<div class="detail-top">'+sprite(p,"large")+'<div><span class="detail-meta">'+(p.num?"NATIONAL #"+String(p.num).padStart(4,"0"):"SPECIAL FORM")+'</span><h2>'+esc(p.name)+'</h2><p style="margin:0;font-size:12px;color:#837399">'+esc(p.category||"Pokémon")+' Pokémon</p>'+chips(p)+'</div></div><div class="detail-content">'+stats+'<h3>Where to find '+esc(p.name)+'</h3><p style="font-size:12px;color:#7c708b;margin-top:0">Wild encounter tables only. Rates are conditional on the chosen method.</p>'+links+'</div>';
    LegendsSprites.hydrate($("#detail-content"),data.sourceCommit);
    if(!modal.open)modal.showModal();$("#close-detail").focus();
    if(share){const url=new URL(location.href);url.searchParams.set("pokemon",id.toLowerCase());history.replaceState(null,"",url);}
  }
  function closePokemon(){
    modal.close();if(new URL(location.href).searchParams.has("pokemon")){let url=new URL(location.href);url.searchParams.delete("pokemon");history.replaceState(null,"",url);}
  }
  function generateMapIndex(){
    bySpecies=new Map(data.species.map(p=>[p.id,p]));pokemonMap=new Map();
    for(const m of data.maps)for(const method of m.methods)for(const e of method.entries){
      if(!pokemonMap.has(e.id))pokemonMap.set(e.id,[]);
      pokemonMap.get(e.id).push({map:m.name,region:m.region,method:method.id,label:method.label,min:e.min,max:e.max,rate:e.rate,mapId:m.id});
    }
    const validTypes=new Set(["NORMAL","FIRE","WATER","GRASS","ELECTRIC","ICE","FIGHTING","POISON","GROUND","FLYING","PSYCHIC","BUG","ROCK","GHOST","DRAGON","DARK","STEEL","FAIRY"]);
    const types=[...new Set(data.species.flatMap(x=>x.types||[]))].filter(x=>validTypes.has(x)).sort();
    $("#type").innerHTML='<option value="all">Any type</option>'+types.map(x=>'<option value="'+esc(x)+'">'+esc(x[0]+x.slice(1).toLowerCase())+'</option>').join("");
    $("#version-meta").textContent="Game v"+data.gameVersion+" · "+data.maps.length+" locations";
  }
  document.addEventListener("error",event=>{if(event.target instanceof HTMLImageElement && event.target.closest(".thumb")){event.target.closest(".thumb").classList.add("fallback-only")}},true);
  let cryAudio=null,cryToken=0;
  function stopCry(){cryToken++;if(cryAudio){cryAudio.pause();cryAudio=null;}document.querySelectorAll('.cry-sprite.playing').forEach(b=>b.classList.remove('playing'));}
  async function playCry(id,button){
    if(!bySpecies.has(id))return;
    stopCry();const token=cryToken;
    const stem=id.toLowerCase()+(window.LegendsCryForms[id]?'_'+window.LegendsCryForms[id]:'');
    const audio=new Audio('https://raw.githubusercontent.com/BabyCRTTV/pokeemerald-emerald-legends/'+data.sourceCommit+'/sound/direct_sound_samples/cries/'+stem+'.wav');cryAudio=audio;audio.preload='none';
    button.classList.add('playing');$('#cry-status').textContent='';
    audio.addEventListener('ended',()=>{if(token===cryToken)stopCry();},{once:true});
    try{await audio.play();if(token===cryToken)$('#cry-status').textContent='Playing '+bySpecies.get(id).name+'’s cry.';}
    catch{if(token===cryToken){stopCry();$('#cry-status').textContent='Could not play this cry. Check your connection and tap the sprite to try again.';}}
  }
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stopCry();});
  modal.addEventListener('close',stopCry);
  document.addEventListener("click",event=>{const cry=event.target.closest('[data-cry]');if(cry){playCry(cry.dataset.cry,cry);return;}const s=event.target.closest("[data-species]");if(s)openPokemon(s.dataset.species);});
  document.querySelectorAll("[data-view]").forEach(b=>b.addEventListener("click",()=>changeView(b.dataset.view)));
  document.querySelectorAll("[data-mobileview]").forEach(b=>b.addEventListener("click",()=>changeView(b.dataset.mobileview)));
  document.querySelectorAll("[data-region]").forEach(b=>b.addEventListener("click",()=>{region=b.dataset.region;render()}));
  search.addEventListener("input",()=>{query=search.value.trim().toLowerCase();render()});
  $("#clear-search").addEventListener("click",()=>{search.value="";query="";render();search.focus()});
  $("#method").addEventListener("change",e=>{method=e.target.value;render()});
  $("#availability").addEventListener("change",e=>{availability=e.target.value;render()});
  $("#type").addEventListener("change",e=>{type=e.target.value;render()});
  $("#about-rates").addEventListener("click",()=>$("#help").showModal());
  $("#close-help").addEventListener("click",()=>$("#help").close());
  $("#close-detail").addEventListener("click",closePokemon);
  modal.addEventListener("click",e=>{if(e.target===modal)closePokemon()});
  modal.addEventListener("close",()=>{let u=new URL(location.href);if(u.searchParams.has("pokemon")){u.searchParams.delete("pokemon");history.replaceState(null,"",u);}});
  $("#help").addEventListener("click",e=>{if(e.target===$("#help"))$("#help").close()});
  fetch("dex-data.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("HTTP "+r.status);return r.json()}).then(async json=>{
    if(!Array.isArray(json.maps)||!Array.isArray(json.species)||json.maps.length===0)throw Error("Invalid Pokédex data");
    data=json;generateMapIndex();
    await LegendsSprites.preload(data.sourceCommit);
    const link=new URL(location.href),pokemon=link.searchParams.get("pokemon")?.toUpperCase(),map=link.searchParams.get("map");
    if(link.searchParams.get("view")==="species")view="species";
    if(link.searchParams.get("view")==="routes")view="routes";
    if(map){query="";region="all";method="all";}
    if(pokemon&&bySpecies.has(pokemon))view="species";
    render();
    if(pokemon&&bySpecies.has(pokemon))openPokemon(pokemon,false);
  }).catch(err=>{
    results.innerHTML='<div class="empty"><strong>Could not load the field guide</strong><p>Connect to the internet and refresh to load the current documented encounters. No account is needed.</p><button class="more" type="button" onclick="location.reload()">Try again</button></div>';
    $("#results-count").textContent="Data temporarily unavailable";more.hidden=true;
    console.error("Dex data error",err);
  });
})();