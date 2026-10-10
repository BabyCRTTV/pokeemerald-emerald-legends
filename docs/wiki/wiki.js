"use strict";
(() => {
 const root=document.getElementById("content"),nav=document.getElementById("sidebar"),outline=document.getElementById("outline"),menu=document.getElementById("menu");
 const categories=["Start here","Core gameplay","World & time","Customization","Exploration","Kanto postgame","Reference"];
 const escape=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
 let pages=[],byId=new Map();
 function inline(s){
   s=escape(s);
   s=s.replace(/\\[\\[([a-z0-9-]+)\\|([^\\]]+)\\]\\]/g,(_,id,label)=>byId.has(id)?'<a href="?page='+id+'" data-page="'+id+'">'+label+'</a>':label);
   s=s.replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g,(_,label,url)=>{
     const safe=/^(https?:\\/\\/|\\.{1,2}\\/|#|\\/)/.test(url);
     return safe?'<a href="'+escape(url)+'"'+(/^https?:/.test(url)?' target="_blank" rel="noopener noreferrer"':'')+'>'+label+'</a>':label;
   });
   s=s.replace(/\\*\\*([^*]+)\\*\\*/g,'<strong>$1</strong>').replace(/\\x60([^\\x60]+)\\x60/g,'<code>$1</code>');
   return s;
 }
 function render(md) {
   const lines=md.trim().split(/\\r?\\n/),out=[],heads=[];
   let list=null,para=[],table=[];
   const flushP=()=>{if(para.length){out.push('<p>'+inline(para.join(' '))+'</p>');para=[];}};
   const flushL=()=>{if(list){out.push('</'+list+'>');list=null;}};
   const flushT=()=>{if(table.length){out.push('<div class="scroll-table"><table><thead><tr>'+table[0].map(c=>'<th>'+inline(c)+'</th>').join('')+'</tr></thead><tbody>'+table.slice(1).map(r=>'<tr>'+r.map(c=>'<td>'+inline(c)+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>');table=[];}};
   for(let i=0;i<lines.length;i++){
     let l=lines[i].trim();if(!l){flushP();flushL();flushT();continue;}
     if(/^\\|/.test(l)){flushP();flushL();if(/^\\|\\s*:?-{3,}/.test(l))continue;table.push(l.replace(/^\\||\\|$/g,'').split('|').map(c=>c.trim()));continue;}
     flushT();
     const h=l.match(/^(#{2,3})\\s+(.+)$/);
     if(h){flushP();flushL();let id="section-"+h[2].toLowerCase().replace(/[^a-z0-9 ]/g,'').trim().replace(/\\s+/g,'-');heads.push({id,label:h[2]});out.push('<h'+h[1].length+' id="'+id+'">'+inline(h[2])+'</h'+h[1].length+'>');continue;}
     const li=l.match(/^([-*]|\\d+\\.)\\s+(.+)$/);
     if(li){flushP();let next=/\\d/.test(li[1][0])?'ol':'ul';if(list!==next){flushL();out.push('<'+next+'>');list=next;}out.push('<li>'+inline(li[2])+'</li>');continue;}
     flushL();para.push(l);
   }
   flushP();flushL();flushT();return {html:out.join('\\n'),heads};
 }
 function side(active){
   nav.innerHTML=categories.map(cat=>'<div class="sidetitle">'+escape(cat)+'</div>'+pages.filter(p=>p.category===cat).map(p=>'<a class="'+(p.id===active?'current':'')+'" href="?page='+p.id+'" data-page="'+p.id+'">'+escape(p.title)+'</a>').join('')).join('');
 }
 function navigate(id,push=true){
   if(!byId.has(id)){home();return;}
   const p=byId.get(id),r=render(p.content);
   if(push)history.pushState({},'', '?page='+encodeURIComponent(id));
   side(id);
   root.innerHTML='<article class="article"><div class="crumbs"><button id="home" type="button">Wiki home</button> › '+escape(p.category)+'</div><h1>'+escape(p.title)+'</h1><p class="lede">'+escape(p.summary)+'</p><div class="articlebody">'+r.html+'</div><div class="articlefooter"><button class="action" id="back" type="button">← All articles</button><button class="action" id="share" type="button">Copy article link</button></div></article>';
   outline.innerHTML='<strong>On this page</strong>'+r.heads.filter(h=>h.id).map(h=>'<a href="#'+h.id+'">'+escape(h.label)+'</a>').join('');
   document.title=p.title+' · Emerald: Legends Wiki';menuClose();window.scrollTo({top:0,behavior:'instant'});
   document.getElementById('home').onclick=()=>home();document.getElementById('back').onclick=()=>home();
   document.getElementById('share').onclick=async()=>{try{await navigator.clipboard.writeText(location.href);document.getElementById('share').textContent='Link copied!';}catch{document.getElementById('share').textContent='Copy the URL from your browser';}};
 }
 function home(){
   history.replaceState({},'','./');side('');
   outline.innerHTML='<strong>Wiki guide</strong><p>Choose an article or search for a feature. Everything is open to read.</p>';
   root.innerHTML='<section class="welcome"><p class="eyebrow">Unofficial player encyclopedia</p><h1>Welcome to the Legends Wiki.</h1><p>Guides for the growing world of Pokémon Emerald: Legends. Find clear answers about core mechanics, trainer customization, seasons, and the playable Kanto postgame.</p><label class="searchrow"><span aria-hidden="true">⌕</span><input id="search" type="search" placeholder="Search articles, features, and places…" aria-label="Search wiki" autocomplete="off"><span class="small">/</span></label><p class="results-note" id="resultsnote">Browse '+pages.length+' articles across seven sections.</p></section><div id="cards"></div>';
   const input=document.getElementById('search');input.addEventListener('input',()=>cards(input.value));cards('');document.title='Emerald: Legends Wiki';menuClose();
 }
 function cards(q){
   const box=document.getElementById('cards'),query=q.trim().toLocaleLowerCase();
   const selected=!query?pages:pages.filter(p=>(p.title+' '+p.category+' '+p.summary+' '+p.content).toLocaleLowerCase().includes(query));
   document.getElementById('resultsnote').textContent=query?selected.length+' matching '+(selected.length===1?'article':'articles'):'Browse '+pages.length+' articles across seven sections.';
   if(!selected.length){box.innerHTML='<p>No articles found. Try a different search term, like “Kanto”, “shiny”, or “wardrobe”.</p>';return;}
   box.innerHTML=(query?'<h2 class="section-head">Search results</h2>':'<h2 class="section-head">Explore the wiki</h2>')+'<div class="cards">'+selected.map(p=>'<button class="card" type="button" data-page="'+p.id+'"><span class="kind">'+escape(p.category)+'</span><strong>'+escape(p.title)+'</strong><p>'+escape(p.summary)+'</p></button>').join('')+'</div>';
 }
 function menuClose(){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');}
 menu.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
 document.addEventListener('click',e=>{const item=e.target.closest('[data-page]');if(item){e.preventDefault();navigate(item.dataset.page);}});
 document.addEventListener('keydown',e=>{if(e.key==='Escape')menuClose();if((e.key==='/'||(e.ctrlKey&&e.key.toLowerCase()==='k'))&&!/input|textarea/i.test(document.activeElement?.tagName)){e.preventDefault();home();document.getElementById('search').focus();}});
 window.addEventListener('popstate',()=>{const page=new URLSearchParams(location.search).get('page');page&&byId.has(page)?navigate(page,false):home();});
 fetch('articles.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error('Network response');return r.json();}).then(data=>{
   if(!Array.isArray(data.articles))throw new Error('Invalid articles');pages=data.articles;byId=new Map(pages.map(p=>[p.id,p]));
   const page=new URLSearchParams(location.search).get('page');page&&byId.has(page)?navigate(page,false):home();
 }).catch(()=>{root.innerHTML='<div class="article"><h1>Wiki unavailable offline</h1><p>The wiki could not load its article catalogue. Reconnect to the internet and refresh. No login is required.</p><button class="action" type="button" id="retry">Try again</button></div>';document.getElementById('retry').onclick=()=>location.reload();});
})();