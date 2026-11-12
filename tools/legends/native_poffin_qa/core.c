#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <stdint.h>
#include <stdlib.h>
#include <fcntl.h>
static struct mCore*c;
static color_t video[240*160];
static void quiet(struct mLogger*l,int k,enum mLogLevel v,const char*f,va_list a){}
static struct mLogger logger={.log=quiet};
int init(const char*path){
 mLogSetDefaultLogger(&logger);c=mCoreFind(path);if(!c||!c->init(c))return 0;
 mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);mCoreLoadConfig(c);
 c->setVideoBuffer(c,video,240);struct VFile*f=VFileOpen(path,O_RDONLY);if(!f||!c->loadROM(c,f))return 0;
 c->reset(c);return 1;
}
void step(int frames,int k){c->setKeys(c,k);while(frames-->0)c->runFrame(c);}
void wr(unsigned int addr,unsigned int value){c->busWrite32(c,addr,value);}
unsigned int rd(unsigned int addr){return c->busRead32(c,addr);}
const void *screen(void){return video;}

#include <stdio.h>
int battery(const char *path)
{
    void *data = NULL;
    size_t size = c->savedataClone(c, &data);
    FILE *file = fopen(path, "wb");
    if (!file || !data)
        return 0;
    size_t written = fwrite(data, 1, size, file);
    fclose(file);
    free(data);
    return written == 131072;
}
int load_battery(const char *path)
{
    struct VFile *file = VFileOpen(path, O_RDWR);
    return file && c->loadSave(c, file);
}
void reset(void) { c->reset(c); }
