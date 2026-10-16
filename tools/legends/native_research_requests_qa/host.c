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
static unsigned mainAddr,callback;static const char *out;
static void frames(int n){while(n--)c->runFrame(c);}
static unsigned box(int n){return c->busRead32(c,0x0203fc00+4*n);}
static void command(int n,int count){unsigned prev=c->busRead32(c,mainAddr+4);c->busWrite32(c,0x0203fc78,0);c->busWrite32(c,0x0203fc7c,prev);c->busWrite32(c,0x0203fc00,n);c->busWrite32(c,mainAddr+4,callback);frames(count);for(int i=0;i<200&&!box(30);i++)frames(1);assert(box(30));frames(2);}
static void key(unsigned k){c->setKeys(c,k);frames(2);c->setKeys(c,0);frames(90);}
static void cap(const char *name);
static void profile(void){command(1,2);assert(box(10)==3&&box(11)==2&&box(12)==3&&box(13)==1&&box(14)==3);if(box(19)!=0||box(20)){fprintf(stderr,"Bad placement x=%u y=%u collision=%u noclip=%u lab=%u devon=%u script=%u\n",box(17),box(18),box(19),box(20),box(39),box(40),box(6));cap("placement-failure");}assert(box(19)==0&&!box(20));}
static void cap(const char *name){char p[4096];snprintf(p,sizeof(p),"%s/%s.rgba",out,name);FILE *f=fopen(p,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);printf("capture %s active=%u menu=%u yesno=%u\n",name,box(1),box(7),box(8));}
static void untilMenu(unsigned menu){for(int n=0;n<65;n++){profile();if(box(7)==menu){frames(30);return;}assert(!box(8));key(1);}fprintf(stderr,"menu timeout expected=%u got=%u\n",menu,box(7));abort();}
static void untilYes(void){for(int n=0;n<120;n++){profile();if(box(8)){frames(30);return;}assert(!box(7));key(1);}cap("yes-timeout");fprintf(stderr,"YesNo timed out script=%u menu=%u lab=%u devon=%u\n",box(6),box(7),box(39),box(40));abort();}
static void endTalk(void){for(int n=0;n<70;n++){profile();if(!box(6)&&!box(7)&&!box(8))return;key(2);}cap("end-timeout");fprintf(stderr,"EndTalk timed out script=%u menu=%u lab=%u devon=%u\n",box(6),box(7),box(39),box(40));abort();}
static void talk(void){key(64);key(1);untilMenu(1);}
static void requests(void){key(1);untilMenu(2);}
static void choose(int row){for(int n=0;n<row;n++)key(128);key(1);untilYes();}
static void battery(const char *name){void *data=NULL;size_t n=c->savedataClone(c,&data);assert(n==131072&&data);char p[4096];snprintf(p,sizeof(p),"%s/%s.sav",out,name);FILE *f=fopen(p,"wb");assert(f&&fwrite(data,1,n,f)==n);fclose(f);free(data);}
int main(int argc,char **argv){
 setbuf(stdout,NULL);assert(argc==7);out=argv[2];mainAddr=strtoul(argv[3],NULL,0);callback=strtoul(argv[4],NULL,0);mLogSetDefaultLogger(&logger);
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);
 video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);struct VFile *f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));c->reset(c);frames(300);c->busWrite32(c,mainAddr,0);
 c->busWrite32(c,0x0203fc74,strtoul(argv[5],NULL,0)|1);c->busWrite32(c,0x0203fc70,strtoul(argv[6],NULL,0)|1);
 command(0,400);profile();assert(box(1)==65535&&box(2)==65535&&box(21));unsigned appearance=box(9);
 command(2,1200);profile();assert(box(15)==1&&box(16)==1&&box(9)==appearance&&box(2)==65535);battery("private-legacy");
 char path[4096];snprintf(path,sizeof(path),"%s/offsets.txt",out);FILE *ofs=fopen(path,"w");assert(ofs);fprintf(ofs,"%u %u %u\n",box(24),box(25),box(41));fclose(ofs);
 if(!getenv("RESEARCH_ONLY")){
 talk();cap("birch-main-menu");requests();cap("six-requests");
 choose(2);cap("accept-berry-request");key(1);endTalk();profile();assert(box(1)==2&&box(5)==35);cap("accepted-berry-request");
 command(2,1200);profile();assert(box(15)==1&&box(16)==1&&box(1)==2&&box(5)==35&&box(9)==appearance);battery("private-active");
 // Actual native pause/journal UI, then return to Birch without changing the pin.
 key(8);cap("tracked-pause");key(16);key(1);key(16);key(128);key(1);cap("side-request-details");key(2);key(8);key(2);profile();assert(box(1)==2);
 talk();key(1);untilMenu(3);cap("active-request-menu");key(128);key(1);untilYes();cap("abandon-confirmation");
 key(2);untilMenu(1);profile();assert(box(1)==2); // Cancel confirmation keeps the work.
 key(1);untilMenu(3);key(128);key(1);untilYes();key(1);untilMenu(1);profile();assert(box(1)==65535&&box(3)==0&&box(21)&&box(5)==65535);
 requests();cap("available-after-abandon");choose(2);key(1);endTalk();profile();assert(box(1)==2);
 // Native full-PC path retains all three samples and the pending request.
 command(6,2);talk();key(1);untilMenu(3);key(1);untilMenu(1);profile();assert(box(1)==2&&box(21)&&!box(3));cap("full-storage-retry");
 endTalk();command(7,2);talk();key(1);untilMenu(3);key(1);untilMenu(1);profile();assert(box(1)==65535&&box(3)==4&&!box(21)&&box(23));
 requests();cap("completed-request-marker");key(128);key(128);key(1);untilMenu(2);profile();assert(box(1)==65535&&box(3)==4&&box(23));endTalk();
 command(2,1200);profile();assert(box(15)==1&&box(16)==1&&box(3)==4&&box(23)&&box(9)==appearance);battery("private-completed");
 puts("Selection, confirmed/cancelled abandonment, retry, full-PC atomic samples, one-time reward and real flash persistence passed.");
 // Actual habitat arrivals with a qualifying partner; no collision disabling.
 for(unsigned id=1;id<=3;id+=2){command(3,2);c->busWrite32(c,0x0203fc68,id);command(4,400);profile();assert(box(27)==0&&box(1)==id&&box(4)==1);command(2,1200);profile();assert(box(4)==1&&box(15)==1&&box(16)==1);command(5,400);profile();assert(box(4)==1);}
 // The actual Pokédex handoff includes the new invitation before rival gifts.
 command(8,400);profile();assert(!box(22));command(9,100);
 for(int n=0;n<55;n++){profile();if(!box(6))break;char name[48];snprintf(name,sizeof(name),"pokedex-invitation-%02d",n);cap(name);key(1);}
 profile();assert(box(22)&&!box(6)&&box(1)==65535);puts("Native Pokédex invitation, rival gift continuation, habitat arrivals and saved observations passed.");

 }
 // v0.0.58 request state is readable and upgrades only on a successful report.
 command(13,400);profile();assert(box(1)==2&&box(2)==0xb703&&box(3)==0x23&&box(32)==0xdead&&box(33)==0xbeef);
 command(2,1200);profile();assert(box(15)==1&&box(16)==1&&box(2)==0xb703&&box(32)==0xdead);battery("private-v58-active");
 talk();key(1);untilMenu(3);key(1);untilMenu(1);profile();assert(box(1)==65535&&box(2)==0xb800&&box(3)==0x27&&!box(32)&&box(33)==0xbeef);
 command(2,1200);profile();assert(box(3)==0x27&&box(2)==0xb800);battery("private-v59-migrated");endTalk();
 // Birch's new groups reveal future work and explain its story requirement.
 command(17,400);talk();key(1);untilMenu(5);cap("birch-research-groups");key(128);key(1);untilMenu(2);cap("birch-story-locked");
 key(1);cap("birch-locked-hint");untilMenu(2);endTalk();
 // The earliest calm lab scene offers an optional branch before the rival errand.
 command(14,400);untilYes();key(128);key(1);untilYes();cap("first-lab-research-offer");key(1);untilYes();key(1);endTalk();profile();assert(box(39)==3&&!box(22));
 command(14,400);untilYes();key(128);key(1);untilYes();key(128);key(1);untilYes();key(1);endTalk();profile();assert(box(39)==3&&!box(22));
 puts("Both Birch early invitation branches passed.");
 // Full original Devon introduction, including letter, PokeNav, healing and optional explanation.
 command(10,400);untilYes();cap("devon-first-research-offer");key(1);endTalk();profile();assert(box(36)&&box(37)&&box(40)==1);cap("devon-story-continued");
 command(10,400);untilYes();key(128);key(1);endTalk();profile();assert(box(36)&&box(37)&&box(40)==1);
 // A Birch report cannot be accepted at Devon or replaced by a second contract.
 command(11,400);profile();assert(box(19)==0);command(15,2);profile();assert(box(27)==0&&box(1)==18);command(5,400);talk();key(1);key(1);untilMenu(1);profile();assert(box(1)==18);cap("other-researcher-busy");endTalk();command(16,2);
 command(18,400);profile();assert(box(27)==0&&box(1)==18&&box(4)==1);command(2,1200);profile();assert(box(4)==1&&box(15)==1&&box(16)==1);command(5,400);profile();assert(box(4)==1);command(16,2);profile();assert(!box(4));
 // Devon's twelfth contract stays locked despite Champion status until all eleven are complete.
 command(11,400);key(16);key(1);untilMenu(4);cap("devon-main-menu");key(1);untilMenu(6);cap("devon-contract-groups");key(128);key(1);untilMenu(2);cap("devon-final-locked");
 for(int i=0;i<5;i++)key(128);key(1);key(1);cap("devon-final-requirements");untilMenu(2);profile();assert(box(1)==65535&&!box(34));endTalk();
 // Controlled prior-eleven completion fixture; accept and report final project through native UI.
 command(12,2);key(16);key(1);untilMenu(4);key(1);untilMenu(6);key(128);key(1);untilMenu(2);cap("devon-final-available");choose(5);cap("devon-final-accept");key(1);endTalk();profile();assert(box(1)==29&&box(5)==62);
 command(2,1200);profile();assert(box(1)==29&&box(32)==0x1ffc);battery("private-v59-master-active");
 command(6,2);key(16);key(1);untilMenu(4);key(1);untilMenu(3);key(1);untilMenu(4);profile();assert(box(1)==29&&!box(34)&&box(32)==0x1ffc);endTalk();
 command(7,2);key(16);key(1);untilMenu(4);key(1);untilMenu(3);key(1);cap("devon-twelfth-report");for(int n=0;n<20;n++){profile();if(box(7)==4)break;char name[48];snprintf(name,sizeof(name),"devon-master-reward-%02d",n);cap(name);key(1);}untilMenu(4);profile();assert(box(1)==65535&&box(34)&&!box(35)&&box(32)==0x3ffc);endTalk();
 command(2,1200);profile();assert(box(15)==1&&box(16)==1&&box(34)&&!box(35)&&box(32)==0x3ffc);battery("private-v59-master-completed");
 key(16);key(1);untilMenu(4);key(1);untilMenu(6);key(128);key(1);untilMenu(2);cap("devon-twelve-completed");for(int i=0;i<5;i++)key(128);key(1);untilMenu(2);profile();assert(box(34)&&!box(35));endTalk();
 puts("Native first-meeting Yes/No branches, story gates, owner restrictions, v58 migration and one-time Master Ball/full-PC/flash checks passed.");
 c->deinit(c);free(video);return 0;
}
