"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const TIERS = [
  { id: "starter", sar: 4999 },
  { id: "standard", sar: 9999 },
  { id: "executive", sar: 15000 },
] as const;

export function DealixDiagnosticLanding() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [catalog, setCatalog] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/public/services`)
      .then((r) => r.json())
      .then(setCatalog)
      .catch(() => setCatalog(null));
  }, []);

  const deliverables = isAr
    ? [
        "خريطة مسارات الإيراد",
        "مراجعة جودة المصادر / CRM",
        "خريطة حدود الموافقة",
        "فجوات مسار الأدلة",
        "أعلى ٣ قرارات محكومة",
        "Proof Pack + توصية Sprint/Retainer",
      ]
    : [
        "Revenue workflow map",
        "CRM / source quality review",
        "Approval boundary map",
        "Evidence trail gaps",
        "Top 3 governed decisions",
        "Proof Pack + Sprint/Retainer recommendation",
      ];

  return (
    <div className="space-y-10">
      <header className={isAr ? "text-right" : "text-left"} dir={isAr ? "rtl" : "ltr"}>
        <p className="text-sm text-muted-foreground">
          Dealix — Governed Revenue &amp; AI Operations
        </p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight">
          {isAr
            ? "تشخيص ٧ أيام — تشغيل إيراد وذكاء اصطناعي محكوم"
            : "7-Day Governed Revenue & AI Ops Diagnostic"}
        </h1>
        <p className="mt-4 max-w-2xl text-muted-foreground leading-relaxed">
          {isAr
            ? "نكشف أين يضيع الإيراد، أين CRM غير جاهز، وأين AI غير محكوم — مع أول ٣ قرارات قابلة للتنفيذ بدليل وProof Pack."
            : "We map revenue leakage, CRM/source gaps, and ungoverned AI — plus three executable decisions with evidence and a Proof Pack."}
        </p>
      </header>

      <p className="text-sm text-muted-foreground">
        {isAr ? "Ops diagnostic — منفصل عن R1 Sprint (499 ر.س) على الرئيسية." : "Ops diagnostic — separate from R1 Sprint (499 SAR) on home."}
      </p>
      <div className="grid gap-4 md:grid-cols-3">
        {TIERS.map((t) => (
          <Card key={t.id} className="p-5 border-border/80">
            <p className="text-xs uppercase tracking-wide text-muted-foreground">{t.id} Ops</p>
            <p className="mt-2 text-2xl font-semibold">
              {t.sar.toLocaleString(isAr ? "ar-SA" : "en-US")} SAR
            </p>
          </Card>
        ))}
      </div>

      <Card className="p-6 border-primary/30 bg-card/50">
        <h2 className="font-semibold text-lg">{isAr ? "المخرجات" : "Deliverables"}</h2>
        <ul
          className={`mt-3 space-y-2 text-sm text-muted-foreground list-disc ${isAr ? "text-right mr-6" : "ml-6"}`}
          dir={isAr ? "rtl" : "ltr"}
        >
          {deliverables.map((line) => (
            <li key={line}>{line}</li>
          ))}
        </ul>
      </Card>

      <div className="flex flex-wrap gap-3">
        <Button asChild size="lg">
          <Link href={`/${locale}/risk-score`}>
            {isAr ? "ابدأ Risk Score" : "Start Risk Score"}
          </Link>
        </Button>
        <Button asChild variant="outline" size="lg">
          <Link href={`/${locale}/proof-pack`}>
            {isAr ? "عيّنة Proof Pack" : "Sample Proof Pack"}
          </Link>
        </Button>
        <Button asChild variant="secondary" size="lg">
          <Link href={`/${locale}/business-now#strategy`}>
            {isAr ? "ديمو ١٢ دقيقة" : "12-min demo"}
          </Link>
        </Button>
      </div>

      <p className="text-xs text-muted-foreground max-w-2xl" dir={isAr ? "rtl" : "ltr"}>
        {isAr
          ? "لا إرسال خارجي آلي · لا ادّعاء إيراد قبل الدفع · المواد: ops_client_pack و FULL_OPS_CLOSE_ENGINE."
          : "No automated outbound · No revenue before payment · ops_client_pack + FULL_OPS_CLOSE_ENGINE."}
      </p>
    </div>
  );
}
