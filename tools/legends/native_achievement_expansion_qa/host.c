#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
static void quiet(struct mLogger *l,int c,enum mLogLevel v,const char *f,va_list a){}
static struct mLogger logger={.log=quiet};static struct mCore *c;static color_t *video;static unsigned mainAddr,callback,selected,detail;static const char *out;
static void frames(int n){while(n--)c->runFrame(c);}
static unsigned box(int n){return c->busRead32(c,0x0203fc00+4*n);}
static void command(int n,int count){unsigned prev=c->busRead32(c,mainAddr+4);c->busWrite32(c,0x0203fc78,0);c->busWrite32(c,0x0203fc7c,prev);c->busWrite32(c,0x0203fc00,n);c->busWrite32(c,mainAddr+4,callback);frames(count);assert(box(30));}
static void key(unsigned k){c->setKeys(c,k);frames(2);c->setKeys(c,0);frames(90);}
static void cap(const char *name){char p[4096];snprintf(p,sizeof(p),"%s/%s.rgba",out,name);FILE *f=fopen(p,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);puts(name);}
static void battery(const char *name){void *data=NULL;size_t n=c->savedataClone(c,&data);assert(n==131072&&data);char p[4096];snprintf(p,sizeof(p),"%s/%s.sav",out,name);FILE *f=fopen(p,"wb");assert(f&&fwrite(data,1,n,f)==n);fclose(f);free(data);}
static void savecheck(void){command(2,1200);printf("flash: %u %u parity=%u profile=%u inventory=%u pin/research=%u\n",box(4),box(5),box(6),box(7),box(8),box(9));for(int i=4;i<=9;i++)assert(box(i)==1);}
int main(int argc,char **argv){
 assert(argc==7);setbuf(stdout,NULL);out=argv[2];mainAddr=strtoul(argv[3],NULL,0);callback=strtoul(argv[4],NULL,0);selected=strtoul(argv[5],NULL,0);detail=strtoul(argv[6],NULL,0);mLogSetDefaultLogger(&logger);
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);
 struct VFile *f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));c->reset(c);frames(300);c->busWrite32(c,mainAddr,0);
 command(0,400);command(1,2);assert(box(1)&&box(2)&&box(3));puts("v0.0.59-layout migration preserved old bits/pin, quietly backfilled ten research goals and rejected legacy garbage.");
 savecheck();battery("private-migrated");command(5,10);assert(box(10)&&!box(11));cap("high-bit-unlock");frames(220);
 command(4,90);for(int n=0;n<21;n++)key(256);for(int n=0;n<3;n++)key(128);assert(c->busRead16(c,selected)==129);cap("last-achievement");key(1);assert(c->busRead8(c,detail));cap("last-details");
 command(6,2);key(1);command(3,2);assert(!box(11)&&!box(12));cap("full-pc-retry");command(7,2);key(1);command(3,2);assert(box(11)&&box(12)&&!box(13));cap("reward-sent");key(1);command(3,2);assert(!box(13));
 key(2);key(8);savecheck();battery("private-claimed");command(3,2);assert(box(10)&&box(11)&&box(12)&&!box(13));
 char path[4096];snprintf(path,sizeof(path),"%s/offsets.txt",out);FILE *ofs=fopen(path,"w");assert(ofs);fprintf(ofs,"%u %u\n",box(15),box(16));fclose(ofs);
 puts("High-ID native notice, index 129 menu/details, full-PC retry, manual once-only berry claim and real flash/load passed.");c->deinit(c);free(video);return 0;
}
