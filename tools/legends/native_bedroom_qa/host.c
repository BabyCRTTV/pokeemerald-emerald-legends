#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
static void quiet(struct mLogger *l,int category,enum mLogLevel level,const char *format,va_list args) {}
static struct mLogger logger={.log=quiet};
static struct mCore *c; static color_t *video; static unsigned mainAddr, callback;
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned n){c->setKeys(c,n);frames(2);c->setKeys(c,0);frames(24);}
static void command(unsigned n,int count){c->busWrite32(c,0x0203fc00,n);c->busWrite32(c,mainAddr+4,callback);frames(count);}
static void capture(const char *folder,const char *name){char p[4096];snprintf(p,sizeof(p),"%s/%s.rgba",folder,name);FILE *f=fopen(p,"wb");assert(f);assert(fwrite(video,4,240*160,f)==240*160);fclose(f);puts(name);}
static unsigned profile(void){command(9,2);return c->busRead32(c,0x0203fc04);}
int main(int argc,char **argv){
 setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);assert(argc==5);mainAddr=strtoul(argv[3],NULL,0);callback=strtoul(argv[4],NULL,0);
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);
 mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);mCoreConfigSetDefaultIntValue(&c->config,"logLevel",0);c->loadConfig(c,&c->config);
 video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);
 struct VFile *f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));c->reset(c);frames(300);
 c->busWrite32(c,mainAddr,0);command(0,400);capture(argv[2],"male-default");
 command(6,350);capture(argv[2],"male-without-poster");
 command(7,350);capture(argv[2],"male-with-poster");
 command(2,40);capture(argv[2],"bedroom-decor-menu");
 key(128);key(128);key(128);key(1);capture(argv[2],"rug-color-menu");
 key(128);key(128);key(1);assert(profile()==0xb420);capture(argv[2],"rug-rose-menu");
 key(128);key(1);key(128);key(128);key(128);key(1);assert(profile()==0xb423);
 // B leaves the selected bed/rug colors intact.
 key(1);key(128);key(2);assert(profile()==0xb423);
 command(3,350);capture(argv[2],"male-rose-rug-mint-bed");
 command(9,2);assert(c->busRead32(c,0x0203fc08)==1&&c->busRead32(c,0x0203fc0c)==0);
 command(4,1200);printf("Flash save=%u load=%u profile=%x\n",c->busRead32(c,0x0203fc10),c->busRead32(c,0x0203fc14),c->busRead32(c,0x0203fc18));assert(c->busRead32(c,0x0203fc10)==1&&c->busRead32(c,0x0203fc14)==1&&c->busRead32(c,0x0203fc18)==0xb423);

 command(2,40);key(1);for(int i=0;i<6;i++)key(128);key(1);key(1);key(1);frames(100);
 capture(argv[2],"placing-doll-start");
 for(int i=0;i<4;i++)key(32);key(128);key(128);key(1);frames(80);
 capture(argv[2],"place-on-wood-prompt");key(1);frames(180);
 command(9,2);printf("Placed decoration=%u position=%x\n",c->busRead32(c,0x0203fc1c),c->busRead32(c,0x0203fc20));
 assert(c->busRead32(c,0x0203fc1c)==77&&c->busRead32(c,0x0203fc20)==7);
 command(4,1200);command(9,2);assert(c->busRead32(c,0x0203fc1c)==77&&c->busRead32(c,0x0203fc20)==7&&profile()==0xb423);
 command(3,350);capture(argv[2],"doll-on-wood-floor");
 command(1,400);capture(argv[2],"female-default");
 command(2,40);key(128);key(128);key(128);key(1);key(128);key(128);key(128);key(128);key(128);key(1);assert(profile()==0xb450);
 key(128);key(1);key(128);key(128);key(128);key(128);key(1);assert(profile()==0xb454);
 command(3,350);capture(argv[2],"female-plum-rug-gold-bed");
 command(5,350);capture(argv[2],"female-doll-on-wood-floor");
 command(6,350);capture(argv[2],"female-without-poster");
 command(7,350);capture(argv[2],"female-with-poster");
 // The original chair has the same seven-color picker as rug and bed.
 command(2,40);for(int i=0;i<5;i++)key(128);key(1);capture(argv[2],"chair-color-menu");
 for(int i=0;i<3;i++)key(128);key(1);
 command(9,2);assert(c->busRead32(c,0x0203fc24)==0xca03);
 key(1);key(64);key(2);command(9,2);assert(c->busRead32(c,0x0203fc24)==0xca03);
 command(4,1200);assert(c->busRead32(c,0x0203fc24)==0xca03);
 command(3,350);capture(argv[2],"female-mint-chair");
 command(8,350);key(64);key(1);frames(100);capture(argv[2],"female-chair-pc-access");
 command(0,400);command(2,40);for(int i=0;i<5;i++)key(128);key(1);
 key(128);key(128);key(1);command(9,2);assert(c->busRead32(c,0x0203fc24)==0xca02);
 command(3,350);capture(argv[2],"male-rose-chair");
 command(8,350);key(64);key(1);frames(100);capture(argv[2],"male-chair-pc-access");
 key(1);frames(80);capture(argv[2],"bedroom-pc-top-menu");
 key(128);key(128);key(1);frames(80);capture(argv[2],"decorate-from-bedroom-pc");
 c->deinit(c);free(video);return 0;
}
