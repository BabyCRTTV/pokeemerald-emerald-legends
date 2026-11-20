"""Guard the two shared Emerald/FireRed save bits used by the bottle quest."""
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
expected = {
    0x4C0: "FLAG_BOTTLE_DRAWING_FOUND",
    0x4C1: "FLAG_BOTTLE_POSTCARD_KEPT",
}
headers = list((root / "include/constants").glob("*.h"))
for value, owner in expected.items():
    aliases = {f"FLAG_UNUSED_0x{value:X}", f"FLAG_0x{value:X}"}
    owners = []
    for header in headers:
        defines = re.findall(r"^#define\s+(FLAG_\w+)\s+(\w+)\b", header.read_text(), re.M)
        for name, target in defines:
            if target in aliases or target == owner:
                owners.append(name)
            if target.lower() == hex(value):
                assert name in aliases, (name, target)
    assert owners == [owner], (owner, owners)
print("Bottle postcard save flag allocations passed.")
