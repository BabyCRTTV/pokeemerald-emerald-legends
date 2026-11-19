"""Count distinct species a player can capture in the Emerald Legends campaign."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path):
    return (ROOT / path).read_text()


def count(header):
    dex = json.loads(read("docs/wiki/dex-data.json"))
    forms = {p["id"]: p.get("formOf", p["id"]) for p in dex["species"]}
    forms["DEOXYS_NORMAL"] = "DEOXYS"
    maps = {m["id"] for m in dex["maps"] if "UNUSED" not in m["id"]}
    group = json.loads(read("src/data/wild_encounters.json"))["wild_encounter_groups"][0]
    ordinary = set()
    seen_maps = set()
    for encounter in group["encounters"]:
        location = encounter["map"]
        if location not in maps or location in seen_maps:
            continue
        seen_maps.add(location)  # Only the default Altering Cave set is active.
        for method, table in encounter.items():
            if isinstance(table, dict) and table["encounter_rate"]:
                if location == "MAP_LEGENDS_KANTO_ROUTE21_SOUTH" and method == "land_mons":
                    continue  # The southern layout has no grass.
                ordinary.update(m["species"].removeprefix("SPECIES_") for m in table["mons"])
    ordinary.update(re.findall(r"\{\d+, \d+, SPECIES_(\w+)\}", header))
    ordinary.update(re.findall(r"\.species = SPECIES_(\w+)", read("src/mass_outbreak.c")))
    ordinary.add("FEEBAS")  # Route 119's special fishing tiles.
    grottos = json.loads(read("src/data/legends/grotto_encounters.json"))
    grotto = {m["species"] for room in grottos["rooms"] for pool in room["seasons"].values() for m in pool}

    # The Wing Survey grants access to Faraway Island. These other islands
    # require separately distributed tickets and ship unlock flags.
    ticket_maps = {"NavelRock_Top", "NavelRock_Bottom", "BirthIsland_Exterior"}
    event = set()
    story = {"LATIAS", "LATIOS"}  # Both become roaming encounters.
    paths = list((ROOT / "data/maps").glob("*/scripts.inc"))
    paths.extend((ROOT / "data/scripts").glob("legends*.inc"))
    for path in paths:
        if path.parent.name.endswith("_Frlg"):
            continue
        species = re.findall(r"^\s*(?:setwildbattle|seteventmon) SPECIES_(\w+)", path.read_text(), re.M)
        pool = event if path.parent.name in ticket_maps else story
        pool.update(species)

    normal, hidden, fixed, ticket = ({forms[s] for s in pool} for pool in (ordinary, grotto, story, event))
    total = normal | hidden | fixed
    return {"ordinary": len(normal), "additional_grotto": len(hidden-normal),
            "additional_story": sorted(fixed-normal-hidden), "total": len(total),
            "additional_ticket": sorted(ticket-total), "including_tickets": len(total|ticket)}


if __name__ == "__main__":
    print(json.dumps(count(read("src/data/legends_seasonal_encounters.h")), indent=2))
