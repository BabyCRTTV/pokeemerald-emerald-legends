#include "global.h"
#include "legends_da_bug.h"
#include "event_data.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "pokedex.h"
#include "random.h"
#include "constants/flags.h"
#include "constants/moves.h"
#include "constants/pokedex.h"
#include "constants/species.h"

// Reserve storage before rolling anything. This also migrates existing saves;
// if every box is full, the next continue retries without consuming the gift.
void LegendsEnsureDaBugGift(void)
{
    struct Pokemon mon;
    bool32 isShiny;
    u8 box, slot;

    if (FlagGet(FLAG_LEGENDS_DA_BUG_RECEIVED))
        return;

    for (box = 0; box < TOTAL_BOXES_COUNT; box++)
    {
        for (slot = 0; slot < IN_BOX_COUNT; slot++)
        {
            if (GetBoxMonDataAt(box, slot, MON_DATA_SPECIES) != SPECIES_NONE)
                continue;

            CreateMon(&mon, SPECIES_DA_BUG, 5, Random32(), OTID_STRUCT_PLAYER_ID);
            // Override the ordinary personality/Options shiny result in both
            // directions: exactly one of ten uniform outcomes is shiny.
            isShiny = RandomUniform(RNG_NONE, 0, 9) == 0;
            SetMonData(&mon, MON_DATA_IS_SHINY, &isShiny);
            SetMonMoveSlot(&mon, MOVE_TACKLE, 0);
            SetMonMoveSlot(&mon, MOVE_LEER, 1);
            SetMonMoveSlot(&mon, MOVE_MEAN_LOOK, 2);
            SetMonMoveSlot(&mon, MOVE_ABSORB, 3);
            SetBoxMonAt(box, slot, &mon.box);
            GetSetPokedexFlag(NATIONAL_DEX_DA_BUG, FLAG_SET_SEEN);
            GetSetPokedexFlag(NATIONAL_DEX_DA_BUG, FLAG_SET_CAUGHT);
            FlagSet(FLAG_LEGENDS_DA_BUG_RECEIVED);
            return;
        }
    }
}
