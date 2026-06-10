import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ANSWERS, answerSlugs, getAnswer } from "@/content/wave3/answers";
import { MarketingShell } from "@/components/wave3/MarketingShell";
import { PrimaryCta } from "@/components/wave3/PrimaryCta";
import { ctaLabelFor, routeToHref } from "@/lib/wave3/routes";
import { buildAnswerMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string; slug: string }> };

export async function generateStaticParams() {
  const locales = ["ar", "en"];
  return locales.flatMap((locale) => answerSlugs().map((slug) => ({ locale, slug })));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale, slug } = await params;
  const a = getAnswer(slug);
  if (!a) return { title: "Dealix" };
  return buildAnswerMetadata(locale, slug, a.questionAr, a.questionEn, a.descAr, a.descEn);
}

export default async function AnswerPage({ params }: PageProps) {
  const { locale, slug } = await params;
  const a = getAnswer(slug);
  if (!a) notFound();

  const isAr = locale === "ar";
  const sections = isAr ? a.sections.ar : a.sections.en;
  const cta = ctaLabelFor(a.routeTo);
  const others = ANSWERS.filter((x) => x.slug !== slug).slice(0, 3);

  return (
    <MarketingShell locale={locale}>
      <article className={isAr ? "text-right" : "text-left"}>
        <Link href={`/${locale}/answers`} className="text-sm text-muted-foreground hover:text-foreground">
          {isAr ? "← مكتبة الإجابات" : "← Answer Library"}
        </Link>
        <h1 className="mt-4 text-3xl font-bold font-display leading-tight md:text-4xl">
          {isAr ? a.questionAr : a.questionEn}
        </h1>
        <p className="mt-3 text-lg text-muted-foreground">{isAr ? a.descAr : a.descEn}</p>

        <div className="mt-8 space-y-8">
          {sections.map((s) => (
            <section key={s.heading}>
              <h2 className="text-xl font-semibold">{s.heading}</h2>
              <p className="mt-2 leading-relaxed text-muted-foreground">{s.body}</p>
            </section>
          ))}
        </div>

        <div className="mt-12 rounded-2xl border border-border/60 bg-muted/30 p-8">
          <h2 className="text-2xl font-bold">{isAr ? "الخطوة التالية" : "Your next step"}</h2>
          <p className="mt-2 text-muted-foreground">
            {isAr ? "خطوة واحدة واضحة وآمنة." : "One clear, safe step."}
          </p>
          <div className="mt-5">
            <PrimaryCta locale={locale} href={routeToHref(a.routeTo)} labelAr={cta.ar} labelEn={cta.en} />
          </div>
        </div>

        {others.length > 0 && (
          <div className="mt-12">
            <h2 className="text-lg font-semibold">{isAr ? "إجابات ذات صلة" : "Related answers"}</h2>
            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              {others.map((o) => (
                <Link
                  key={o.slug}
                  href={`/${locale}/answers/${o.slug}`}
                  className="rounded-xl border border-border p-4 text-sm hover:bg-accent transition-colors"
                >
                  {isAr ? o.questionAr : o.questionEn}
                </Link>
              ))}
            </div>
          </div>
        )}
      </article>
    </MarketingShell>
  );
}
