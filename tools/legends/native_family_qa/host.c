// Uses libmgba to inspect native diagnostic buffers, not simulated C output.
#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv)
{
    assert(argc == 5);
    unsigned mainAddr = strtoul(argv[3], NULL, 0), pal = strtoul(argv[4], NULL, 0);
    struct mCore *c = mCoreFind(argv[1]);
    assert(c && c->init(c));
    mCoreInitConfig(c, NULL);
    mCoreConfigSetDefaultIntValue(&c->config, "skipBios", 1);
    mCoreConfigSetDefaultIntValue(&c->config, "logLevel", 0);
    c->loadConfig(c, &c->config);
    color_t *video = calloc(240 * 160, sizeof(color_t));
    c->setVideoBuffer(c, video, 240);
    struct VFile *f = VFileOpen(argv[1], O_RDONLY);
    assert(f && c->loadROM(c, f));
    c->reset(c);
    for (int i = 0; i < 300; i++) c->runFrame(c);
    c->busWrite32(c, mainAddr, 0); // isolate callback1 from the title scene
    c->busWrite32(c, 0x0203fc00, 0);
    c->busWrite32(c, mainAddr + 4, 0x09f80001);
    FILE *out = fopen(argv[2], "wb");
    assert(out);
    unsigned previous = 0;
    for (int tick = 0; tick < 1000 && previous < 10; tick++)
    {
        c->runFrame(c);
        unsigned progress = c->busRead32(c, 0x0203fc00);
        if (progress == previous) continue;
        assert(progress == previous + 1);
        unsigned box[19];
        for (int i = 0; i < 19; i++) box[i] = c->busRead32(c, 0x0203fc00 + i * 4);
        assert(box[3] < 64 && box[4] < 64 && box[5] < 64);
        assert(box[6] < 16 && box[7] < 16 && box[8] < 16);
        assert(box[6] != box[7] && box[6] != box[8] && box[7] != box[8]);
        assert(box[15] < 16 && box[16] < 16 && box[15] != box[16]);
        assert(box[17] == (progress - 1) % 5 && box[18] == 1 + (progress - 1) % 5);
        assert(box[12] == box[6] && box[13] == box[7] && box[14] == 255);
        fwrite(box, 4, 19, out);
        for (int i = 0; i < 512; i++) fputc(c->busRead8(c, pal + 512 + i), out);
        for (int j = 9; j <= 10; j++)
        {
            unsigned data = c->busRead32(c, box[j]);
            assert(c->busRead8(c, box[j] + 6));
            for (int i = 0; i < 2304; i++) fputc(c->busRead8(c, data + i), out);
        }
        for (int i = 0; i < 32; i++) fputc(c->busRead8(c, box[11] + i), out);
        printf("Round %u: parent slots %u/%u, NPC4 slot %u; reflection/wardrobe/full-slot assertions passed.\n", progress, box[6], box[7], box[8]);
        fflush(stdout);
        previous = progress;
    }
    assert(previous == 10);
    fclose(out); c->deinit(c); free(video);
    return 0;
}
