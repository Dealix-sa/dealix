export const metadata = { title: "Import — Dealix CRM" };

export default function ImportPage() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-12">
      <h1 className="text-2xl font-semibold tracking-tight">Import leads</h1>
      <p className="mt-2 text-sm text-neutral-600">
        Operational guidance only. CSV → CRM happens via founder-run scripts, not autonomous ingestion.
      </p>

      <section className="mt-8 rounded-2xl border border-neutral-200 p-6">
        <h2 className="text-lg font-semibold">From CSV</h2>
        <pre className="mt-3 overflow-x-auto rounded-lg bg-neutral-900 p-4 text-xs text-neutral-100">
{`python3 scripts/import_leads_csv.py --csv path/to/leads.csv`}
        </pre>
      </section>

      <section className="mt-6 rounded-2xl border border-neutral-200 p-6">
        <h2 className="text-lg font-semibold">From manual research</h2>
        <p className="mt-2 text-sm text-neutral-700">
          Edit <code>business/_data/leads.json</code> directly, then:
        </p>
        <pre className="mt-3 overflow-x-auto rounded-lg bg-neutral-900 p-4 text-xs text-neutral-100">
{`python3 scripts/score_leads.py --demo
python3 scripts/generate_outreach_drafts.py --demo`}
        </pre>
      </section>

      <section className="mt-6 rounded-2xl bg-yellow-50 p-6 text-sm text-yellow-900">
        No bulk web scraping. No purchased lead lists. Manual or customer-supplied lists only.
      </section>
    </main>
  );
}
