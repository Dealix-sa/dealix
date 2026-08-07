import { loadQuotes } from "@/lib/finance/deals";

export const metadata = { title: "Quotes — Dealix" };
export const dynamic = "force-static";

export default function QuotesPage() {
  const quotes = loadQuotes();
  const byStatus = (s: string) => quotes.filter((q) => q.status === s);

  return (
    <main className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Quotes</h1>
      <p className="mt-2 text-sm text-neutral-600">
        Registered quotes. Status flows: <code>draft → pending_review → approved → sent → accepted/expired/rejected</code>.
      </p>

      <section className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card label="Pending review" value={byStatus("pending_review").length.toString()} />
        <Card label="Approved" value={byStatus("approved").length.toString()} />
        <Card label="Sent" value={byStatus("sent").length.toString()} />
        <Card label="Accepted" value={byStatus("accepted").length.toString()} />
      </section>

      <section className="mt-10">
        <h2 className="text-xl font-semibold">All quotes</h2>
        <div className="mt-3 overflow-x-auto rounded-xl border border-neutral-200">
          <table className="w-full text-sm">
            <thead className="bg-neutral-50 text-left text-xs uppercase tracking-wide text-neutral-500">
              <tr>
                <th className="px-4 py-3">Quote</th>
                <th className="px-4 py-3">Account</th>
                <th className="px-4 py-3">Offer</th>
                <th className="px-4 py-3">Setup / MRR</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Valid until</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-100">
              {quotes.map((q) => (
                <tr key={q.id}>
                  <td className="px-4 py-3 font-medium">{q.id}</td>
                  <td className="px-4 py-3 text-neutral-600">{q.accountId}</td>
                  <td className="px-4 py-3 text-neutral-600">{q.offer}</td>
                  <td className="px-4 py-3 text-neutral-600">
                    {q.setupPrice.toLocaleString()} / {q.monthlyPrice.toLocaleString()}
                  </td>
                  <td className="px-4 py-3 text-neutral-600">{q.status}</td>
                  <td className="px-4 py-3 text-neutral-600">{q.validUntil ?? "—"}</td>
                </tr>
              ))}
              {quotes.length === 0 ? (
                <tr><td colSpan={6} className="px-4 py-6 text-center text-sm text-neutral-500">No quotes yet. Run `scripts/generate_quote.py`.</td></tr>
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
