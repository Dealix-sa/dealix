export default function TrustPage() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold">Trust Center</h1>
      <p className="mt-2 max-w-3xl">
        Monitor approval breaches, suppression, no-overclaim scans, AI evals, and incidents.
      </p>
      <section className="mt-8 grid gap-4 md:grid-cols-4">
        <Card label="Trust Flags" value="0" />
        <Card label="Suppression Issues" value="0" />
        <Card label="Overclaim Violations" value="0" />
        <Card label="Incidents" value="0" />
      </section>
    </main>
  );
}

function Card({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border p-4">
      <p className="text-sm opacity-70">{label}</p>
      <p className="mt-2 text-2xl font-bold">{value}</p>
    </div>
  );
}
