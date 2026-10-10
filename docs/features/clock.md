# Real and manual clocks

Introduced in v0.0.31; identical in Release and Debug.

REAL TIME is the default. The ROM reads Emerald’s native cartridge RTC interface, supplied by RTC-capable emulators from the device clock. It cannot read the host operating system directly; enable RTC support in the emulator. Valid RTC time always takes priority over played time, including when menus are open.

The initial bedroom interaction confirms the running clock rather than setting an offset. The rival’s bedroom clock remains view-only. Return to your bedroom clock anytime to choose REAL TIME or MANUAL. Choosing MANUAL opens the native analog adjustment screen; confirmation saves its offset. Choosing REAL TIME resumes the device clock. Cancelling either introductory confirmation leaves the room event unfinished so you can try again.

If RTC initialization fails or its date/time fields are invalid, the final-priority fallback is 9 AM plus accumulated played seconds, stored across saves. Old saves initialize that counter from existing playtime; the additional counter keeps ticking after the native 999-hour display cap. A manual clock also advances from played time when RTC is unavailable. If RTC becomes available again, real mode immediately follows it.

The pause panel polls once every 60 emulated frames and redraws when the displayed minute changes. It does not stop the clock. A fully paused emulator cannot render new digits until resumed; fast-forward affects fallback playtime, whereas real mode follows RTC.

As of v0.0.31.1, existing berry/daily timestamps retain a separately saved native date origin when real mode ignores the old hour/minute offset. Native hour borrowing cannot shift that origin when switching modes. A manual clock first configured without RTC is translated into a native offset when RTC becomes available.

The Adventure Log’s played-day count remains based on distinct dates played, not the bedroom’s manual hour. Seasonal/calendar systems continue to use their established RTC/date rules. No new save layout is introduced: clock state occupies previously unreferenced route-state variables.

QA: leave pause open across a real minute and midnight; check both bedroom modes on a fresh/existing save; cancel first confirmation; test an RTC-disabled emulator; save/reload fallback and manual time; then restore RTC support. Automated actual-C checks cover these time-source/rollover cases; emulator playtesting is still required.
