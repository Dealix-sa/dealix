const funnel: Array<[string, number]> = [
  ["Lead Intelligence", 0],
  ["A Leads", 0],
  ["Pending Approval", 0],
  ["Approved Outreach", 0],
  ["Sent", 0],
  ["Replies", 0],
  ["Positive Replies", 0],
  ["Samples", 0],
  ["Proposals", 0],
  ["Payment Capture", 0],
];

export default function SalesCockpitPage() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold">Sales Cockpit</h1>
      <p className="mt-2 max-w-3xl">
        Track the Dealix revenue factory from market intelligence to payment capture.
      </p>
      <section className="mt-8 grid gap-4 md:grid-cols-5">
        {funnel.map(([label, value]) => (
          <div key={label} className="rounded-xl border p-4">
            <p className="text-xs uppercase opacity-60">{label}</p>
            <p className="mt-2 text-2xl font-bold">{value}</p>
          </div>
        ))}
      </section>
    </main>
  );
}
