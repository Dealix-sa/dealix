import type { Metadata } from "next";
import Link from "next/link";
import { getTranslations } from "next-intl/server";
import { LEARN_ARTICLES } from "@/content/learn/articles";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return { title: locale === "ar" ? "تعلّم — Dealix" : "Learn — Dealix" };
}

export default async function LearnIndexPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "learn" });
  const isAr = locale === "ar";
  const base = `/${locale}`;
  return (
    <PublicGtmShell compactNav>
      <main className={`mx-auto max-w-3xl px-6 py-12 ${isAr ? "text-right" : "text-left"}`} dir={isAr ? "rtl" : "ltr"}>
        <h1 className="text-3xl font-bold">{isAr ? "مكتبة Dealix" : "Dealix Learn"}</h1>
        <ul className="mt-10 space-y-6">
          {LEARN_ARTICLES.map((a) => (
            <li key={a.slug}>
              <Link href={`${base}/learn/${a.slug}`} className="text-xl font-semibold text-primary hover:underline">
                {isAr ? a.titleAr : a.titleEn}
              </Link>
            </li>
          ))}
        </ul>
        <div className="mt-8 flex gap-3 text-sm">
          <Link href={`${base}/risk-score`}>{t("ctaRisk")}</Link>
          <Link href={`${base}/proof-pack`}>{t("ctaProof")}</Link>
          <Link href={`${base}/dealix-diagnostic`}>{t("ctaDiagnostic")}</Link>
        </div>
      </main>
    </PublicGtmShell>
  );
}
