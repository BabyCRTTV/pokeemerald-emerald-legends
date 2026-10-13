#include "global.h"
#include "legends_appearance.h"
#include "constants/rgb.h"
#include "data/legends/male_front.h"

// One material-based portrait supplies the intro, wardrobe and Trainer Card.
// It reuses the existing front-picture buffers and never touches battle/world art.
enum { MATERIAL_COUNT = 29, HAIR_MID = 16, HAIR_LIGHT = 17, HAIR_DARK = 18 };
EWRAM_DATA static u16 sMaleFrontPalette[16] = {0};
EWRAM_DATA static u8 sMaterialSlots[MATERIAL_COUNT] = {0};
EWRAM_DATA static u8 sLastChoices[6] = {0};
EWRAM_DATA static u16 sLastSkin[3] = {0};
EWRAM_DATA static bool8 sPaletteReady = FALSE;
EWRAM_DATA static bool8 sPixelsReady = FALSE;

static const u16 sNativeColors[16] = {
    0x530E,0x677F,0x4A9B,0x3A19,0x296F,0x4DEC,0x4169,0x3506,
    0x28A3,0x779B,0x3B71,0x2E6C,0x2D9F,0x2118,0x7FFF,0,
};
static const u16 sHairColors[8][3] = {
    {RGB(17,11,7),RGB(23,16,10),RGB(8,5,4)},
    {RGB(6,6,7),RGB(12,12,14),RGB(2,2,3)},
    {RGB(10,6,5),RGB(17,11,8),RGB(5,3,2)},
    {RGB(15,9,6),RGB(23,15,10),RGB(7,4,3)},
    {RGB(17,6,4),RGB(26,12,7),RGB(7,2,2)},
    {RGB(21,13,6),RGB(29,22,11),RGB(10,6,3)},
    {RGB(26,20,11),RGB(31,28,20),RGB(13,9,4)},
    {RGB(18,20,23),RGB(28,29,31),RGB(7,8,11)},
};
static const u16 sShirtColors[5][2] = {
    {0x4DEC,0x4169},{0x3AB7,0x25F1},{0x6ECC,0x55E6},
    {0x0BDF,0x0235},{0x7A58,0x6171},
};
static const u16 sShoes[8][2] = {
    {0,0},{RGB(29,8,9),RGB(17,3,5)},{RGB(8,18,29),RGB(3,9,19)},
    {RGB(10,25,14),RGB(4,14,7)},{RGB(30,30,28),RGB(18,19,21)},
    {RGB(23,15,29),RGB(12,7,20)},{RGB(24,17,10),RGB(14,8,4)},
    {RGB(9,10,12),RGB(3,4,5)},
};
static const u16 sScarves[6] = {0,0x2118,0x6EAC,0x2EAA,0x7A58,0x679F};

static bool8 IsMalePortrait(enum TrainerPicID pic)
{
    if (LegendsGetCostume())
        return FALSE;
    if (!LegendsGetHair() && !LegendsGetHairColor() && !LegendsGetOutfit()
        && !LegendsGetJacketStyle() && !LegendsGetScarf() && !LegendsGetShoes())
        return FALSE; // Untouched Original keeps its native image and palette.
    if (pic >= TRAINER_PIC_LEGENDS_BRENDAN_EMERALD && pic < TRAINER_PIC_LEGENDS_ACCESSORY_0)
        return (pic - TRAINER_PIC_LEGENDS_BRENDAN_EMERALD) / LEGENDS_OUTFIT_COUNT == MALE;
    if (pic >= TRAINER_PIC_LEGENDS_ACCESSORY_0 && pic < TRAINER_PIC_LEGENDS_COSTUME_0)
        return ((pic - TRAINER_PIC_LEGENDS_ACCESSORY_0) / LEGENDS_OUTFIT_COUNT) % 2 == MALE;
    return FALSE;
}

static u32 Distance(u16 a, u16 b)
{
    s32 r=(a&31)-(b&31),g=((a>>5)&31)-((b>>5)&31),bl=((a>>10)&31)-((b>>10)&31);
    return r*r+g*g+bl*bl;
}

static u16 Shade(u16 color)
{
    return RGB((color&31)*2/3,((color>>5)&31)*2/3,((color>>10)&31)*2/3);
}

static u8 PixelMaterial(const u8 *body, u32 pixel, u8 hair, u8 shoes)
{
    u8 v=body[pixel];
    if (hair && pixel < 64*24)
        v=sMaleFrontHeads[(hair-1)*64*24+pixel];
    if (shoes)
    {
        u8 mask=sMaleFrontShoes[(shoes>=6 ? 4096 : 0)+pixel];
        if (mask)
            v=mask==3 ? 15 : mask==1 ? 22 : 23;
    }
    return v;
}

