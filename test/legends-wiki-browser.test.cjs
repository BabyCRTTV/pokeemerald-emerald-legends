const {chromium}=require(process.env.WIKI_PLAYWRIGHT);
const assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({headless:true});
 fs.mkdirSync('wiki-preview',{recursive:true});
 for(const [width,height] of [[360,800],[412,915],[690,800],[768,900],[1280,900]]){
  const context=await browser.newContext({viewport:{width,height},isMobile:width<1100,hasTouch:width<1100,userAgent:width<1100?'Mozilla/5.0 Chrome/130.0.0.0 Mobile LegendsWikiAndroid/5':undefined});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/wiki/');await page.locator('.topic-cards').waitFor();
  assert.equal(await page.locator('.topic-cards .card').count(),7);
  assert(await page.getByRole('link',{name:'Open LegendsDex',exact:true}).isVisible());
  assert.equal(await page.locator('.wiki-mobile-nav a').count(),2);
  await page.getByRole('link',{name:'Open LegendsDex',exact:true}).click();
  await page.locator('.route-card').first().waitFor();
  assert(await page.getByRole('link',{name:'Back to guide',exact:true}).isVisible());
  assert.equal(await page.locator('.mobile-nav button').count(),2);
  assert.equal(await page.locator('.mobile-nav a').count(),0);
  await page.getByRole('link',{name:'Back to guide',exact:true}).click();await page.locator('.topic-cards').waitFor();
  async function noOverflow(){assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'horizontal overflow at '+width);}
  await noOverflow();await page.screenshot({path:`wiki-preview/home-${width}.png`,fullPage:true});
  await page.locator('.topic-cards [data-category="Customization"]').click();
  await page.getByRole('heading',{name:'Customization',exact:true}).waitFor();
  await page.locator('#content [data-page="wardrobe"]').click();
  await page.getByRole('heading',{name:'Wardrobe, costumes, and footwear',exact:true}).waitFor();await noOverflow();
  await page.goBack();await page.getByRole('heading',{name:'Customization',exact:true}).waitFor();
  await page.goBack();await page.locator('.topic-cards').waitFor();
  await page.getByLabel('Search wiki',{exact:true}).fill('boots');assert(await page.locator('#cards [data-page="wardrobe"]').isVisible());
  await page.goto('http://127.0.0.1:8765/wiki/dex.html?view=species');
  await page.locator('.dex-card').first().waitFor();await page.locator('#search').fill('Bulbasaur');
  assert.equal(await page.locator('.dex-card').count(),1);await noOverflow();
  const reply=page.waitForResponse(r=>r.url().endsWith('/cries/bulbasaur.wav'));
  await page.getByRole('button',{name:'Play Bulbasaur cry',exact:true}).click();assert((await reply).ok(),'cry request failed');
  await page.getByRole('status').filter({hasText:'Playing Bulbasaur'}).waitFor();assert(!await page.locator('#detail').isVisible());
  await page.locator('.dex-card [data-species="BULBASAUR"]').click();await page.locator('#detail').waitFor();
  assert.equal(await page.locator('button button').count(),0,'nested interactive controls');await noOverflow();
  await page.locator('#close-detail').click();
  await page.locator('#search').fill('');await page.locator('#type').selectOption('FIRE');
  assert((await page.locator('.dex-card .types').allTextContents()).every(t=>t.includes('fire')));
  await page.screenshot({path:`wiki-preview/dex-${width}.png`,fullPage:false});
  // A live resize preserves both the current page and selected filter.
  if(width===412){await page.setViewportSize({width:690,height:800});assert.equal(await page.locator('#type').inputValue(),'FIRE');await noOverflow();}
  await page.goto('http://127.0.0.1:8765/wiki/dex.html?view=routes');await page.locator('.route-card').first().waitFor();await noOverflow();
  await page.screenshot({path:`wiki-preview/routes-${width}.png`,fullPage:false});
  await page.locator('#method').selectOption('surf');await page.locator('[data-view="species"]').click();await page.locator('#type').selectOption('all');
  assert((await page.locator('#results-count').innerText()).startsWith('1026 '),'hidden route method must not filter the National Dex');
  assert.equal(await page.locator('.hero').evaluate(e=>getComputedStyle(e,'::before').content),'none');
  assert.deepEqual(errors,[]);await context.close();
 }
 await browser.close();console.log('PASS: browser navigation, search, cries, profile controls, types and overflow at 360/412/690/768/1280px, plus live fold-size change');
})().catch(e=>{console.error(e);process.exit(1);});
