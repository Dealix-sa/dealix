import { WorkerTable } from "../../components/workers/WorkerTable";
import { KPIGrid } from "../../components/ceo/KPIGrid";
import type { Counter, WorkerRow } from "../../lib/types";

// TODO: live wire — GET /api/v1/observability + /api/v1/agent-mesh
const workers: WorkerRow[] = [];

const totals: Counter[] = [
  { label: "Total Workers", value: workers.length },
  { label: "OK", value: workers.filter((w) => w.status === "ok").length },
  { label: "Degraded", value: workers.filter((w) => w.status === "degraded").length },
  { label: "Failed", value: workers.filter((w) => w.status === "failed").length },
  { label: "Idle", value: workers.filter((w) => w.status === "idle").length },
  { label: "Total Backlog", value: workers.reduce((s, w) => s + w.backlog, 0) },
];

export default function WorkersPage() {
  return (
    <main className="grid">
      <section>
        <h1>Workers</h1>
        <p style={{ maxWidth: 720 }}>
          هل المكاين شغّالة 24/7؟ كل worker: آخر تشغيل، الحالة، الفشل، الطابور، التشغيل القادم.
        </p>
      </section>
      <KPIGrid title="Health" counters={totals} />
      <WorkerTable workers={workers} />
    </main>
  );
}
