"use strict";
(() => {
  const button=document.getElementById("update-wiki");
  const dialog=document.getElementById("wiki-update-dialog");
  const heading=document.getElementById("update-heading");
  const status=document.getElementById("update-status");
  const actions=document.getElementById("update-actions");
  const warning=document.getElementById("update-warning");
  if(!button||!dialog||!heading||!status||!actions||!warning)return;

  const BASE="https://babycrttv.github.io/pokeemerald-emerald-legends/wiki/";
  const ua=navigator.userAgent||"";
  const android=ua.match(/LegendsWikiAndroid\/(\d+)/);
  const windows=ua.match(/LegendsWikiWindows\/([\d.]+)/);
  const installed=android?{platform:"android",version:Number(android[1])}:
                  windows?{platform:"windows",version:windows[1]}:null;
  const labels={android:"Android APK",windows:"Windows installer"};
  let requestSequence=0;

  function clear() {
    requestSequence++;
    actions.replaceChildren();
    warning.hidden=true;
    warning.textContent="";
  }
  function makeButton(label,handler,kind="secondary"){
    const b=document.createElement("button");
    b.type="button";b.textContent=label;b.className=kind;
    b.addEventListener("click",handler);return b;
  }
  function downloadLink(url,label) {
    const a=document.createElement("a");
    // The published app manifests are the only sources of download locations.
    const destination=new URL(url,location.href);
    if(destination.protocol!=="https:")throw new Error("Invalid installer address");
    a.href=destination.href;a.textContent=label;a.className="primary";
    a.rel="noopener noreferrer";
    // Companion apps open the download in the system browser.
    a.target=installed?"_self":"_blank";
    return a;
  }
  function compareVersions(a,b){
    const left=String(a).split(".").map(Number),right=String(b).split(".").map(Number);
    for(let i=0;i<Math.max(left.length,right.length);i++){
      const difference=(left[i]||0)-(right[i]||0);
      if(difference)return Math.sign(difference);
    }
    return 0;
  }
  function choose() {
    clear();
    heading.textContent="Install Legends Wiki";
    status.textContent="Choose your device. Already installed? We'll check whether there's a newer version before offering a download.";
    actions.append(
      makeButton("↓ Android APK",()=>check("android"),"primary"),
      makeButton("↓ Windows EXE",()=>check("windows"),"primary"),
      makeButton("Close",()=>dialog.close())
    );
  }
  async function check(platform) {
    clear();
    const sequence=requestSequence;
    heading.textContent=labels[platform];
    status.textContent="Checking the latest "+labels[platform]+"…";
    try {
      const response=await fetch(BASE+platform+"-version.json?check="+Date.now(),{cache:"no-store"});
      if(!response.ok)throw new Error("Latest version information is unavailable");
      const release=await response.json();
      if(!release.available||!release.version||!release.url)
        throw new Error("The installer isn't available yet");
      if(sequence!==requestSequence||!dialog.open)return;
      const currentInstall=installed?.platform===platform?installed.version:null;
      const upToDate=currentInstall!==null&&(platform==="android"
        ? Number(currentInstall)>=Number(release.versionCode)
        : compareVersions(currentInstall,release.version)>=0);
      if(upToDate) {
        heading.textContent="You're up to date";
        status.textContent="Legends Wiki "+release.version+" is already installed. No update is needed.";
      } else {
        heading.textContent=currentInstall===null?"Install Legends Wiki":"Update available";
        status.textContent=currentInstall===null
          ?"Latest "+labels[platform]+": version "+release.version+". Download the installer to get the companion app. No login is required."
          :"Version "+release.version+" is available. Installed version: "+
           (platform==="android"?"build "+currentInstall:currentInstall)+".";
        actions.append(downloadLink(release.url,currentInstall===null?"↓ Download "+labels[platform]:"↓ Download update"));
        if(platform==="android"&&release.signing==="ephemeral-debug"){
          warning.textContent="Android note: this APK uses a temporary signing certificate. If Android rejects installation over an older copy, you may need to uninstall the old app first.";
          warning.hidden=false;
        } else if(platform==="windows"){
          warning.textContent="Windows may show an unknown-publisher warning because the installer isn't code-signed yet.";
          warning.hidden=false;
        }
      }
    } catch(error) {
      if(sequence!==requestSequence)return;
      status.textContent="Couldn't check the download: "+error.message+". Please try again.";
    }
    actions.append(makeButton("Other devices",choose),makeButton("Close",()=>dialog.close()));
  }
  button.addEventListener("click",()=>{
    if(!dialog.open)dialog.showModal();
    if(installed)check(installed.platform);else choose();
  });
  dialog.addEventListener("close",clear);
  dialog.addEventListener("click",event=>{if(event.target===dialog)dialog.close()});
})();