"use strict";
const {app, BrowserWindow, shell, dialog, Menu} = require("electron");
const path = require("node:path");
const {URL} = require("node:url");

const HOME = "https://babycrttv.github.io/pokeemerald-emerald-legends/wiki/dex.html";
const HOME_ORIGIN = "https://babycrttv.github.io";
const WIKI_PREFIX = "/pokeemerald-emerald-legends/wiki/";
let mainWindow = null;

function internalLink(value) {
  try {
    const url = new URL(value);
    return url.protocol === "https:" && url.origin === HOME_ORIGIN &&
      (url.pathname === WIKI_PREFIX.slice(0,-1) || url.pathname.startsWith(WIKI_PREFIX));
  } catch { return false; }
}
function externalLink(value) {
  try {
    const url = new URL(value);
    if (!["https:","http:"].includes(url.protocol)) return;
    shell.openExternal(url.toString()).catch(() => {
      dialog.showMessageBox({type:"warning",message:"No browser is available to open that link."});
    });
  } catch { /* Discard unsafe destinations. */ }
}
function createWindow() {
  const win = new BrowserWindow({
    title:"Legends Wiki",width:1080,height:760,minWidth:385,minHeight:480,
    show:false,backgroundColor:"#f8f5ff",autoHideMenuBar:true,
    icon:path.join(__dirname,"assets","happiny.ico"),
    webPreferences:{nodeIntegration:false,contextIsolation:true,sandbox:true,
      webSecurity:true,devTools:false}
  });
  mainWindow=win;
  win.once("ready-to-show",()=>win.show());
  win.webContents.setUserAgent(
    win.webContents.getUserAgent()+" LegendsWikiWindows/"+app.getVersion());
  win.webContents.setWindowOpenHandler(({url})=>{
    externalLink(url);return {action:"deny"};
  });
  win.webContents.on("will-navigate",(event,url)=>{
    if (!internalLink(url)) {
      event.preventDefault();externalLink(url);
    }
  });
  win.webContents.on("did-fail-load",(_event,errorCode,_message,_url,isMainFrame)=>{
    if(!isMainFrame||errorCode===-3)return;
    dialog.showMessageBox(win,{
      type:"warning",title:"Wiki connection unavailable",
      message:"The Legends Wiki couldn't be loaded.",
      detail:"Check your internet connection. No login is needed, and no data was changed.",
      buttons:["Retry","Close"],defaultId:0
    }).then(({response})=>{
      if(response===0&&!win.isDestroyed())win.loadURL(HOME);
    });
  });
  win.loadURL(HOME);
  win.on("closed",()=>{if(mainWindow===win)mainWindow=null;});
}
app.whenReady().then(()=>{
  Menu.setApplicationMenu(null);createWindow();
  app.on("activate",()=>{if(BrowserWindow.getAllWindows().length===0)createWindow();});
});
app.on("window-all-closed",()=>{if(process.platform!=="darwin")app.quit();});
