export default function FinancePage() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold">Finance Center</h1>
      <p className="mt-2 max-w-3xl">
        Track cash, MRR, pipeline, weighted pipeline, payment capture, expenses, and runway.
      </p>
      <section className="mt-8 grid gap-4 md:grid-cols-4">
        <Card label="Cash SAR" value="0" />
        <Card label="MRR SAR" value="0" />
        <Card label="Pipeline SAR" value="0" />
        <Card label="Payment Follow-ups" value="0" />
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
