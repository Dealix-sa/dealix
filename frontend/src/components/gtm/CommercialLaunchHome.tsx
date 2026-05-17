"use client";

import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const OFFERS = ["audit", "agencyProof", "diagnostic"] as const;

export function CommercialLaunchHome() {
  const locale = useLocale();
  const t = useTranslations("commercialLaunch");
  const isAr = locale === "ar";
  const base = `/${locale}`;

  const problemItems = [0, 1, 2, 3, 4] as const;
  const howSteps = [0, 1, 2, 3, 4] as const;
  const trustItems = [0, 1, 2, 3] as const;

  return (
    <div className="min-h-screen bg-background grid-pattern" dir={isAr ? "rtl" : "ltr"}>
      <header className="border-b border-border/60 bg-card/30 backdrop-blur-sm sticky top-0 z-10">
        <div className="mx-auto max-w-5xl px-6 py-4 flex items-center justify-between gap-4">
          <span className="font-semibold tracking-tight">Dealix</span>
          <nav className="flex items-center gap-3 text-sm">
            <Link href={`${base}/learn`} className="text-muted-foreground hover:text-foreground">
              {t("navLearn")}
            </Link>
            <Link href={`${base}/login`} className="text-primary hover:underline">
              {t("navLogin")}
            </Link>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-16 space-y-20">
        <section className={isAr ? "text-right" : "text-left"}>
          <p className="text-sm text-primary font-medium">{t("eyebrow")}</p>
          <h1 className="mt-3 text-4xl font-bold tracking-tight md:text-5xl">{t("heroTitle")}</h1>
          <p className="mt-6 max-w-2xl text-lg text-muted-foreground leading-relaxed">{t("heroSubtitle")}</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href={`${base}/risk-score`}>{t("ctaRiskScore")}</Link>
            </Button>
            <Button asChild variant="secondary" size="lg">
              <Link href={`${base}/proof-pack`}>{t("ctaSampleProof")}</Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href={`${base}/dealix-diagnostic`}>{t("ctaDemo")}</Link>
            </Button>
            <Button asChild variant="ghost" size="lg">
              <Link href={`${base}/partners`}>{t("ctaPartners")}</Link>
            </Button>
          </div>
        </section>

        <section className={isAr ? "text-right" : "text-left"}>
          <h2 className="text-2xl font-semibold">{t("problemTitle")}</h2>
          <p className="mt-2 text-muted-foreground">{t("problemIntro")}</p>
          <ul className={`mt-6 space-y-2 text-muted-foreground ${isAr ? "list-disc mr-6" : "list-disc ml-6"}`}>
            {problemItems.map((i) => (
              <li key={i}>{t(`problemItems.${i}`)}</li>
            ))}
          </ul>
        </section>

        <section className={isAr ? "text-right" : "text-left"}>
          <h2 className="text-2xl font-semibold">{t("howTitle")}</h2>
          <ol className={`mt-6 space-y-4 ${isAr ? "list-decimal mr-6" : "list-decimal ml-6"}`}>
            {howSteps.map((i) => (
              <li key={i} className="text-muted-foreground">
                <span className="font-medium text-foreground">{t(`howSteps.${i}.title`)}</span>
                {" — "}
                {t(`howSteps.${i}.body`)}
              </li>
            ))}
          </ol>
        </section>

        <section>
          <h2 className={`text-2xl font-semibold mb-6 ${isAr ? "text-right" : "text-left"}`}>{t("offersTitle")}</h2>
          <div className="grid gap-4 md:grid-cols-3">
            {OFFERS.map((key) => (
              <Card key={key} className="p-6 border-border/80 flex flex-col">
                <p className="text-xs uppercase tracking-wide text-muted-foreground">{t(`offers.${key}.label`)}</p>
                <p className="mt-2 text-xl font-semibold">{t(`offers.${key}.price`)}</p>
                <p className="mt-3 text-sm text-muted-foreground flex-1">{t(`offers.${key}.desc`)}</p>
                <Button asChild className="mt-4 w-full" variant={key === "diagnostic" ? "default" : "secondary"}>
                  <Link href={`${base}/dealix-diagnostic`}>{t("offersCta")}</Link>
                </Button>
              </Card>
            ))}
          </div>
        </section>

        <section className={`rounded-lg border border-primary/20 bg-card/50 p-8 ${isAr ? "text-right" : "text-left"}`}>
          <h2 className="text-2xl font-semibold">{t("trustTitle")}</h2>
          <ul className={`mt-4 space-y-2 text-sm text-muted-foreground ${isAr ? "list-disc mr-6" : "list-disc ml-6"}`}>
            {trustItems.map((i) => (
              <li key={i}>{t(`trustItems.${i}`)}</li>
            ))}
          </ul>
        </section>
      </main>

      <footer className="border-t border-border/60 py-8 text-center text-xs text-muted-foreground">
        {t("footer")}
      </footer>
    </div>
  );
}
