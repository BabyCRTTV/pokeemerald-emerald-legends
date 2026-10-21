const {chromium}=require(process.env.WIKI_PLAYWRIGHT||process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.WIKI_CHROME});
 const output=process.env.GROTTO_WIKI_OUTPUT||'build/grotto-wiki';fs.mkdirSync(output,{recursive:true});
 for(const width of [360,412,768,1280]){
  const page=await browser.newPage({viewport:{width,height:915},deviceScaleFactor:1});const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/wiki/dex.html');await page.locator('.route-card').first().waitFor();
  assert.equal(await page.getByText('Updated on request',{exact:true}).count(),0);
  assert.equal(await page.locator('[data-region="Sevii"]').textContent(),'Sevii');
  await page.locator('[data-region="Grotto"]').click();
  assert.equal(await page.locator('.route-card').count(),3);assert.equal(await page.locator('.encounter').count(),15);
  assert(await page.locator('.route-card').first().textContent().then(t=>t.includes('4,500')));
  for(const s of ['spring','summer','autumn','winter']){
   await page.locator('#season').selectOption(s);assert.equal(await page.locator('.encounter').count(),15);
   for(const card of await page.locator('.route-card').all())assert.equal((await card.locator('.rate').allTextContents()).reduce((sum,t)=>sum+parseInt(t),0),100);
  }
  await page.locator('#season').selectOption('all');assert(await page.locator('.encounter').count()>15);
  await page.locator('#tab-species').click();assert(await page.locator('.dex-card').count()>15);
  await page.locator('#tab-routes').click();
  await page.locator('#season').selectOption('spring');
  await page.locator('#method').selectOption('grotto');assert.equal(await page.locator('.route-card').count(),3);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  const chips=await page.locator('[data-region]').evaluateAll(nodes=>nodes.map(n=>({text:n.textContent,height:n.getBoundingClientRect().height,scroll:n.scrollHeight,client:n.clientHeight})));
  assert(chips.every(c=>c.height===chips[0].height),JSON.stringify(chips));
  await page.locator('#region-filters').scrollIntoViewIfNeeded();
  if(width===412){await page.screenshot({path:output+'/LegendsDex-Grotto-Filter.png'});await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:output+'/LegendsDex-Clean-Header.png'});}
  await page.locator('.route-card .pokemon-link').first().click();await page.locator('#detail').waitFor({state:'visible'});
  assert.match(await page.locator('#detail-content').textContent(),/4,500-step/);assert.match(await page.locator('#detail-content').textContent(),/Leafshade/);
  assert.deepEqual(errors,[]);await page.close();console.log('PASS Grotto filter, all seasonal shares, details and equal chips at '+width+'px');
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
