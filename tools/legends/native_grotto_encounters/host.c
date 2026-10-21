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
static struct mCore *c;static color_t *video;static unsigned mainAddr,callback,controller,choices[3],save3Ptr;static const char *out;
static unsigned box(int n){return c->busRead32(c,0x0203ffc0+n*4);}
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned k){c->setKeys(c,k);frames(3);c->setKeys(c,0);frames(42);}
static void command(int n){unsigned previous=c->busRead32(c,mainAddr+4);c->busWrite32(c,0x0203ffc0,n);c->busWrite32(c,0x0203ffd0,0);c->busWrite32(c,0x0203ffcc,previous);c->busWrite32(c,mainAddr+4,callback);frames(2);for(int i=0;i<1000&&!box(4);i++){c->busWrite32(c,mainAddr+4,callback);frames(1);}assert(box(4));}
static void capture(const char *name){char path[4096];snprintf(path,sizeof(path),"%s/%s.rgba",out,name);FILE *f=fopen(path,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);}
static void status(void){command(4);printf("state=%u steps=%u identity=%x outcome=%u battle=%u script=%u party=%u hidden=%u caught=%u\n",box(5),box(6),box(7),box(8),box(9),box(10),box(11),box(12),box(13));printf("pp=%u battlefunc=%x controller=%x\n",box(14),box(15),c->busRead32(c,controller));}
static void setup(void){c->reset(c);frames(500);c->busWrite32(c,mainAddr,0);c->busWrite32(c,0x0203ffc4,0);c->busWrite32(c,0x0203ffc8,0);command(0);frames(500);command(1);assert(box(10)==9&&box(11)==9);}
static void menu(void){for(int i=0;i<30;i++){unsigned ptr=c->busRead32(c,controller);if(ptr==choices[0]||ptr==choices[1]||ptr==choices[2])return;key(1);frames(80);}capture("no-menu");assert(!"battle menu not reached");}
static void battery(const char *name,int legacy){void *data=NULL;size_t n=c->savedataClone(c,&data);assert(n==131072&&data);char p[4096];snprintf(p,sizeof(p),"%s/private-%s.sav",out,name);FILE *f=fopen(p,"wb");assert(f&&fwrite(data,1,n,f)==n);fclose(f);free(data);command(4);unsigned ptr=c->busRead32(c,save3Ptr)+716;snprintf(p,sizeof(p),"%s/private-%s.json",out,name);f=fopen(p,"w");assert(f);fprintf(f,"{\"checksum\":%u,\"state\":%u,\"steps\":%u,\"party\":%u}\n",legacy?0:c->busRead32(c,ptr+4),box(5),box(6),box(11));fclose(f);}
static void walkY(int y,unsigned direction){for(int i=0;i<5;i++){command(1);if(box(11)==(unsigned)y)return;key(direction);}assert(!"walking target not reached");}
static void challenge(void){for(int i=0;i<5;i++){command(1);printf("approach xy=%u,%u script=%u\n",box(10),box(11),box(12));if(box(11)<=7)break;key(64);}command(1);capture("approach");assert(box(10)==9&&box(11)==7);key(1);frames(100);capture("visitor-prompt");key(1);frames(300);menu();status();capture("battle");assert(box(9));}
static void finish(int button){for(int i=0;i<90;i++){key(button);command(4);if(!box(9)&&!box(10))return;}status();capture("unfinished");assert(!"battle failed to return to field");}
int main(int argc,char **argv){assert(argc==10);setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);out=argv[2];mainAddr=strtoul(argv[3],0,0);callback=strtoul(argv[4],0,0)|1;controller=strtoul(argv[5],0,0);save3Ptr=strtoul(argv[9],0,0);for(int i=0;i<3;i++)choices[i]=strtoul(argv[6+i],0,0)|1;c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);struct VFile *f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));
 setup();command(2);frames(500);printf("legacy save=%u load=%u prefix=%u party=%u bag/season=%u initialized=%u\n",box(5),box(6),box(7),box(8),box(9),box(10));assert(box(5)==1&&box(6)==1&&box(7)&&box(8)&&box(9)&&box(10));battery("legacy",1);command(3);frames(500);assert(box(5)==1&&box(6)==1&&box(7));battery("active",0);puts("PASS legacy and active actual flash round-trip");
 challenge();unsigned identity=box(7);key(128);key(16);key(1);finish(2);status();assert(box(8)==4&&box(5)==1&&box(7)==identity&&box(6)==0);puts("PASS actual escape retains visitor");
 setup();challenge();key(64);key(32);key(1);frames(80);key(1);frames(400);finish(1);status();capture("defeated-empty");assert(box(8)==1&&box(5)==2&&box(6)==4500&&box(12));puts("PASS actual KO starts cooldown and removes visitor");
 command(3);frames(500);assert(box(5)==1&&box(6)==1&&box(7));battery("cooldown",0);walkY(8,128);status();assert(box(6)==4499);c->busWrite32(c,0x0203ffc4,4498);command(5);assert(box(5)==2&&box(6)==1);c->busWrite32(c,0x0203ffc4,1);command(5);assert(box(5)==1&&box(6)==0);puts("PASS persisted cooldown expires exactly at 4500 and visibly respawns");frames(100);capture("refreshed");walkY(7,64);key(64);
 key(1);frames(100);key(1);frames(300);menu();status();assert(box(9));key(256);frames(700);finish(2);status();capture("captured-empty");assert(box(8)==7&&box(5)==2&&box(6)==4500&&box(11)==2&&box(13)>0);puts("PASS actual Master Ball capture, party award, cooldown and removal");
 command(3);frames(500);assert(box(5)==1&&box(6)==1&&box(7));battery("captured",0);puts("PASS capture state actual flash round-trip");c->deinit(c);free(video);return 0;}
