# Both Eon roamers — v0.0.75

Model: GPT-6 (Codex).

Mom’s postgame TV question still selects the first level-40 roamer: Red gives Latias; Blue gives Latios. After the first actual roaming battle returns to the field, the opposite level-40 Eon starts roaming too. Running away, the Eon fleeing, catching it or defeating it all unlock the other. A Repel-blocked encounter roll does not unlock it. Both use native Hoenn roaming routes, encounter checks, Repel and Pokédex area tracking; this adds no seasonal or static encounter.

Each Pokémon retains its own IVs, personality, shiny identity, HP and status between encounters. Catching or defeating either removes only that Pokémon; it does not remove, regenerate or revive the other. Catching both is possible in one save. Defeated roamers retain native permanent-removal behavior. Native Southern Island/Eon Ticket behavior is unchanged.

The original 28-byte roamer stays at its original SaveBlock1 offset and every subsequent native offset remains intact. A signed, versioned, checksummed 40-byte extension at SaveBlock3 offset 992 holds the second Pokémon and its one-time unlock state. Existing 992 bytes, save sectors, storage codecs, flags, vars, species IDs, artwork and maps stay unchanged. New/Continue initialization recognizes absent legacy data once; saving the new state prevents duplicate unlocks or revival.

Older saves have no exact first-roamer-battle bit. After the TV event, a retained chosen Eon that is inactive (caught/defeated), or whose species is already marked seen, unlocks the opposite during Continue. This intentionally uses the old Pokédex seen flag as a compatibility proxy; it cannot distinguish a prior roaming battle from seeing the chosen species elsewhere. An active, unseen first roamer stays alone until its first battle. The native first roamer is never regenerated.

The unused TV broadcast initialization call was removed so the color question remains authoritative. Repeated imported Celio initialization calls cannot create duplicates or revive a completed first roamer. Each native roamer consumer uses a shared accessor; the native one-element serialized array never grows.

See [QA and publication state](../qa/eon-roamers-v0.0.75.md).
