#ifndef GUARD_LEGENDS_GROTTOS_H
#define GUARD_LEGENDS_GROTTOS_H

#define LEGENDS_GROTTO_COUNT 3
#define LEGENDS_GROTTO_REFRESH_STEPS 4500
#define LEGENDS_GROTTO_BOX_BYTES 80
#define LEGENDS_GROTTO_READY 0
#define LEGENDS_GROTTO_ACTIVE 1
#define LEGENDS_GROTTO_COOLDOWN 2

// Append-only, independently signed extension. Serialized Pokémon are native
// BoxPokemon bytes; the engine build asserts their exact width and alignment.
struct LegendsGrottoRoomSave
{
    u32 mon[LEGENDS_GROTTO_BOX_BYTES / 4];
    u16 species;
    u16 remainingSteps;
    u8 level;
    u8 season;
    u8 state;
    u8 reserved;
};
struct LegendsGrottoSave
{
    u32 magic;
    u32 checksum;
    u16 version;
    u16 reserved;
    struct LegendsGrottoRoomSave rooms[LEGENDS_GROTTO_COUNT];
};

void LegendsGrottoInit(bool32 newGame);
void LegendsGrottoStep(void);
void LegendsGrottoPrepareVisitor(void);
bool32 LegendsGrottoStartBattle(void);
void LegendsGrottoFinishBattle(u8 outcome);
u16 LegendsGrottoRemainingSteps(u8 room);
#endif
