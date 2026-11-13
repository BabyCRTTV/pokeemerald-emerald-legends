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
static struct mLogger logger={.log=quiet};static struct mCore*c;static color_t*video;
static unsigned mainAddr,callback,controller,choices[3],mapIds[6],yesNo,whiteout;static const char*out;
static unsigned box(int n){return c->busRead32(c,0x0203ffc0+n*4);}
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned k){c->setKeys(c,k);frames(3);c->setKeys(c,0);frames(42);}
static void walk(unsigned k){c->setKeys(c,k);frames(12);c->setKeys(c,0);frames(30);}
static void command(int n){unsigned old=c->busRead32(c,mainAddr+4);c->busWrite32(c,0x0203ffc0,n);c->busWrite32(c,0x0203ffd0,0);c->busWrite32(c,0x0203ffcc,old);c->busWrite32(c,mainAddr+4,callback);frames(2);for(int i=0;i<1000&&!box(4);i++){c->busWrite32(c,mainAddr+4,callback);frames(1);}assert(box(4));}
static void status(void){command(1);printf("map=%u/%u xy=%u,%u flags=%02x wing=%u battle=%u script=%u party=%u outcome=%u state=%x\n",box(5),box(6),box(10),box(11),box(7),box(8),box(9),box(12),box(14),box(15),box(13));}
static void capture(const char*name){char p[4096];snprintf(p,sizeof(p),"%s/%s.rgba",out,name);FILE*f=fopen(p,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);}
static void setup(int scene,unsigned mask){c->reset(c);frames(500);c->busWrite32(c,mainAddr,0);c->busWrite32(c,0x0203ffc4,scene);c->busWrite32(c,0x0203ffc8,mask);command(0);frames(500);c->busWrite32(c,0x0203ffc8,yesNo);status();}
static void dismiss(int max){for(int i=0;i<max;i++){command(1);if(!box(12)&&!box(9))return;key(1);frames(55);}status();capture("failure-dialogue");assert(!"script failed to finish");}
static void menu(void){for(int i=0;i<45;i++){unsigned p=c->busRead32(c,controller);if(p==choices[0]||p==choices[1]||p==choices[2])return;key(1);frames(70);}status();capture("failure-battle-menu");assert(!"battle menu not reached");}
static void finish(int button){for(int i=0;i<160;i++){key(button);if(c->busRead32(c,mainAddr+4)==whiteout)frames(200);command(1);if(!box(9)&&!box(12)){frames(200);command(1);if(!box(9)&&!box(12))return;}}status();capture("failure-battle-return");assert(!"battle failed to return");}
static int isWarp(int grid,int at){for(int i=0;i<warp_counts[grid];i++)if(at==warps[grid][i])return 1;return 0;}
static void navigate(int grid,int tx,int ty){
 command(1);int width=widths[grid],size=sizes[grid],start=box(11)*width+box(10),target=ty*width+tx;
 unsigned story=box(7);int parent[4096],queue[4096],first=0,last=0;assert(start>=0&&start<size&&target>=0&&target<size);for(int i=0;i<size;i++)parent[i]=-1;queue[last++]=start;parent[start]=start;
 while(first<last&&parent[target]<0){int at=queue[first++],x=at%width;int near[4]={at-width,at+width,at-1,at+1};for(int k=0;k<4;k++){int n=near[k];if((k==2&&x==0)||(k==3&&x==width-1)||n<0||n>=size||parent[n]>=0||((grids[grid][n]&0xc00)&&!(n==target&&isWarp(grid,n))))continue;if(grid==5&&!(story&64)&&n%width>=11&&n%width<=13&&n/width>=21&&n/width<=22)continue;if(grid==1&&n==5*width+8&&(!(story&1)||(story&32)))continue;if(isWarp(grid,n)&&n!=target)continue;parent[n]=at;queue[last++]=n;}}
 if(parent[target]<0){printf("No path grid%d %d,%d to%d,%d\n",grid,start%width,start/width,tx,ty);capture("failure-no-path");}assert(parent[target]>=0);
 int reverse[4096],count=0;for(int at=target;at!=start;at=parent[at])reverse[count++]=at;
 int at=start;while(count){int next=reverse[--count],delta=next-at;walk(delta==-width?64:delta==width?128:delta==-1?32:16);at=next;}
 for(int wi=0;wi<warp_counts[grid];wi++)if(target==warps[grid][wi]&&warp_dirs[grid][wi])walk(warp_dirs[grid][wi]);
 frames(220);status();if(!isWarp(grid,target)){if(box(10)!=(unsigned)tx||box(11)!=(unsigned)ty)capture("failure-walking");assert(box(10)==(unsigned)tx&&box(11)==(unsigned)ty);}
}
static void flash(void){command(3);assert(box(5)==1&&box(6)==1&&box(7));}
static void untilYes(void){for(int i=0;i<60;i++){command(1);if(box(13)){frames(12);return;}key(1);frames(50);}capture("failure-yesno");assert(!"yes/no prompt not reached");}
static void challenge(void){key(32);key(1);untilYes();key(1);frames(130);menu();}
int main(int argc,char**argv){
 assert(argc==11);setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);out=argv[2];yesNo=strtoul(argv[9],0,0)|1;whiteout=strtoul(argv[10],0,0)|1;mainAddr=strtoul(argv[3],0,0);callback=strtoul(argv[4],0,0)|1;controller=strtoul(argv[5],0,0);for(int i=0;i<3;i++)choices[i]=strtoul(argv[6+i],0,0)|1;
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);mCoreLoadConfig(c);video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);struct VFile*f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));
 if(getenv("LEGENDS_NIGHTMARE_BED_ONLY")){
  setup(1,1);unsigned home=box(6);navigate(1,8,5);key(64);key(1);frames(150);capture("03-miras-slumber");dismiss(20);command(1);assert(box(6)==home&&!(box(7)&8));
  setup(1,7);navigate(1,8,5);key(64);key(1);untilYes();key(1);frames(400);status();assert(box(6)!=home&&(box(7)&8));unsigned dream=box(6);
  navigate(3,6,4);key(64);key(1);dismiss(25);navigate(3,8,5);key(64);key(1);untilYes();key(1);frames(400);status();assert(box(6)==home);
  setup(1,63);navigate(1,9,4);key(32);key(1);untilYes();key(1);frames(400);status();assert(box(6)==dream&&(box(7)&32));
  puts("PASS bed-only native sleeping interaction, wing entry, moved chair, safe waking and resolved side revisit");c->deinit(c);free(video);return 0;
 }
 for(int i=0;i<6;i++){setup(i,7);mapIds[i]=box(6);}
 setup(1,0);capture("00-before-the-call");
 setup(6,0);for(int i=0;i<10;i++)walk(i%2?16:32);status();assert(!(box(7)&1)&&!box(12));puts("PASS no call before a successful Regidrago outcome");
 setup(6,1<<16);for(int i=0;i<8;i++)walk(i%2?16:32);frames(150);status();assert(box(12));capture("01-unknown-number");key(1);frames(100);capture("01b-fathers-plea");key(1);frames(140);capture("01c-elias-and-briney");key(1);frames(140);capture("01d-daughter-wont-wake");dismiss(80);status();assert(box(7)&1);
 for(int i=0;i<10;i++)walk(i%2?16:32);status();assert(!box(12));flash();puts("PASS native eight-step one-time call and persisted progress");
 setup(0,1);command(5);frames(650);status();assert(box(6)==mapIds[0]&&box(10)==50&&box(11)==16);walk(16);walk(32);status();assert(box(10)==50&&box(11)==16);puts("PASS older-style Lilycove wall-position flash/load and real Continue relocation");navigate(0,50,15);assert(box(6)==mapIds[1]);navigate(1,6,5);key(64);key(1);frames(150);capture("02-father-at-the-bedside");dismiss(55);status();assert(box(7)&2);
 navigate(1,8,5);key(64);key(1);frames(150);capture("03-miras-slumber");dismiss(20);status();assert(!(box(7)&4));
 // Both visible doorway lanes work, with the original Lilycove warps retained.
 for(int x=5;x<=6;x++){navigate(1,x,9);assert(box(6)==mapIds[0]);navigate(0,50,15);assert(box(6)==mapIds[1]);}
 puts("PASS native new-house door, father investigation, bed and both exit lanes");
 setup(2,3);key(64);key(1);frames(150);capture("04-mt-pyre-caretaker");dismiss(85);status();assert((box(7)&4)&&box(8));flash();assert(box(8)&&box(9));
 key(1);dismiss(25);flash();assert(box(8)&&box(9));puts("PASS actual Lunar Wing key item and unchanged Cleanse Tag grant, no duplicate wing, native flash save/load");
 setup(1,7);navigate(1,8,5);key(64);key(1);untilYes();capture("05-lunar-wing-at-the-bed");
 // Select NO on the real native yes/no task, after all dialogue pages finish.
 key(128);key(1);dismiss(20);status();assert(box(6)==mapIds[1]&&!(box(7)&8));
 key(1);untilYes();key(1);frames(400);status();assert(box(6)==mapIds[3]&&(box(7)&8));capture("06-empty-dream-bedroom");
 navigate(3,6,4);key(64);key(1);frames(160);capture("06b-the-empty-chair");dismiss(25);
 navigate(3,5,9);assert(box(6)==mapIds[4]);capture("07-deserted-lilycove");navigate(4,53,18);key(64);key(1);frames(150);capture("08-miras-echo");dismiss(35);status();assert(box(7)&16);
 navigate(4,55,15);assert(box(6)==mapIds[5]);capture("09-the-wrong-door");navigate(5,14,22);capture("10-moonless-shore");challenge();capture("11-darkrai-battle");
 // A real capture ends the dream and returns to the home, not a reset fixture.
 key(256);frames(750);finish(1);status();assert(box(6)==mapIds[1]&&(box(7)&96)==96&&box(14)==2);capture("12-mira-awakens");
 key(16);key(1);frames(150);capture("13-miras-return");dismiss(40);navigate(1,6,5);key(64);key(1);frames(150);capture("14-fathers-thanks");dismiss(40);status();assert(box(7)&128);flash();puts("PASS actual bed-to-dream-room-to-street-to-shore walking, echo, Darkrai capture, awakening and father completion");
 setup(5,127);navigate(5,12,22);puts("PASS caught Darkrai is absent and its full footprint is walkable on revisit");
 // Fleeing leaves Mira asleep and Darkrai available.
 setup(5,31);challenge();key(128);key(16);key(1);finish(1);status();assert(box(6)==mapIds[5]&&box(15)==4&&!(box(7)&96));capture("15-escape-retry");
 // Defeat releases Mira but deliberately preserves a later capture opportunity.
 command(4);
 challenge();key(64);key(32);key(1);frames(80);key(1);frames(400);finish(1);status();assert(box(6)==mapIds[1]&&box(15)==1&&(box(7)&32)&&!(box(7)&64));capture("16-defeat-also-wakes-mira");flash();
 navigate(1,9,4);key(32);key(1);untilYes();key(1);frames(400);status();assert(box(6)==mapIds[3]);puts("PASS escape, defeat awakening, retained catch opportunity and post-resolution dream revisit");
 // Dream bed is an explicit early exit: no battle or reward required.
 navigate(3,8,5);key(64);key(1);untilYes();key(1);frames(400);status();assert(box(6)==mapIds[1]);puts("PASS safe wake-up route from the dream bedroom");
 // Both forest passages from the shore lead back to the same wrong door.
 for(int x=14;x<=15;x++){setup(5,31);navigate(5,x,5);assert(box(6)==mapIds[4]);}
 puts("PASS both native shore exit lanes");
 setup(5,31);command(2);challenge();key(1);frames(70);key(1);frames(600);finish(1);status();assert(box(15)==2&&!(box(7)&96));capture("17-blackout-safe");flash();puts("PASS actual loss/blackout preserves unfinished quest and wing");
 puts("PASS complete native Nightmare progression and retry suite");c->deinit(c);free(video);return 0;
}
