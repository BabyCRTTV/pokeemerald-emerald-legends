#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
static void quiet(struct mLogger *l,int c,enum mLogLevel v,const char *f,va_list a){}
static struct mLogger logger={.log=quiet};static struct mCore *c;static color_t *video;static unsigned mainAddr,qa,overworld,scene;static const char *out;
static unsigned box(int n){return c->busRead32(c,0x0203fc00+n*4);}
static void frames(int n){while(n--)c->runFrame(c);}
static void command(int n,int count){unsigned previous=c->busRead32(c,mainAddr+4);c->busWrite32(c,0x0203fc00,n);c->busWrite32(c,0x0203fc04,scene);c->busWrite32(c,0x0203fc78,0);c->busWrite32(c,0x0203fc7c,previous);c->busWrite32(c,mainAddr+4,qa);frames(count);for(int i=0;i<1000&&!box(30);i++)frames(1);assert(box(30));}
static void query(void){command(2,2);}
static void key(unsigned k){c->setKeys(c,k);frames(3);c->setKeys(c,0);frames(90);}
static void cap(int page){char p[4096];snprintf(p,sizeof(p),"%s/scene-%02u-page-%02d.rgba",out,scene,page);FILE *f=fopen(p,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);}
static void fail(const char *message){cap(99);fprintf(stderr,"scene %u: %s; script=%u menu=%u yesno=%u expected=%u cursor=%u\n",scene,message,box(3),box(4),box(5),box(6),box(7));exit(2);}
static void untilMenu(unsigned id){for(int i=0;i<30;i++){query();if(box(4)==id)return;if(box(4)||box(5))fail("unexpected menu before research root");key(1);}fail("root menu timeout");}
static void untilExpected(void){for(int i=0;i<30;i++){query();if(box(6))return;if(box(4)||box(5)||!box(3))fail("wrong branch before expected text");key(1);}fail("expected text timeout");}
int main(int argc,char **argv){
 assert(argc==8);setbuf(stdout,NULL);out=argv[2];mainAddr=strtoul(argv[3],0,0);qa=strtoul(argv[4],0,0)|1;overworld=strtoul(argv[5],0,0)|1;unsigned birch=strtoul(argv[6],0,0),devon=strtoul(argv[7],0,0);mLogSetDefaultLogger(&logger);
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);struct VFile *f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));
 for(scene=0;scene<23;scene++){
  c->reset(c);frames(650);c->busWrite32(c,mainAddr,0);command(0,400);
  for(int i=0;i<2000&&c->busRead32(c,mainAddr+4)!=overworld;i++)frames(1);assert(c->busRead32(c,mainAddr+4)==overworld);frames(260);query();assert(!box(16));unsigned before[8];for(int i=8;i<=15;i++)before[i-8]=box(i);
  command(1,90);
  if(scene<8){unsigned menu=scene<4?birch:devon;untilMenu(menu);key(128);key(128);query();if(box(4)!=menu||box(7)!=2)fail("did not select Research Notes");key(1);untilExpected();cap(0);
   int page=1;for(int i=0;i<30;i++){query();if(box(4)==menu)break;key(1);cap(page++);}query();if(box(4)!=menu)fail("research notes did not return to root");key(2);
  }else if(scene==8){untilExpected();cap(0);for(int i=0;i<12;i++){query();if(box(5)||box(4))fail("bulletin offered before rescue");if(!box(3))break;key(1);}
  }else if(scene<=13){for(int i=0;i<20;i++){query();if(box(5))break;key(1);}query();if(!box(5))fail("missing bulletin choice");if(scene==9){key(2);}else{key(1);untilExpected();cap(0);for(int i=0;i<10;i++){query();if(!box(3))break;key(1);cap(i+1);}}
  }else{untilExpected();cap(0);for(int i=0;i<10;i++){query();if(!box(3))break;key(1);cap(i+1);}}
  query();if(box(3)||box(4)||box(5))fail("dialogue failed to release");for(int i=8;i<=15;i++)if(before[i-8]!=box(i))fail("dialogue mutated journal, rewards, research or active season");printf("PASS scene %u: correct branch, closed dialogue and unchanged protected state\n",scene);
 }
 c->deinit(c);free(video);return 0;
}
