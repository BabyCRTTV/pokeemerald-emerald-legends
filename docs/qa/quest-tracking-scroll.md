# Tracked quest overflow — review follow-up

Status: implemented on `feature/quest-tracking-preview`, awaiting the owner's original preview approval before release publication. VERSION, master, patches and Pages remain v0.0.56. [Native animation](quest-tracking-scroll.gif) · [Verification receipt](quest-tracking-scroll.json).

## Behavior and implementation

The complete title and current objective wrap using native small-font widths. Text that fits the five-line body remains stationary and allocates no scroll resources. Longer text pauses at the top, moves down through the text one pixel at a time, pauses at the bottom, then smoothly reverses to the top and repeats. Each endpoint pause lasts 120 menu updates (about two seconds). Motion advances one pixel every three menu updates; the controlled Debug compositor produced uniform four-native-frame move intervals. Opening the card again resets it to the top.

TRACKED QUEST and its divider remain fixed. Only the 96×60 body at screen x=8..103, y=20..79 changes. The existing card frame, 16-pixel right-menu gap, clock/weather rectangle and physical VRAM allocation remain unchanged. Updates run only during ordinary pause input. Existing help, Save, special-menu and popup exclusions still apply.

Wrapped line boundaries are cached once on opening. A RAM-only 96×16 scratch window renders visible lines with the native font; clipped whole-word 4bpp row copies update only the body. Its tilemap is never installed and its graphics are never uploaded. This replaced an exploratory repeated-layout/per-pixel blit that missed brief menu taps with deliberately long text. Both the cache and scratch window are freed on closing or failed allocation. There are no new saved fields, identifiers, assets or quest text changes.

## Verification and limits

- Both normal Debug and Release builds passed. The existing Release LTO warnings remain unrelated to these files.
- Actual-C tests used packed native 4bpp buffers and checked all catalogue strings, stationary short text, full long-text traversal/return, endpoint pauses, fixed heading, hidden updates, failed cache/window allocation and cleanup. Pause-menu exclusions and physical tile bounds passed again.
- Controlled native Debug short and oversized fixtures passed actual Details tracking, both pause pages, brief close/reopen input, DexNav help/return, Save/cancel, real flash persistence, next-objective update, completion and Safari suppression. Non-default appearance, bedroom colors and Winter remained intact; the player occupied a verified walkable floor tile.
- The oversized fixture recorded 1,316 native frames and 439 images through a 132-pixel scroll and return. All 264 moves were single pixels. Heading/frame/right-menu pixels stayed identical in every captured image; the final card exactly matched the opening card.
- The 480×354 GIF retains exact 2× nearest-neighbor game pixels and places its caption outside the game. All 265 decoded GIF frames and the full 439-frame timeline matched their native source captures, including coalesced holds.
- Unmodified Release loaded the controlled battery fixture through ordinary title/Continue input, displayed both pause pages and Details, and stopped tracking. Short reminder pixels matched Debug. The oversized animation fixture was exercised in Debug; it is not represented as an unmodified Release overflow test.

The animation uses a deliberately oversized objective in a private QA ROM to exercise text beyond the present catalogue. That text is not shipped. No ROMs or battery saves are committed. The original quest-tracking receipt remains historical; the linked fresh receipt contains these builds and checks. Historical-release saves, uninterrupted story traversal and Pizza Boy remain outside this focused check. Final coordinated version/changelog/BPS/Pages work follows owner preview approval.
