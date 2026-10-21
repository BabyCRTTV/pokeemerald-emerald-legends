# v0.0.69 publication checkpoint

Model: GPT-6 (Codex). Updated 21 October 2026.

- Owner approved publication: “Ok, please publish. Approved.” Do not ask again.
- Approved scope: three compact hidden grottos (Petalburg Woods, Route 114, Route 119), custom recessed cliff entrance, requested Route 119 cliff cleanup, rare seasonal visitors, independent 4,500-step renewal only after capture/defeat, stable visitors across other outcomes/seasons/save-load, and LegendsDex label/filter changes. Preserve all approved art.
- Implementation: `6b200593e15db7a643de247eb4bbb2fba79efa3c`; all relevant workflows passed. Details and existing save/native limits: [grotto QA](grotto-encounters.md).
- v0.0.69 release metadata: `4552f10083967dcfb625f4be4401e9a3d3a85dac`.
- PR #87 merged: `e50e6880b746dd9351a73b925dae6f90065fcdc7`.
- Master project/wiki checks and companion publication passed. Public site shows v0.0.69; this alone does not establish patch publication.
- Release/Debug patch workflow `39603762891` and native mGBA workflow `39603762879` are still running. The release workflow verifies the supported clean Emerald SHA1, applies both BPS patches with Floating IPS, independently decodes them with the shipped browser engine, then commits the patches automatically.
- Matching wiki promotion is prepared locally but uncommitted: v0.0.69/LegendsDex 1.5.0/Wiki 1.7.1 metadata, published grotto provenance, an Exploration article and related season notes, profile metadata/cache key, generator provenance retention and patcher cache key. Nine-file upload manifest: `/workspace/scratch/27608836c157/grotto-wiki-publish-upload.json`. The canonical ordinary encounter/atlas pin stays `0d13f23794686525203fcfe3f8c6496e6921d2f2`; approved artwork stays exact.

## Finish

1. Verify both running workflows; resolve any failure before claiming success.
2. Verify the automatic v0.0.69 Release/Debug patch commit and actual live downloads against SHA256SUMS and independent decoder evidence.
3. Publish the prepared nine wiki/doc files through GitHub tools with a fresh master/tree SHA lease. Do not overwrite companion manifests or patch files committed by Actions.
4. Verify Pages, live LegendsDex Grotto/Sevii/no-old-tag, wiki data/version, patcher and both downloads. Record final commit/workflow/hash evidence here and update the development handoff.
5. Report publication only after those live checks pass. Never upload ROMs or private battery fixtures. All remote writes use connected GitHub tools.
