// Real-browser checks of the manually reviewed encounter availability snapshot.
const {chromium}=require(process.env.WIKI_PLAYWRIGHT||process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const assert=require('node:assert/strict'),http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const server=http.createServer((req,res)=>{
 let file=path.join(root,'docs',decodeURIComponent(req.url.split('?')[0]));if(file.endsWith('/'))file+='index.html';
 try{const b=fs.readFileSync(file);const ext=path.extname(file);res.setHeader('Content-Type',({'.json':'application/json','.js':'text/javascript','.css':'text/css','.webp':'image/webp','.png':'image/png','.svg':'image/svg+xml'})[ext]||'text/html');res.end(b)}catch{res.statusCode=404;res.end()}
});
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const url='http://127.0.0.1:'+server.address().port+'/wiki/';
 fs.mkdirSync(path.join(root,'wiki-preview'),{recursive:true});
 const browser=await chromium.launch({headless:true,...(process.env.WIKI_CHROMIUM?{executablePath:process.env.WIKI_CHROMIUM,args:['--no-sandbox','--no-zygote','--single-process','--disable-gpu','--disable-software-rasterizer','--disable-gpu-compositing','--use-gl=disabled','--disable-dev-shm-usage']}:{})});
 const page=await browser.newPage({viewport:{width:412,height:915},deviceScaleFactor:2});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const width of [320,360,412,580,581,619,620,690,768,820,900,960,1024,1280]){
  await page.setViewportSize({width,height:915});
  await page.goto(url+'dex.html?season=autumn');await page.locator('.route-card').first().waitFor();
  const snapshot=JSON.parse(fs.readFileSync(path.join(root,'docs/wiki/dex-data.json')));
  assert.equal(await page.locator('#seasonal-preview-note').isVisible(),snapshot.seasonalStatus==='preview');
  const route=page.locator('#route-MAP_ROUTE101');
  assert.equal(await route.locator('.encounter').count(),5);assert((await route.innerText()).includes('Tarountula'));
  assert.equal(await route.locator('.season--all').count(),3);assert.equal(await route.locator('.season--autumn').count(),2);
  assert.equal(await route.locator('.time--all-day').count(),5);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow '+width);
  for(const season of ['spring','summer','autumn','winter']){
   await page.locator('#season').selectOption(season);assert.equal(await route.locator('.season--'+season).count(),2);
   assert.equal((await route.locator('.rate').allTextContents()).reduce((a,b)=>a+parseInt(b),0),100);
  }
  await page.locator('#search').fill('Route 101');
  await page.locator('#season').selectOption('all');
  assert.equal(await route.locator('.encounter').count(),11);assert.equal(await route.locator('.season--all').count(),3);
  for(const season of ['spring','summer','autumn','winter'])assert.equal(await route.locator('.season--'+season).count(),2);
  assert((await route.innerText()).includes('Shares apply in the seasons shown'));
  assert.equal((await route.locator('.rate').allTextContents()).reduce((a,b)=>a+parseInt(b),0),190,'union retains per-season rates, never an invented 100% total');
  assert(new URL(page.url()).searchParams.get('season')==='all');
  await page.reload();await route.waitFor();assert.equal(await page.locator('#season').inputValue(),'all');
  await page.locator('#search').fill('Route 101');assert.equal(await route.locator('.encounter').count(),11);
  for(const n of [113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134]){
   await page.locator('#search').fill('Route '+n);
   const card=page.locator('#route-MAP_ROUTE'+n);await card.waitFor();
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'All Seasons overflow '+width+' route '+n);
   for(const row of await card.locator('.encounter').all())assert(await row.evaluate(e=>{const a=e.querySelector('.enc-availability').getBoundingClientRect(),n=e.querySelector('.species-copy').getBoundingClientRect(),r=e.querySelector('.rate').getBoundingClientRect();return a.left>=n.right-1&&a.right<=r.left+1;}),'All Seasons badge overlap '+width+' route '+n);
   for(const row of await card.locator('.encounter').all())assert(await row.evaluate(e=>{
    const name=e.querySelector('.species-copy strong'),level=e.querySelector('.enc-meta'),badge=e.querySelector('.availability-badge');
    return name.getBoundingClientRect().height<=parseFloat(getComputedStyle(name).lineHeight)*2+1 &&
     level.getBoundingClientRect().height<=parseFloat(getComputedStyle(level).lineHeight)+1 && badge.scrollWidth<=badge.clientWidth+1;
   }),'readable All Seasons name, level and badge at '+width+' route '+n);
  }
  await page.locator('#season').selectOption('winter');
  await page.locator('#search').fill('Route 104');
  assert.equal(await page.locator('[data-cry="SANDSHREW_ALOLA"] .sprite-ready').count(),1,'Alolan icon');
  await page.locator('[data-species="SANDSHREW_ALOLA"]').click();assert(await page.locator('#detail-content .type--ice').isVisible());assert((await page.locator('#detail-content').innerText()).includes('Winter'));
  await page.locator('#close-detail').click();await page.locator('#season').selectOption('autumn');
  assert.equal(await page.locator('[data-cry="DEERLING_AUTUMN"] .sprite-ready').count(),1);
  await page.locator('#search').fill('Route 101');
  await page.locator('#route-MAP_ROUTE101').scrollIntoViewIfNeeded();
  if([360,412,768,1280].includes(width))await page.screenshot({path:path.join(root,`wiki-preview/seasonal-${width}.png`)});
  for(const row of await page.locator('.encounter').all()){
   assert(await row.evaluate(e=>{const a=e.querySelector('.enc-availability').getBoundingClientRect(),n=e.querySelector('.species-copy').getBoundingClientRect(),r=e.querySelector('.rate').getBoundingClientRect();return a.left>=n.right-1&&a.right<=r.left+1;}),'badge overlaps '+width);
  }
  // Page overflow alone misses names crushed into one-letter columns.
  for(const row of await route.locator('.encounter').all()){
   assert(await row.evaluate(e=>{
    const name=e.querySelector('.species-copy strong'),level=e.querySelector('.enc-meta'),badge=e.querySelector('.availability-badge');
    const lineHeight=parseFloat(getComputedStyle(name).lineHeight);
    return name.getBoundingClientRect().height<=lineHeight*2+1 &&
     level.getBoundingClientRect().height<=parseFloat(getComputedStyle(level).lineHeight)+1 &&
     badge.scrollWidth<=badge.clientWidth+1;
   }),'readable name, level and season badge at '+width);
  }
  await page.goto(url+'?page=research');await page.locator('.article h1').waitFor();assert((await page.locator('#content').innerText()).includes('Devon Master Project'));
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'article overflow '+width);
  assert.deepEqual(errors,[]);console.log('PASS season switching, All Seasons unions/shared links, rates, badges, forms, guide and layout at '+width);
 }
 await browser.close();server.close();
})().catch(e=>{console.error(e);server.close();process.exit(1)});
