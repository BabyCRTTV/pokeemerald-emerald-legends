"""Private LPC2 fixture from a native current save; retain exact published bytes."""
import struct

def unpack(src,size):
 out=bytearray();at=0
 while len(out)<size:
  flags=src[at];at+=1
  for bit in range(8):
   if len(out)==size:break
   if flags&(128>>bit):
    a,b=src[at:at+2];at+=2;length=(a>>4)+3;distance=((a&15)<<8)+b+1
    assert distance<=len(out) and len(out)+length<=size
    for _ in range(length):out.append(out[-distance])
   else:out.append(src[at]);at+=1
 assert at==len(src)
 return out

def pack(src):
 out=bytearray();history={};at=0
 while at<len(src):
  group=len(out);out.append(0)
  for bit in range(8):
   if at==len(src):break
   key=bytes(src[at:at+3]);prev=history.get(key,-1);length=0
   if prev>=0 and at-prev<=4096:
    while length<18 and at+length<len(src) and src[prev+length]==src[at+length]:length+=1
   if length>=3:
    distance=at-prev-1;out[group]|=128>>bit;out.extend([((length-3)<<4)|(distance>>8),distance&255])
   else:length=1;out.append(src[at])
   for i in range(length):history[bytes(src[at+i:at+i+3])]=at+i
   at+=length
 return out

def fnv(raw):
 h=2166136261
 for b in raw:h=((h^b)*16777619)&0xffffffff
 return h

def convert(source,target,layout):
 save=bytearray(source.read_bytes());converted=0
 for half in range(2):
  sectors={}
  for n in range(14):
   off=(half*14+n)*4096;ident,checksum,signature,counter=struct.unpack_from('<HHII',save,off+4084)
   if ident<14 and signature==0x8012025:sectors[ident]=off
  if len(sectors)!=14:
   save[half*14*4096:(half+1)*14*4096]=b'\xff'*(14*4096);continue
  packed=b''.join(save[sectors[i]:sectors[i]+3968] for i in range(5,14))
  magic,rawSize,checksum,payload=struct.unpack_from('<4I',packed)
  assert magic==0x4c504333
  raw=unpack(packed[16:16+payload],rawSize);assert fnv(raw)==checksum
  offset=layout['inventoryOffset'];counts=struct.unpack_from('<5H',raw,offset);limits=[150,32,128,80,60]
  if any(n>cap for n,cap in zip(counts,limits)):
   save[half*14*4096:(half+1)*14*4096]=b'\xff'*(14*4096);continue
  chunks=[];start=offset+10
  for n,cap in zip(counts,limits):chunks.append(bytes(raw[start:start+n*4])+bytes((cap-n)*4));start+=n*4
  old=raw[:offset]+b''.join(chunks[i] for i in [0,4,1,2,3])+raw[offset+layout['bagSize']:offset+layout['bagSize']+600]
  body=pack(old);assert unpack(body,len(old))==old
  data=struct.pack('<4I',0x4c504332,len(old),fnv(old),len(body))+body;assert len(data)<=35712;data+=bytes(35712-len(data))
  for i in range(5,14):
   off=sectors[i];chunk=data[(i-5)*3968:(i-4)*3968];save[off:off+3968]=chunk
   total=sum(struct.unpack('<992I',chunk))&0xffffffff;struct.pack_into('<H',save,off+4086,((total>>16)+total)&65535)
  converted+=1
 assert converted,'No legacy-compatible native seed'
 target.write_bytes(save)
 print('Prepared controlled LPC2 battery fixture; original sector tails, counters and other saved state retained.')
