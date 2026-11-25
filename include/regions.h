#ifndef GUARD_REGIONS_H
#define GUARD_REGIONS_H

#include "global.h"
#include "constants/regions.h"

enum KantoSubRegion GetKantoSubregion(u32 mapSecId);

static inline enum Region GetRegionForSectionId(u32 sectionId)
{
    if (sectionId >= MAPSEC_LEGENDS_NEW_BARK_TOWN && sectionId <= MAPSEC_LEGENDS_SLOWPOKE_WELL)
        return REGION_JOHTO;
    if (sectionId >= MAPSEC_LEGENDS_ROUTE26 && sectionId <= MAPSEC_LEGENDS_TOHJO_FALLS)
        return REGION_KANTO;
    if (sectionId >= KANTO_MAPSEC_START && sectionId < MAPSEC_SPECIAL_AREA)
        return REGION_KANTO;
    return REGION_HOENN;
}

static inline enum Region GetCurrentRegion(void)
{
    return GetRegionForSectionId(gMapHeader.regionMapSectionId);
}

#endif // GUARD_REGIONS_H
