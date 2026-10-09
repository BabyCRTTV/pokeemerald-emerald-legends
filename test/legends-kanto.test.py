"""Exercise the shipped event scripts and audit their real map/warp geometry."""
import json
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "data/scripts/legends_kanto.inc").read_text()
LABELS = {}
COMMANDS = []
for line in SOURCE.splitlines():
    line = line.strip()
    if re.fullmatch(r"\w+::?", line):
        LABELS[line.rstrip(":")] = len(COMMANDS)
    elif line and not line.startswith(("@", ".")):
        COMMANDS.append(line)


class Events:
    """Small event-command interpreter; visual commands are recorded, not rendered."""
    def __init__(self, champion=False, ticket=False, answer=True, bag_room=True):
        self.flags = {"FLAG_SYS_GAME_CLEAR"} if champion else set()
        self.items = {"ITEM_INVITE_TICKET"} if ticket else set()
        self.vars = {"VAR_RESULT": 0}
        self.answer, self.bag_room = answer, bag_room
        self.warp = None
        self.battles = 0
        self.messages = []
        self.respawn = None
        self.comparison = 0

    def value(self, token):
        return {"TRUE": 1, "FALSE": 0, "YES": 1, "NO": 0}.get(token, self.vars.get(token, token))

    def run(self, event):
        pc = LABELS["LegendsKanto_EventScript_" + event]
        for _ in range(200):
            command = COMMANDS[pc]
            pc += 1
            op, _, args = command.partition(" ")
            args = [a.strip() for a in args.split(",")]
            if op == "end":
                return self
            if op in ("goto_if_set", "goto_if_unset"):
                match = args[0] in self.flags
                if match == (op == "goto_if_set"):
                    pc = LABELS[args[1]]
            elif op == "goto_if":
                if self.comparison == self.value(args[0]):
                    pc = LABELS[args[1]]
            elif op == "goto_if_eq":
                if self.value(args[0]) == self.value(args[1]):
                    if args[2] == "EventScript_BagIsFull":
                        return self
                    pc = LABELS[args[2]]
            elif op == "checkitem":
                self.vars["VAR_RESULT"] = int(args[0] in self.items)
            elif op == "giveitem":
                self.vars["VAR_RESULT"] = int(self.bag_room)
                if self.bag_room:
                    self.items.add(args[0])
            elif op == "setflag":
                self.flags.add(args[0])
            elif op == "setvar":
                self.vars[args[0]] = int(args[1])
            elif op == "msgbox":
                self.messages.append(args[0])
                if args[1] == "MSGBOX_YESNO":
                    self.vars["VAR_RESULT"] = int(self.answer)
            elif op == "warp":
                self.warp = args
            elif op == "setrespawn":
                self.respawn = args[0]
            elif op == "checktrainerflag":
                self.comparison = int(args[0] in self.flags)
            elif op == "trainerbattle_single":
                self.battles += 1
                self.flags.add(args[0])
            elif op not in {"lock", "lockall", "faceplayer", "release", "releaseall", "closemessage", "fadescreen", "playse", "delay", "waitstate", "applymovement", "waitmovement"}:
                raise AssertionError("Unsupported event command: " + command)
        raise AssertionError("Event did not terminate")


