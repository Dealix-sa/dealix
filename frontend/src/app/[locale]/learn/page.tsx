import type { Metadata } from "next";
import Link from "next/link";
import { getTranslations } from "next-intl/server";
import { LEARN_ARTICLES } from "@/content/learn/articles";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "تعلّم — Dealix Revenue OS" : "Learn — Dealix Revenue OS",
    description: isAr
      ? "مقالات AEO: Post-Lead Revenue Ops، Proof Pack، حوكمة، وكالات السعودية."
      : "AEO articles: Post-Lead Revenue Ops, Proof Pack, governance, Saudi agencies.",
  };
}

export default async function LearnIndexPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "learn" });
  const isAr = locale === "ar";
  const base = `/${locale}`;

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>
      <header className="border-b border-border/60">
        <div className="mx-auto max-w-3xl px-6 py-4 flex gap-4 text-sm">
          <Link href={base} className="text-muted-foreground hover:text-foreground">
            {t("backHome")}
          </Link>
        </div>
      </header>
      <main className={`mx-auto max-w-3xl px-6 py-12 ${isAr ? "text-right" : "text-left"}`}>
        <h1 className="text-3xl font-bold">
          {isAr ? "مكتبة Dealix — AEO" : "Dealix Learn — AEO"}
        </h1>
        <p className="mt-4 text-muted-foreground">
          {isAr
            ? "إجابات قصيرة للأسئلة الشائعة — Risk Score وProof Pack وديمو عند الجاهزية."
            : "Short answers to common questions — Risk Score, Proof Pack, and demo when ready."}
        </p>
        <ul className="mt-10 space-y-6">
          {LEARN_ARTICLES.map((a) => (
            <li key={a.slug} className="border-b border-border/50 pb-6">
              <Link
                href={`${base}/learn/${a.slug}`}
                className="text-xl font-semibold text-primary hover:underline"
              >
                {isAr ? a.titleAr : a.titleEn}
              </Link>
              <p className="mt-2 text-sm text-muted-foreground">
                {isAr ? a.descriptionAr : a.descriptionEn}
              </p>
            </li>
          ))}
        </ul>
        <div className="mt-12 flex flex-wrap gap-3">
          <Link
            href={`${base}/risk-score`}
            className="text-sm font-medium text-primary hover:underline"
          >
            {t("ctaRisk")}
          </Link>
          <Link
            href={`${base}/proof-pack`}
            className="text-sm font-medium text-primary hover:underline"
          >
            {t("ctaProof")}
          </Link>
          <Link
            href={`${base}/dealix-diagnostic`}
            className="text-sm font-medium text-primary hover:underline"
          >
            {t("ctaDiagnostic")}
          </Link>
        </div>
      </main>
    </div>
  );
}
