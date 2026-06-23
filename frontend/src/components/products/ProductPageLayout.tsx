"use client";

import type { ReactNode } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";
import { ArrowLeft, ArrowRight, ShieldCheck, ShieldAlert } from "lucide-react";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export interface DeliverablePhase {
  days: "7" | "14" | "30";
  titleAr: string;
  titleEn: string;
  itemsAr: string[];
  itemsEn: string[];
}

export interface ProductPageLayoutProps {
  nameAr: string;
  nameEn: string;
  taglineAr: string;
  taglineEn: string;
  problemAr: string;
  problemEn: string;
  whatItDoesAr: string[];
  whatItDoesEn: string[];
  deliverables: DeliverablePhase[];
  pricingHintAr: string;
  pricingHintEn: string;
  outboundNote?: boolean;
  children?: ReactNode;
}

export function ProductPageLayout({
  nameAr,
  nameEn,
  taglineAr,
  taglineEn,
  problemAr,
  problemEn,
  whatItDoesAr,
  whatItDoesEn,
  deliverables,
  pricingHintAr,
  pricingHintEn,
  outboundNote = false,
  children,
}: ProductPageLayoutProps) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const dir = isAr ? "rtl" : "ltr";

  return (
    <PublicGtmShell compactNav>
      <div dir={dir} className="mx-auto max-w-5xl px-6 py-12 grid-pattern">
        {/* HERO */}
        <section className="mb-10">
          <Badge variant="gold" className="mb-3">
            {isAr ? "منتج Dealix" : "Dealix Product"}
          </Badge>
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
            {isAr ? nameAr : nameEn}
          </h1>
          <p className="mt-2 text-lg text-muted-foreground max-w-2xl">
            {isAr ? taglineAr : taglineEn}
          </p>
          <p className="mt-1 text-sm text-muted-foreground/70" dir={isAr ? "ltr" : "rtl"}>
            {isAr ? nameEn : nameAr}
          </p>
          <div className="mt-5 flex flex-wrap gap-3">
            <Button asChild variant="gold" size="lg">
              <Link href={`${base}/book-call`}>
                {isAr ? "احجز التشخيص" : "Book Diagnostic"}
                {isAr ? <ArrowLeft className="size-4" /> : <ArrowRight className="size-4" />}
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href={`${base}/pricing`}>
                {isAr ? "شاهد الأسعار" : "See pricing"}
              </Link>
            </Button>
          </div>
        </section>

        {/* OUTBOUND SAFETY NOTE */}
        {outboundNote && (
          <div className="mb-8 flex items-start gap-3 rounded-xl border border-amber-500/30 bg-amber-500/5 p-4">
            <ShieldAlert className="size-5 text-amber-400 shrink-0 mt-0.5" />
            <div className="text-sm text-amber-200/90">
              {isAr
                ? "هذا المنتج يعمل افتراضياً في وضع المسودات فقط (OUTBOUND_MODE=draft_only). لا يتم أي إرسال خارجي دون موافقتك الصريحة وبعد استيفاء بوابات الأمان للقناة."
                : "This product runs in draft-only mode by default (OUTBOUND_MODE=draft_only). No external send happens without your explicit approval and after channel safety gates are satisfied."}
            </div>
          </div>
        )}

        {/* PROBLEM */}
        <section className="mb-10">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span className="inline-block size-2 rounded-full bg-red-500/70" />
                {isAr ? "المشكلة" : "The problem"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground leading-relaxed">
                {isAr ? problemAr : problemEn}
              </p>
            </CardContent>
          </Card>
        </section>

        {/* WHAT IT DOES */}
        <section className="mb-10">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span className="inline-block size-2 rounded-full bg-emerald-500/70" />
                {isAr ? "ماذا يفعل" : "What it does"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {(isAr ? whatItDoesAr : whatItDoesEn).map((item, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-foreground/90">
                    <ShieldCheck className="size-4 text-emerald-400 shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </section>

        {/* DELIVERABLES */}
        <section className="mb-10">
          <h2 className="mb-4 text-xl font-semibold">
            {isAr ? "المخرجات على مراحل" : "Deliverables by phase"}
          </h2>
          <div className="grid gap-4 md:grid-cols-3">
            {deliverables.map((phase) => (
              <Card key={phase.days} className="border-gold-500/20">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>{isAr ? phase.titleAr : phase.titleEn}</span>
                    <Badge variant="gold">{phase.days}-day</Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-sm">
                    {(isAr ? phase.itemsAr : phase.itemsEn).map((item, i) => (
                      <li key={i} className="flex items-start gap-2 text-muted-foreground">
                        <span className="text-gold-400 shrink-0">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* PRICING HINT */}
        <section className="mb-10">
          <Card className="border-emerald-500/20 bg-emerald-500/5">
            <CardContent className="py-5">
              <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">
                    {isAr ? "تلميح التسعير" : "Pricing hint"}
                  </p>
                  <p className="font-medium text-foreground">
                    {isAr ? pricingHintAr : pricingHintEn}
                  </p>
                </div>
                <Button asChild variant="emerald">
                  <Link href={`${base}/pricing`}>
                    {isAr ? "تفاصيل الأسعار" : "Pricing details"}
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        </section>

        {children}

        {/* CTA */}
        <section className="mt-12 rounded-2xl border border-border bg-card p-8 text-center">
          <h2 className="text-2xl font-bold">
            {isAr ? "ابدأ بتشخيص ٢٠ دقيقة" : "Start with a 20-minute diagnostic"}
          </h2>
          <p className="mt-2 text-muted-foreground">
            {isAr
              ? "خطة واضحة وأدلة — لا وعود. موافقتك مطلوبة قبل أي إجراء."
              : "Clear plan and evidence — no promises. Your approval is required before any action."}
          </p>
          <div className="mt-5">
            <Button asChild variant="gold" size="lg">
              <Link href={`${base}/book-call`}>
                {isAr ? "احجز التشخيص" : "Book Diagnostic"}
                {isAr ? <ArrowLeft className="size-4" /> : <ArrowRight className="size-4" />}
              </Link>
            </Button>
          </div>
        </section>
      </div>
    </PublicGtmShell>
  );
}

export default ProductPageLayout;