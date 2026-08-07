import type { Account } from "@/lib/crm/crm";

export function AccountTable({ accounts }: { accounts: Account[] }) {
  if (!accounts.length) {
    return <p className="text-sm text-neutral-500">No accounts yet. Run `python3 scripts/score_leads.py --demo`.</p>;
  }
  return (
    <div className="overflow-x-auto rounded-xl border border-neutral-200">
      <table className="w-full text-sm">
        <thead className="bg-neutral-50 text-left text-xs uppercase tracking-wide text-neutral-500">
          <tr>
            <th className="px-4 py-3">Account</th>
            <th className="px-4 py-3">Segment</th>
            <th className="px-4 py-3">City</th>
            <th className="px-4 py-3">Score</th>
            <th className="px-4 py-3">Stage</th>
            <th className="px-4 py-3">Review</th>
            <th className="px-4 py-3">Next action</th>
            <th className="px-4 py-3">Setup / MRR</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-neutral-100">
          {accounts.map((a) => (
            <tr key={a.id}>
              <td className="px-4 py-3 font-medium">
                <a href={`/crm/accounts/${a.id}`} className="text-blue-700 hover:underline">{a.name}</a>
                {a.demo ? <span className="ml-2 rounded-full bg-yellow-100 px-2 py-0.5 text-[10px] text-yellow-800">DEMO</span> : null}
              </td>
              <td className="px-4 py-3 text-neutral-600">{a.segment}</td>
              <td className="px-4 py-3 text-neutral-600">{a.city}</td>
              <td className="px-4 py-3 font-semibold">{a.score}</td>
              <td className="px-4 py-3 text-neutral-600">{a.stage}</td>
              <td className="px-4 py-3 text-neutral-600">{a.reviewStatus}</td>
              <td className="px-4 py-3 text-neutral-600">{a.nextAction} <span className="text-neutral-400">({a.nextActionDate})</span></td>
              <td className="px-4 py-3 text-neutral-600">{a.setupValue.toLocaleString()} / {a.monthlyValue.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
