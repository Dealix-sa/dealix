import { loadDeals, summarizeDeals, setupValue, mrrValue, dealStatus } from "@/lib/finance/deals";

export const metadata = { title: "Deals — Dealix" };
export const dynamic = "force-static";

export default function DealsPage() {
  const deals = loadDeals();
  const s = summarizeDeals(deals);

  return (
    <main className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Deals</h1>
      <p className="mt-2 text-sm text-neutral-600">
        Source of truth: <code>business/_data/deals.ledger.json</code>. Demo records labeled.
      </p>

      <section className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card label="Open" value={s.open.toString()} />
        <Card label="Won" value={s.won.toString()} />
        <Card label="Lost" value={s.lost.toString()} />
        <Card label="Won MRR" value={`${s.wonMrr.toLocaleString()} SAR`} />
      </section>

      <section className="mt-10">
        <h2 className="text-xl font-semibold">Ledger</h2>
        <div className="mt-3 overflow-x-auto rounded-xl border border-neutral-200">
          <table className="w-full text-sm">
            <thead className="bg-neutral-50 text-left text-xs uppercase tracking-wide text-neutral-500">
              <tr>
                <th className="px-4 py-3">Account</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Offer</th>
                <th className="px-4 py-3">Setup (SAR)</th>
                <th className="px-4 py-3">MRR (SAR)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-100">
              {deals.map((d, i) => (
                <tr key={d.id ?? i}>
                  <td className="px-4 py-3 font-medium">{d.account_id ?? d.accountId ?? "—"}</td>
                  <td className="px-4 py-3 text-neutral-600">{dealStatus(d)}</td>
                  <td className="px-4 py-3 text-neutral-600">{d.offer ?? "—"}</td>
                  <td className="px-4 py-3 text-neutral-600">{setupValue(d).toLocaleString()}</td>
                  <td className="px-4 py-3 text-neutral-600">{mrrValue(d).toLocaleString()}</td>
                </tr>
              ))}
              {deals.length === 0 ? (
                <tr><td colSpan={5} className="px-4 py-6 text-center text-sm text-neutral-500">No deals yet. Run `scripts/mark_deal_won.py --demo`.</td></tr>
              ) : null}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}

function Card({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-neutral-200 bg-white p-5">
      <p className="text-xs uppercase tracking-wide text-neutral-500">{label}</p>
      <p className="mt-1 text-2xl font-semibold">{value}</p>
    </div>
  );
}
