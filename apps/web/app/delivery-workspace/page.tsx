import { loadDemoWorkspaces, loadWorkspaces } from "@/lib/client/portal";
import { ClientStatusCard } from "@/components/client/ClientStatusCard";

export const metadata = { title: "Delivery Workspace — Dealix" };
export const dynamic = "force-static";

export default function DeliveryWorkspacePage() {
  const all = [...loadDemoWorkspaces(), ...loadWorkspaces()];
  return (
    <main className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Delivery Workspace</h1>
      <p className="mt-2 text-sm text-neutral-600">All live client workspaces. Internal view.</p>
      <div className="mt-8 grid gap-6 md:grid-cols-2">
        {all.map((w) => <ClientStatusCard key={w.id} w={w} />)}
      </div>
      <section className="mt-10 rounded-2xl border border-neutral-200 p-6">
        <h2 className="text-lg font-semibold">Operator commands</h2>
        <pre className="mt-3 overflow-x-auto rounded-lg bg-neutral-900 p-4 text-xs text-neutral-100">
{`python3 scripts/create_client_workspace.py --account-id <id> --offer "<offer>" --demo
python3 scripts/add_deliverable.py --client-id <id> --title "<title>"
python3 scripts/mark_deliverable_done.py --client-id <id> --deliverable-id latest
python3 scripts/request_client_approval.py --client-id <id> --item "<item>"
python3 scripts/record_client_approval.py --client-id <id> --approval-id latest --reviewer "<name>"
python3 scripts/generate_client_status_report.py --client-id <id> --lang both`}
        </pre>
      </section>
    </main>
  );
}
