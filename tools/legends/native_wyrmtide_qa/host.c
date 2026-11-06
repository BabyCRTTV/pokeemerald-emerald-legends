#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba/core/blip_buf.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "paths.h"
static void quiet(struct mLogger*l,int c,enum mLogLevel v,const char*f,va_list a){}
static struct mLogger logger={.log=quiet};static struct mCore*c;static color_t*video;static unsigned mainAddr,callback,controller,choices[3],mapIds[8];static const char*out;static int scenesOnly;
static int recording,audioReady;static FILE *movieVideo,*movieAudio,*movieNotes;static unsigned movieTicks,movieFrames,movieSamples;
static unsigned box(int n){return c->busRead32(c,0x0203ffc0+n*4);}static void frames(int n){while(n--){c->runFrame(c);
 if(audioReady){blip_t*l=c->getAudioChannel(c,0),*r=c->getAudioChannel(c,1);int count=blip_samples_avail(l);assert(count==blip_samples_avail(r)&&count<=4096);short samples[8192];blip_read_samples(l,samples,count,1);blip_read_samples(r,samples+1,count,1);if(recording){assert(fwrite(samples,4,count,movieAudio)==count);movieSamples+=count;}}
 if(recording){if(movieTicks%2==0){assert(fwrite(video,4,240*160,movieVideo)==240*160);movieFrames++;}movieTicks++;}
 }}static void key(unsigned k){c->setKeys(c,k);frames(3);c->setKeys(c,0);frames(42);}
