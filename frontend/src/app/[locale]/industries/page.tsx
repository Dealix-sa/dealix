import type { Metadata } from "next";
import Link from "next/link";
import { SECTORS } from "@/content/wave3/sectors";
import { MarketingShell } from "@/components/wave3/MarketingShell";
import { PrimaryCta } from "@/components/wave3/PrimaryCta";
import { buildWave3Metadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildWave3Metadata(
    locale,
    "/industries",
    "القطاعات — Dealix",
    "Industries — Dealix",
    "كيف يساعد دييلكس كل قطاع على توضيح الفرص والمتابعة والإثبات.",
    "How Dealix helps each sector clarify opportunities, follow-up, and proof.",
  );
}

export default async function IndustriesIndex({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <MarketingShell locale={locale}>
      <h1 className="text-3xl font-bold font-display md:text-4xl">
        {isAr ? "القطاعات" : "Industries"}
      </h1>
      <p className="mt-3 text-muted-foreground">
        {isAr
          ? "اختر قطاعك لترى كيف يوضّح دييلكس فرصك وخطوتك التالية."
          : "Pick your sector to see how Dealix clarifies your opportunities and next step."}
      </p>

      <div className="mt-8 grid gap-3 sm:grid-cols-2">
        {SECTORS.map((s) => (
          <Link
            key={s.slug}
            href={`/${locale}/industries/${s.slug}`}
            className="rounded-xl border border-border p-5 hover:bg-accent transition-colors"
          >
            <p className="font-semibold">{isAr ? s.nameAr : s.nameEn}</p>
            <p className="mt-1 text-sm text-muted-foreground">{isAr ? s.descAr : s.descEn}</p>
          </Link>
        ))}
      </div>

      <div className="mt-12">
        <PrimaryCta
          locale={locale}
          href="/tools/business-os-score"
          labelAr="احصل على تقييم قطاعك"
          labelEn="Get Sector Score"
        />
      </div>
    </MarketingShell>
  );
}
