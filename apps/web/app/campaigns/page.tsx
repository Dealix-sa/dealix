import { getCampaignSummary } from "../../components/marketAttack/runtimeClient";
import { MetricGrid } from "../../components/marketAttack/MetricGrid";
import { SourceBadge } from "../../components/marketAttack/SourceBadge";

export const dynamic = "force-static";

export default async function CampaignsPage() {
  const s = await getCampaignSummary();
  const cs = s.campaignsByStatus;
  const qs = s.queueByStatus;
  return (
    <main className="grid">
      <h1>
        Campaign Command Room
        <SourceBadge source={s.source} />
      </h1>
      <div className="card">
        <p>
          هذه الصفحة تعرض حالة الحملات والأصول والقائمة. لا يخرج شيء من
          الصف بدون صفّ موافقة صريح في
          <code> approval_log.csv</code>.
        </p>
      </div>
      <MetricGrid
        metrics={[
          { label: "Draft", value: cs.draft ?? 0 },
          { label: "Pending approval", value: cs.pending_approval ?? 0 },
          { label: "Live", value: cs.live ?? 0 },
          { label: "Paused", value: cs.paused ?? 0 },
          { label: "Complete", value: cs.complete ?? 0 },
          { label: "Killed", value: cs.killed ?? 0 }
        ]}
      />
      <h2>Queue</h2>
      <MetricGrid
        metrics={[
          { label: "Queued", value: qs.queued ?? 0 },
          { label: "Approved", value: qs.approved ?? 0 },
          { label: "Sent", value: qs.sent ?? 0 },
          { label: "Held", value: qs.held ?? 0 },
          { label: "Rejected", value: qs.rejected ?? 0 }
        ]}
      />
      <h2>Funnel</h2>
      <MetricGrid
        metrics={[
          { label: "Impressions", value: s.results.impressions },
          { label: "Clicks", value: s.results.clicks },
          { label: "Replies", value: s.results.replies },
          {
            label: "Positive replies",
            value: s.results.positiveReplies,
            hint: "what we actually act on"
          },
          { label: "Samples requested", value: s.results.samples },
          { label: "Proposals sent", value: s.results.proposals },
          { label: "Payments collected", value: s.results.payments }
        ]}
      />
      <div className="card">
        <h2>Approval doctrine</h2>
        <ul>
          <li>Every campaign has an `approval_class`.</li>
          <li>Every asset has `approval_status` and `proof_status`.</li>
          <li>
            Sending happens only through documented manual channels — no AI
            agent sends without an approval row.
          </li>
        </ul>
      </div>
    </main>
  );
}
