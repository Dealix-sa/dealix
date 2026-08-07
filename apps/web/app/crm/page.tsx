import { loadAccounts, loadOutreachQueue, pendingReviewCount } from "@/lib/crm/crm";
import { AccountTable } from "@/components/crm/AccountTable";
import { PipelineSummary } from "@/components/crm/PipelineSummary";

export const metadata = {
  title: "CRM — Dealix",
  description: "Founder-operated CRM. Accounts, scores, stages, drafts pending review.",
};

export const dynamic = "force-static";

export default function CrmPage() {
  const accounts = loadAccounts();
  const drafts = loadOutreachQueue();
  const pending = pendingReviewCount(drafts);

  return (
    <main className="mx-auto max-w-6xl px-6 py-12">
      <header className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">CRM</h1>
          <p className="mt-2 text-neutral-600">
            Founder-operated. All outbound is human-approved before it leaves.
          </p>
        </div>
        <nav className="flex gap-3 text-sm">
          <a href="/crm/import" className="rounded-full bg-neutral-100 px-4 py-2 hover:bg-neutral-200">Import</a>
          <a href="/crm/review" className="rounded-full bg-yellow-100 px-4 py-2 text-yellow-900 hover:bg-yellow-200">
            Review queue ({pending})
          </a>
          <a href="/crm/followups" className="rounded-full bg-neutral-100 px-4 py-2 hover:bg-neutral-200">Follow-ups</a>
          <a href="/crm/reports" className="rounded-full bg-neutral-100 px-4 py-2 hover:bg-neutral-200">Reports</a>
        </nav>
      </header>

      <PipelineSummary accounts={accounts} />

      <section className="mt-10">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-xl font-semibold">Accounts</h2>
          <a href="/crm/accounts" className="text-sm text-blue-700 hover:underline">View all →</a>
        </div>
        <AccountTable accounts={accounts.slice(0, 25)} />
      </section>
    </main>
  );
}
