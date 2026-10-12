"""Bounded lossless PC compression: round trips, malformed input and capacity guards."""
from pathlib import Path
import subprocess,tempfile
R=Path(__file__).resolve().parents[1]
s=(R/'src/legends_storage.c').read_text()
def function(name):
 start=s.index(name+'('); start=s.rfind('\n',0,start)+1
 brace=s.index('{',start);end=brace+1;depth=1
 while depth:depth+=(s[end]=='{')-(s[end]=='}');end+=1
 return s[start:end]
code=function('LegendsStoragePack')+'\n'+function('LegendsStorageUnpack')
fixture=r'''
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int bool32;
#define FALSE 0
#define TRUE 1
static u8 raw[60000],packed[70000],back[60000];static u16 hash[4096];
'''
main=r'''
int main(void)
{
    uint32_t seed=1234567;
    for(unsigned pattern=0;pattern<5;pattern++)for(unsigned size=1;size<60000;size=size<100?size+1:size+997)
    {
        for(unsigned i=0;i<size;i++)
        {
            seed=seed*1664525+1013904223;
            raw[i]=pattern==0?0:pattern==1?i%80:pattern==2?(i%80<50?0:seed>>24):pattern==3?seed>>24:i%255;
        }
        unsigned n=LegendsStoragePack(raw,size,packed,sizeof(packed),hash);assert(n);
        assert(LegendsStorageUnpack(packed,n,back,size));assert(!memcmp(raw,back,size));
        assert(!LegendsStorageUnpack(packed,n-1,back,size));
        assert(!LegendsStorageUnpack(packed,n,back,size+1));
        if(n>1)assert(!LegendsStoragePack(raw,size,packed,n-1,hash));
    }
    memset(raw,0,sizeof(raw));unsigned n=LegendsStoragePack(raw,60000,packed,35712,hash);assert(n<7100);
    u8 bad[]={0x80,0,0};assert(!LegendsStorageUnpack(bad,sizeof(bad),back,3));
    puts("Lossless codec: five data patterns, tiny and full PC payloads, truncated/malformed input and overflow refusal passed.");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'codec.c').write_text(fixture+code+main)
 subprocess.run(['cc','-std=gnu11','-O2','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p/'codec.c'),'-o',str(p/'codec')],check=True)
 subprocess.run([str(p/'codec')],check=True)