static const u8 *PreparePalette(void)
{
    u8 choices[6] = {LegendsGetOutfit(),LegendsGetJacketStyle(),LegendsGetScarf(),LegendsGetShoes(),LegendsGetHair(),LegendsGetHairColor()};
    const u8 *body;
    u16 materials[MATERIAL_COUNT],counts[MATERIAL_COUNT] = {0};
    static const u8 clothSlots[] = {6,10,11,12,13};
    static const u8 stableSlots[] = {5,8,14,15};
    u32 i,j,k;
    bool8 same=sPaletteReady;
    LegendsUpdateAppearancePalettes();
    for (i=0;i<6;i++)
        if (choices[i]!=sLastChoices[i])same=FALSE;
    for (i=0;i<3;i++)
        if (gLegendsTrainerPalettes[MALE][i+1]!=sLastSkin[i])same=FALSE;
    body=sMaleFrontBodies+(choices[0]*6+choices[1]*2+(choices[2]!=0))*4096;
    if (same)
        return body;
    sPixelsReady=FALSE;
    for (i=0;i<6;i++)sLastChoices[i]=choices[i];
    for (i=0;i<16;i++)materials[i]=sNativeColors[i];
    for (i=0;i<3;i++)
    {
        sLastSkin[i]=materials[i+1]=gLegendsTrainerPalettes[MALE][i+1];
        materials[HAIR_MID+i]=sHairColors[choices[5]][i];
    }
    materials[19]=choices[1]==2 ? RGB(4,11,7) : RGB(4,7,13);
    materials[20]=choices[1]==2 ? RGB(2,6,4) : RGB(2,4,8);
    materials[21]=sScarves[choices[2]];
    materials[22]=sShoes[choices[3]][0];materials[23]=sShoes[choices[3]][1];
    materials[24]=sShirtColors[choices[0]][0];materials[25]=sShirtColors[choices[0]][1];
    materials[26]=Shade(materials[21]);materials[27]=RGB(29,27,22);materials[28]=sNativeColors[5];
    for (i=0;i<16;i++)sMaleFrontPalette[i]=sNativeColors[i];
    for (i=1;i<=3;i++)sMaleFrontPalette[i]=materials[i];
    sMaleFrontPalette[4]=materials[16];sMaleFrontPalette[7]=materials[17];sMaleFrontPalette[9]=materials[18];
    // Clothing palette selection never sees skin or hair colors. It keeps
    // wardrobe hue stable when either choice changes. Eye blue/white/black
    // are fixed; the remaining five slots use weighted native clothing RGB.
    for (i=64*24;i<4096;i++)
        counts[PixelMaterial(body,i,choices[4],choices[3])]++;
    for (k=0;k<ARRAY_COUNT(clothSlots);k++)
    {
        u32 bestScore=0;u8 selected=5;
        for (i=4;i<MATERIAL_COUNT;i++)
        {
            u32 nearest=0xFFFFFFFF,score;
            if (!counts[i] || (i>=16 && i<=18))continue;
            for (j=0;j<ARRAY_COUNT(stableSlots);j++)
            {
                u32 d=Distance(materials[i],sMaleFrontPalette[stableSlots[j]]);
                if (d<nearest)nearest=d;
            }
            for (j=0;j<k;j++)
            {
                u32 d=Distance(materials[i],sMaleFrontPalette[clothSlots[j]]);
                if (d<nearest)nearest=d;
            }
            score=nearest*counts[i]*(i==10 || i==11 || i==12 || i==13 ? 3 : 1);
            if (score>bestScore){bestScore=score;selected=i;}
        }
        sMaleFrontPalette[clothSlots[k]]=materials[selected];
    }
    for (i=0;i<MATERIAL_COUNT;i++)
    {
        u32 best=0xFFFFFFFF;u8 slot=15;
        for (j=0;j<16;j++)
        {
            u32 d;
            if (j==0 || (j>=1 && j<=4) || j==7 || j==9)continue;
            d=Distance(materials[i],sMaleFrontPalette[j]);
            if (d<best){best=d;slot=j;}
        }
        sMaterialSlots[i]=slot;
    }
    sMaterialSlots[0]=0;
    for (i=1;i<=3;i++)sMaterialSlots[i]=i;
    sMaterialSlots[16]=4;sMaterialSlots[17]=7;sMaterialSlots[18]=9;
    sMaterialSlots[8]=8;sMaterialSlots[14]=14;sMaterialSlots[15]=15;sMaterialSlots[28]=5;
    sPaletteReady=TRUE;
    return body;
}

const u16 *LegendsMaleFrontPalette(enum TrainerPicID pic)
{
    if (!IsMalePortrait(pic))
        return NULL;
    PreparePalette();
    return sMaleFrontPalette;
}

void LegendsBuildMaleFront(u32 *picture, u8 *tiles)
{
    const u8 *body=PreparePalette();
    u8 hair=sLastChoices[4],shoes=sLastChoices[3];
    u32 x,y,i,pos;
    u8 *out=(u8 *)picture;
    if (sPixelsReady)
        return;
    for (y=0;y<64;y++)
        for (x=0;x<64;x+=2)
        {
            u32 index=((y>>3)*8+(x>>3))*32+(y&7)*4+(x&7)/2;
            tiles[index]=sMaterialSlots[PixelMaterial(body,y*64+x,hair,shoes)]
                | (sMaterialSlots[PixelMaterial(body,y*64+x+1,hair,shoes)]<<4);
        }
    picture[0]=0x00080010;
    pos=4;
    for (i=0;i<2048;i+=8)
    {
        u32 j;
        out[pos++]=0;
        for (j=0;j<8;j++)out[pos++]=tiles[i+j];
    }
    sPixelsReady=TRUE;
}
