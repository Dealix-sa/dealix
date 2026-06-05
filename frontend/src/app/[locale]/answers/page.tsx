import type { Metadata } from "next";
import Link from "next/link";
import { ANSWERS } from "@/content/wave3/answers";
import { MarketingShell } from "@/components/wave3/MarketingShell";
import { buildWave3Metadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildWave3Metadata(
    locale,
    "/answers",
    "مكتبة الإجابات — Dealix",
    "Answer Library — Dealix",
    "إجابات عربية واضحة عن نظام تشغيل الأعمال بالذكاء الاصطناعي و Command Sprint.",
    "Clear Arabic-first answers about the AI Business Operating System and the Command Sprint.",
  );
}

export default async function AnswersIndex({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <MarketingShell locale={locale}>
      <h1 className="text-3xl font-bold font-display md:text-4xl">
        {isAr ? "مكتبة الإجابات" : "Answer Library"}
      </h1>
      <p className="mt-3 text-muted-foreground">
        {isAr
          ? "إجابات قصيرة وواضحة. كل إجابة تقودك لخطوة واحدة آمنة."
          : "Short, clear answers. Each routes you to one safe step."}
      </p>
      <div className="mt-8 grid gap-3 sm:grid-cols-2">
        {ANSWERS.map((a) => (
          <Link
            key={a.slug}
            href={`/${locale}/answers/${a.slug}`}
            className="rounded-xl border border-border p-5 hover:bg-accent transition-colors"
          >
            <p className="font-semibold">{isAr ? a.questionAr : a.questionEn}</p>
            <p className="mt-1 text-sm text-muted-foreground">{isAr ? a.descAr : a.descEn}</p>
          </Link>
        ))}
      </div>
    </MarketingShell>
  );
}
