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
static struct mCore *c;static color_t *video;static unsigned mainAddr,callback,controller,choices[3];static const char *out;
static unsigned box(int n){return c->busRead32(c,0x0203ffc0+n*4);}
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned k){c->setKeys(c,k);frames(3);c->setKeys(c,0);frames(42);}
static void command(int n){unsigned previous=c->busRead32(c,mainAddr+4);c->busWrite32(c,0x0203ffc0,n);c->busWrite32(c,0x0203ffd0,0);c->busWrite32(c,0x0203ffcc,previous);c->busWrite32(c,mainAddr+4,callback);frames(2);for(int i=0;i<1000&&!box(4);i++){c->busWrite32(c,mainAddr+4,callback);frames(1);}assert(box(4));}
static void capture(const char *name){char path[4096];snprintf(path,sizeof(path),"%s/%s.rgba",out,name);FILE *f=fopen(path,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);}
static void status(void){command(4);printf("first=%u partner=%u unlocked=%u outcome=%u battle=%u script=%u party=%u species=%u/%u identity=%x\n",box(5),box(6),box(7),box(8),box(9),box(10),box(11),box(12),box(13),box(14));}
static void menu(void){for(int i=0;i<40;i++){unsigned ptr=c->busRead32(c,controller);if(ptr==choices[0]||ptr==choices[1]||ptr==choices[2])return;key(1);frames(80);}capture("no-menu");assert(!"battle menu not reached");}
static void finish(int button){for(int i=0;i<100;i++){key(button);command(4);if(!box(9)&&!box(10))return;}status();capture("unfinished");assert(!"battle failed to return");}
static void roundtrip(int legacy){command(legacy?2:5);printf("flash=%u load=%u native=%u prefix=%u party=%u partner=%u Bag/season=%u\n",box(5),box(6),box(7),box(8),box(9),box(10),box(11));for(int i=5;i<=11;i++)assert(box(i)==1);}
static void battery(int choice,int outcome,const char*stage){void *data=NULL;size_t n=c->savedataClone(c,&data);assert(n==131072&&data);char p[4096];snprintf(p,sizeof(p),"%s/private-%d-%d-%s.sav",out,choice,outcome,stage);FILE*f=fopen(p,"wb");assert(f&&fwrite(data,1,n,f)==n);fclose(f);free(data);command(7);snprintf(p,sizeof(p),"%s/private-%d-%d-%s.json",out,choice,outcome,stage);f=fopen(p,"w");assert(f);fprintf(f,"{\"offset\":%u,\"first_hash\":%u,\"checksum\":%u,\"first_active\":%u,\"partner_active\":%u,\"unlocked\":%u,\"party\":%u}\n",box(5),box(6),box(7),box(8),box(9),box(10),box(11));fclose(f);}
static void challenge(unsigned index){c->busWrite32(c,0x0203ffc4,index);command(3);assert(box(5));frames(300);menu();status();assert(box(9));}
int main(int argc,char **argv){assert(argc==9);setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);out=argv[2];mainAddr=strtoul(argv[3],0,0);callback=strtoul(argv[4],0,0)|1;controller=strtoul(argv[5],0,0);for(int i=0;i<3;i++)choices[i]=strtoul(argv[6+i],0,0)|1;c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);struct VFile *f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));
 for(int choice=0;choice<2;choice++)for(int outcome=0;outcome<3;outcome++){
  c->reset(c);frames(500);c->busWrite32(c,mainAddr,0);c->busWrite32(c,0x0203ffc4,choice);command(0);frames(500);status();assert(box(5)&&!box(6)&&!box(7));roundtrip(1);if(outcome==0)battery(choice,outcome,"legacy");
  challenge(0);char name[80];snprintf(name,sizeof(name),"first-%d-%d",choice,outcome);capture(name);
  if(outcome==0){key(128);key(16);key(1);}else if(outcome==1){key(256);frames(700);}else{key(64);key(32);key(1);frames(80);key(1);frames(400);}
  finish(outcome==2?1:2);status();assert(box(6)&&box(7)&&box(12)!=box(13));if(outcome)assert(!box(5)&&box(8)==(outcome==1?7:1));else assert(box(5));
  unsigned active=box(5);roundtrip(0);battery(choice,outcome,"unlocked");challenge(1);snprintf(name,sizeof(name),"partner-%d-%d",choice,outcome);capture(name);key(256);frames(700);finish(2);status();assert(box(8)==7&&!box(6)&&box(7)&&box(5)==active);roundtrip(0);if(outcome==1)battery(choice,outcome,"resolved");roundtrip(0);status();assert(!box(6)&&box(7)&&box(5)==active);puts("PASS both species, first outcome, partner capture and persistent independent removal");
 }
 c->deinit(c);free(video);return 0;}
