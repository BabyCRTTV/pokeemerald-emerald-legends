#!/usr/bin/env bash
# Full ROMs, canonical base and compiler outputs stay on this private runner.
set -euo pipefail
patch_work="$(pwd)/build/shared-build/private"
publication="$(pwd)/build/shared-build/publication"
mkdir -p "$patch_work" "$publication"
patch_jobs="$(nproc)"
if [ "$patch_jobs" -gt 2 ]; then patch_jobs=2; fi

git clone --depth 1 https://github.com/pret/pokeemerald.git "$patch_work/vanilla"
git clone --depth 1 https://github.com/pret/agbcc.git "$patch_work/agbcc"
(
  cd "$patch_work/agbcc"
  ./build.sh
  ./install.sh "$patch_work/vanilla"
)
make -C "$patch_work/vanilla" -j"$patch_jobs"
echo "f3ae088181bf583e55daf962a92bb46f4f1d07b7  $patch_work/vanilla/pokeemerald.gba" | sha1sum -c -

git clone --depth 1 https://github.com/bates64/flips.git "$patch_work/flips"
TARGET=cli make -C "$patch_work/flips" -j"$patch_jobs"
game_version="$(tr -d '\r\n' < VERSION)"
release_patch="$publication/Pokemon-Emerald-Legends-v${game_version}.bps"
debug_patch="$publication/Pokemon-Emerald-Legends-v${game_version}-debug.bps"
base="$patch_work/vanilla/pokeemerald.gba"
flips="$patch_work/flips/flips"
"$flips" --create --bps "$base" pokeemerald-release.gba "$release_patch"
"$flips" --create --bps "$base" pokeemerald.gba "$debug_patch"
"$flips" --apply "$release_patch" "$base" "$patch_work/release-verified.gba"
"$flips" --apply "$debug_patch" "$base" "$patch_work/debug-verified.gba"
cmp "$patch_work/release-verified.gba" pokeemerald-release.gba
cmp "$patch_work/debug-verified.gba" pokeemerald.gba
node tools/legends/verify_bps_with_browser.cjs \
  "$base" "$release_patch" "$debug_patch" pokeemerald-release.gba pokeemerald.gba \
  "$publication/browser-decoder-verification.json"
