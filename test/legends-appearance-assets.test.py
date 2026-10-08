"""Check pose coverage, native face/ball protection and reproducible 4bpp art."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "tools/legends"))
import build_appearance as art

generated = [root / p for p in (
    "src/data/legends/overworld_outfits.h",
    "src/data/legends/trainer_outfits.h",
    "tools/legends/appearance_asset_manifest.json")]
before = [p.read_bytes() for p in generated]
art.build()
assert before == [p.read_bytes() for p in generated], "Regenerate checked-in outfit assets"
count = 0
for gender, name in enumerate(("brendan", "may")):
    cases = [("overworld", root / f"graphics/object_events/pics/people/{name}/{file}.png", 16 if i == 0 else 32)
             for i, file in enumerate(art.FILES)]
    cases += [("overworld", root / f"graphics/object_events/pics/people/{name}/running.png", 16)]
    cases += [(kind, root / f"graphics/trainers/{directory}/{name}.png", 64)
              for kind, directory in (("front", "front_pics"), ("back", "back_pics"))]
    for kind, path, width in cases:
        for pose, frame in enumerate(art.frames(path, width, 32 if kind == "overworld" else 64)):
            groups = art.skin_components(frame)
            face = (max(groups, key=len) if kind == "overworld" else
                    min((g for g in groups if len(g) > 30), key=lambda g: min(y for x, y in g))) if groups else set()
            for outfit in (1, 2):
                result = art.outfit_frame(frame, gender, outfit, kind, pose)
                assert all(frame[y][x] == result[y][x] for x, y in face), (path, pose, "face")
                assert all((v == 0) == (result[y][x] == 0) for y, row in enumerate(frame) for x, v in enumerate(row))
                if kind != "overworld":
                    assert all(result[y][x] == v for y, row in enumerate(frame) for x, v in enumerate(row)
                               if v in (12, 13) and not 24 <= x <= 42), (path, pose, "held ball/glove")
                raw = art.pack(result)
                assert len(raw) == width * len(frame) // 2
                compressed = art.literal_lz(raw)
                assert compressed[0] == 0x10 and int.from_bytes(compressed[1:4], "little") == len(raw)
                decoded = bytearray()
                for i in range(4, len(compressed), 9):
                    if len(decoded) >= len(raw):
                        break
                    assert compressed[i] == 0
                    decoded.extend(compressed[i + 1:i + 9])
                assert decoded[:len(raw)] == raw
                count += 1
print(f"{count} outfit poses: reproducible art, faces, held balls, silhouettes and LZ77 roundtrip passed.")
