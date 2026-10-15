# Native OPTION card review capture

Build Debug and Release, then run:

```
python3 tools/legends/native_option_card_qa/run.py --output /tmp/option-debug --prefix /path/to/extracted/usr
python3 tools/legends/native_option_card_qa/run.py --release --output /tmp/option-release --prefix /path/to/extracted/usr
```

Requires ARM binutils, Pillow and mGBA 0.10.2 headers/library. The host loads the unmodified locally built ROM, initializes its native main menu and uses controlled RAM to select its four existing layout states. It drives Up/Down/A/B through normal emulated input and captures selected/unselected cards and Options entry/return. It does not patch ROM bytes or distribute a ROM. Mystery Gift/Events layouts are rendering fixtures, not complete progression tests. Task offsets follow the actual 40-byte `struct Task` in `include/task.h`.

Each receipt pins the build hash, native frames, font baseline pixels and right boundary. Phone previews are scaled 2× nearest neighbor; captions remain outside the game image. The title card uses current root VERSION for review; any later release bump must update both main-menu version strings, enforced alongside the existing Options version checks.
