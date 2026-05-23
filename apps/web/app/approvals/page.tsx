import { FounderShell } from "../../components/founder-shell";
import { getApprovals } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ApprovalCenterPage() {
  const approvals = await getApprovals();
  return (
    <FounderShell>
      <main className="p-8">
        <h1 className="text-4xl font-bold">Approval Center</h1>
        <p className="mt-2 max-w-3xl">
          Approve, reject, edit, or escalate outreach, proposals, pricing,
          proof, and trust actions. Every decision writes to the audit
          ledger before any external action runs.
        </p>
        <section className="mt-8 rounded-2xl border p-6">
          {approvals.length === 0 ? (
            <p>
              No pending approvals. Connect the queue or create the first
              outreach batch.
            </p>
          ) : (
            <div className="grid gap-4">
              {approvals.map((item) => (
                <div key={item.id} className="rounded-xl border p-4">
                  <p className="font-semibold">{item.company}</p>
                  <p className="text-sm">Type: {item.type}</p>
                  <p className="text-sm">Approval: {item.approval_class}</p>
                  <p className="text-sm">Risk: {item.risk_level}</p>
                  <p className="mt-2">{item.summary}</p>
                  <div className="mt-4 flex gap-2">
                    <button className="rounded-lg border px-3 py-2 text-sm">
                      Approve
                    </button>
                    <button className="rounded-lg border px-3 py-2 text-sm">
                      Reject
                    </button>
                    <button className="rounded-lg border px-3 py-2 text-sm">
                      Needs Edit
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
        <p className="mt-6 text-xs">
          Source: approval_queue · Endpoint: /api/v1/internal/approvals
        </p>
      </main>
    </FounderShell>
  );
}