static void walk(unsigned k){c->setKeys(c,k);frames(12);c->setKeys(c,0);frames(recording?8:30);}
static void command(int n){if(recording)assert(n==1);unsigned old=c->busRead32(c,mainAddr+4);c->busWrite32(c,0x0203ffc0,n);c->busWrite32(c,0x0203ffd0,0);c->busWrite32(c,0x0203ffcc,old);c->busWrite32(c,mainAddr+4,callback);frames(2);for(int i=0;i<1000&&!box(4);i++){c->busWrite32(c,mainAddr+4,callback);frames(1);}assert(box(4));}
static void status(void){command(1);printf("map=%u/%u xy=%u,%u flags=%02x maker=%u battle=%u script=%u party=%u outcome=%u\n",box(5),box(6),box(10),box(11),box(7),box(8),box(9),box(12),box(14),box(15));}
static void capture(const char*name){char path[4096];snprintf(path,sizeof(path),"%s/%s.rgba",out,name);FILE*f=fopen(path,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);}
static void setup(int scene,unsigned flags){assert(!recording);c->reset(c);frames(500);c->busWrite32(c,mainAddr,0);c->busWrite32(c,0x0203ffc4,scene);c->busWrite32(c,0x0203ffc8,flags);command(0);frames(500);status();}
static void dismiss(int max){for(int i=0;i<max;i++){command(1);if(!box(12)&&!box(9))return;key(1);frames(55);}status();assert(!"script failed to finish");}
static void menu(void){for(int i=0;i<35;i++){unsigned p=c->busRead32(c,controller);if(p==choices[0]||p==choices[1]||p==choices[2])return;key(1);frames(70);}status();capture("battle-menu-timeout");assert(!"battle menu not reached");}
static void finish(int button){for(int i=0;i<100;i++){key(button);command(1);if(!box(9)&&!box(12)){frames(200);command(1);if(!box(9)&&!box(12))return;}}status();assert(!"battle failed to return");}
static int isWarp(int grid,int at){for(int i=0;i<warp_counts[grid];i++)if(at==warps[grid][i])return 1;return 0;}
static void navigate(int grid,int targetX,int targetY){
 command(1);int width=widths[grid],size=sizes[grid],start=box(11)*width+box(10),target=targetY*width+targetX;
 int parent[986],queue[986],first=0,last=0;for(int i=0;i<size;i++)parent[i]=-1;
 queue[last++]=start;parent[start]=start;
 while(first<last&&parent[target]<0){int at=queue[first++],x=at%width;
  int near[4]={at-width,at+width,at-1,at+1};
  for(int k=0;k<4;k++){int n=near[k];if((k==2&&x==0)||(k==3&&x==width-1)||n<0||n>=size||parent[n]>=0||(grids[grid][n]&0xc00))continue;
   if(isWarp(grid,n)&&n!=target)continue;
   parent[n]=at;queue[last++]=n;
  }
 }
 assert(parent[target]>=0);int reverse[986],count=0;
 for(int at=target;at!=start;at=parent[at])reverse[count++]=at;
 int stairSteps=0;for(int i=0;i<count;i++)if(((grids[grid][reverse[i]]&1023)>=0x3b1&&(grids[grid][reverse[i]]&1023)<=0x3b8)||(grids[grid][reverse[i]]&1023)==0x3c7)stairSteps++;
 if(grid<4&&targetX==11&&targetY==20&&(start==3*width+8||start==4*width+8)){// The tidal gallery now has one two-cell flight plus the two-cell exit;
  // the other landings retain two short flights plus that exit.
  static const int minimumSteps[]={6,4,6,6};assert(stairSteps>=minimumSteps[grid]);printf("PASS descent %d route crosses %d native stair cells\n",grid+1,stairSteps);}
 int at=start;while(count){int next=reverse[--count],delta=next-at;walk(delta==-width?64:delta==width?128:delta==-1?32:16);at=next;}
 for(int wi=0;wi<warp_counts[grid];wi++)if(target==warps[grid][wi]&&warp_dirs[grid][wi])walk(warp_dirs[grid][wi]);
 frames(recording?(isWarp(grid,target)?180:20):350);status();if(!isWarp(grid,target))assert(box(10)==targetX&&box(11)==targetY);
}
static FILE*movieFile(const char*name){char path[4096];snprintf(path,sizeof(path),"%s/%s",out,name);FILE*f=fopen(path,"wb");assert(f);return f;}
static void startMovie(void){assert(!recording);movieVideo=movieFile("walkthrough-video.raw");movieAudio=movieFile("walkthrough-audio.raw");movieNotes=movieFile("walkthrough-chapters.txt");movieTicks=movieFrames=movieSamples=0;recording=1;}
static void note(const char*title){fprintf(movieNotes,"%u|%s\n",movieTicks,title);fflush(movieNotes);}
static void stopMovie(void){assert(recording);recording=0;fclose(movieVideo);fclose(movieAudio);fclose(movieNotes);FILE*f=movieFile("walkthrough-recording.json");fprintf(f,"{\"emulatedFrames\":%u,\"videoFrames\":%u,\"audioSamples\":%u,\"sampleRate\":48000,\"videoFrameStep\":2,\"noResetsDuringRecording\":true}\n",movieTicks,movieFrames,movieSamples);fclose(f);}
static void readTablet(void){key(64);key(1);frames(180);dismiss(30);frames(30);}
static void tour(void){
 setup(10,1|2|4);startMovie();note("Cave entrance");frames(120);
 navigate(4,16,11);walk(64);frames(180);status();assert(box(6)==mapIds[3]);
 note("First chamber - upper stairwell");capture("31-upper-stairwell");frames(90);
 navigate(0,8,8);frames(60);navigate(0,12,12);frames(45);navigate(0,6,17);frames(45);
 navigate(0,13,19);note("First chamber inscription");readTablet();navigate(0,11,20);assert(box(6)==mapIds[4]);
 note("Tidal gallery - upper stairwell");frames(60);navigate(1,11,8);frames(120);navigate(1,6,12);frames(60);navigate(1,12,17);frames(90);navigate(1,11,20);assert(box(6)==mapIds[5]);
 note("Third chamber - descending terraces");frames(60);navigate(2,12,10);frames(45);navigate(2,6,15);frames(45);navigate(2,13,19);readTablet();navigate(2,11,20);assert(box(6)==mapIds[6]);
 note("Fourth chamber - final descent");frames(60);navigate(3,9,10);frames(90);navigate(3,9,16);frames(90);navigate(3,11,20);assert(box(6)==mapIds[7]);
 note("Regidrago sanctuary");frames(90);navigate(5,11,5);note("Final inscription");readTablet();navigate(5,11,9);key(64);frames(180);capture("32-sanctuary-walkthrough-end");note("Sleeping Regidrago - end of cavern walkthrough");stopMovie();
 puts("PASS continuous entrance-to-Regidrago walkthrough with native audio and no scene resets");
}
int main(int argc,char**argv){assert(argc==10);setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);out=argv[2];mainAddr=strtoul(argv[3],0,0);callback=strtoul(argv[4],0,0)|1;controller=strtoul(argv[5],0,0);for(int i=0;i<3;i++)choices[i]=strtoul(argv[6+i],0,0)|1;scenesOnly=atoi(argv[9]);c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);mCoreConfigSetDefaultIntValue(&c->config,"volume",256);mCoreConfigSetDefaultIntValue(&c->config,"mute",0);mCoreLoadConfig(c);video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);struct VFile*f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));
 if(scenesOnly==3){audioReady=1;c->setAudioBufferSize(c,4096);blip_set_rates(c->getAudioChannel(c,0),c->frequency(c),48000);blip_set_rates(c->getAudioChannel(c,1),c->frequency(c),48000);}
 const char*names[]={"01-dewford-dock","02-island-landing","03-ancient-seal","04-stair-descent","05-second-landing","06-third-landing","07-fourth-landing","08-slumbering-regidrago"};
 for(int i=0;i<8;i++){setup(i,1);mapIds[i]=box(6);capture(names[i]);if(i==0){key(16);key(1);frames(130);key(1);frames(80);capture("01b-briney-voyage-menu");}}
 setup(10,1|4);capture("23-open-headland-entrance");
 setup(9,1);key(64);key(1);frames(130);key(1);frames(100);capture("19-maker-inscription");key(1);frames(100);capture("20-maker-among-six");
 setup(4,1);navigate(1,11,8);capture("26-tidal-pool");frames(16);capture("27-tidal-pool-animation");
 setup(4,1);navigate(1,6,12);capture("28-stone-stair-flight");
 setup(6,1);navigate(3,9,10);capture("29-wide-stone-flight");
 setup(6,1);navigate(3,9,6);c->setKeys(c,128);
 for(int i=0;i<24;i++){char name[64];frames(4);snprintf(name,sizeof(name),"30-descending-%02d",i);capture(name);}
 c->setKeys(c,0);frames(40);command(1);assert(box(6)==mapIds[6]&&box(11)>8);puts("PASS actual southward walking descent captured through the upper flight");
 setup(3,1|4);navigate(0,8,4);capture("33-recessed-upper-passage");navigate(0,11,19);key(128);frames(30);capture("34-south-exit-approach");
 setup(3,1|4);navigate(0,13,19);key(64);capture("45-clean-lower-exit");
 setup(7,1|4);command(7);assert(!box(5)&&box(6)==64&&box(7)==64&&box(8)==2048&&box(9)==0x0e00&&box(10)==0x1176&&box(11)==32);capture("35-large-regidrago");navigate(5,11,16);capture("36-sanctuary-exit");
 setup(3,1|4);navigate(0,8,8);key(64);key(1);frames(160);capture("37-threshold-inscription");key(1);frames(100);capture("38-threshold-lore");dismiss(30);
 setup(4,1|4);navigate(1,12,17);key(64);key(1);frames(160);capture("39-tidal-inscription");key(1);frames(100);capture("40-tidal-lore");dismiss(30);
 setup(5,1|4);navigate(2,13,19);key(64);key(1);frames(160);capture("41-deep-inscription");key(1);frames(100);capture("42-deep-lore");dismiss(30);
 if(scenesOnly==3)tour();
 if(scenesOnly==1){puts("PASS native world scenes");c->deinit(c);free(video);return 0;}
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
 capture("14b-deepest-arrival");navigate(5,11,5);key(64);key(1);dismiss(25);puts("PASS actual walking and reading of the final inscription");navigate(5,11,9);capture("22-walked-dragon-dais");navigate(5,11,17);frames(350);status();assert(box(6)==mapIds[6]);
 for(int i=3;i>=0;i--){if(i==0||i==2){navigate(i,13,19);key(64);key(1);dismiss(25);}navigate(i,8,3);assert(box(6)==mapIds[i?i+2:1]);}
 puts("PASS all four descent maps, both stair directions, both depth inscriptions and surface exit");
 // Walk through the actual opened map doorway, independently of the seal's
 // dialogue-driven entry, then return through the native stair warp.
 walk(64);frames(350);status();assert(box(6)==mapIds[3]);capture("24-walked-open-entrance");
 // Native map-warp entry lands on the return tile; step off before re-entry.
 walk(128);navigate(0,8,3);assert(box(6)==mapIds[1]);capture("25-returned-through-entrance");
 puts("PASS actual open-door walking entry and native stair return");
 for(int i=0;i<4;i++){setup(3+i,1|4);walk(128);navigate(i,9,3);assert(box(6)==mapIds[i?i+2:1]);}
 puts("PASS both active columns of all four widened upper return stairwells");
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
 // Actual non-repelled controller walking must trigger a native encounter on every floor.
 for(int room=0;room<4;room++){
  setup(11+room,1|4);command(5);assert(box(7)==8);
  int steps;for(steps=0;steps<600;steps++){walk(steps%2?64:128);command(1);if(box(9))break;}assert(steps<600);frames(180);menu();
  command(5);assert(box(11));unsigned species=box(5),level=box(6);int match=0;
  for(int slot=0;slot<12;slot++){c->busWrite32(c,0x0203ffc4,slot);command(5);if(species==box(8)&&level>=box(9)&&level<=box(10))match=1;}assert(match);
  char name[64];snprintf(name,sizeof(name),"43-wild-floor-%d",room+1);capture(name);printf("PASS floor%d actual walking encounter after%d steps, species%u level%u, native live roster match\n",room+1,steps+1,species,level);
  key(128);key(16);key(1);finish(1);status();assert(box(15)==4&&!(box(7)&(16|32)));
 }
 // A controlled seed selects the real 4% dragon slot through production generation.
 setup(11,1|4);command(6);assert(box(5)<8192);frames(180);menu();capture("44-rare-dragon-encounter");c->busWrite32(c,0x0203ffc4,8);command(5);assert(box(5)==box(8)&&box(6)>=box(9)&&box(6)<=box(10)&&box(11));printf("PASS native table-generated rare dragon preview, species%u level%u\n",box(5),box(6));key(128);key(16);key(1);finish(1);
 c->deinit(c);free(video);return 0;}
