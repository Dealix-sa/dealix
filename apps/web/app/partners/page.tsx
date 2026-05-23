import { getPartnerPipeline } from "../../components/marketAttack/runtimeClient";
import { MetricGrid } from "../../components/marketAttack/MetricGrid";
import { SourceBadge } from "../../components/marketAttack/SourceBadge";

export const dynamic = "force-static";

export default async function PartnersPage() {
  const s = await getPartnerPipeline();
  const t = s.byType;
  const st = s.byStatus;
  return (
    <main className="grid">
      <h1>
        Partners
        <SourceBadge source={s.source} />
      </h1>
      <div className="card">
        <p>
          ثلاث طبقات شركاء أولى: الوكالات، أنظمة ERP/CRM، شركات الأمن
          السيبراني وGRC. كل صف يخضع لـ
          <code> PARTNER_REFERRAL_TERMS_GUARDRAILS.md</code>.
        </p>
      </div>
      <MetricGrid
        metrics={[
          { label: "Agencies", value: t.agency ?? 0 },
          { label: "ERP / CRM", value: t.erp_crm ?? 0 },
          { label: "Cyber / GRC", value: t.cybersecurity_grc ?? 0 },
          { label: "Consultancy", value: t.consultancy ?? 0 },
          { label: "Other", value: t.other ?? 0 }
        ]}
      />
      <h2>Status</h2>
      <MetricGrid
        metrics={[
          { label: "Prospect", value: st.prospect ?? 0 },
          { label: "Intro meeting", value: st.intro_meeting ?? 0 },
          { label: "Pilot partner", value: st.pilot_partner ?? 0 },
          { label: "Active", value: st.active ?? 0 },
          { label: "Paused", value: st.paused ?? 0 },
          { label: "Terminated", value: st.terminated ?? 0 }
        ]}
      />
      <MetricGrid
        metrics={[
          {
            label: "High referral potential",
            value: s.highReferralPartners
          },
          {
            label: "White-label candidates",
            value: s.whiteLabelCandidates,
            hint: "governance review required"
          }
        ]}
      />
      <div className="card">
        <h2>Guardrails</h2>
        <ul>
          <li>No revenue share outside the approved partner program.</li>
          <li>No exclusivity without a counter-signed contract.</li>
          <li>White-label is governance-reviewed; not a default offer.</li>
        </ul>
      </div>
    </main>
  );
}
