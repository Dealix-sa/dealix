"use client";
import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { CheckoutPanel } from "@/components/gtm/CheckoutPanel";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { usePublicLaunchStatus } from "@/lib/usePublicLaunchStatus";

const OFFERS = ["audit", "agencyProof", "diagnostic"] as const;
const PLANS: Record<(typeof OFFERS)[number], { plan: string; priceHint: string } | null> = {
  audit: { plan: "pilot_managed", priceHint: "499 SAR" },
  agencyProof: null,
  diagnostic: null,
};

export function CommercialLaunchHome() {
  const locale = useLocale();
  const t = useTranslations("commercialLaunch");
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const [pay, setPay] = useState<(typeof OFFERS)[number] | null>(null);
  const { moyasarLive } = usePublicLaunchStatus();

  return (
    <PublicGtmShell>
      <div className={`mx-auto max-w-5xl px-6 py-12 space-y-16 ${isAr ? "text-right" : "text-left"}`}>
        <section>
          <p className="text-sm font-medium text-dealix-green uppercase">{t("eyebrow")}</p>
          <h1 className="mt-4 text-4xl font-bold text-gradient-brand md:text-5xl">{t("heroTitle")}</h1>
          <p className="mt-6 text-lg text-muted-foreground">{t("heroSubtitle")}</p>
          <p className="mt-2 text-sm italic text-muted-foreground">{t("heroProofLine")}</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Button asChild size="lg" className="bg-[var(--dealix-deep-green)]"><Link href={`${base}/dealix-diagnostic`}>{t("ctaPrimary")}</Link></Button>
            <Button asChild variant="secondary" size="lg"><Link href={`${base}/demo`}>{isAr ? "شاهد Demo حي ⚡" : "Watch Live Demo ⚡"}</Link></Button>
            <Button asChild variant="outline" size="lg"><Link href={`${base}/proof-pack`}>{t("ctaSampleProof")}</Link></Button>
            <Link href={`${base}/risk-score`} className="text-sm text-[var(--dealix-deep-green)]">{t("ctaRiskScore")} →</Link>
          </div>
          <div className="mt-4 flex items-center gap-2 text-xs text-amber-600 dark:text-amber-400">
            <span>⏰</span>
            <span>{isAr ? "ZATCA Wave 24 — الموعد النهائي ٣٠ يونيو ٢٠٢٦ · نجهّزك للامتثال ونحسّن إيراداتك" : "ZATCA Wave 24 — Deadline June 30, 2026 · We get you compliant & revenue-optimized"}</span>
          </div>
        </section>
        <section className="rounded-xl border p-8 bg-card/60">
          <h2 className="text-xl font-semibold text-dealix-green">{t("visionTitle")}</h2>
          <ul className={`mt-4 space-y-2 ${isAr ? "list-disc mr-6" : "list-disc ml-6"}`}>{[0,1,2].map((i) => <li key={i}>{t(`visionItems.${i}`)}</li>)}</ul>
        </section>
        <section>
          <h2 className="text-2xl font-semibold">{t("pillarsTitle")}</h2>
          <p className="text-muted-foreground">{t("pillarsIntro")}</p>
          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {[0,1,2,3,4,5].map((i) => (
              <Card key={i} className="p-4"><p className="font-semibold text-dealix-green">{t(`pillars.${i}.title`)}</p><p className="mt-2 text-sm text-muted-foreground">{t(`pillars.${i}.body`)}</p></Card>
            ))}
          </div>
        </section>
        <blockquote className="border-s-4 border-dealix-gold ps-4 italic font-medium">{t("ceoQuote")}</blockquote>
        <section>
          <h2 className="text-2xl font-semibold">{t("problemTitle")}</h2>
          <ul className={`mt-4 text-sm ${isAr ? "list-disc mr-6" : "list-disc ml-6"}`}>{[0,1,2,3,4].map((i) => <li key={i}>{t(`problemItems.${i}`)}</li>)}</ul>
        </section>
        <section>
          <h2 className="text-2xl font-semibold">{t("howTitle")}</h2>
          <ol className={`mt-4 ${isAr ? "list-decimal mr-6" : "list-decimal ml-6"}`}>{[0,1,2,3,4].map((i) => <li key={i}><strong>{t(`howSteps.${i}.title`)}</strong> — {t(`howSteps.${i}.body`)}</li>)}</ol>
        </section>
        <section>
          <h2 className="text-2xl font-semibold mb-4">{t("offersTitle")}</h2>
          {!moyasarLive && <p className="mb-4 text-sm text-muted-foreground">{t("softPayHint")}</p>}
          <div className="grid gap-4 md:grid-cols-3">
            {OFFERS.map((key) => {
              const meta = PLANS[key];
              return (
                <Card key={key} className="p-6 flex flex-col">
                  <p className="text-xs uppercase text-dealix-green">{t(`offers.${key}.label`)}</p>
                  <p className="mt-2 text-2xl font-semibold text-gradient-gold">{t(`offers.${key}.price`)}</p>
                  <p className="mt-2 text-sm text-muted-foreground flex-1">{t(`offers.${key}.desc`)}</p>
                  {meta && moyasarLive ? (
                    <>
                      <Button className="mt-4" onClick={() => setPay(pay === key ? null : key)}>{isAr ? "ادفع" : "Pay"}</Button>
                      {pay === key && <CheckoutPanel plan={meta.plan} planLabel={t(`offers.${key}.label`)} priceHint={meta.priceHint} isAr={isAr} />}
                    </>
                  ) : (
                    <Button asChild className="mt-4"><Link href={`${base}/dealix-diagnostic`}>{t("softPayCta")}</Link></Button>
                  )}
                  <Button asChild variant="outline" size="sm" className="mt-2"><Link href={`${base}/dealix-diagnostic`}>{t("offersCta")}</Link></Button>
                </Card>
              );
            })}
          </div>
        </section>
        <section className="rounded-lg border p-8">
          <h2 className="text-2xl font-semibold">{t("trustTitle")}</h2>
          <ul className={`mt-4 text-sm ${isAr ? "list-disc mr-6" : "list-disc ml-6"}`}>{[0,1,2,3].map((i) => <li key={i}>{t(`trustItems.${i}`)}</li>)}</ul>
        </section>
      </div>
    </PublicGtmShell>
  );
}
