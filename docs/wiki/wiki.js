"use strict";
(() => {
 const root=document.getElementById("content"),nav=document.getElementById("sidebar"),outline=document.getElementById("outline"),menu=document.getElementById("menu");
 if(/LegendsWikiAndroid\/\d+/.test(navigator.userAgent))document.documentElement.classList.add("legends-wiki-android");
 const categories=["Start here","Core gameplay","World & time","Customization","Exploration","Kanto postgame","Reference"];
 const escape=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
 let pages=[],byId=new Map();
 const walkthroughStops=[
  {label:'New Game',page:'walkthrough-littleroot',section:'before-choosing-new-game',hint:'Settings and starter choices'},
  {label:'Littleroot',page:'walkthrough-littleroot',section:'arriving-in-littleroot',hint:'Settle in and rescue the Professor'},
  {label:'Oldale',page:'walkthrough-littleroot',section:'oldale-and-the-first-rival-battle',hint:'Heal and meet your rival'},
  {label:'Petalburg',page:'walkthrough-petalburg',section:'meet-norman-and-help-wally',hint:'Meet Norman and help Wally'},
  {label:'Petalburg Woods',page:'walkthrough-petalburg',section:'route-104-and-the-woods',hint:'Cross the forest and help Devon'},
  {label:'Rustboro',page:'walkthrough-rustboro',section:'prepare-in-rustboro',hint:'Prepare for your first badge'},
  {label:'Rusturf Tunnel',page:'walkthrough-rustboro',section:'rescue-peeko-in-rusturf-tunnel',hint:'Rescue Peeko and recover the goods'},
  {label:'Devon Corporation',page:'walkthrough-rustboro',section:'devon-corporation-and-your-delivery-jobs',hint:'Collect your delivery jobs'},
  {label:'Boat to Dewford',page:'walkthrough-rustboro',section:'reach-the-boat-for-dewford',hint:"Return to Mr. Briney's cottage"}
 ];
 function readingWalkthrough(active){document.documentElement.classList.toggle('reading-walkthrough',active);root.dataset.walkthroughPage='';}
 function walkthroughNavigation(id){
   const options=walkthroughStops.map(stop=>'<option value="'+stop.page+'#section-'+stop.section+'">'+escape(stop.label)+'</option>').join('');
   const cards=id==='walkthrough'?'<div class="walkthrough-stops">'+walkthroughStops.map((stop,i)=>'<a href="?page='+stop.page+'#section-'+stop.section+'" data-page="'+stop.page+'" data-section="section-'+stop.section+'"><span class="stop-number" aria-hidden="true">'+(i+1)+'</span><span><strong>'+escape(stop.label)+'</strong><small>'+escape(stop.hint)+'</small></span></a>').join('')+'</div>':'';
   return '<nav class="walkthrough-navigation" aria-label="Walkthrough locations"><div class="walkthrough-nav-heading"><label for="walkthrough-town">Jump to a town or stop</label>'+(id!=='walkthrough'?'<a href="?page=walkthrough" data-page="walkthrough">All walkthrough stops</a>':'')+'</div><select id="walkthrough-town"><option value="">Choose your current location…</option>'+options+'</select>'+cards+'</nav>';
 }
 function focusSection(section){const target=section&&document.getElementById(section);if(!target)return;target.tabIndex=-1;target.focus({preventScroll:true});target.scrollIntoView({block:'start',behavior:'instant'});}

 const descriptions={"Start here":"Start the walkthrough, install the game, and prepare your save.","Core gameplay":"Starters, experience, shiny odds, and battle essentials.","World & time":"Understand seasons, weather, and the game clock.","Customization":"Outfits, shoes, costumes, and your Trainer Card.","Exploration":"DexNav, field moves, followers, and travel tools.","Kanto postgame":"Plan your journey through Kanto and its gym challenge.","Reference":"Answers, troubleshooting, and project information."};
 function setLocation(params,push,section=""){
   if(!push)return;
   const url=new URL(location.href);url.search='';url.hash='';
   for(const [key,value] of Object.entries(params))url.searchParams.set(key,value);
   if(section)url.hash=section;
   if(url.href!==location.href)history.pushState({},'',url);
 }
 function focusContent(){root.focus({preventScroll:true});window.scrollTo({top:0,behavior:'instant'});}
 function articleCards(selected){return '<div class="cards">'+selected.map(p=>'<a class="card" href="?page='+p.id+'" data-page="'+p.id+'"><strong>'+escape(p.title)+'</strong><p>'+escape(p.summary)+'</p></a>').join('')+'</div>';}
 function category(cat,push=true){
   if(cat!=='all'&&!categories.includes(cat)){home(push);return;}
   readingWalkthrough(false);setLocation({category:cat},push);side(cat);outline.innerHTML='';
   const selected=cat==='all'?pages:pages.filter(p=>p.category===cat);
   root.innerHTML='<section class="article"><div class="crumbs"><a href="./" data-home>Wiki home</a> › Browse</div><h1>'+escape(cat==='all'?'All articles':cat)+'</h1><p class="lede">'+escape(descriptions[cat]||'Browse the complete wiki article index.')+'</p>'+articleCards(selected)+'</section>';
   document.title=(cat==='all'?'All articles':cat)+' · Emerald: Legends Wiki';menuClose();focusContent();
 }
 function readLocation(){const params=new URLSearchParams(location.search);if(params.has('page'))navigate(params.get('page'),false,location.hash.slice(1));else if(params.has('category'))category(params.get('category'),false);else home(false);}
 function inline(s){
   s=escape(s);
   s=s.replace(/\[\[([a-z0-9-]+)\|([^\]]+)\]\]/g,(_,id,label)=>byId.has(id)?'<a href="?page='+id+'" data-page="'+id+'">'+label+'</a>':label);
   s=s.replace(/\[([^\]]+)\]\(([^)]+)\)/g,(_,label,url)=>{
     const safe=/^(https?:\/\/|\.{1,2}\/|#|\/)/.test(url);
     return safe?'<a href="'+escape(url)+'"'+(/^https?:/.test(url)?' target="_blank" rel="noopener noreferrer"':'')+'>'+label+'</a>':label;
   });
   s=s.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/\x60([^\x60]+)\x60/g,'<code>$1</code>');
   return s;
 }
 function render(md) {
   const lines=md.trim().split(/\r?\n/),out=[],heads=[];
   let list=null,para=[],table=[];
   const flushP=()=>{if(para.length){out.push('<p>'+inline(para.join(' '))+'</p>');para=[];}};
   const flushL=()=>{if(list){out.push('</'+list+'>');list=null;}};
   const flushT=()=>{if(table.length){out.push('<div class="scroll-table"><table><thead><tr>'+table[0].map(c=>'<th>'+inline(c)+'</th>').join('')+'</tr></thead><tbody>'+table.slice(1).map(r=>'<tr>'+r.map(c=>'<td>'+inline(c)+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>');table=[];}};
   for(let i=0;i<lines.length;i++){
     let l=lines[i].trim();if(!l){flushP();flushL();flushT();continue;}
     if(/^\|/.test(l)){flushP();flushL();if(/^\|\s*:?-{3,}/.test(l))continue;table.push(l.replace(/^\||\|$/g,'').split('|').map(c=>c.trim()));continue;}
     flushT();
     const h=l.match(/^(#{2,3})\s+(.+)$/);
     if(h){flushP();flushL();let id="section-"+h[2].toLowerCase().replace(/[^a-z0-9 ]/g,'').trim().replace(/\s+/g,'-');heads.push({id,label:h[2]});out.push('<h'+h[1].length+' id="'+id+'">'+inline(h[2])+'</h'+h[1].length+'>');continue;}
     const li=l.match(/^([-*]|\d+\.)\s+(.+)$/);
     if(li){flushP();let next=/\d/.test(li[1][0])?'ol':'ul';if(list!==next){flushL();out.push('<'+next+'>');list=next;}out.push('<li>'+inline(li[2])+'</li>');continue;}
     flushL();para.push(l);
   }
   flushP();flushL();flushT();return {html:out.join('\n'),heads};
 }
 function side(active){
   const current=byId.get(active)?.category||(categories.includes(active)?active:'');
   nav.innerHTML='<a href="./" data-home>Wiki home</a><div class="sidetitle">Topics</div>'+categories.map(cat=>'<a class="'+(cat===current?'current':'')+'" href="?category='+encodeURIComponent(cat)+'" data-category="'+escape(cat)+'">'+escape(cat)+'</a>').join('')+'<a href="?category=all" data-category="all">All articles</a>';
   if(byId.has(active))nav.innerHTML+='<div class="sidetitle">In this section</div>'+pages.filter(p=>p.category===current).map(p=>'<a class="'+(p.id===active?'current':'')+'" href="?page='+p.id+'" data-page="'+p.id+'">'+escape(p.title)+'</a>').join('');
 }
 function navigate(id,push=true,section=""){
   if(!byId.has(id)){home(push);return;}
   const p=byId.get(id),r=render(p.content);
   const walkthrough=id==='walkthrough'||id.startsWith('walkthrough-');readingWalkthrough(walkthrough);
   setLocation({page:id},push,section);
   side(id);
   root.innerHTML='<article class="article"><div class="crumbs"><button id="home" type="button">Wiki home</button> › '+'<a href="?category='+encodeURIComponent(p.category)+'" data-category="'+escape(p.category)+'">'+escape(p.category)+'</a></div><h1>'+escape(p.title)+'</h1><p class="lede">'+escape(p.summary)+'</p>'+(walkthrough?walkthroughNavigation(id):'')+'<div class="articlebody">'+r.html+'</div><div class="articlefooter"><button class="action" id="back" type="button">← '+escape(p.category)+'</button><button class="action" id="share" type="button">Copy article link</button></div></article>';
   outline.innerHTML='<strong>On this page</strong>'+r.heads.filter(h=>h.id).map(h=>'<a href="#'+h.id+'">'+escape(h.label)+'</a>').join('');
   document.title=p.title+' · Emerald: Legends Wiki';menuClose();focusContent();focusSection(section);
   if(walkthrough){root.dataset.walkthroughPage=id;window.LegendsWalkthroughMaps?.decorate(root,id);}
   const towns=document.getElementById('walkthrough-town');if(towns){if(section)towns.value=id+'#'+section;towns.onchange=()=>{if(!towns.value)return;const [page,anchor]=towns.value.split('#');navigate(page,true,anchor);};}
   document.getElementById('home').onclick=()=>home();document.getElementById('back').onclick=()=>category(p.category);
   document.getElementById('share').onclick=async()=>{try{await navigator.clipboard.writeText(location.href);document.getElementById('share').textContent='Link copied!';}catch{document.getElementById('share').textContent='Copy the URL from your browser';}};
 }
 function home(push=true){
   readingWalkthrough(false);setLocation({},push);side('');
   outline.innerHTML='<strong>Wiki guide</strong><p>Choose an article or search for a feature. Everything is open to read.</p>';
   root.innerHTML='<section class="welcome"><p class="eyebrow">Unofficial player encyclopedia</p><h1>Your Legends guide.</h1><p>Choose a topic below, or jump straight to Pokémon and wild encounters.</p><div class="dex-shortcuts" aria-label="LegendsDex shortcuts"><a href="dex.html?view=routes">⌁ Routes <small>Wild encounter guide</small></a><a href="dex.html?view=species">◈ Pokédex <small>Browse Pokémon</small></a></div><p class="walkthrough-shortcut"><a href="?page=walkthrough" data-page="walkthrough" class="action">Walkthrough <span aria-hidden="true">→</span></a><small>New Game to the Stone Badge and the boat to Dewford</small></p><label class="searchrow"><span aria-hidden="true">⌕</span><input id="search" type="search" placeholder="Search articles, features, and places…" aria-label="Search wiki" autocomplete="off"><span class="small">/</span></label><p class="results-note" id="resultsnote">Browse '+pages.length+' articles across seven sections.</p></section><div id="cards"></div>';
   const input=document.getElementById('search');input.addEventListener('input',()=>cards(input.value));cards('');document.title='Emerald: Legends Wiki';menuClose();focusContent();
 }
 function cards(q){
   const box=document.getElementById('cards'),query=q.trim().toLocaleLowerCase();
   if(!query){
     document.getElementById('resultsnote').textContent='Choose a section to explore.';
     box.innerHTML='<h2 class="section-head">Browse by topic</h2><div class="cards topic-cards">'+categories.map(cat=>'<a class="card" href="?category='+encodeURIComponent(cat)+'" data-category="'+escape(cat)+'"><strong>'+escape(cat)+'</strong><p>'+escape(descriptions[cat])+'</p><span class="topic-count">'+pages.filter(p=>p.category===cat).length+' articles <span aria-hidden="true">→</span></span></a>').join('')+'</div><p class="index-link"><a href="?category=all" data-category="all">View all '+pages.length+' articles →</a></p>';return;
   }
   const selected=pages.filter(p=>(p.title+' '+p.category+' '+p.summary+' '+p.content).toLocaleLowerCase().includes(query));
   document.getElementById('resultsnote').textContent=query?selected.length+' matching '+(selected.length===1?'article':'articles'):'Browse '+pages.length+' articles across seven sections.';
   if(!selected.length){box.innerHTML='<p>No articles found. Try a different search term, like “Kanto”, “shiny”, or “wardrobe”.</p>';return;}
   box.innerHTML=(query?'<h2 class="section-head">Search results</h2>':'<h2 class="section-head">Explore the wiki</h2>')+'<div class="cards">'+selected.map(p=>'<button class="card" type="button" data-page="'+p.id+'"><span class="kind">'+escape(p.category)+'</span><strong>'+escape(p.title)+'</strong><p>'+escape(p.summary)+'</p></button>').join('')+'</div>';
 }
 function menuClose(){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');}
 menu.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
 const headerSearch=document.getElementById('header-search');
 if(headerSearch)headerSearch.addEventListener('click',()=>{home();document.getElementById('search')?.focus();});
 document.addEventListener('click',e=>{const cat=e.target.closest('[data-category]'),homeLink=e.target.closest('[data-home]');if(cat){e.preventDefault();category(cat.dataset.category);return;}if(homeLink){e.preventDefault();home();return;}const item=e.target.closest('[data-page]');if(item){e.preventDefault();navigate(item.dataset.page,true,item.dataset.section||"");}});
 document.addEventListener('keydown',e=>{if(e.key==='Escape')menuClose();if((e.key==='/'||(e.ctrlKey&&e.key.toLowerCase()==='k'))&&!/input|textarea/i.test(document.activeElement?.tagName)){e.preventDefault();home();document.getElementById('search').focus();}});
 window.addEventListener('popstate',readLocation);
 fetch('articles.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error('Network response');return r.json();}).then(data=>{
   if(!Array.isArray(data.articles))throw new Error('Invalid articles');pages=data.articles;byId=new Map(pages.map(p=>[p.id,p]));
   readLocation();
 }).catch(()=>{root.innerHTML='<div class="article"><h1>Wiki unavailable offline</h1><p>The wiki could not load its article catalogue. Reconnect to the internet and refresh. No login is required.</p><button class="action" type="button" id="retry">Try again</button></div>';document.getElementById('retry').onclick=()=>location.reload();});
})();