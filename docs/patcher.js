(() => {
  "use strict";

  const EXPECTED_SHA1 = "f3ae088181bf583e55daf962a92bb46f4f1d07b7";
  const VERSION = "0.0.25.1";
  const params = new URLSearchParams(window.location.search);
  const IS_DEBUG = params.get("build") === "debug";
  const BUILD_LABEL = IS_DEBUG ? "Debug" : "Release";
  const BUILD_SUFFIX = IS_DEBUG ? "-debug" : "";
  const PATCH_URL = `downloads/Pokemon-Emerald-Legends-v${VERSION}${BUILD_SUFFIX}.bps`;
  const OUTPUT_NAME = `Pokemon-Emerald-Legends-v${VERSION}${BUILD_SUFFIX}.gba`;

  const input = document.getElementById("rom-file");
  const button = document.getElementById("patch-button");
  const status = document.getElementById("patch-status");
  const buildVersion = document.getElementById("build-version");
  const buildLabel = document.getElementById("build-label");
  const buildDescription = document.getElementById("build-description");
  const buildFooter = document.getElementById("build-footer");

  document.title = `Patch Pokémon Emerald: Legends v${VERSION} ${BUILD_LABEL}`;
  buildVersion.textContent = `v${VERSION}${IS_DEBUG ? " DEBUG" : ""}`;
  buildLabel.textContent = BUILD_LABEL;
  buildDescription.textContent = IS_DEBUG
    ? "Developer build with the same game content as Release, plus the expansion debug menus, sprite visualizer, and title-screen Quickstart."
    : "Recommended for normal play. Developer/debug entry points are disabled while all Pokémon Emerald: Legends gameplay and content changes remain intact.";
  buildFooter.textContent = `Pokémon Emerald: Legends v${VERSION} ${BUILD_LABEL}`;
  button.textContent = `2. Create Emerald: Legends v${VERSION} ${BUILD_LABEL}`;

  let sourceBytes = null;
  // Ignore results from a ROM selection that has since been replaced.
  let romSelectionRevision = 0;

  input.addEventListener("change", async () => {
    const revision = ++romSelectionRevision;
    button.disabled = true;
    sourceBytes = null;

    const file = input.files && input.files[0];
    if (!file) {
      setStatus("Waiting for a ROM file.", "");
      return;
    }

    try {
      setStatus("Checking clean ROM…", "busy");
      const buffer = await file.arrayBuffer();

      if (buffer.byteLength !== 16777216) {
        throw new Error("This file is not the expected 16 MiB Pokémon Emerald ROM.");
      }

      const sha1 = await digestHex("SHA-1", buffer);
      if (sha1 !== EXPECTED_SHA1) {
        throw new Error(
          "ROM does not match the supported clean U.S./Europe Emerald image. " +
          "Expected SHA-1 " + EXPECTED_SHA1 + "."
        );
      }

      if (revision !== romSelectionRevision) return;
      sourceBytes = new Uint8Array(buffer);
      setStatus(`Clean ROM verified. Ready to build Emerald: Legends v${VERSION} ${BUILD_LABEL}.`, "ok");
      button.disabled = false;
    } catch (err) {
      if (revision === romSelectionRevision)
        setStatus(err.message || String(err), "error");
    }
  });

  button.addEventListener("click", async () => {
    if (!sourceBytes) return;

    const sourceForPatch = sourceBytes;
    const revision = romSelectionRevision;
    button.disabled = true;
    try {
      setStatus(`Downloading the v${VERSION} ${BUILD_LABEL} BPS patch…`, "busy");
      const response = await fetch(PATCH_URL, { cache: "no-store" });
      if (!response.ok) {
        throw new Error(`The v${VERSION} ${BUILD_LABEL} patch is still being built. Please try again shortly.`);
      }

      const patchBytes = new Uint8Array(await response.arrayBuffer());
      if (revision !== romSelectionRevision) return;
      setStatus("Applying patch locally…", "busy");
      const output = applyBps(sourceForPatch, patchBytes);
      if (revision !== romSelectionRevision) return;

      setStatus("Verifying and preparing download…", "busy");
      const blob = new Blob([output], { type: "application/octet-stream" });
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = OUTPUT_NAME;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);

      setStatus(`Done. Your Emerald: Legends v${VERSION} ${BUILD_LABEL} .gba has been created locally.`, "ok");
    } catch (err) {
      if (revision === romSelectionRevision)
        setStatus(err.message || String(err), "error");
    } finally {
      button.disabled = !sourceBytes;
    }
  });

  function setStatus(message, type) {
    status.textContent = message;
    status.className = "patch-status" + (type ? " " + type : "");
  }

  async function digestHex(algorithm, buffer) {
    const digest = new Uint8Array(await crypto.subtle.digest(algorithm, buffer));
    return Array.from(digest, b => b.toString(16).padStart(2, "0")).join("");
  }

  function readVarInt(state) {
    let data = 0;
    let shift = 1;

    while (true) {
      if (state.pos >= state.limit) throw new Error("Invalid BPS patch.");
      const x = state.patch[state.pos++];
      data += (x & 0x7f) * shift;
      if (x & 0x80) break;
      shift <<= 7;
      data += shift;
    }
    return data;
  }

  function readSignedVarInt(state) {
    const value = readVarInt(state);
    const magnitude = value >>> 1;
    return (value & 1) ? -magnitude : magnitude;
  }

  function readU32LE(bytes, offset) {
    return (
      bytes[offset] |
      (bytes[offset + 1] << 8) |
      (bytes[offset + 2] << 16) |
      (bytes[offset + 3] << 24)
    ) >>> 0;
  }

  const CRC_TABLE = (() => {
    const table = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) {
        c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
      }
      table[n] = c >>> 0;
    }
    return table;
  })();

  function crc32(bytes, start = 0, end = bytes.length) {
    let crc = 0xffffffff;
    for (let i = start; i < end; i++) {
      crc = CRC_TABLE[(crc ^ bytes[i]) & 0xff] ^ (crc >>> 8);
    }
    return (crc ^ 0xffffffff) >>> 0;
  }

  function applyBps(source, patch) {
    if (patch.length < 16) throw new Error("BPS patch is too small.");
    if (
      patch[0] !== 0x42 || patch[1] !== 0x50 ||
      patch[2] !== 0x53 || patch[3] !== 0x31
    ) {
      throw new Error("Download is not a valid BPS1 patch.");
    }

    const footer = patch.length - 12;
    const expectedSourceCrc = readU32LE(patch, footer);
    const expectedTargetCrc = readU32LE(patch, footer + 4);
    const expectedPatchCrc = readU32LE(patch, footer + 8);

    if (crc32(patch, 0, patch.length - 4) !== expectedPatchCrc) {
      throw new Error("BPS patch checksum failed.");
    }
    if (crc32(source) !== expectedSourceCrc) {
      throw new Error("The selected ROM does not match the source expected by this patch.");
    }

    const state = { patch, pos: 4, limit: footer };
    const sourceSize = readVarInt(state);
    const targetSize = readVarInt(state);
    const metadataSize = readVarInt(state);

    if (sourceSize !== source.length) {
      throw new Error("Source ROM size does not match this patch.");
    }

    state.pos += metadataSize;
    if (state.pos > footer) throw new Error("Invalid BPS metadata.");

    const target = new Uint8Array(targetSize);
    let outputOffset = 0;
    let sourceRelativeOffset = 0;
    let targetRelativeOffset = 0;

    while (outputOffset < targetSize) {
      const command = readVarInt(state);
      const action = command & 3;
      const length = (command >>> 2) + 1;

      if (outputOffset + length > targetSize) {
        throw new Error("BPS command exceeds target size.");
      }

      if (action === 0) {
        if (outputOffset + length > source.length) throw new Error("Invalid BPS SourceRead.");
        target.set(source.subarray(outputOffset, outputOffset + length), outputOffset);
        outputOffset += length;
      } else if (action === 1) {
        if (state.pos + length > footer) throw new Error("Invalid BPS TargetRead.");
        target.set(patch.subarray(state.pos, state.pos + length), outputOffset);
        state.pos += length;
        outputOffset += length;
      } else if (action === 2) {
        sourceRelativeOffset += readSignedVarInt(state);
        if (sourceRelativeOffset < 0 || sourceRelativeOffset + length > source.length) {
          throw new Error("Invalid BPS SourceCopy.");
        }
        target.set(source.subarray(sourceRelativeOffset, sourceRelativeOffset + length), outputOffset);
        sourceRelativeOffset += length;
        outputOffset += length;
      } else {
        targetRelativeOffset += readSignedVarInt(state);
        if (targetRelativeOffset < 0 || targetRelativeOffset >= outputOffset) {
          throw new Error("Invalid BPS TargetCopy.");
        }
        for (let i = 0; i < length; i++) {
          if (targetRelativeOffset >= outputOffset + i) {
            throw new Error("Invalid overlapping BPS TargetCopy.");
          }
          target[outputOffset + i] = target[targetRelativeOffset++];
        }
        outputOffset += length;
      }
    }

    if (crc32(target) !== expectedTargetCrc) {
      throw new Error("Patched ROM checksum failed.");
    }

    return target;
  }
})();
