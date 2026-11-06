#include "global.h"
#include "legends_nightmare.h"
#include "event_data.h"
#include "script.h"
#include "field_player_avatar.h"
#include "constants/flags.h"
#include "constants/map_types.h"

extern const u8 Nightmare_UnknownCall[];
static EWRAM_DATA u8 sNightmareCallSteps;

// The shared CALMED flag covers capture or defeat, but never escape/blackout.
// Called only after higher-priority field events and the Wyrmtide call.
bool32 LegendsNightmareTryCall(void)
{
#if !IS_FRLG
    if (FlagGet(FLAG_LEGENDS_NIGHTMARE_CALL)
     || !FlagGet(FLAG_LEGENDS_WYRMTIDE_CALMED)
     || !FlagGet(FLAG_RECEIVED_POKENAV)
     || FlagGet(FLAG_SYS_SAFARI_MODE)
     || (gPlayerAvatar.flags & PLAYER_AVATAR_FLAG_FORCED_MOVE)
     || (gMapHeader.mapType != MAP_TYPE_ROUTE
      && gMapHeader.mapType != MAP_TYPE_TOWN
      && gMapHeader.mapType != MAP_TYPE_CITY))
    {
        sNightmareCallSteps = 0;
        return FALSE;
    }
    if (++sNightmareCallSteps < 8)
        return FALSE;
    sNightmareCallSteps = 0;
    ScriptContext_SetupScript(Nightmare_UnknownCall);
    return TRUE;
#else
    return FALSE;
#endif
}
