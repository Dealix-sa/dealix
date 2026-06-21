import { loadOutreachQueue } from "@/lib/crm/crm";
import { DraftPreview } from "@/components/crm/DraftPreview";

export const metadata = { title: "Outreach lab — Dealix" };
export const dynamic = "force-static";

export default function OutreachLabPage() {
  const drafts = loadOutreachQueue();
  const byLang = (lang: string) => drafts.filter((d) => d.language === lang);

  return (
    <main className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Outreach lab</h1>
      <p className="mt-2 text-sm text-neutral-600">
        Drafts produced by `generate_outreach_drafts.py`. Founder reviews tone and edits before approval.
      </p>

      <section className="mt-8 grid gap-6 md:grid-cols-2">
        <div>
          <h2 className="text-xl font-semibold">Arabic ({byLang("ar").length})</h2>
          <div className="mt-3 space-y-4">
            {byLang("ar").slice(0, 5).map((d) => <DraftPreview key={d.id} draft={d} />)}
          </div>
        </div>
        <div>
          <h2 className="text-xl font-semibold">English ({byLang("en").length})</h2>
          <div className="mt-3 space-y-4">
            {byLang("en").slice(0, 5).map((d) => <DraftPreview key={d.id} draft={d} />)}
          </div>
        </div>
      </section>
    </main>
  );
}
