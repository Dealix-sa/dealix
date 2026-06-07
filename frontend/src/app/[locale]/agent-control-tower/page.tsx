export default function AgentControlTowerPage() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <p className="text-sm uppercase tracking-[0.3em] text-neutral-500">Dealix OS</p>
      <h1 className="mt-4 text-4xl font-bold">Agent Control Tower</h1>
      <p className="mt-4 max-w-3xl text-lg text-neutral-600">
        طبقة تشغيل داخلية للوكلاء: queue، مخرجات، موافقات، تقييم، ومخاطر. كل إجراء خارجي يبقى تحت مراجعة بشرية.
      </p>
      <section className="mt-10 grid gap-4 md:grid-cols-4">
        {['Queued Tasks','Needs Approval','Draft Outputs','Incidents'].map((x) => (
          <div key={x} className="rounded-2xl border p-5"><h2 className="font-semibold">{x}</h2><p className="mt-2 text-sm text-neutral-500">Connected to V7 scripts/data.</p></div>
        ))}
      </section>
    </main>
  );
}
