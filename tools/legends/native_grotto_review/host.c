#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>

static void quiet(struct mLogger *l,int c,enum mLogLevel v,const char *f,va_list a) {}
static struct mLogger logger = {.log=quiet};
static struct mCore *c;
static color_t *video;
static unsigned mainAddr, callback;
static const char *output;
static int recording, recordFrames, recorded;
static unsigned box(int n) { return c->busRead32(c,0x0203ffc0+n*4); }
static void frames(int n) {
    while(n--) {
        c->runFrame(c);
        if(recording && recordFrames++ % 6 == 0) {
            char p[4096];snprintf(p,sizeof(p),"%s/discovery-%04d.rgba",output,recorded++);
            FILE *f=fopen(p,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);
        }
    }
}
static void key(unsigned k) { c->setKeys(c,k); frames(3); c->setKeys(c,0); frames(42); }
static void command(int n,int count) {
    unsigned previous=c->busRead32(c,mainAddr+4);
    c->busWrite32(c,0x0203ffc0,n); c->busWrite32(c,0x0203ffd0,0);
    c->busWrite32(c,0x0203ffcc,previous); c->busWrite32(c,mainAddr+4,callback);
    frames(count); for(int i=0;i<1000&&!box(4);i++) {
        c->busWrite32(c,mainAddr+4,callback); frames(1);
    }
    if(!box(4)) fprintf(stderr,"callback timeout command=%d current=%x qa=%x\n",n,c->busRead32(c,mainAddr+4),callback);
    assert(box(4));
}
static void capture(const char *out,int room,int season,const char *label) {
    char p[4096]; snprintf(p,sizeof(p),"%s/room-%d-season-%d-%s.rgba",out,room,season,label);
    FILE *f=fopen(p,"wb"); assert(f&&fwrite(video,4,240*160,f)==240*160); fclose(f);
}
int main(int argc,char **argv) {
    assert(argc==5); setbuf(stdout,NULL); mLogSetDefaultLogger(&logger);
    output=argv[2];
    mainAddr=strtoul(argv[3],0,0); callback=strtoul(argv[4],0,0)|1;
    c=mCoreFind(argv[1]); assert(c&&c->init(c)); mCoreInitConfig(c,NULL);
    mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1); c->loadConfig(c,&c->config);
    video=calloc(240*160,sizeof(color_t)); c->setVideoBuffer(c,video,240);
    struct VFile *f=VFileOpen(argv[1],O_RDONLY); assert(f&&c->loadROM(c,f));
    unsigned leafGroup=0, leafMap=0;
    for(int room=0;room<3;room++) for(int season=0;season<4;season++) {
        c->reset(c); frames(500); c->busWrite32(c,mainAddr,0);
        c->busWrite32(c,0x0203ffc4,room); c->busWrite32(c,0x0203ffc8,season);
        command(0,500); command(1,2);
        printf("room=%d season=%d active=%u map=%u,%u floor=%u xy=%u,%u gfx=%u/%u\n",
            room,season,box(7),box(5),box(6),box(9),box(10),box(11),box(8),box(13));
        assert(box(7)==season&&box(9)==0&&box(10)==11&&box(11)==11&&box(8)==box(13));
        unsigned group=box(5), map=box(6);
        if(room==0){leafGroup=group;leafMap=map;}
        capture(argv[2],room,season,"overview");
        if(season==0) {
            for(int i=0;i<5&&box(11)>9;i++){key(64);command(1,2);}
            assert(box(10)==11&&box(11)==9);
            key(1); command(1,2); assert(box(12)); capture(argv[2],room,season,"visitor");
            for(int i=0;i<8&&box(12);i++) {key(1);command(1,2);} assert(!box(12));
            for(int i=0;i<12;i++) {key(128);command(1,2);if(box(5)!=group||box(6)!=map) break;}
            frames(250);command(1,2);assert(box(5)!=group||box(6)!=map);
            capture(argv[2],room,season,"exit");
            // Entry approaches face the inspected tree/cliff/bush.
            unsigned outsideGroup=box(5), outsideMap=box(6);
            key(room==1?32:64);key(1);frames(90);capture(argv[2],room,season,"entrance");command(1,2);
            for(int i=0;i<8&&box(12);i++){key(2);command(1,2);}
            assert(!box(12)&&box(5)==outsideGroup&&box(6)==outsideMap);
            key(1);key(1);key(1);key(1);frames(300);command(1,2);
            printf("reentry room=%d map=%u,%u xy=%u,%u script=%u\n",room,box(5),box(6),box(10),box(11),box(12));
            assert(box(5)==group&&box(6)==map&&!box(12));
            capture(argv[2],room,season,"reentry");
        }
    }
    command(2,500);command(1,2);
    assert(box(10)==13&&box(11)==35&&!box(12));
    capture(argv[2],0,0,"discovery-start");
    recording=1;frames(45);
    for(int i=0;i<6&&box(11)>32;i++){key(64);command(1,2);}
    assert(box(10)==13&&box(11)==32);
    frames(45);key(64);key(1);command(1,2);assert(box(12));
    frames(90);capture(argv[2],0,0,"discovery-clue");
    key(1);frames(90);capture(argv[2],0,0,"discovery-choice");
    key(1);frames(320);command(1,2);assert(box(5)==leafGroup&&box(6)==leafMap&&!box(12));
    capture(argv[2],0,0,"discovery-inside");frames(90);recording=0;
    printf("PASS: filmed native approach, examine, confirm and entry; %d original frames.\n",recorded);
    c->deinit(c);free(video);puts("PASS: twelve seasonal scenes, native movement and visitor dialogue.");
}
