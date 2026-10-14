// Drive real journal tasks with emulated GBA keys and capture native video.
#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static struct mCore *c;
static color_t *video;
static unsigned selected, top, detail;
static void frames(int n) { while (n--) c->runFrame(c); }
static void key(unsigned keys) { c->setKeys(c, keys); frames(2); c->setKeys(c, 0); frames(40); }
static void state(unsigned s, unsigned t, unsigned d)
{
    assert(c->busRead16(c, selected) == s);
    assert(c->busRead16(c, top) == t);
    assert(c->busRead8(c, detail) == d);
}
static void capture(const char *folder, const char *name)
{
    char path[4096]; snprintf(path, sizeof(path), "%s/%s.rgba", folder, name);
    FILE *out = fopen(path, "wb"); assert(out && sizeof(color_t) == 4);
    assert(fwrite(video, sizeof(color_t), 240 * 160, out) == 240 * 160);
    fclose(out); printf("%s: selected=%u top=%u detail=%u\n", name,
        c->busRead16(c, selected), c->busRead16(c, top), c->busRead8(c, detail));
}
int main(int argc, char **argv)
{
    assert(argc == 8);
    unsigned noticeWindow = strtoul(argv[7], NULL, 0);
    unsigned mainAddr = strtoul(argv[3], NULL, 0);
    selected = strtoul(argv[4], NULL, 0); top = strtoul(argv[5], NULL, 0); detail = strtoul(argv[6], NULL, 0);
    c = mCoreFind(argv[1]); assert(c && c->init(c)); mCoreInitConfig(c, NULL);
    mCoreConfigSetDefaultIntValue(&c->config, "skipBios", 1);
    mCoreConfigSetDefaultIntValue(&c->config, "logLevel", 0); c->loadConfig(c, &c->config);
    video = calloc(240 * 160, sizeof(color_t)); c->setVideoBuffer(c, video, 240);
    struct VFile *f = VFileOpen(argv[1], O_RDONLY); assert(f && c->loadROM(c, f)); c->reset(c); frames(300);
    c->busWrite32(c, mainAddr, 0); c->busWrite32(c, 0x0203fc00, 0);
    c->busWrite32(c, mainAddr + 4, 0x09f80001); frames(350);
    assert(c->busRead8(c,noticeWindow)==0);
    capture(argv[2], "field-before");
    c->busWrite32(c, 0x0203fc00, 1); c->busWrite32(c, mainAddr + 4, 0x09f80001); frames(10);
    assert(c->busRead32(c, 0x0203fc04)==1 && c->busRead32(c, 0x0203fc08)==0);
    assert(c->busRead8(c,noticeWindow)!=0);
    capture(argv[2], "unlock-notice");
    unsigned position=c->busRead32(c,0x0203fc10),before=c->busRead32(c,position);
    color_t panel[144*32];
    for(int y=0;y<32;y++)memcpy(panel+y*144,video+(8+y)*240+8,144*sizeof(color_t));
    unsigned stableFrames=0,moved=0;
    c->setKeys(c, 16);
    for(int i=0;i<210;i++){
        c->runFrame(c);
        if(c->busRead8(c,noticeWindow)){
            for(int y=0;y<32;y++)assert(!memcmp(panel+y*144,video+(8+y)*240+8,144*sizeof(color_t)));
            stableFrames++;
        }
        if(i%6==0){char name[64];snprintf(name,sizeof(name),"animation-%02d",i/6);capture(argv[2],name);}
        if(c->busRead32(c,position)!=before)moved=1;
        if(i==23)c->setKeys(c,128);
        if(i==47)c->setKeys(c,32);
        if(i==71)c->setKeys(c,64);
        if(i==95)c->setKeys(c,0);
        if(i==60)assert(c->busRead8(c,noticeWindow)!=0);
    }
    assert(moved);
    assert(c->busRead8(c,noticeWindow)==0);
    assert(stableFrames>=150);
    printf("Pixel-stable visible banner frames: %u (movement included).\n",stableFrames);
    capture(argv[2], "field-after");
    c->busWrite32(c, 0x0203fc00, 2); c->busWrite32(c, mainAddr + 4, 0x09f80001); frames(90);
    for(int i=0;i<13;i++)key(256);key(128);key(128);state(80,75,0);
    key(1);state(80,75,1);capture(argv[2], "manual-claim");
    key(1);state(80,75,1);assert(c->busRead8(c,c->busRead32(c,0x0203fc0c)+34)&1);capture(argv[2], "reward-sent");
    frames(180);capture(argv[2], "reward-claimed");
    key(2);key(256);state(86,81,0);capture(argv[2], "new-achievements");
    c->deinit(c); free(video); return 0;
}
