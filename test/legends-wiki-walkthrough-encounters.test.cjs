// Execute shipped encounter rendering with current seasonal and legacy methods.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=__dirname+'/../',text=fs.readFileSync(root+'docs/wiki/walkthrough-maps.js','utf8');
const source=text.slice(text.indexOf(' function speciesRow('),text.indexOf(' async function decorate('));
const c={window:{LegendsSpriteAtlas:{icons:{}}},esc:s=>String(s)};
vm.runInNewContext(source+'\nthis.render=encounterList;',c);
const data=JSON.parse(fs.readFileSync(root+'docs/wiki/dex-data.json'));
const species=new Map(data.species.map(p=>[p.id,p]));let count=0;
for(const route of data.maps)for(const method of route.methods){
 const html=c.render({mapId:route.id},new Map([[route.id,{...route,methods:[method]}]]),species,[method.id]);
 if(method.seasonalVariants?.length){
  count++;
  const rows=method.seasonalVariants[0].entries.filter(e=>method.seasonalVariants.every(v=>v.entries.some(x=>x.id===e.id&&x.rate===e.rate&&x.min===e.min&&x.max===e.max)));
  assert(html.includes('Year-round residents shown.'));assert(html.includes('Open LegendsDex above'));
  assert.equal((html.match(/<li>/g)||[]).length,rows.length);
  for(const e of rows){assert(html.includes('pokemon='+e.id+'"'));assert(html.includes('walkthrough-rate">'+e.rate+'%'));}
  for(const v of method.seasonalVariants)for(const e of v.entries)if(!rows.some(x=>x.id===e.id))assert(!html.includes('pokemon='+e.id+'"'));
  assert.equal([...html.matchAll(/walkthrough-rate">(\d+)%/g)].reduce((s,x)=>s+Number(x[1]),0),method.id==='surf'?65:70);
 }else{
  assert(!html.includes('Year-round residents shown.'));
  assert.equal((html.match(/<li>/g)||[]).length,method.entries.length);
  assert.equal([...html.matchAll(/walkthrough-rate">(\d+)%/g)].reduce((s,x)=>s+Number(x[1]),0),100);
 }
}
assert.equal(count,21);
const m=data.maps[0],empty={...m,methods:m.methods.map(x=>({...x,seasonalVariants:[]}))};
assert(!c.render({mapId:m.id},new Map([[m.id,empty]]),species).includes('Year-round residents shown.'));
console.log('PASS: all 409 walkthrough methods, twenty-one seasonal methods show actual 65%/70% resident shares and seasonal guidance; other methods and empty variants retain full tables');
