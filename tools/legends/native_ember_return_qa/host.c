#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
static void quiet(struct mLogger *l,int c,enum mLogLevel v,const char *f,va_list a) {}
static struct mLogger logger={.log=quiet};
static struct mCore *c; static color_t *video; static unsigned mainAddr,callback;
static unsigned box(int n){return c->busRead32(c,0x0203ffc0+n*4);}
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned k){c->setKeys(c,k);frames(3);c->setKeys(c,0);frames(42);}
// A three-frame tap may only turn the avatar. Hold long enough to start one real step.
static void walk(unsigned k){c->setKeys(c,k);frames(12);c->setKeys(c,0);frames(42);}
static void command(int n){unsigned previous=c->busRead32(c,mainAddr+4);c->busWrite32(c,0x0203ffc0,n);c->busWrite32(c,0x0203ffd0,0);c->busWrite32(c,0x0203ffcc,previous);c->busWrite32(c,mainAddr+4,callback);for(int i=0;i<1000&&!box(4);i++){frames(1);if(!box(4))c->busWrite32(c,mainAddr+4,callback);}assert(box(4));}
static void snapshot(void){command(1);}
static void choice(void){for(int i=0;i<50;i++){snapshot();if(box(13)){frames(12);snapshot();assert(box(13));return;}key(1);}assert(!"Choice did not appear");}
static void finish(void){for(int i=0;i<80;i++){frames(30);snapshot();if(!box(12)){frames(120);snapshot();if(!box(12))return;}assert(!box(13));if(box(12))key(1);}assert(!"Event did not finish");}
static void capture(const char *out,const char *name){char p[4096];snprintf(p,sizeof(p),"%s/%s.rgba",out,name);FILE *f=fopen(p,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);}
static void location(unsigned group,unsigned map,unsigned x,unsigned y){snapshot();printf("map=%u,%u xy=%u,%u collision=%u script=%u flags=%u noclip=%u choice=%u result=%u\n",box(5),box(6),box(10),box(11),box(9),box(12),box(14),box(15),box(13),box(1));assert(box(5)==group&&box(6)==map&&box(10)==x&&box(11)==y&&box(9)==0&&!box(12)&&!box(13)&&!box(15));}
static void fixture(const char*out,int ready,unsigned eg,unsigned em,unsigned tg,unsigned tm){
 command(2);assert(box(5)==1);void*data=NULL;size_t n=c->savedataClone(c,&data);assert(n==131072&&data);
 char path[4096];snprintf(path,sizeof(path),"%s/private-%s.sav",out,ready?"ready":"locked");FILE*f=fopen(path,"wb");assert(f&&fwrite(data,1,n,f)==n);fclose(f);free(data);
 snprintf(path,sizeof(path),"%s/private-%s.json",out,ready?"ready":"locked");f=fopen(path,"w");assert(f);fprintf(f,"{\"flags_offset\":%u,\"flag_ids\":[%u,%u,%u],\"ember\":[%u,%u],\"town\":[%u,%u]}\n",box(6),box(7),box(8),box(9),eg,em,tg,tm);fclose(f);
}
int main(int argc,char **argv){
 assert(argc==5);setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);mainAddr=strtoul(argv[3],0,0);callback=strtoul(argv[4],0,0)|1;
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);
 video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);struct VFile *f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));
 for(int ready=0;ready<2;ready++){
  c->reset(c);frames(500);c->busWrite32(c,mainAddr,0);c->busWrite32(c,0x0203ffc4,ready);command(0);frames(500);snapshot();
  unsigned group=box(5),map=box(6),townGroup=box(7),townMap=box(8);location(group,map,28,47);fixture(argv[2],ready,group,map,townGroup,townMap);
  walk(64);location(group,map,28,46);key(16);location(group,map,28,46);key(1);choice();key(2);finish();location(group,map,28,46);
  assert(box(14)==(ready?3:0));puts("PASS: declined return without movement or progression change");
  key(1);choice();key(1);finish();location(townGroup,townMap,21,8);assert(box(14)==(ready?3:0));capture(argv[2],ready?"return-ready":"return-without-gates");
  walk(64);location(townGroup,townMap,21,7);walk(128);location(townGroup,townMap,21,8);puts("PASS: native return and real walking on Cinnabar ground");
  key(32);location(townGroup,townMap,21,8);key(1);
  if(ready){choice();key(2);finish();location(townGroup,townMap,21,8);key(1);choice();key(1);finish();location(group,map,28,47);assert(box(14)==3);capture(argv[2],"reboarded");puts("PASS: declined then reboarded the production expedition boat");}
  else{finish();location(townGroup,townMap,21,8);assert(box(14)==0);puts("PASS: return remained available without opening outbound expedition gates");}
 }
 c->deinit(c);free(video);return 0;
}
