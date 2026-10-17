// mGBA native emulator renders actual Legends game frames with private QA state.
// Direct video-buffer captures, no image compositing or text rendering by host.
#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
static void quiet(struct mLogger *log, int category, enum mLogLevel level, const char *format, va_list args)
{ (void)log; (void)category; (void)level; (void)format; (void)args; }
static struct mLogger logger={.log=quiet};
static struct mCore *core;
static color_t *screen;
static unsigned gMain, qa, overworld;
static const char *output;
static const char *names[] = {"birch-research","devon-research","weather-bulletin","littleroot-champion"};
static void frames(unsigned n){while(n--)core->runFrame(core);}
static unsigned box(unsigned n){return core->busRead32(core,0x0203fc00+4*n);}
static void command(unsigned code,unsigned scene,unsigned frameCount)
{
    unsigned original=core->busRead32(core,gMain+4);
    core->busWrite32(core,0x0203fc00,code);
    core->busWrite32(core,0x0203fc04,scene);
    core->busWrite32(core,0x0203fc78,0);
    core->busWrite32(core,0x0203fc7c,original);
    core->busWrite32(core,gMain+4,qa);
    frames(frameCount);
    assert(box(30)==1 && "Injected private QA dispatcher did not acknowledge command");
}
static void key(unsigned k)
{
    core->setKeys(core,k);
    frames(3);
    core->setKeys(core,0);
    frames(130);
}
static void cap(unsigned scene,unsigned step)
{
    char path[512];
    snprintf(path,sizeof(path),"%s/%s-%02u.rgba",output,names[scene],step);
    FILE *f=fopen(path,"wb");
    assert(f&&fwrite(screen,4,240*160,f)==240*160);
    fclose(f);
    printf("capture %s-%02u callback=%08x\n",names[scene],step,core->busRead32(core,gMain+4));
}
int main(int argc,char **argv)
{
    assert(argc==6);
    setbuf(stdout,NULL);
    output=argv[2]; gMain=strtoul(argv[3],0,0);
    qa=strtoul(argv[4],0,0)|1;overworld=strtoul(argv[5],0,0)|1;
    mLogSetDefaultLogger(&logger);
    core=mCoreFind(argv[1]);assert(core&&core->init(core));
    mCoreInitConfig(core,NULL);
    mCoreConfigSetDefaultIntValue(&core->config,"skipBios",1);
    core->loadConfig(core,&core->config);
    screen=calloc(240*160,sizeof(color_t));
    assert(screen);core->setVideoBuffer(core,screen,240);
    struct VFile *rom=VFileOpen(argv[1],O_RDONLY);assert(rom&&core->loadROM(core,rom));
    for(unsigned scene=0;scene<4;scene++)
    {
        core->reset(core);frames(360);
        command(0,scene,6);
        unsigned ready=0;
        for(unsigned x=0;x<2000;x++)
        {
            frames(1);
            if(core->busRead32(core,gMain+4)==overworld){ready=1;break;}
        }
        printf("scene %u overworld=%u callback=%08x\n",scene,ready,core->busRead32(core,gMain+4));
        if(!ready) {cap(scene,98);return 3;}
        frames(250);
        cap(scene,0);
        command(1,scene,3);
        frames(170);
        cap(scene,1);
        for(unsigned i=0;i<6;i++){key(1);cap(scene,i+2);} // real A through dialogue pages
        // Research panels are the third option; test UP/DOWN via real native input.
        if(scene<2)
        {
            key(128);cap(scene,8);  // DOWN
            key(128);cap(scene,9);  // DOWN
            key(1);cap(scene,10);   // A on Research Notes
            for(unsigned i=0;i<7;i++){key(1);cap(scene,11+i);}
        }
        else if(scene==2)
        {
            // Scientist's YES is the default; A advances native bulletin page.
            for(unsigned i=0;i<5;i++){key(1);cap(scene,8+i);}
        }
        else {key(1);cap(scene,8);}
    }
    core->deinit(core);free(screen);
    puts("Private mGBA scenarios ran using the original Legends maps/scripts.");
    return 0;
}
