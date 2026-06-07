export function AgentApprovalCard({ title, risk }: { title: string; risk: string }) {
  return (
    <div className="rounded-2xl border p-5">
      <div className="text-xs uppercase tracking-wide text-neutral-500">Approval Required</div>
      <h3 className="mt-2 font-semibold">{title}</h3>
      <p className="mt-2 text-sm text-neutral-600">Risk level: {risk}</p>
      <div className="mt-4 flex gap-2"><button>Approve</button><button>Reject</button><button>Needs edit</button></div>
    </div>
  );
}
