import { loadAccounts } from "@/lib/crm/crm";

export const metadata = { title: "Follow-ups — Dealix" };
export const dynamic = "force-static";

export default function FollowupsTopPage() {
  const accounts = loadAccounts();
  const today = new Date().toISOString().slice(0, 10);
  const due = accounts.filter((a) => a.nextActionDate <= today);
  const upcoming = accounts.filter((a) => a.nextActionDate > today).sort((a, b) => a.nextActionDate.localeCompare(b.nextActionDate));
  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Follow-ups</h1>
      <p className="mt-2 text-sm text-neutral-600">As of {today}. Same data as /crm/followups.</p>
      <section className="mt-8">
        <h2 className="text-lg font-semibold">Due ({due.length})</h2>
        <ul className="mt-3 space-y-2 text-sm">
          {due.map((a) => (
            <li key={a.id} className="rounded-xl border border-red-100 bg-red-50 p-3">
              <a href={`/crm/accounts/${a.id}`} className="font-medium hover:underline">{a.name}</a> — {a.nextAction} ({a.nextActionDate})
            </li>
          ))}
        </ul>
      </section>
      <section className="mt-10">
        <h2 className="text-lg font-semibold">Upcoming ({upcoming.length})</h2>
        <ul className="mt-3 space-y-2 text-sm">
          {upcoming.map((a) => (
            <li key={a.id} className="rounded-xl border border-neutral-200 p-3">
              <a href={`/crm/accounts/${a.id}`} className="font-medium hover:underline">{a.name}</a> — {a.nextAction} ({a.nextActionDate})
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
