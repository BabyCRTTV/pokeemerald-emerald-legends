"""Focused v0.0.61 story/dependency regression: no new saved state or reward paths."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
def read(p): return (ROOT / p).read_text(encoding="utf-8")
field = read("data/scripts/legends_field_requests.inc")
menu = read("src/data/script_menu.h")
specials = read("data/specials.inc")
requests = read("src/legends_field_requests.c")
season = read("src/legends_seasons.c")
weather = read("data/maps/Route119_WeatherInstitute_1F/scripts.inc")
weather2 = read("data/maps/Route119_WeatherInstitute_2F/scripts.inc")
devon = read("data/maps/RustboroCity_DevonCorp_3F/scripts.inc")
birch = read("data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc")

assert field.count("case 2, LegendsFieldRequests_ResearchNotes") == 2
assert menu.count('COMPOUND_STRING("RESEARCH NOTES")') == 2
for block, native in (("sLegendsBirchMain", "POKéDEX RATING"),
                      ("sLegendsDevonMain", "DEVON BUSINESS")):
    entries = menu.split(f"static const struct MenuAction {block}[] = {{", 1)[1].split("};", 1)[0]
    assert entries.index(native) < entries.index("RESEARCH NOTES") < entries.index("NOT NOW")
for item in ("BirchNotesNone", "BirchNotesEarly", "BirchNotesAdvanced", "BirchNotesFinal",
             "DevonNotesNone", "DevonNotesEarly", "DevonNotesAdvanced", "DevonNotesFinal"):
    assert f"LegendsFieldRequests_Text_{item}:" in field
notes = field.split("LegendsFieldRequests_ResearchNotes:",1)[1].split("LegendsFieldRequests_Work:",1)[0]
assert not re.search(r"\b(setflag|clearflag|setvar|giveitem|givemon|warp|applymovement)\b", notes)
assert "def_special LegendsFieldRequestsResearchNotes" in specials
assert "def_special LegendsSeasonBulletinSpecial" in specials
assert "completed == (sPatron == FIELD_PATRON_DEVON ? 12 : 18)" in requests
assert "completed >= (sPatron == FIELD_PATRON_DEVON ? 6 : 9)" in requests
assert "gSpecialVar_Result = completed >= 3 ? 1 : 0;" in requests
assert "LegendsFieldRequestComplete(id)" in requests
assert "gSpecialVar_Result = LegendsGetActiveSeason();" in season
assert "VAR_WEATHER_INSTITUTE_STATE, 0, Route119_WeatherInstitute_1F_EventScript_BulletinEnd" in weather
for i, name in enumerate(("Spring", "Summer", "Autumn", "Winter")):
    assert f"Route119_WeatherInstitute_1F_Text_Bulletin{name}:" in weather
    if i < 3: assert f"VAR_RESULT, {i}, Route119_WeatherInstitute_1F_EventScript_Bulletin{name}" in weather
assert "FLAG_RECEIVED_CASTFORM" in weather2 and "GetAbnormalWeatherMapNameAndType" in weather2
assert "FLAG_RECEIVED_EXP_SHARE, LegendsDevonRequests_Talk" in devon
assert "FLAG_DELIVERED_STEVEN_LETTER, RustboroCity_DevonCorp_3F_EventScript_GiveLuckyEgg" in devon
assert "LegendsFieldRequests_Talk" in birch
assert "goto_if_set FLAG_SYS_GAME_CLEAR, LittlerootTown_EventScript_FatManChampion" in read("data/maps/LittlerootTown/scripts.inc")
assert "goto_if_set FLAG_BADGE01_GET, RustboroCity_EventScript_DevonEmployee2Badge" in read("data/maps/RustboroCity/scripts.inc")
assert "goto_if_set FLAG_BADGE06_GET, FortreeCity_EventScript_OldManBadge" in read("data/maps/FortreeCity/scripts.inc")
assert "goto_if_set FLAG_SYS_GAME_CLEAR, LilycoveCity_EventScript_Man3Champion" in read("data/maps/LilycoveCity/scripts.inc")
assert read("VERSION").strip() == "0.0.61"
assert read("docs/changelog.html").count("<h2>v0.0.60 ") == 2
assert read("docs/changelog.html").count("<h2>v0.0.61 ") == 2

for source in (field, weather):
    # Text control codes must have a single source backslash, not doubly escaped.
    assert not re.search(r"\\\\[npl]", source)

print("Living Hoenn: optional menus, milestones, season, script priorities and release metadata OK")
