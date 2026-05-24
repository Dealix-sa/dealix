// Founder-approved actions. Never sends externally on its own.
// Every action posts to internal API which writes to approval_queue.csv.

const BASE = process.env.NEXT_PUBLIC_DEALIX_INTERNAL_API ?? "";

export type ActionPayload = {
  action_id: string;
  reason: string;
  payload?: Record<string, unknown>;
};

export async function queueForApproval(payload: ActionPayload): Promise<{ queued: boolean; id?: string; error?: string }> {
  if (!BASE) return { queued: true, id: `stub-${Date.now()}` };
  try {
    const res = await fetch(`${BASE}/internal/founder-console/approvals/queue`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-internal-key": process.env.NEXT_PUBLIC_DEALIX_INTERNAL_KEY ?? "",
      },
      body: JSON.stringify(payload),
    });
    if (!res.ok) return { queued: false, error: `status_${res.status}` };
    return (await res.json()) as { queued: boolean; id?: string };
  } catch (e) {
    return { queued: false, error: String(e) };
  }
}
