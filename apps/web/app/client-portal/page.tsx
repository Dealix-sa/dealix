export const metadata = { title: "Client Portal — Dealix" };

export default function ClientPortalIndex() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Client Portal</h1>
      <p className="mt-2 text-sm text-neutral-600">
        Where Dealix clients see status, deliverables, approvals, proof, and the next review.
      </p>
      <section className="mt-8 rounded-2xl bg-neutral-50 p-6">
        <h2 className="text-lg font-semibold">Try the demo workspace</h2>
        <p className="mt-2 text-sm text-neutral-600">No login required. Demo data clearly labeled.</p>
        <a href="/client-portal/demo" className="mt-4 inline-block rounded-full bg-neutral-900 px-5 py-2 text-sm font-medium text-white">
          Open demo workspace →
        </a>
      </section>
      <section className="mt-6 rounded-2xl border border-neutral-200 p-6">
        <h2 className="text-lg font-semibold">Production portal (V13)</h2>
        <p className="mt-2 text-sm text-neutral-600">
          Production tenancy requires IdP wiring (see <a className="text-blue-700 hover:underline" href="/safety">/safety</a>) and a customer-specific workspace ID at <code>/client-portal/[id]</code>.
        </p>
      </section>
    </main>
  );
}
