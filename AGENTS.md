# Pokémon Emerald: Legends development

The owner may switch models, including Astra and Sol, for different tasks. Use the currently selected model's strengths while preserving the same quality standard, decisions, approvals and project constraints. Maintain a concise, durable handoff so work continues across model or conversation changes.

- Read `docs/DEVELOPMENT-HANDOFF.md` and inspect the live repository before changing anything. Recent commits, PRs, Actions and published files take precedence over older summaries. Root `VERSION` is authoritative.
- Check the connected GitHub tools first and use them for repository writes. A failed web request, clone or container operation does not establish that the connector is unavailable. Check it before asking the owner for files.
- Preserve approved artwork, existing functionality, native animation geometry and version history. Keep the accepted baseline when making repairs. Publish visual revisions that need approval only after the owner approves those revisions; carry existing authorization forward.
- Use in-game assets for world building and design unless the owner supplies artwork, designs, generations or references for that purpose.
- Prefer previews from the actual game compositor for existing sprite work. Distinguish sprite-buffer previews from emulator captures and retain exact pixels when scaling.
- Validate relevant changes and regressions. Verify native Release and Debug builds and independently apply both BPS patches against the supported clean Emerald base before claiming readiness. Confirm commits, merges, Actions results and live downloads before reporting them as completed.
- Keep versioning, all three changelogs, Options, README, site and browser patcher consistent. Preserve Release/Debug distinctions.
- Write changelog entries in past tense so readers can easily distinguish completed changes from planned work. Apply this convention to all three changelog files and the website changelog.
- Update the handoff with accepted decisions, approval state, commit/build evidence and outstanding work at each completed milestone or interruption. Keep it short, and store detailed evidence in linked QA records. Avoid dumping full logs, registries, binary data or repeated inspections into the conversation.
