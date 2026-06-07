// Browser-safe client for the Dealix "Now" surface.
//
// Doctrine: AI drafts → founder approves → human sends. Nothing here ever
// auto-sends. approve/reject only change review state; mailto/whatsapp are
// the only "send" paths and they hand control to the founder's own client.

import type { NowDraft, NowPack, DraftActionResult } from "./now-types";

export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ?? "https://api.dealix.me";

/**
 * Load today's NowPack. Tries the live API first (no-store so the founder
 * always sees fresh data); on ANY error or non-OK response, falls back to the
 * static sample served at /now-pack.json. Always resolves to a valid NowPack.
 */
export async function getNowPack(): Promise<NowPack> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/now/pack`, {
      cache: "no-store",
    });
    if (res.ok) {
      return (await res.json()) as NowPack;
    }
  } catch {
    // network/CORS/offline — fall through to the static sample
  }
  // Static fallback. Relative URL works in the browser against the same origin.
  const fallback = await fetch("/now-pack.json", { cache: "no-store" });
  return (await fallback.json()) as NowPack;
}

async function postDraftAction(
  id: string,
  action: "approve" | "reject",
): Promise<DraftActionResult> {
  const offlineStub: DraftActionResult = {
    ok: true,
    status:
      action === "approve"
        ? "approved — ready to send by founder"
        : "rejected",
    offline: true,
  };
  try {
    const res = await fetch(
      `${API_BASE}/api/v1/now/drafts/${encodeURIComponent(id)}/${action}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      },
    );
    if (!res.ok) return offlineStub;
    const data = (await res.json()) as Partial<DraftActionResult>;
    return {
      ok: data.ok ?? true,
      status: data.status ?? offlineStub.status,
      offline: data.offline,
    };
  } catch {
    // Never throw — the console must keep working fully offline.
    return offlineStub;
  }
}

/**
 * Mark a draft approved for sending. Does NOT send anything — it only flips
 * review state. On any failure returns a local "ready to send" stub.
 */
export function approveDraft(id: string): Promise<DraftActionResult> {
  return postDraftAction(id, "approve");
}

/** Mark a draft rejected. Never throws. */
export function rejectDraft(id: string): Promise<DraftActionResult> {
  return postDraftAction(id, "reject");
}

/**
 * Build a mailto: link from a draft. The founder's mail client opens with the
 * subject + body prefilled; they choose the recipient and press send.
 */
export function buildMailto(draft: NowDraft): string {
  const to = draft.contact?.to ?? "";
  const subject = encodeURIComponent(draft.subject ?? "");
  const body = encodeURIComponent(draft.body ?? "");
  return `mailto:${to}?subject=${subject}&body=${body}`;
}

/**
 * Build a wa.me link from a draft (subject + body as a single message). No
 * phone number is hardcoded — the founder picks the contact in WhatsApp.
 */
export function buildWhatsapp(draft: NowDraft): string {
  const parts = [draft.subject, draft.body].filter(Boolean).join("\n\n");
  return `https://wa.me/?text=${encodeURIComponent(parts)}`;
}
