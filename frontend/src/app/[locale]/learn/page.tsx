import type { Metadata } from "next";
import Link from "next/link";
import { LEARN_ARTICLES } from "@/content/learn/articles";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "learn");
}

export default async function LearnIndexPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const base = `/${locale}`;

  const TOPICS_AR = [
    { slug: "pdpl-guide-saudi-b2b-2026", tag: "PDPL", tagColor: "bg-blue-100 dark:bg-blue-950/30 text-blue-700 dark:text-blue-300" },
    { slug: "zatca-wave-24-guide", tag: "ZATCA", tagColor: "bg-amber-100 dark:bg-amber-950/30 text-amber-700 dark:text-amber-300" },
    { slug: "ai-governance-saudi-b2b", tag: "AI Governance", tagColor: "bg-purple-100 dark:bg-purple-950/30 text-purple-700 dark:text-purple-300" },
    { slug: "revenue-leakage-detection", tag: "Revenue Ops", tagColor: "bg-emerald-100 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300" },
    { slug: "post-lead-revenue-ops", tag: "Revenue Ops", tagColor: "bg-emerald-100 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300" },
    { slug: "what-is-proof-pack", tag: "Proof Pack", tagColor: "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300" },
    { slug: "crm-vs-revenue-ops", tag: "CRM", tagColor: "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300" },
    { slug: "no-cold-whatsapp-policy", tag: "Compliance", tagColor: "bg-red-100 dark:bg-red-950/30 text-red-700 dark:text-red-300" },
    { slug: "10-lead-audit", tag: "Sprint", tagColor: "bg-orange-100 dark:bg-orange-950/30 text-orange-700 dark:text-orange-300" },
    { slug: "audit-lead-follow-up", tag: "Process", tagColor: "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300" },
  ];

  const tagMap = Object.fromEntries(TOPICS_AR.map((t) => [t.slug, { tag: t.tag, tagColor: t.tagColor }]));

  return (
    <PublicGtmShell compactNav>
      <main className={`mx-auto max-w-4xl px-6 py-12 ${isAr ? "text-right" : "text-left"}`} dir={isAr ? "rtl" : "ltr"}>

        {/* Header */}
        <header className="mb-10">
          <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-2">
            {isAr ? "مكتبة المعرفة" : "Knowledge Library"}
          </p>
          <h1 className="text-4xl font-bold">
            {isAr ? "Dealix — تعلّم Revenue Ops بالعربية" : "Dealix — Learn Revenue Ops"}
          </h1>
          <p className="mt-4 text-muted-foreground leading-relaxed max-w-2xl">
            {isAr
              ? "محتوى متخصص لشركات B2B السعودية — PDPL، ZATCA، حوكمة AI، وتشغيل الإيرادات. كل مقالة عملية وقابلة للتطبيق فوراً."
              : "Specialized content for Saudi B2B companies — PDPL, ZATCA, AI governance, and revenue operations. Every article is practical and immediately applicable."}
          </p>
          <div className="mt-6 flex flex-wrap gap-2">
            {["PDPL", "ZATCA", "AI Governance", "Revenue Ops", "Proof Pack", "Compliance"].map((tag) => (
              <span key={tag} className="rounded-full border border-border/60 bg-card/50 px-3 py-1 text-xs font-medium text-muted-foreground">
                {tag}
              </span>
            ))}
          </div>
        </header>

        {/* Featured Articles */}
        <div className="mb-6">
          <p className="text-xs text-muted-foreground uppercase tracking-wide font-semibold mb-4">
            {isAr ? "مقالات مميزة" : "Featured Articles"}
          </p>
          <div className="grid gap-4 sm:grid-cols-2">
            {LEARN_ARTICLES.slice(0, 4).map((a) => {
              const meta = tagMap[a.slug];
              return (
                <Link
                  key={a.slug}
                  href={`${base}/learn/${a.slug}`}
                  className="group rounded-xl border border-border/60 bg-card/50 p-5 hover:border-border hover:shadow-sm transition-all"
                >
                  {meta && (
                    <span className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-medium mb-3 ${meta.tagColor}`}>
                      {meta.tag}
                    </span>
                  )}
                  <h2 className="font-semibold text-base group-hover:text-primary transition-colors">
                    {isAr ? a.titleAr : a.titleEn}
                  </h2>
                  <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
                    {isAr ? a.descriptionAr : a.descriptionEn}
                  </p>
                  {a.readTimeMinAr && (
                    <p className="text-xs text-muted-foreground mt-3">
                      ⏱ {isAr ? a.readTimeMinAr : a.readTimeMinEn}
                    </p>
                  )}
                </Link>
              );
            })}
          </div>
        </div>

        {/* All Articles */}
        <div>
          <p className="text-xs text-muted-foreground uppercase tracking-wide font-semibold mb-4">
            {isAr ? "جميع المقالات" : "All Articles"}
          </p>
          <ul className="space-y-3">
            {LEARN_ARTICLES.map((a) => {
              const meta = tagMap[a.slug];
              return (
                <li key={a.slug}>
                  <Link
                    href={`${base}/learn/${a.slug}`}
                    className="group flex items-center justify-between rounded-xl border border-border/40 bg-card/30 px-5 py-3 hover:border-border hover:bg-card/60 transition-all"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      {meta && (
                        <span className={`hidden sm:inline-block flex-shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ${meta.tagColor}`}>
                          {meta.tag}
                        </span>
                      )}
                      <span className="font-medium group-hover:text-primary transition-colors text-sm truncate">
                        {isAr ? a.titleAr : a.titleEn}
                      </span>
                    </div>
                    {a.readTimeMinAr && (
                      <span className="text-xs text-muted-foreground flex-shrink-0 ms-3">
                        {isAr ? a.readTimeMinAr : a.readTimeMinEn}
                      </span>
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>

        {/* CTA */}
        <div className="mt-12 rounded-xl border border-border/60 bg-card/50 p-6 flex flex-wrap gap-4 items-center justify-between">
          <div>
            <p className="font-semibold">{isAr ? "جاهز للتطبيق؟" : "Ready to apply?"}</p>
            <p className="text-sm text-muted-foreground mt-1">
              {isAr ? "ابدأ بـ Risk Score مجاني أو تشخيص محكوم." : "Start with a free Risk Score or governed diagnostic."}
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Link href={`${base}/risk-score`} className="rounded-lg bg-primary text-primary-foreground px-4 py-2 text-sm font-medium hover:bg-primary/90 transition-colors">
              {isAr ? "Risk Score" : "Risk Score"}
            </Link>
            <Link href={`${base}/dealix-diagnostic`} className="rounded-lg border border-border bg-card px-4 py-2 text-sm font-medium hover:bg-muted/30 transition-colors">
              {isAr ? "تشخيص" : "Diagnostic"}
            </Link>
          </div>
        </div>

      </main>
    </PublicGtmShell>
  );
}
