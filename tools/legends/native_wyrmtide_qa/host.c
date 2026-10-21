#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "paths.h"
static void quiet(struct mLogger*l,int c,enum mLogLevel v,const char*f,va_list a){}
static struct mLogger logger={.log=quiet};static struct mCore*c;static color_t*video;static unsigned mainAddr,callback,controller,choices[3],mapIds[8];static const char*out;static int scenesOnly;
static unsigned box(int n){return c->busRead32(c,0x0203ffc0+n*4);}static void frames(int n){while(n--)c->runFrame(c);}static void key(unsigned k){c->setKeys(c,k);frames(3);c->setKeys(c,0);frames(42);}
static void walk(unsigned k){c->setKeys(c,k);frames(12);c->setKeys(c,0);frames(30);}
static void command(int n){unsigned old=c->busRead32(c,mainAddr+4);c->busWrite32(c,0x0203ffc0,n);c->busWrite32(c,0x0203ffd0,0);c->busWrite32(c,0x0203ffcc,old);c->busWrite32(c,mainAddr+4,callback);frames(2);for(int i=0;i<1000&&!box(4);i++){c->busWrite32(c,mainAddr+4,callback);frames(1);}assert(box(4));}
static void status(void){command(1);printf("map=%u/%u xy=%u,%u flags=%02x maker=%u battle=%u script=%u party=%u outcome=%u\n",box(5),box(6),box(10),box(11),box(7),box(8),box(9),box(12),box(14),box(15));}
static void capture(const char*name){char path[4096];snprintf(path,sizeof(path),"%s/%s.rgba",out,name);FILE*f=fopen(path,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);}
static void setup(int scene,unsigned flags){c->reset(c);frames(500);c->busWrite32(c,mainAddr,0);c->busWrite32(c,0x0203ffc4,scene);c->busWrite32(c,0x0203ffc8,flags);command(0);frames(500);status();}
static void dismiss(int max){for(int i=0;i<max;i++){command(1);if(!box(12)&&!box(9))return;key(1);frames(55);}status();assert(!"script failed to finish");}
static void menu(void){for(int i=0;i<35;i++){unsigned p=c->busRead32(c,controller);if(p==choices[0]||p==choices[1]||p==choices[2])return;key(1);frames(70);}status();capture("battle-menu-timeout");assert(!"battle menu not reached");}
static void finish(int button){for(int i=0;i<100;i++){key(button);command(1);if(!box(9)&&!box(12)){frames(200);command(1);if(!box(9)&&!box(12))return;}}status();assert(!"battle failed to return");}
static void navigate(int grid,int targetX,int targetY){
 command(1);int width=widths[grid],size=sizes[grid],start=box(11)*width+box(10),target=targetY*width+targetX;
 int parent[986],queue[986],first=0,last=0;for(int i=0;i<size;i++)parent[i]=-1;
 queue[last++]=start;parent[start]=start;
 while(first<last&&parent[target]<0){int at=queue[first++],x=at%width;
  int near[4]={at-width,at+width,at-1,at+1};
  for(int k=0;k<4;k++){int n=near[k];if((k==2&&x==0)||(k==3&&x==width-1)||n<0||n>=size||parent[n]>=0||(grids[grid][n]&0xc00))continue;
   if((n==warps[grid][0]||n==warps[grid][1])&&n!=target)continue;
   parent[n]=at;queue[last++]=n;
  }
 }
 assert(parent[target]>=0);int reverse[986],count=0;
 for(int at=target;at!=start;at=parent[at])reverse[count++]=at;
 int at=start;while(count){int next=reverse[--count],delta=next-at;walk(delta==-width?64:delta==width?128:delta==-1?32:16);at=next;}
 frames(350);status();if(target!=warps[grid][0]&&target!=warps[grid][1])assert(box(10)==targetX&&box(11)==targetY);
}
int main(int argc,char**argv){assert(argc==10);setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);out=argv[2];mainAddr=strtoul(argv[3],0,0);callback=strtoul(argv[4],0,0)|1;controller=strtoul(argv[5],0,0);for(int i=0;i<3;i++)choices[i]=strtoul(argv[6+i],0,0)|1;scenesOnly=atoi(argv[9]);c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);struct VFile*f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));
 const char*names[]={"01-dewford-dock","02-island-landing","03-ancient-seal","04-stair-descent","05-second-landing","06-third-landing","07-fourth-landing","08-slumbering-regidrago"};
 for(int i=0;i<8;i++){setup(i,1);mapIds[i]=box(6);capture(names[i]);if(i==0){key(16);key(1);frames(130);key(1);frames(80);capture("01b-briney-voyage-menu");}}
 setup(9,1);key(64);key(1);frames(130);key(1);frames(100);capture("19-maker-inscription");key(1);frames(100);capture("20-maker-among-six");
 if(scenesOnly){puts("PASS native world scenes");c->deinit(c);free(video);return 0;}
 // Actual free movement invokes the production eight-step call hook.
 setup(8,0);for(int i=0;i<8;i++){walk(i%2?32:16);status();}frames(150);status();assert(box(12));key(1);frames(180);capture("09-unknown-number-call");dismiss(90);status();assert(box(7)&1);puts("PASS actual eight-step mystery call and one-time completion");command(3);assert(box(5)==1&&box(6)==1&&box(7));
 // Use Briney's real dialogue/menu and actual voyage warp.
 setup(0,1);command(4);assert(box(5)==1&&box(6)==1&&box(7)&&box(8)&&box(9)&&box(10));puts("PASS old Dewford cached-template flash/load repair preserves native NPCs");key(16);key(1);frames(130);key(1);frames(80);capture("10-departure-choice");key(1);frames(180);dismiss(25);frames(500);status();assert(box(6)==mapIds[1]&&(box(7)&2));capture("11-actual-arrival");
 navigate(4,10,18);key(64);key(1);dismiss(25);navigate(4,23,15);key(64);key(1);dismiss(25);navigate(4,19,21);key(64);key(1);dismiss(25);navigate(4,16,11);capture("21-walked-ruined-court");puts("PASS actual shore-to-all-three-tablets-to-seal walking route");
 // Party gate: no companion, an egg, then a fainted real Regigigas.
 setup(2,1);command(2);assert(!box(5));key(64);key(1);frames(120);capture("12-sealed-without-maker");dismiss(20);status();assert(!(box(7)&4)&&box(6)==mapIds[1]);
 c->busWrite32(c,0x0203ffc4,2);command(2);assert(!box(5));c->busWrite32(c,0x0203ffc4,3);command(2);assert(box(5));key(1);frames(120);
 for(int i=0;i<25;i++){command(1);if(box(7)&4)break;key(1);frames(60);}assert(box(7)&4);capture("13-maker-opens-seal");
 // Finish opening dialogue and enter via the actual choice.
 for(int i=0;i<20;i++){command(1);if(box(6)==mapIds[3])break;key(1);frames(100);}status();assert(box(6)==mapIds[3]);capture("14-first-descent-arrival");command(3);assert(box(5)==1&&box(6)==1&&box(7));puts("PASS party/egg/fainted gate, actual opening and first stair entry, native flash flags");
 // Traverse every descending and ascending stair warp using actual movement.
 for(int i=0;i<4;i++){navigate(i,11,20);assert(box(6)==mapIds[i<3?4+i:7]);}
 capture("14b-deepest-arrival");navigate(5,11,8);capture("22-walked-dragon-dais");navigate(5,11,17);frames(350);status();assert(box(6)==mapIds[6]);
 for(int i=3;i>=0;i--){navigate(i,8,3);assert(box(6)==mapIds[i?i+2:1]);}
 puts("PASS all four descent maps, both stair directions and surface exit");
 // Escape, defeat, then challenge the same native field sprite again.
 setup(7,1|4);key(64);key(1);frames(100);menu();key(128);key(16);key(1);finish(1);status();assert(box(15)==4&&!(box(7)&(16|32)));capture("15b-escaped-retry");
 key(1);frames(100);menu();key(64);key(32);key(1);frames(80);key(1);frames(400);finish(1);status();assert(box(15)==1&&(box(7)&16)&&!(box(7)&32));capture("15c-defeated-retry");
 key(1);frames(100);menu();key(128);key(16);key(1);finish(1);status();assert(box(15)==4&&!(box(7)&32));puts("PASS escape, defeat and actual same-sprite rematch");
 // Natural chamber interaction, real capture and no repeat award.
 setup(7,1|4);key(64);key(1);frames(150);capture("15-sleeping-dragon-prompt");menu();capture("16-regidrago-battle");key(256);frames(750);finish(1);status();assert((box(7)&(16|32))==(16|32)&&box(14)==2);capture("17-capture-resolved");command(3);assert(box(5)==1&&box(6)==1&&box(7));puts("PASS actual Regidrago capture, caught/calmed flags, party award and flash persistence");
 // A captured dragon cannot be challenged or awarded a second time.
 unsigned captured=box(14);key(1);frames(150);status();assert(!box(9)&&box(14)==captured);
 // Shore report and actual return/revisit remain available after calming it.
 setup(1,1|4|16);key(32);key(1);frames(130);dismiss(40);frames(350);status();capture("18-report-and-return");assert((box(7)&64)&&box(6)==mapIds[0]);puts("PASS Briney report, quest completion and actual return voyage");
 c->deinit(c);free(video);return 0;}
