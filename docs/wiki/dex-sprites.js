/* All documented Pokémon share one preloaded transparent icon atlas. */
"use strict";
window.LegendsSprites = (() => {
  const atlas=window.LegendsSpriteAtlas;
  let pending=null,ready=false,portraitsReady=false;
  function preload(commit){
    if(!atlas || atlas.sourceCommit!==commit)return Promise.resolve();
    if(pending)return pending;
    const urls=[atlas.url,'dex-portraits.webp','dex-portraits-shiny.webp'];
    pending=Promise.all(urls.map(url=>new Promise(resolve=>{
      const image=new Image();
      image.onload=async()=>{
        try{if(image.decode)await image.decode();resolve(true);}
        catch{resolve(false);}
      };
      image.onerror=()=>resolve(false);
      image.src=url;
    }))).then(loaded=>{ready=loaded[0];portraitsReady=loaded[1]&&loaded[2];});
    return pending;
  }
  function markup(p,size="small"){
    const id=/^[a-z0-9_]+$/.test(p.sprite||"")?p.sprite:p.id.toLowerCase();
    const position=ready&&atlas.icons[id];
    const art=position?'<span class="sprite-art" aria-hidden="true" style="--sprite-x:'+(-position[0])+';--sprite-y:'+(-position[1])+';--atlas-columns:'+atlas.columns+';--atlas-rows:'+atlas.rows+'"></span>':'';
    return '<span class="thumb'+(size==="large"?' thumb-large':'')+(position?' sprite-ready':' fallback-only')+(size==='large'&&portraitsReady?' portrait-ready':'')+'"><span class="missing-icon" aria-hidden="true">◉</span>'+art+'</span>';
  }
  // Kept for shared profile/reader callers; markup is immediately ready after preload.
  function hydrate(){}
  return {markup,hydrate,preload,portraitsAvailable:()=>portraitsReady};
})();
