#ifndef GUARD_LEGENDS_ROAMERS_H
#define GUARD_LEGENDS_ROAMERS_H

struct Roamer
{
    /*0x00*/ u32 ivs;
    /*0x04*/ u32 personality;
    /*0x08*/ enum Species species;
    /*0x0A*/ u16 hp;
    /*0x0C*/ u8 level;
    /*0x0D*/ u8 statusA;
    /*0x0E*/ u8 cool;
    /*0x0F*/ u8 beauty;
    /*0x10*/ u8 cute;
    /*0x11*/ u8 smart;
    /*0x12*/ u8 tough;
    /*0x13*/ bool8 active;
    /*0x14*/ u8 statusB; // Stores frostbite
    /*0x15*/ bool8 shiny;
    /*0x16*/ u8 filler[0x6];
};

// Append-only extension; the original native roamer stays in SaveBlock1.
struct LegendsEonSave
{
    u32 magic;
    u32 checksum;
    u8 version;
    bool8 unlocked;
    u8 reserved[2];
    struct Roamer partner;
};

#endif
