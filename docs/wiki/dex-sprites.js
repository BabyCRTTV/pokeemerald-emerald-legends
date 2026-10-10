/* All documented Pokémon share one preloaded transparent icon atlas. */
"use strict";
window.LegendsSprites = (() => {
  const atlas=window.LegendsSpriteAtlas;
  let pending=null,ready=false;
  function preload(commit){
    if(!atlas || atlas.sourceCommit!==commit)return Promise.resolve();
    if(pending)return pending;
    pending=new Promise(resolve=>{
      const image=new Image();
      image.onload=async()=>{
        try{if(image.decode)await image.decode();ready=true;}
        catch{ready=false;}
        resolve();
      };
      image.onerror=()=>resolve();
      image.src=atlas.url;
    });
    return pending;
  }
  function markup(p,size="small"){
    const id=/^[a-z0-9_]+$/.test(p.sprite||"")?p.sprite:p.id.toLowerCase();
    const position=ready&&atlas.icons[id];
    const art=position?'<span class="sprite-art" aria-hidden="true" style="--sprite-x:'+(-position[0])+';--sprite-y:'+(-position[1])+';--atlas-columns:'+atlas.columns+';--atlas-rows:'+atlas.rows+'"></span>':'';
    return '<span class="thumb'+(size==="large"?' thumb-large':'')+(position?' sprite-ready':' fallback-only')+'"><span class="missing-icon" aria-hidden="true">◉</span>'+art+'</span>';
  }
  // Kept for shared profile/reader callers; markup is immediately ready after preload.
  function hydrate(){}
  return {markup,hydrate,preload};
})();
