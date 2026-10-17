// Run an unmodified Legends Debug ROM in the actual mGBA 0.10.x core.
// Buttons only. No game RAM, save data or code is patched by this host.
#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void quiet(struct mLogger *logger, int category, enum mLogLevel level, const char *fmt, va_list args)
{
    (void)logger; (void)category; (void)level; (void)fmt; (void)args;
}
static struct mLogger logger = { .log = quiet };

static void frames(struct mCore *core, int count)
{
    for (int i = 0; i < count; i++)
        core->runFrame(core);
}

static void tap(struct mCore *core, unsigned int keys, int releaseFrames)
{
    core->setKeys(core, keys);
    frames(core, 4);
    core->setKeys(core, 0);
    frames(core, releaseFrames);
}

static void capture(const char *directory, const char *name, const color_t *buffer)
{
    char file[4096];
    assert(snprintf(file, sizeof(file), "%s/%s.rgba", directory, name) < (int)sizeof(file));
    FILE *output = fopen(file, "wb");
    assert(output);
    assert(fwrite(buffer, sizeof(color_t), 240 * 160, output) == 240 * 160);
    assert(fclose(output) == 0);
}

int main(int argc, char *argv[])
{
    // args: ROM, output directory, gMain symbol, CB2_Overworld symbol.
    assert(argc == 5);
    setbuf(stdout, NULL);
    const unsigned int gMain = strtoul(argv[3], NULL, 0);
    const unsigned int overworld = strtoul(argv[4], NULL, 0) | 1u;
    mLogSetDefaultLogger(&logger);
    struct mCore *core = mCoreFind(argv[1]);
    assert(core && core->init(core));
    mCoreInitConfig(core, NULL);
    mCoreConfigSetDefaultIntValue(&core->config, "skipBios", 1);
    core->loadConfig(core, &core->config);
    color_t *video = calloc(240 * 160, sizeof(color_t));
    assert(video);
    core->setVideoBuffer(core, video, 240);
    struct VFile *rom = VFileOpen(argv[1], O_RDONLY);
    assert(rom && core->loadROM(core, rom));
    core->reset(core);

    // Do not use quickstart's direct memory hooks. Press the same SELECT
    // key a human uses at the native Debug title screen.
    frames(core, 900);
    int foundOverworld = 0;
    for (int i = 0; i < 48; i++)
    {
        if (core->busRead32(core, gMain + 4) == overworld)
        {
            foundOverworld = 1;
            break;
        }
        tap(core, 4u, 90); // GBA SELECT: native debug Quickstart.
    }
    printf("booted_overworld=%d callback=%08x expected=%08x\n",
           foundOverworld, core->busRead32(core, gMain + 4), overworld);
    if (!foundOverworld)
    {
        capture(argv[2], "debug-boot-diagnostic", video);
        core->deinit(core);
        free(video);
        return 2;
    }

    frames(core, 250);
    capture(argv[2], "living-hoenn-gameplay", video);
    for (int i = 0; i < 10; i++)
        tap(core, 1u, 45);  // A: dismiss any new-game messages naturally.
    frames(core, 150);
    capture(argv[2], "living-hoenn-interaction", video);
    puts("mGBA native Debug quickstart reached a live overworld without ROM or RAM mutation.");
    core->deinit(core);
    free(video);
    return 0;
}
