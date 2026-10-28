// Unmodified Release: real title/Continue, read-only RAM assertions, no ROM/RAM writes.
#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
static void quiet(struct mLogger *l,int c,enum mLogLevel v,const char *f,va_list a){}
static struct mLogger logger={.log=quiet};static struct mCore *c;static color_t *video;
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned mask){c->setKeys(c,mask);frames(3);c->setKeys(c,0);frames(60);}
int main(int argc,char **argv){assert(argc==16);setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);
 struct VFile *rom=VFileOpen(argv[1],O_RDONLY),*save=VFileOpen(argv[2],O_RDWR);assert(rom&&save&&c->loadROM(c,rom)&&c->loadSave(c,save));c->reset(c);frames(300);
 unsigned main=strtoul(argv[4],0,0),overworld=strtoul(argv[5],0,0)|1;
 for(int n=0;n<12&&c->busRead32(c,main+4)!=overworld;n++){key(1);frames(240);}assert(c->busRead32(c,main+4)==overworld);
 unsigned first=c->busRead32(c,strtoul(argv[6],0,0))+strtoul(argv[8],0,0),ptr=c->busRead32(c,strtoul(argv[7],0,0))+992;
 unsigned hash=2166136261u;for(int i=0;i<28;i++)hash=(hash^c->busRead8(c,first+i))*16777619u;assert(hash==strtoul(argv[9],0,0));
 unsigned check=2166136261u;for(int i=8;i<40;i++)check=(check^c->busRead8(c,ptr+i))*16777619u;assert(c->busRead32(c,ptr)==0x314e4f45&&c->busRead32(c,ptr+4)==check&&check==strtoul(argv[10],0,0));
 assert(c->busRead8(c,first+19)==strtoul(argv[11],0,0)&&c->busRead8(c,ptr+31)==strtoul(argv[12],0,0)&&c->busRead8(c,ptr+9)==strtoul(argv[13],0,0));
 assert(c->busRead8(c,strtoul(argv[14],0,0))==strtoul(argv[15],0,0));
 FILE *f=fopen(argv[3],"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);printf("PASS normal Release Continue: exact first identity/HP/status/removal, signed partner checksum/identity/removal and party count\n");c->deinit(c);free(video);return 0;}
