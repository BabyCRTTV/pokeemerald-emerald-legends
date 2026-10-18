#!/usr/bin/env python3
"""Package the actual wiki reader + LegendsDex into one offline review HTML.

The wrapper is preview-only. Production files retain their normal URLs/history.
"""
from pathlib import Path
import base64,json,mimetypes,re
R=Path(__file__).resolve().parents[1];W=R/'docs/wiki';O=R.parent/'Emerald-Legends-Wiki-preview.html'
assets={}
for p in list(W.glob('*.png'))+list(W.glob('*.webp'))+list(W.glob('*.svg')):
 assets[p.name]='data:'+mimetypes.guess_type(p.name)[0]+';base64,'+base64.b64encode(p.read_bytes()).decode()
# Embed the reader's original project title artwork too, when referenced.
for url in re.findall(r'(?:src|href)=[\"\']([^\"\']+)[\"\']',(W/'wiki.js').read_text()):
 p=W/url
 if p.is_file() and p.suffix in ('.png','.svg','.webp'):
  assets[url]='data:'+mimetypes.guess_type(p.name)[0]+';base64,'+base64.b64encode(p.read_bytes()).decode()
def js(s):return s.replace('</script','<\\/script')
def embed(s):
 for name,uri in sorted(assets.items(),key=lambda x:-len(x[0])):s=s.replace(name,uri)
 return s
payload={p.name:json.loads(embed(p.read_text())) for p in W.glob('*.json')}
bootstrap='''<script>
window.previewLocation=new URL('https://wiki-preview.invalid/wiki/'+(parent.previewPage==='dex'?'dex.html?season=autumn':parent.previewQuery||''));
let previewStack=[previewLocation.href],previewIndex=0;
window.previewHistory={pushState(a,b,u){previewLocation=new URL(u,previewLocation);previewStack.splice(++previewIndex);previewStack.push(previewLocation.href)},replaceState(a,b,u){previewLocation=new URL(u,previewLocation);previewStack[previewIndex]=previewLocation.href},back(){if(previewIndex){previewLocation=new URL(previewStack[--previewIndex]);dispatchEvent(new PopStateEvent('popstate'))}}};
const nativeFetch=window.fetch.bind(window);
window.fetch=(url,options)=>{let name=String(url).split('?')[0].split('/').pop();return parent.PREVIEW_DATA[name]?Promise.resolve(new Response(JSON.stringify(parent.PREVIEW_DATA[name]),{status:200,headers:{'Content-Type':'application/json'}})):nativeFetch(url,options)};
document.addEventListener('click',e=>{const a=e.target.closest('a');if(!a)return;const href=a.getAttribute('href')||'';if(a.hasAttribute('data-page')||a.hasAttribute('data-home')||a.hasAttribute('data-category'))return;if(href.startsWith('dex.html')){e.preventDefault();parent.showPreview('dex',href.slice(8));}else if(href==='./'||href.startsWith('./?')){e.preventDefault();parent.showPreview('guide',href.slice(2));}},true);
</script>'''
def page(name):
 s=(W/name).read_text()
 s=re.sub(r'<link\b[^>]*rel="stylesheet"[^>]*>',lambda m:'<style>'+embed((W/re.search(r'href="([^"?]+)',m[0])[1]).read_text())+'</style>',s)
 def script(m):
  name=m[1].split('?')[0]
  if name=='wiki-updates.js':return '<script>document.getElementById("update-wiki")?.addEventListener("click",()=>alert("This is a review preview. App builds will be updated after publication approval."));</script>'
  text=embed((W/name).read_text());text=re.sub(r'\blocation\.', 'previewLocation.',text);text=text.replace('history.pushState','previewHistory.pushState').replace('history.replaceState','previewHistory.replaceState')
  return '<script>'+js(text)+'</script>'
 s=re.sub(r'<script\b[^>]*src="([^"]+)"[^>]*>\s*</script>',script,s)
 s=embed(s)
 return s.replace('<head>','<head>'+bootstrap,1)
pages={'dex':page('dex.html'),'guide':page('index.html')}
body='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Emerald: Legends · Wiki review preview</title><style>*{box-sizing:border-box}body{margin:0;background:#f7f4fd;font:14px system-ui;color:#594073}.preview-controls{height:50px;display:flex;align-items:center;justify-content:center;gap:8px;border-bottom:1px solid #dfd2ee;background:#fffaff}.preview-controls button{font:700 12px system-ui;padding:7px 11px;border:1px solid #d8c8ea;border-radius:8px;background:#eee5fb;color:#594073;cursor:pointer;min-height:34px}.preview-controls .selected{background:#7150a7;color:white;border-color:#7150a7}.preview-controls small{font-size:10px}iframe{display:block;border:0;width:100%;height:calc(100dvh - 50px);background:#f7f4fd}</style></head><body><nav class="preview-controls" aria-label="Preview pages"><small>PREVIEW</small><button id="dex" onclick="showPreview('dex')">Encounters</button><button id="guide" onclick="showPreview('guide')">Updated guide</button><button onclick="document.querySelector('iframe').contentWindow.previewHistory.back()" aria-label="Back in guide">←</button></nav><iframe title="Legends wiki preview"></iframe><script>'''
body+='window.PREVIEW_DATA='+js(json.dumps(payload,ensure_ascii=False,separators=(',',':')))+';\nconst pages='+js(json.dumps(pages,ensure_ascii=False,separators=(',',':')))+';\n'
body+='''window.previewPage='dex';window.previewQuery='';function showPreview(page,query=''){window.previewPage=page;window.previewQuery=query;document.querySelectorAll('.preview-controls button[id]').forEach(b=>b.classList.toggle('selected',b.id===page));document.querySelector('iframe').srcdoc=pages[page];}showPreview('dex');</script></body></html>'''
O.write_text(body);print(O, O.stat().st_size)
