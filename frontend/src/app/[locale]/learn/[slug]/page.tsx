import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { Button } from "@/components/ui/button";
import { allSlugs, getArticle } from "@/content/learn/articles";

type PageProps = {
  params: Promise<{ locale: string; slug: string }>;
};

export async function generateStaticParams() {
  const locales = ["ar", "en"];
  return locales.flatMap((locale) => allSlugs().map((slug) => ({ locale, slug })));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale, slug } = await params;
  const article = getArticle(slug);
  if (!article) return { title: "Dealix Learn" };
  const isAr = locale === "ar";
  return {
    title: isAr ? article.titleAr : article.titleEn,
    description: isAr ? article.descriptionAr : article.descriptionEn,
  };
}

export default async function LearnArticlePage({ params }: PageProps) {
  const { locale, slug } = await params;
  const article = getArticle(slug);
  if (!article) notFound();

  const t = await getTranslations({ locale, namespace: "learn" });
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const sections = isAr ? article.sections.ar : article.sections.en;

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>
      <header className="border-b border-border/60">
        <div className="mx-auto max-w-3xl px-6 py-4 flex flex-wrap gap-4 text-sm">
          <Link href={base} className="text-muted-foreground hover:text-foreground">
            {t("backHome")}
          </Link>
          <Link href={`${base}/learn`} className="text-muted-foreground hover:text-foreground">
            {t("backLearn")}
          </Link>
        </div>
      </header>

      <article className={`mx-auto max-w-3xl px-6 py-12 ${isAr ? "text-right" : "text-left"}`}>
        <h1 className="text-3xl font-bold">{isAr ? article.titleAr : article.titleEn}</h1>
        <p className="mt-4 text-muted-foreground">{isAr ? article.descriptionAr : article.descriptionEn}</p>

        <div className="mt-10 space-y-8">
          {sections.map((s) => (
            <section key={s.heading}>
              <h2 className="text-xl font-semibold">{s.heading}</h2>
              <p className="mt-2 text-muted-foreground leading-relaxed">{s.body}</p>
            </section>
          ))}
        </div>

        <div className="mt-12 flex flex-wrap gap-3">
          <Button asChild>
            <Link href={`${base}/risk-score`}>{t("ctaRisk")}</Link>
          </Button>
          <Button asChild variant="secondary">
            <Link href={`${base}/proof-pack`}>{t("ctaProof")}</Link>
          </Button>
          <Button asChild variant="outline">
            <Link href={`${base}/dealix-diagnostic`}>{t("ctaDiagnostic")}</Link>
          </Button>
        </div>
      </article>
    </div>
  );
}
