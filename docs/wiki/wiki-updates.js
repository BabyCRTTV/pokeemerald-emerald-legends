"use strict";
(() => {
  const button=document.getElementById("update-wiki");
  const dialog=document.getElementById("wiki-update-dialog");
  const status=document.getElementById("update-status");
  const actions=document.getElementById("update-actions");
  if(!button||!dialog||!status||!actions)return;
  const BASE="https://babycrttv.github.io/pokeemerald-emerald-legends/";
  const detected=(()=>{
    const android=navigator.userAgent.match(/LegendsWikiAndroid\/(\d+)/);
    if(android)return {platform:"android",version:Number(android[1])};
    const windows=navigator.userAgent.match(/LegendsWikiWindows\/([\d.]+)/);
    if(windows)return {platform:"windows",version:windows[1]};
    return null;
  })();
  const link=(url,label)=>{
    const a=document.createElement("a");
    a.href=url;a.className="primary";a.textContent=label;
    a.rel="noopener noreferrer";a.target="_blank";return a;
  };
  const action=(label,fn)=>{
    const b=document.createElement("button");b.type="button";b.textContent=label;
    b.addEventListener("click",fn);return b;
  };
  const cmp=(left,right)=>{
    const a=String(left).split(".").map(Number),b=String(right).split(".").map(Number);
    for(let i=0;i<Math.max(a.length,b.length);i++){
      const n=(a[i]||0)-(b[i]||0);if(n)return Math.sign(n);
    }return 0;
  };
  async function check(platform){
    status.textContent="Checking the latest "+(platform==="android"?"Android":"Windows")+" Wiki release…";
    actions.replaceChildren();
    try{
      const url=BASE+"wiki/"+(platform==="android"?"android-version.json":"windows-version.json");
      const response=await fetch(url+"?check="+Date.now(),{cache:"no-store"});
      if(!response.ok)throw new Error("Release information unavailable");
      const release=await response.json();
      if(!release.available||!release.version||!release.url)
        throw new Error("The installer has not been published yet");
      const installed=detected?.platform===platform?detected.version:null;
      const current=platform==="android" ? release.versionCode : release.version;
      const upToDate=installed!==null&&(platform==="android"
        ? Number(installed)>=Number(current)
        : cmp(installed,current)>=0);
      if(upToDate){
        status.textContent="You're on the most current "+(platform==="android"?"Android":"Windows")+
          " Wiki app version ("+release.version+"). No update is needed.";
      }else{
        status.textContent=(installed===null
          ? "Latest "+(platform==="android"?"Android":"Windows")+" Wiki app: "+release.version+". This browser cannot determine whether the app is installed."
          : "An update is available: "+release.version+". Your installed version is "+(platform==="android"?"build "+installed:installed)+".")+
          " Installation requires your approval.";
        actions.append(link(release.url,installed===null?"Install / download latest":"Download update"));
        if(platform==="android"&&release.signing==="ephemeral-debug"){
          const note=document.createElement("p");
          note.textContent="Important: this APK uses a temporary debug signing key. Android may require uninstalling an older build before installing this one. Preserve any important app settings.";
          actions.after(note);
        }
      }
    }catch(e){status.textContent="Could not verify the latest installer: "+e.message+". Please try again later.";}
    actions.append(action("Back",choose));
  }
  function choose(){
    status.textContent="Choose your device to check the latest Wiki installer.";
    actions.replaceChildren(action("Android",()=>check("android")),action("Windows",()=>check("windows")),action("Close",()=>dialog.close()));
  }
  button.addEventListener("click",()=>{
    if(!dialog.open)dialog.showModal();
    if(detected)check(detected.platform);else choose();
  });
  dialog.addEventListener("click",e=>{if(e.target===dialog)dialog.close();});
})();