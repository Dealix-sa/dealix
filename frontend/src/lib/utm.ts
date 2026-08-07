/**
 * First-touch marketing attribution capture (client-side, dependency-free).
 *
 * Captures standard UTM params + common ad-click identifiers + minimal first-touch
 * context (referrer, landing path, first-seen timestamp) on the visitor's first page
 * load, persists them in localStorage (first touch wins), and exposes them so they can
 * be attached to governed lead submissions. SSR-safe: returns {} on the server.
 *
 * This only records *where a lead came from*. It performs no network calls and no
 * external send — attribution is sanitized + bounded again server-side in
 * dealix/revenue_ops_autopilot/attribution.py before it enters the governed store.
 */

export type Attribution = Record<string, string>;

const STORAGE_KEY = "dealix_attribution_v1";
const MAX_VALUE_LEN = 512;

const UTM_KEYS = [
  "utm_source",
  "utm_medium",
  "utm_campaign",
  "utm_term",
  "utm_content",
] as const;

const CLICK_ID_KEYS = ["gclid", "fbclid", "msclkid", "ttclid"] as const;

function bounded(value: string): string {
  return value.trim().slice(0, MAX_VALUE_LEN);
}

function readStored(): Attribution | null {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed: unknown = JSON.parse(raw);
    if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
      return parsed as Attribution;
    }
  } catch {
    /* storage unavailable or malformed JSON — treat as no attribution */
  }
  return null;
}

function parseFromLocation(): Attribution {
  const attribution: Attribution = {};
  const params = new URLSearchParams(window.location.search);
  for (const key of [...UTM_KEYS, ...CLICK_ID_KEYS]) {
    const value = params.get(key);
    if (value) attribution[key] = bounded(value);
  }
  const referrer = document.referrer || "";
  if (referrer) attribution.referrer = bounded(referrer);
  attribution.landing_path = bounded(window.location.pathname + window.location.search);
  attribution.first_seen_at = new Date().toISOString();
  return attribution;
}

/** Capture first-touch attribution once and persist it (first touch wins). */
export function captureFirstTouchAttribution(): Attribution {
  if (typeof window === "undefined") return {};
  const existing = readStored();
  if (existing) return existing;
  const fresh = parseFromLocation();
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(fresh));
  } catch {
    /* private mode / quota — non-fatal, attribution simply isn't persisted */
  }
  return fresh;
}

/** Return stored attribution, capturing first touch if none exists yet. SSR-safe → {}. */
export function getAttribution(): Attribution {
  if (typeof window === "undefined") return {};
  return readStored() ?? captureFirstTouchAttribution();
}