class KantoTests(unittest.TestCase):
    def test_invitation_and_ticket_progression(self):
        for champion in (False, True):
            for ticket in (False, True):
                e = Events(champion, ticket).run("OutboundFerry")
                self.assertEqual(bool(e.warp), champion and ticket)
        e = Events(champion=True).run("Invitation")
        self.assertIn("ITEM_INVITE_TICKET", e.items)
        e.run("OutboundFerry")
        self.assertEqual(e.warp, ["MAP_LEGENDS_KANTO_HARBOR", "32", "9"])
        e.run("ReturnFerry")
        self.assertEqual(e.warp, ["MAP_LILYCOVE_CITY_HARBOR", "4", "13"])
        self.assertEqual(e.respawn, "HEAL_LOCATION_LILYCOVE_CITY")
        e.run("OutboundFerry")
        self.assertEqual(e.warp[0], "MAP_LEGENDS_KANTO_HARBOR")
        self.assertIn("ITEM_INVITE_TICKET", e.items)
        self.assertNotIn("ITEM_INVITE_TICKET", Events().run("Invitation").items)
        self.assertNotIn("ITEM_INVITE_TICKET", Events(champion=True, bag_room=False).run("Invitation").items)
        self.assertIsNone(Events(ticket=False).run("ReturnFerry").warp)

    def test_declining_does_not_travel_or_start_battle(self):
        for event in ("OutboundFerry", "ReturnFerry"):
            self.assertIsNone(Events(True, True, answer=False).run(event).warp)
        e = Events(answer=False)
        e.vars["VAR_RESULT"] = 1  # Stale item/menu result must not imply trainer victory.
        e.run("Alex")
        self.assertEqual(e.battles, 0)
        e.answer = True
        e.run("Alex")
        self.assertEqual(e.battles, 1)
        e.vars["VAR_RESULT"] = 0
        e.run("Alex")
        self.assertEqual(e.battles, 1)

    def test_welcome_persists_across_reentry_and_reload(self):
        e = Events().run("FirstWelcome")
        self.assertEqual(len(e.messages), 3)
        self.assertIn("FLAG_LEGENDS_KANTO_WELCOMED", e.flags)
        e.vars["VAR_TEMP_0"] = 0
        e.run("FirstWelcome")
        self.assertEqual(len(e.messages), 3)

    def test_maps_and_respawn_have_real_destinations(self):
        maps = {d["id"]: d for p in (ROOT / "data/maps").glob("*/map.json") if (d := json.loads(p.read_text()))}
        layouts = {d["id"]: d for d in json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]}
        new = [d for d in maps.values() if d["name"].startswith("LegendsKanto_")]
        self.assertEqual(len(new), 9)
        for d in new:
            layout = layouts[d["layout"]]
            self.assertEqual((ROOT / layout["blockdata_filepath"]).stat().st_size, layout["width"] * layout["height"] * 2)
            for warp in d["warp_events"]:
                self.assertIn(warp["dest_map"], maps)
                self.assertLess(int(warp["dest_warp_id"]), len(maps[warp["dest_map"]]["warp_events"]))
            for event in d["object_events"] + d["warp_events"] + d["bg_events"]:
                self.assertTrue(0 <= event["x"] < layout["width"] and 0 <= event["y"] < layout["height"])
        heal = next(d for d in json.loads((ROOT / "src/data/heal_locations.json").read_text())["heal_locations"] if d["id"] == "HEAL_LOCATION_LEGENDS_KANTO_VERMILION")
        self.assertEqual(heal["respawn_map"], "MAP_LEGENDS_KANTO_POKEMON_CENTER_1F")
        self.assertIn(heal["respawn_npc"], [o.get("local_id") for o in maps[heal["respawn_map"]]["object_events"]])
        city = maps["MAP_LEGENDS_KANTO_VERMILION_CITY"]
        self.assertIsNone(city["connections"])
        self.assertNotIn("FLAG_HIDE_SS_ANNE", json.dumps(new))
        self.assertNotIn("VAR_SS_TIDAL_STATE", SOURCE)

    def test_native_graphics_are_registered_in_emerald(self):
        # Source assets can exist while their runtime pointers are FRLG-only.
        import subprocess
        flags = ["-DIS_FRLG=0", "-iquote", "src"]
        script = "#include \"data/object_events/object_event_graphics_info_pointers.h\"\n"
        result = subprocess.run(["gcc", "-E", "-P", "-x", "c", *flags, "-"], input=script, text=True,
                                capture_output=True, cwd=ROOT, check=True).stdout
        for symbol in ("Woman1Frlg", "CooltrainerM", "SailorFrlg", "SSAnne"):
            self.assertIn("= &gObjectEventGraphicsInfo_" + symbol, result)

    def test_spectator_stands_on_walkable_land(self):
        d = json.loads((ROOT / "data/maps/LegendsKanto_VermilionCity/map.json").read_text())
        alex = next(o for o in d["object_events"] if o.get("local_id") == "LOCALID_LEGENDS_KANTO_ALEX")
        data = (ROOT / "data/layouts/LegendsKanto_VermilionCity/map.bin").read_bytes()
        block = struct.unpack_from("<H", data, 2 * (alex["y"] * 48 + alex["x"]))[0]
        self.assertEqual((block >> 10) & 3, 0)
        mid = block & 1023
        path = "primary/general_frlg" if mid < 640 else "secondary/vermilion_city_frlg"
        offset = mid if mid < 640 else mid - 640
        attrs = (ROOT / f"data/tilesets/{path}/metatile_attributes.bin").read_bytes()
        behavior = struct.unpack_from("<I", attrs, offset * 4)[0] & 511
        self.assertNotIn(behavior, (16, 18, 21), "Spectator must not stand in water")

    def test_residents_and_walk_routes_clear_furniture_and_doors(self):
        layouts = {d['id']: d for d in json.loads((ROOT / 'data/layouts/layouts.json').read_text())['layouts']}
        names = ('FanClub', 'VermilionCity', 'Mart', 'PokemonCenter_1F')
        service = {'LegendsKanto_EventScript_Nurse', 'LegendsKanto_EventScript_Clerk'}
        for name in names:
            d = json.loads((ROOT / f'data/maps/LegendsKanto_{name}/map.json').read_text())
            l = layouts[d['layout']]
            blocks = (ROOT / l['blockdata_filepath']).read_bytes()
            for o in d['object_events']:
                if o['script'] in service:
                    continue
                positions = [(o['x'], o['y'])]
                if o['movement_type'] == 'MOVEMENT_TYPE_WANDER_UP_AND_DOWN':
                    positions += [(o['x'], o['y'] + dy) for dy in (-1, 1)]
                if o['movement_type'] == 'MOVEMENT_TYPE_WANDER_LEFT_AND_RIGHT':
                    positions += [(o['x'] + dx, o['y']) for dx in (-1, 1)]
                for x, y in positions:
                    block = struct.unpack_from('<H', blocks, 2 * (y * l['width'] + x))[0]
                    self.assertEqual((block >> 10) & 3, 0, (name, o['script'], x, y))
                    self.assertIn(block >> 12, (0, o['elevation']), (name, o['script'], 'layer'))
                    self.assertNotIn((x, y), [(w['x'], w['y']) for w in d['warp_events']])
        city = json.loads((ROOT / 'data/maps/LegendsKanto_VermilionCity/map.json').read_text())
        machop = next(o for o in city['object_events'] if o['script'].endswith('_Machop'))
        self.assertEqual(machop['graphics_id'], 'OBJ_EVENT_GFX_SPECIES(MACHOP)')
        harbor = json.loads((ROOT / 'data/maps/LilycoveCity_Harbor/map.json').read_text())
        sailor = next(o for o in harbor['object_events'] if o['script'].endswith('_OutboundFerry'))
        lady = next(o for o in harbor['object_events'] if o.get('local_id') == 'LOCALID_LILYCOVE_HARBOR_ATTENDANT')
        self.assertLessEqual(abs(sailor['x'] - lady['x']) + abs(sailor['y'] - lady['y']), 2)

    def test_invite_ticket_fits_native_bag_description(self):
        # Measure actual encoded glyph widths, rather than assuming equal-width letters.
        fonts = (ROOT / 'src/fonts.c').read_text()
        glyphs = re.search(r'gFontNormalLatinGlyphWidths\[\] = \{(.*?)\};', fonts, re.S)[1]
        widths = [int(n) for n in re.findall(r'\d+', glyphs)]
        encoding = {char: int(code, 16) for char, code in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})$", (ROOT / 'charmap.txt').read_text(), re.M)}
        items = (ROOT / 'src/data/items.h').read_text().split('[ITEM_INVITE_TICKET] =', 1)[1].split('.importance', 1)[0]
        description = items.split('.description = COMPOUND_STRING(', 1)[1]
        lines = [line.replace('\\n', '') for line in re.findall(r'"([^\"]*)"', description)]
        self.assertEqual(len(lines), 3)
        menu = (ROOT / 'src/item_menu.c').read_text()
        width = int(re.search(r'\[WIN_DESCRIPTION\] = \{.*?\.width = (\d+)', menu, re.S)[1]) * 8
        for line in lines:
            self.assertLessEqual(sum(widths[encoding[c]] for c in line), width - 3, line)


if __name__ == "__main__":
    unittest.main()
