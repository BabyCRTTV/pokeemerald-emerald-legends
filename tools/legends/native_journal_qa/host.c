// Drive real journal tasks with emulated GBA keys and capture native video.
#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
static struct mCore *c;
static color_t *video;
static unsigned selected, top, detail;
static void frames(int n) { while (n--) c->runFrame(c); }
static void key(unsigned keys) { c->setKeys(c, keys); frames(2); c->setKeys(c, 0); frames(90); }
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
    assert(argc == 7);
    unsigned mainAddr = strtoul(argv[3], NULL, 0);
    selected = strtoul(argv[4], NULL, 0); top = strtoul(argv[5], NULL, 0); detail = strtoul(argv[6], NULL, 0);
    c = mCoreFind(argv[1]); assert(c && c->init(c)); mCoreInitConfig(c, NULL);
    mCoreConfigSetDefaultIntValue(&c->config, "skipBios", 1);
    mCoreConfigSetDefaultIntValue(&c->config, "logLevel", 0); c->loadConfig(c, &c->config);
    video = calloc(240 * 160, sizeof(color_t)); c->setVideoBuffer(c, video, 240);
    struct VFile *f = VFileOpen(argv[1], O_RDONLY); assert(f && c->loadROM(c, f)); c->reset(c); frames(300);
    c->busWrite32(c, mainAddr, 0); c->busWrite32(c, 0x0203fc00, 0);
    c->busWrite32(c, mainAddr + 4, 0x09f80001); frames(150);
    assert(c->busRead32(c, 0x0203fc0c) == 0);
    state(0, 0, 0); capture(argv[2], "quest-first");
    key(128); state(1, 0, 0); capture(argv[2], "quest-second");
    key(256); state(7, 2, 0); capture(argv[2], "quest-scrolled");
    key(1); state(7, 2, 1); capture(argv[2], "quest-detail");
    key(2); state(7, 2, 0); capture(argv[2], "quest-return");
    key(16); state(0, 0, 0); capture(argv[2], "quest-side");
    c->busWrite32(c, 0x0203fc00, 1); c->busWrite32(c, mainAddr + 4, 0x09f80001); frames(150);
    assert(c->busRead32(c, 0x0203fc04)); state(0, 0, 0); capture(argv[2], "achievement-claimed");
    key(128); state(1, 0, 0); capture(argv[2], "achievement-second");
    key(1); state(1, 0, 1); capture(argv[2], "achievement-detail");
    key(1); state(1, 0, 1); capture(argv[2], "achievement-claim-popup");
    frames(200); capture(argv[2], "achievement-claimed-status");
    key(2); state(1, 0, 0); capture(argv[2], "achievement-return");
    key(16); state(0, 0, 0); capture(argv[2], "achievement-ready");
    key(16); state(0, 0, 0); capture(argv[2], "achievement-claimed-filter");
    c->deinit(c); free(video); return 0;
}
