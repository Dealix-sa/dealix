import { loadAccounts } from "@/lib/crm/crm";
import { AccountTable } from "@/components/crm/AccountTable";

export const metadata = { title: "Accounts — Dealix CRM" };
export const dynamic = "force-static";

export default function AccountsPage() {
  const accounts = loadAccounts();
  return (
    <main className="mx-auto max-w-6xl px-6 py-12">
      <h1 className="text-2xl font-semibold tracking-tight">All accounts ({accounts.length})</h1>
      <p className="mt-2 text-sm text-neutral-600">
        Sorted by score. Demo accounts labeled. Approve outreach drafts from <a className="text-blue-700 hover:underline" href="/crm/review">Review queue</a>.
      </p>
      <div className="mt-6">
        <AccountTable accounts={accounts} />
      </div>
    </main>
  );
}
