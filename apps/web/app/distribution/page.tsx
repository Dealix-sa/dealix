export default function DistributionPage() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold">Distribution Portfolio</h1>
      <p className="mt-2 max-w-3xl">
        Compare sectors, channels, experiments, and conversion performance.
      </p>
      <section className="mt-8 grid gap-4 md:grid-cols-4">
        <Card label="Channels" value="0" />
        <Card label="Active Sectors" value="0" />
        <Card label="Experiments" value="0" />
        <Card label="Double Down" value="-" />
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
