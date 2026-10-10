/* Pokémon Emerald icon.png: two opaque 32x32 frames stacked into one 32x64 file.
 * Extract the FIRST frame, flood-clear its exterior background, and center it.
 * A lazy, per-species cache avoids processing every image on each search.
 */
"use strict";
window.LegendsSprites = (() => {
  const cached = new Map();
  const observer = typeof IntersectionObserver === "function"
    ? new IntersectionObserver(entries => {
        for (const entry of entries) if (entry.isIntersecting) {
          observer.unobserve(entry.target);
          load(entry.target);
        }
      }, {rootMargin:"180px"})
    : null;

  function markup(p, size="small") {
    const id = /^[a-z0-9_]+$/.test(p.sprite || "") ? p.sprite : p.id.toLowerCase();
    return '<span class="thumb'+(size==="large"?" thumb-large":"")+'">'+
      '<span class="missing-icon" aria-hidden="true">✦</span>'+
      '<img alt="" data-icon="'+id+'" decoding="async"></span>';
  }

  function extract(source) {
    const side = Math.min(source.naturalWidth, source.naturalHeight);
    if (!side || side > 256) throw new Error("Unexpected icon dimensions");
    const frame = document.createElement("canvas");
    frame.width = frame.height = side;
    const ctx = frame.getContext("2d", {willReadFrequently:true});
    if (!ctx) throw new Error("Canvas is unavailable");
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(source, 0, 0, side, side, 0, 0, side, side);
    const image = ctx.getImageData(0, 0, side, side);
    const px = image.data;
    const bg = [px[0], px[1], px[2], px[3]];
    const seen = new Uint8Array(side*side);
    const stack = [];

    function enqueue(x,y) {
      if (x < 0 || y < 0 || x >= side || y >= side) return;
      const i = y*side + x;
      if (seen[i]) return;
      seen[i] = 1;
      const j = 4*i;
      if (px[j+3] === 0 ||
         (px[j] === bg[0] && px[j+1] === bg[1] &&
          px[j+2] === bg[2] && px[j+3] === bg[3])) stack.push(i);
    }

    // Only exterior-connected pixels are cleared: interior colors survive.
    for (let x=0;x<side;x++) { enqueue(x,0); enqueue(x,side-1); }
    for (let y=0;y<side;y++) { enqueue(0,y); enqueue(side-1,y); }
    while (stack.length) {
      const i=stack.pop(),x=i%side,y=Math.floor(i/side);
      px[4*i+3]=0;
      enqueue(x+1,y); enqueue(x-1,y);
      enqueue(x,y+1); enqueue(x,y-1);
    }
    ctx.putImageData(image,0,0);

    // Recenter the silhouette inside a transparent square.
    let left=side,top=side,right=-1,bottom=-1;
    for (let y=0;y<side;y++) for (let x=0;x<side;x++) {
      if (!px[4*(y*side+x)+3]) continue;
      left=Math.min(left,x);top=Math.min(top,y);
      right=Math.max(right,x);bottom=Math.max(bottom,y);
    }
    if (right < left) throw new Error("Empty Pokémon icon");
    const w=right-left+1,h=bottom-top+1;
    const output=document.createElement("canvas");
    output.width=output.height=side;
    const dest=output.getContext("2d");
    if (!dest) throw new Error("Canvas is unavailable");
    dest.imageSmoothingEnabled=false;
    dest.drawImage(frame,left,top,w,h,
      Math.floor((side-w)/2),Math.floor((side-h)/2),w,h);
    return output.toDataURL("image/png");
  }

  function cleanedUrl(icon,commit) {
    const key=commit+"/"+icon;
    if (cached.has(key)) return cached.get(key);
    const pending=new Promise(resolve=>{
      const source=new Image();
      source.crossOrigin="anonymous";
      source.onload=()=> {
        try { resolve(extract(source)); }
        catch (error) {
          console.warn("Icon processing failed:",icon,error);
          resolve(null);
        }
      };
      source.onerror=()=>resolve(null);
      source.src="https://raw.githubusercontent.com/BabyCRTTV/pokeemerald-emerald-legends/"
        +commit+"/graphics/pokemon/"+icon+"/icon.png";
    });
    cached.set(key,pending);
    return pending;
  }

  function load(img) {
    const icon=img.dataset.icon,commit=img.dataset.sourceCommit;
    if (!icon || !commit) return;
    cleanedUrl(icon,commit).then(url=>{
      if (!img.isConnected || img.dataset.icon!==icon) return;
      const thumb=img.closest(".thumb");
      if (url) {
        img.src=url;
        if (thumb) thumb.classList.add("sprite-ready");
      } else if (thumb) {
        thumb.classList.add("fallback-only");
      }
    });
  }

  function hydrate(scope,commit) {
    scope.querySelectorAll("img[data-icon]").forEach(img=>{
      img.dataset.sourceCommit=commit;
      if (observer) observer.observe(img);
      else load(img);
    });
  }
  return {markup,hydrate};
})();
