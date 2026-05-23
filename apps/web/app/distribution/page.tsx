import { FounderShell } from "../../components/founder-shell";
import { getDistributionSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DistributionPage() {
  const dist = await getDistributionSummary();
  return (
    <FounderShell>
      <main className="p-8">
        <h1 className="text-4xl font-bold">Distribution</h1>
        <p className="mt-2 max-w-3xl">
          Channels, sectors, and live experiments. The double-down call
          highlights where to concentrate next.
        </p>
        <section className="mt-8 grid grid-cols-2 gap-4 md:grid-cols-4">
          <Tile label="Channels" value={dist.channels} />
          <Tile label="Active sectors" value={dist.active_sectors} />
          <Tile label="Experiments" value={dist.experiments} />
          <Tile label="Double-down" value={dist.double_down ?? "—"} />
        </section>
        <p className="mt-6 text-xs">
          Source: {dist.source ?? "channel_sector_scorecards"} · Updated:{" "}
          {dist.last_updated || "—"}
        </p>
      </main>
    </FounderShell>
  );
}

function Tile({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded-xl border p-4">
      <p className="text-sm">{label}</p>
      <p className="mt-2 text-2xl font-bold">{value}</p>
    </div>
  );
}
