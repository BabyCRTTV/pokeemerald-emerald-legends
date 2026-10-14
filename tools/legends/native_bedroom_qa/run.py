"""Controlled native bedroom preview. Requires built Debug ELF/ROM, ARM tools and mGBA."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--mgba-prefix',type=Path,required=True);args=p.parse_args();out=args.output.resolve();out.mkdir(exist_ok=True,parents=True)
 src=Path(__file__).resolve().parent;env=os.environ.copy();prefix=args.mgba_prefix.resolve();env['PATH']=str(prefix/'bin')+':'+env['PATH'];env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','')
 def run(cmd,log):
  with (out/log).open('w') as f:subprocess.run(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-fno-jump-tables','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols=pokeemerald.elf',str(src/'arm.c'),'-o',str(out/'arm.elf')],'arm-build.log')
 arm_nm=subprocess.check_output(['arm-none-eabi-nm',str(out/'arm.elf')],cwd=ROOT,env=env,text=True)
 callback=next(int(line.split()[0],16)|1 for line in arm_nm.splitlines() if line.split()[-1]=='qa')
 run(['arm-none-eabi-objcopy','-O','binary',str(out/'arm.elf'),str(out/'arm.bin')],'objcopy.log')
 rom=bytearray((ROOT/'pokeemerald.gba').read_bytes());arm=(out/'arm.bin').read_bytes();assert len(arm)<65536 and set(rom[0x1f80000:0x1f80000+len(arm)])=={255};rom[0x1f80000:0x1f80000+len(arm)]=arm;(out/'private-bedroom.gba').write_bytes(rom)
 nm=subprocess.check_output(['arm-none-eabi-nm','pokeemerald.elf'],cwd=ROOT,env=env,text=True);symbols={p[2]:int(p[0],16) for line in nm.splitlines() if len(p:=line.split())==3}
 run(['cc',str(src/'host.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],'host-build.log')
 run([str(out/'host'),str(out/'private-bedroom.gba'),str(out),hex(symbols['gMain']),hex(callback)],'emulator.log')
 for raw in sorted(out.glob('*.rgba')):Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(out/(raw.stem+'.png'))
 # Native color changes must leave every pixel outside the two materials intact.
 for before,after,bed,rug in [
  ('male-default','male-rose-rug-mint-bed',(48,40,96,88),(96,40,176,104)),
  ('female-default','female-plum-rug-gold-bed',(144,40,192,88),(64,40,144,104))]:
  a=Image.open(out/(before+'.png'));b=Image.open(out/(after+'.png'));changed=0
  for y in range(160):
   for x in range(240):
    if a.getpixel((x,y))!=b.getpixel((x,y)):
     changed+=1
     assert any(r[0]<=x<r[2] and r[1]<=y<r[3] for r in [bed,rug]),(before,x,y)
  assert changed>1000
 # Unlocking the poster may only change the wall pixels; furniture below and
 # the female bookcase at x7 must remain pixel-identical in actual compositor.
 for gender,rect in [('male',(96,0,112,16)),('female',(128,0,144,16))]:
  a=Image.open(out/(gender+'-without-poster.png'));b=Image.open(out/(gender+'-with-poster.png'));changes=0
  for y in range(160):
   for x in range(240):
    if a.getpixel((x,y))!=b.getpixel((x,y)):
     changes+=1;assert rect[0]<=x<rect[2] and rect[1]<=y<rect[3],(gender,x,y)
  assert changes>20
 groups=[('bedroom-native-room.png',['male-default','male-rose-rug-mint-bed','female-plum-rug-gold-bed']),('bedroom-native-menu.png',['bedroom-decor-menu','rug-color-menu','doll-on-wood-floor']),('bedroom-native-chairs.png',['chair-style-menu-scrolled','male-pokemon-chair','female-hard-chair'])]
 for name,images in groups:
  sheet=Image.new('RGB',(480,len(images)*354),(34,29,40));draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
  for i,n in enumerate(images):draw.text((12,i*354+8),n.replace('-',' ').title(),font=font,fill='white');sheet.paste(Image.open(out/(n+'.png')).resize((480,320),Image.Resampling.NEAREST),(0,i*354+30))
  sheet.save(out/name)
 proof={'state':'unpublished native preview','emulator':'mGBA 0.10.2','unrelated_scene_pixels_unchanged_both_layouts':True,'poster_furniture_pixels_preserved_both_layouts':True,'chair_menu_scroll_cancel_and_flash_roundtrip':True,'ROM_sha256':hashlib.sha256((ROOT/'pokeemerald.gba').read_bytes()).hexdigest(),'scope':'Controlled callbacks prepared both rooms. Real task input selected separate colors and canceled without applying; room reload, real flash write/load and native menu placement of a Pikachu Doll on wood floor checked; both colors and its saved position survived real flash write/load. Actual chair menus selected Pokémon and Hard styles, scrolled and canceled, then restored the Hard style through flash write/load; original PC interaction captured from both replacement seats. Poster unlock changed only its wall rectangle, preserving both consoles and the female books. No complete historical-save matrix or Pizza Boy playtest claimed.','log':(out/'emulator.log').read_text(),'images':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(out.glob('*.png'))}}
 (out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
if __name__=='__main__':main()
