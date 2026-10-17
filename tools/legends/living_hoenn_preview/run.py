"""Read-only native mGBA captures of v0.0.61 feature scripts, private QA ROM only."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import subprocess, json, hashlib, os

ROOT=Path(__file__).resolve().parents[3]
SOURCE=Path(__file__).resolve().parent
OUT=ROOT/"build"/"living-hoenn-feature-captures"
OUT.mkdir(parents=True,exist_ok=True)
runlog=lambda args,file: subprocess.run(args,cwd=ROOT,stdout=(OUT/file).open("w"),stderr=subprocess.STDOUT,check=True)
assert (ROOT/"pokeemerald.gba").exists() and (ROOT/"pokeemerald.elf").exists()
runlog(["arm-none-eabi-gcc","-iquote","include","-iquote",".","-DMODERN=1","-DEMERALD",
        "-mthumb","-mcpu=arm7tdmi","-mabi=apcs-gnu","-Os","-ffreestanding",
        "-fno-builtin","-fno-jump-tables","-nostdlib",
        "-Wl,-Ttext=0x09f80000","-Wl,--entry=qa",
        "-Wl,--just-symbols=pokeemerald.elf",str(SOURCE/"arm.c"),"-o",str(OUT/"qa.elf")],"qa-compile.log")
def symbols(path):
    z=subprocess.check_output(["arm-none-eabi-nm",str(path)],text=True)
    return {parts[2]:int(parts[0],16) for line in z.splitlines() if len(parts:=line.split())==3}
native=symbols(ROOT/"pokeemerald.elf")
extra=symbols(OUT/"qa.elf")
for name in ["gMain","CB2_Overworld"]: assert name in native
assert "qa" in extra
runlog(["arm-none-eabi-objcopy","-O","binary",str(OUT/"qa.elf"),str(OUT/"qa.bin")],"objcopy.log")
rom=bytearray((ROOT/"pokeemerald.gba").read_bytes())
payload=(OUT/"qa.bin").read_bytes()
offset=0x1F80000
assert payload and len(payload)<65536 and all(v==255 for v in rom[offset:offset+len(payload)])
rom[offset:offset+len(payload)]=payload
private=OUT/"PRIVATE-Legends-Debug-QA.gba";private.write_bytes(rom)
runlog(["cc","-O2","-std=gnu11",str(SOURCE/"host.c"),"-lmgba","-o",str(OUT/"host")],"host-compile.log")
proc=subprocess.run([str(OUT/"host"),str(private),str(OUT),hex(native["gMain"]),hex(extra["qa"]),hex(native["CB2_Overworld"])],
                    cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
(OUT/"emulator.log").write_text(proc.stdout)
if proc.returncode: raise SystemExit(f"mGBA harness failed: {proc.returncode}\n"+proc.stdout[-1600:])
files=[]
for raw in sorted(OUT.glob("*.rgba")):
    data=raw.read_bytes()
    assert len(data)==240*160*4
    img=Image.frombytes("RGBA",(240,160),data).convert("RGB")
    png=raw.with_suffix(".png");img.save(png);files.append(png)
    raw.unlink()
for prefix in ["birch-research","devon-research","weather-bulletin","littleroot-champion"]:
    items=sorted(OUT.glob(prefix+"-*.png"))
    w,h=4*240,((len(items)+3)//4)*185
    sheet=Image.new("RGB",(w,h),"#101820")
    for idx,p in enumerate(items):
        x=(idx%4)*240; y=(idx//4)*185
        sheet.paste(Image.open(p),(x,y))
        ImageDraw.Draw(sheet).text((x+6,y+161),p.stem,fill="white")
    sheet.save(OUT/(prefix+"-contact-sheet.png"))
(OUT/"proof.json").write_text(json.dumps({
    "version":(ROOT/"VERSION").read_text().strip(),
    "base_ROM_sha256":hashlib.sha256((ROOT/"pokeemerald.gba").read_bytes()).hexdigest(),
    "instrumented_private_ROM":True,
    "emulator":"Ubuntu libmGBA native core 0.10.x",
    "scope":"Loaded actual game maps and ran original embedded NPC/research scripts with temporary state fixtures.",
    "limitation":"Private test fixture, not unmodified normal gameplay; cannot establish normal progression or persistent save compatibility.",
    "screenshots":len(files),
    "scenes":["Birch","Devon","Weather Institute","Littleroot"]
},indent=2)+"\n")
private.unlink()
print(f"Verified {len(files)} real mGBA frames from four controlled Legends v0.0.61 dialogue scenarios.")
