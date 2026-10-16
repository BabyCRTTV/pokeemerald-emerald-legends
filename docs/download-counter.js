(() => {
  "use strict";

  // One shared all-version total. /get reads only; /hit increments atomically.
  // Counts initiated BPS/GBA downloads, not unique people or completed transfers.
  const API = "https://abacus.jasoncameron.dev";
  const KEY = "babycrttv-emerald-legends/downloads-20261016-995fafb8";
  const badge = document.getElementById("download-count");
  let latestCount = null;

  function display(value) {
    if (!Number.isSafeInteger(value) || value < 0) throw new Error("Invalid counter");
    latestCount = Math.max(latestCount ?? 0, value);
    if (!badge) return;
    const compact = new Intl.NumberFormat("en", { notation: "compact", maximumFractionDigits: 1 });
    badge.textContent = "↓ " + compact.format(latestCount);
    badge.setAttribute("aria-label", latestCount.toLocaleString("en") + " download actions since October 15, 2026");
  }

  async function request(action) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);
    try {
      const response = await fetch(`${API}/${action}/${KEY}`, {
        cache: "no-store", credentials: "omit", referrerPolicy: "no-referrer",
        keepalive: action === "hit", signal: controller.signal
      });
      const data = await response.json();
      if (action === "get" && response.status === 404 && data.error === "Key not found") {
        display(0);
        return;
      }
      if (!response.ok) throw new Error("Counter unavailable");
      display(data.value);
    } catch {
      // Never block a download, invent a count or retry an uncertain increment.
      if (badge && latestCount === null) {
        badge.textContent = "—";
        badge.setAttribute("aria-label", "Download count temporarily unavailable");
      }
    } finally {
      clearTimeout(timeout);
    }
  }

  document.addEventListener("click", event => {
    if (event.defaultPrevented || event.button !== 0) return;
    if (event.target.closest?.('a[download][href$=".bps"]')) void request("hit");
  });
  window.addEventListener("legends:download-started", () => { void request("hit"); });
  if (badge) void request("get");
})();
