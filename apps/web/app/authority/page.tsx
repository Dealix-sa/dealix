import { getAuthorityQueue } from "../../components/marketAttack/runtimeClient";
import { MetricGrid } from "../../components/marketAttack/MetricGrid";
import { SourceBadge } from "../../components/marketAttack/SourceBadge";

export const dynamic = "force-static";

export default async function AuthorityPage() {
  const s = await getAuthorityQueue();
  return (
    <main className="grid">
      <h1>
        Authority Engine
        <SourceBadge source={s.source} />
      </h1>
      <div className="card">
        <p>
          محرك السلطة المؤسس على ملاحظات قطاع B2B السعودي. كل بوست
          ينتظر <code>approval_status=approved</code> قبل أي نشر. لا
          ادعاء بدون دليل مرفق.
        </p>
      </div>
      <MetricGrid
        metrics={[
          { label: "Posts pending", value: s.postsPending },
          { label: "Posts approved", value: s.postsApproved },
          { label: "Validated insights", value: s.insightsValidated },
          { label: "Sector report ideas", value: s.reportIdeas }
        ]}
      />
      <div className="card">
        <h2>Doctrine</h2>
        <ul>
          <li>LinkedIn only, until it proves signal. Other channels follow.</li>
          <li>
            Each post links to a sector insight or a proof-safe artifact.
          </li>
          <li>
            No engagement-farming patterns. No customer logos without
            permission.
          </li>
        </ul>
      </div>
    </main>
  );
}
