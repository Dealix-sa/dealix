import { PipelineSummary } from "@/components/crm/PipelineSummary";
import { loadAccounts, loadOutreachQueue, pendingReviewCount } from "@/lib/crm/crm";

export const metadata = { title: "Operator — Dealix" };
export const dynamic = "force-static";

const DAILY_COMMANDS = [
  { label: "Run the full daily pack", cmd: "python3 scripts/dealix_daily_operator.py --mode demo" },
  { label: "Score leads", cmd: "python3 scripts/score_leads.py --demo" },
  { label: "Generate outreach drafts", cmd: "python3 scripts/generate_outreach_drafts.py --demo" },
  { label: "Generate follow-up queue", cmd: "python3 scripts/generate_followup_queue.py" },
  { label: "Generate prospect pack", cmd: "python3 scripts/generate_prospect_pack.py" },
  { label: "Generate daily CEO brief", cmd: "python3 scripts/generate_daily_ceo_brief.py" },
  { label: "Generate weekly review", cmd: "python3 scripts/generate_weekly_operating_review.py" },
];

const WEEKLY_COMMANDS = [
  { label: "Run V10 master pack", cmd: "bash scripts/dealix_v10_run_all.sh" },
  { label: "Generate health snapshot", cmd: "python3 scripts/generate_health_snapshot.py" },
  { label: "Generate release notes", cmd: "python3 scripts/generate_release_notes.py" },
];

export default function OperatorPage() {
  const accounts = loadAccounts();
  const drafts = loadOutreachQueue();
  const pending = pendingReviewCount(drafts);
  const today = new Date().toISOString().slice(0, 10);
  const dueToday = accounts.filter((a) => a.nextActionDate <= today).length;
  const top5 = [...accounts].sort((a, b) => b.score - a.score).slice(0, 5);

  return (
    <main>
      <section>
        <p className="eyebrow">Operator console</p>
        <h1>لوحة المشغّل · Operator console</h1>
        <p className="stat-label">كوكبيت المؤسس اليومي — لا إرسال تلقائي، كل شيء ينتظر المراجعة. · No autosend; everything queues for review.</p>
      </section>

      <section className="card">
        <PipelineSummary accounts={accounts} />
      </section>

      <section className="grid-3">
        <Stat label="مسودات بانتظار المراجعة · Drafts pending" value={pending} link="/crm/review" />
        <Stat label="متابعات مستحقة · Follow-ups due" value={dueToday} link="/crm/followups" />
        <Stat label="حسابات في الـCRM · Accounts" value={accounts.length} link="/crm" />
      </section>

      <section className="card">
        <h3>أعلى 5 حسابات · Top 5 accounts</h3>
        <ul style={{ listStyle: "none", padding: 0, marginTop: "var(--sp-4)" }}>
          {top5.map((a) => (
            <li key={a.id} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 8, padding: "10px 0", borderBottom: "1px solid rgba(255,255,255,.07)" }}>
              <a href={`/crm/accounts/${a.id}`}>{a.name}</a>
              <span className="stat-label">score {a.score} · {a.stage}</span>
            </li>
          ))}
        </ul>
      </section>

      <section className="grid-2">
        <CommandBlock title="أوامر يومية · Daily commands" commands={DAILY_COMMANDS} />
        <CommandBlock title="أوامر أسبوعية · Weekly commands" commands={WEEKLY_COMMANDS} />
      </section>
    </main>
  );
}

function Stat({ label, value, link }: { label: string; value: number; link: string }) {
  return (
    <a href={link} className="card" style={{ display: "block", textAlign: "center" }}>
      <div className="stat-value">{value}</div>
      <p className="stat-label">{label}</p>
    </a>
  );
}

function CommandBlock({ title, commands }: { title: string; commands: { label: string; cmd: string }[] }) {
  return (
    <article className="card">
      <h3>{title}</h3>
      <ul style={{ listStyle: "none", padding: 0, marginTop: "var(--sp-3)" }}>
        {commands.map((c) => (
          <li key={c.cmd} style={{ marginBottom: "var(--sp-3)" }}>
            <p className="stat-label">{c.label}</p>
            <pre style={{ marginTop: 4, overflowX: "auto", borderRadius: 8, background: "rgba(0,0,0,.35)", padding: "8px 10px", fontSize: ".78rem" }}>{c.cmd}</pre>
          </li>
        ))}
      </ul>
    </article>
  );
}
