import { loadAccounts, loadOutreachQueue, pendingReviewCount } from "@/lib/crm/crm";
import { PipelineSummary } from "@/components/crm/PipelineSummary";

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
    <main className="mx-auto max-w-6xl px-6 py-12">
      <header className="mb-6">
        <h1 className="text-3xl font-semibold tracking-tight">Operator console</h1>
        <p className="mt-2 text-neutral-600">Founder's daily cockpit. No autosend. Everything queues for review.</p>
      </header>

      <PipelineSummary accounts={accounts} />

      <section className="mt-8 grid gap-5 md:grid-cols-3">
        <Stat label="Drafts pending review" value={pending} link="/review-queue" />
        <Stat label="Follow-ups due / overdue" value={dueToday} link="/followups" />
        <Stat label="Accounts in CRM" value={accounts.length} link="/crm" />
      </section>

      <section className="mt-10">
        <h2 className="text-xl font-semibold">Top 5 accounts</h2>
        <ul className="mt-3 space-y-2 text-sm">
          {top5.map((a) => (
            <li key={a.id} className="flex items-center justify-between rounded-xl border border-neutral-200 p-3">
              <a href={`/crm/accounts/${a.id}`} className="font-medium hover:underline">{a.name}</a>
              <span className="text-neutral-600">score {a.score} · {a.stage}</span>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-10 grid gap-6 md:grid-cols-2">
        <CommandBlock title="Daily commands" commands={DAILY_COMMANDS} />
        <CommandBlock title="Weekly commands" commands={WEEKLY_COMMANDS} />
      </section>
    </main>
  );
}

function Stat({ label, value, link }: { label: string; value: number; link: string }) {
  return (
    <a href={link} className="block rounded-2xl border border-neutral-200 bg-white p-5 hover:border-neutral-300">
      <p className="text-xs uppercase tracking-wide text-neutral-500">{label}</p>
      <p className="mt-1 text-3xl font-semibold">{value}</p>
    </a>
  );
}

function CommandBlock({ title, commands }: { title: string; commands: { label: string; cmd: string }[] }) {
  return (
    <div className="rounded-2xl border border-neutral-200 p-5">
      <h3 className="text-lg font-semibold">{title}</h3>
      <ul className="mt-3 space-y-3 text-sm">
        {commands.map((c) => (
          <li key={c.cmd}>
            <p className="text-neutral-700">{c.label}</p>
            <pre className="mt-1 overflow-x-auto rounded-lg bg-neutral-900 p-2 text-xs text-neutral-100">{c.cmd}</pre>
          </li>
        ))}
      </ul>
    </div>
  );
}
