import { summarize, type Account } from "@/lib/crm/crm";

export function PipelineSummary({ accounts }: { accounts: Account[] }) {
  const s = summarize(accounts);
  return (
    <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <Card label="Accounts" value={s.count.toString()} />
      <Card label="Avg score" value={s.avgScore.toString()} />
      <Card label="Pipeline MRR" value={s.pipelineMrr.toLocaleString() + " SAR"} />
      <Card label="Pipeline setup" value={s.pipelineSetup.toLocaleString() + " SAR"} />
    </section>
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
