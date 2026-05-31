"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import api from "@/lib/api";

const SECTORS_AR: Record<string, string> = {
  technology: "تقنية المعلومات",
  healthcare: "الرعاية الصحية",
  real_estate: "العقارات",
  logistics: "اللوجستيات والنقل",
  b2b_services: "خدمات B2B",
  engineering: "الهندسة والمقاولات",
  food_and_beverage: "المطاعم والأغذية",
  ecommerce: "التجارة الإلكترونية",
  training: "التدريب والتعليم",
  marketing_agency: "وكالات التسويق",
  finance: "المالية والاستشارات",
  other: "أخرى",
};

const SECTORS_EN: Record<string, string> = {
  technology: "Technology / SaaS",
  healthcare: "Healthcare",
  real_estate: "Real Estate",
  logistics: "Logistics & Transport",
  b2b_services: "B2B Services",
  engineering: "Engineering & Construction",
  food_and_beverage: "Food & Beverage",
  ecommerce: "E-Commerce",
  training: "Training & Education",
  marketing_agency: "Marketing Agency",
  finance: "Finance & Consulting",
  other: "Other",
};

const PAIN_POINTS_AR = [
  "ضعف تحويل العروض إلى عملاء",
  "بيانات CRM غير موثوقة",
  "AI غير محكوم بدون governance",
  "تسرّب إيراد غير مُفسَّر",
  "ZATCA Wave 24 — الامتثال قبل يونيو 2026",
  "PDPL — حماية البيانات الشخصية",
  "غياب الرؤية على قرارات الإيراد",
];

const PAIN_POINTS_EN = [
  "Low proposal-to-customer conversion",
  "Unreliable CRM / data quality",
  "Ungoverned AI without oversight",
  "Unexplained revenue leakage",
  "ZATCA Wave 24 — June 2026 deadline",
  "PDPL — personal data compliance",
  "No visibility on revenue decisions",
];

const STEPS_AR = [
  { n: "١", title: "أدخل بيانات شركتك", desc: "اسم الشركة والقطاع والمشكلة الرئيسية" },
  { n: "٢", title: "تحليل فوري بالذكاء الاصطناعي", desc: "نكشف فجوات الإيراد وCRM وAI خلال ٧ أيام" },
  { n: "٣", title: "Proof Pack مُتحقَّق منه", desc: "أول ٣ قرارات قابلة للتنفيذ بدليل مُوثَّق" },
  { n: "٤", title: "قرار بيدك", desc: "تختار: Sprint 499 SAR أو Retainer شهري" },
];

const STEPS_EN = [
  { n: "1", title: "Enter company details", desc: "Name, sector, main challenge" },
  { n: "2", title: "AI analysis in 7 days", desc: "Revenue, CRM, and AI governance gaps mapped" },
  { n: "3", title: "Verified Proof Pack", desc: "Top 3 executable decisions with documented evidence" },
  { n: "4", title: "Your decision", desc: "Choose: 499 SAR Sprint or monthly Retainer" },
];

const SOCIAL_PROOF_AR = [
  { sector: "لوجستيات", result: "كشف تسرّب إيراد 18% غير مُفسَّر", city: "الرياض" },
  { sector: "خدمات B2B", result: "جهّزناهم لـ ZATCA قبل الموعد", city: "جدة" },
  { sector: "رعاية صحية", result: "ضبط governance للـ AI قبل PDPL", city: "الدمام" },
];

export function DealixDiagnosticLanding() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const steps = isAr ? STEPS_AR : STEPS_EN;
  const painPoints = isAr ? PAIN_POINTS_AR : PAIN_POINTS_EN;
  const sectorLabels = isAr ? SECTORS_AR : SECTORS_EN;

  const [companyName, setCompanyName] = useState("");
  const [selectedSector, setSelectedSector] = useState("");
  const [selectedPains, setSelectedPains] = useState<string[]>([]);
  const [sectorMatch, setSectorMatch] = useState<string | null>(null);
  const [diagLoading, setDiagLoading] = useState(false);
  const [diagResult, setDiagResult] = useState<{
    recommended_bundle?: string;
    bundle_name_ar?: string;
    bundle_name_en?: string;
    services_in_bundle?: string[];
  } | null>(null);
  const [diagError, setDiagError] = useState("");
  const nameRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (companyName.length > 2) {
      const lower = companyName.toLowerCase();
      const matched = Object.entries(sectorLabels).find(([, label]) =>
        label.toLowerCase().includes(lower)
      );
      if (matched) setSectorMatch(matched[1]);
      else setSectorMatch(null);
    } else {
      setSectorMatch(null);
    }
  }, [companyName, sectorLabels]);

  const togglePain = (p: string) =>
    setSelectedPains((prev) =>
      prev.includes(p) ? prev.filter((x) => x !== p) : [...prev, p]
    );

  async function runDiagnostic() {
    if (!companyName.trim()) {
      nameRef.current?.focus();
      return;
    }
    setDiagLoading(true);
    setDiagError("");
    setDiagResult(null);
    try {
      const res = await api.postPublicDiagnostic({
        company: companyName.trim(),
        sector: selectedSector || "b2b_services",
      });
      setDiagResult(res.data as typeof diagResult);
    } catch {
      setDiagError(isAr ? "تعذّر تحميل التشخيص. حاول مجدداً." : "Could not load diagnostic. Please retry.");
    } finally {
      setDiagLoading(false);
    }
  }

  const ctaHref = `/${locale}/offer/lead-intelligence-sprint${
    companyName ? `?company=${encodeURIComponent(companyName)}&sector=${selectedSector}` : ""
  }`;

  return (
    <div className="space-y-12" dir={isAr ? "rtl" : "ltr"}>
      {/* Hero */}
      <header className={isAr ? "text-right" : "text-left"}>
        <div className="flex flex-wrap gap-2 mb-3">
          <Badge variant="outline" className="text-xs border-amber-500/50 text-amber-600 bg-amber-50 dark:bg-amber-950/30">
            {isAr ? "⏰ ZATCA Wave 24 — يونيو 2026" : "⏰ ZATCA Wave 24 — June 2026"}
          </Badge>
          <Badge variant="outline" className="text-xs border-blue-500/50 text-blue-600 bg-blue-50 dark:bg-blue-950/30">
            {isAr ? "سوق الذكاء الاصطناعي السعودي — $13.3B (2026)" : "Saudi AI Market — $13.3B (2026)"}
          </Badge>
        </div>
        <h1 className="text-3xl font-bold tracking-tight leading-tight">
          {isAr
            ? "تشخيص ٧ أيام — Proof Pack محكوم بالدليل"
            : "7-Day Diagnostic — Evidence-Governed Proof Pack"}
        </h1>
        <p className="mt-3 max-w-2xl text-muted-foreground leading-relaxed">
          {isAr
            ? "نكشف أين يضيع الإيراد، أين CRM غير جاهز، وأين AI غير محكوم — مع أول ٣ قرارات قابلة للتنفيذ بدليل حقيقي وProof Pack."
            : "We map revenue leakage, CRM gaps, and ungoverned AI — then deliver top 3 executable decisions with real evidence and a Proof Pack."}
        </p>
      </header>

      {/* 4-Step Process */}
      <section>
        <h2 className="text-lg font-semibold mb-4">
          {isAr ? "كيف يعمل التشخيص" : "How the Diagnostic Works"}
        </h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {steps.map((s) => (
            <div
              key={s.n}
              className="flex gap-3 items-start p-4 rounded-xl border border-border/60 bg-card/50"
            >
              <span className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-sm">
                {s.n}
              </span>
              <div>
                <p className="font-medium text-sm">{s.title}</p>
                <p className="text-xs text-muted-foreground mt-0.5">{s.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Interactive Form */}
      <Card className="p-6 border-primary/20 bg-gradient-to-br from-card to-card/50">
        <h2 className="font-semibold text-lg mb-4">
          {isAr ? "ابدأ تشخيصك المجاني" : "Start Your Free Diagnostic"}
        </h2>
        <div className="space-y-4">
          <div>
            <label className="text-xs text-muted-foreground mb-1 block">
              {isAr ? "اسم الشركة" : "Company Name"}
            </label>
            <Input
              ref={nameRef}
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              placeholder={isAr ? "مثال: شركة الواحة للاستشارات" : "e.g. Horizon Tech Co."}
              className="max-w-sm"
            />
            {sectorMatch && (
              <p className="text-xs text-primary mt-1">
                {isAr ? `تطابق قطاع: ${sectorMatch}` : `Sector match: ${sectorMatch}`}
              </p>
            )}
          </div>
          <div>
            <label className="text-xs text-muted-foreground mb-1 block">
              {isAr ? "القطاع" : "Sector"}
            </label>
            <div className="flex flex-wrap gap-2">
              {Object.entries(sectorLabels)
                .filter(([k]) => k !== "other")
                .map(([key, label]) => (
                  <button
                    key={key}
                    onClick={() => setSelectedSector(selectedSector === key ? "" : key)}
                    className={`px-3 py-1 rounded-full text-xs border transition-colors ${
                      selectedSector === key
                        ? "bg-primary text-primary-foreground border-primary"
                        : "border-border text-muted-foreground hover:border-primary/50"
                    }`}
                  >
                    {label}
                  </button>
                ))}
            </div>
          </div>
          <div>
            <label className="text-xs text-muted-foreground mb-2 block">
              {isAr ? "المشكلة الرئيسية (اختر ما ينطبق)" : "Main challenges (select all that apply)"}
            </label>
            <div className="flex flex-wrap gap-2">
              {painPoints.map((p) => (
                <button
                  key={p}
                  onClick={() => togglePain(p)}
                  className={`px-3 py-1 rounded-full text-xs border transition-colors ${
                    selectedPains.includes(p)
                      ? "bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-400"
                      : "border-border text-muted-foreground hover:border-amber-300"
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>
          <div className="flex flex-wrap gap-3 pt-2">
            <Button
              size="lg"
              className="font-semibold"
              onClick={runDiagnostic}
              disabled={diagLoading || !companyName.trim()}
            >
              {diagLoading
                ? (isAr ? "جارٍ التحليل…" : "Analysing…")
                : (isAr ? "احصل على تشخيص فوري ←" : "Get Instant Diagnostic →")}
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href={`/${locale}/demo`}>
                {isAr ? "شاهد demo مباشر" : "Watch live demo"}
              </Link>
            </Button>
          </div>

          {diagError && (
            <p className="text-sm text-destructive mt-2">{diagError}</p>
          )}

          {diagResult && (
            <div className="mt-4 rounded-xl border border-emerald-500/40 bg-emerald-50/50 dark:bg-emerald-950/20 p-5 space-y-3">
              <p className="text-xs font-semibold text-emerald-700 dark:text-emerald-400 uppercase tracking-wide">
                {isAr ? "✅ التشخيص جاهز" : "✅ Diagnostic ready"}
              </p>
              <p className="font-semibold text-base">
                {isAr
                  ? `التوصية: ${diagResult.bundle_name_ar || diagResult.recommended_bundle}`
                  : `Recommendation: ${diagResult.bundle_name_en || diagResult.recommended_bundle}`}
              </p>
              {diagResult.services_in_bundle && diagResult.services_in_bundle.length > 0 && (
                <ul className="space-y-1">
                  {diagResult.services_in_bundle.map((s) => (
                    <li key={s} className="flex items-start gap-2 text-sm text-foreground/80">
                      <span className="text-emerald-500 mt-0.5 flex-shrink-0">✓</span>
                      <span>{s}</span>
                    </li>
                  ))}
                </ul>
              )}
              <Button asChild size="lg" className="font-semibold w-full sm:w-auto mt-2">
                <Link href={ctaHref}>
                  {isAr ? "ابدأ Sprint 499 SAR ←" : "Start Sprint 499 SAR →"}
                </Link>
              </Button>
              <p className="text-xs text-muted-foreground">
                {isAr
                  ? "القيمة التقديرية ليست قيمة مُتحقَّقة — كل الأرقام تقديرية حتى يُوثَّق الدليل الفعلي."
                  : "Estimated value is not Verified value — all figures are estimates until actual evidence is documented."}
              </p>
            </div>
          )}

          {!diagResult && (
            <div className="flex flex-wrap gap-3 pt-1">
              <Button asChild variant="ghost" size="sm" className="text-muted-foreground">
                <Link href={ctaHref}>
                  {isAr ? "أو ابدأ Sprint 499 SAR مباشرةً ←" : "Or start Sprint 499 SAR directly →"}
                </Link>
              </Button>
            </div>
          )}
        </div>
      </Card>

      {/* Social Proof */}
      <section>
        <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-3">
          {isAr ? "نتائج من شركات سعودية" : "Results from Saudi Companies"}
        </h2>
        <div className="grid gap-3 sm:grid-cols-3">
          {SOCIAL_PROOF_AR.map((proof, i) => (
            <div
              key={i}
              className="p-4 rounded-xl border border-border/50 bg-muted/20"
            >
              <Badge variant="secondary" className="text-xs mb-2">
                {isAr ? proof.sector : proof.sector}
              </Badge>
              <p className="text-sm font-medium">{proof.result}</p>
              <p className="text-xs text-muted-foreground mt-1">{proof.city}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Deliverables Card */}
      <Card className="p-6 border-primary/30 bg-card/50">
        <h2 className="font-semibold text-lg">
          {isAr ? "ما تحصل عليه في ٧ أيام" : "What You Get in 7 Days"}
        </h2>
        <div className="mt-4 grid gap-2 sm:grid-cols-2">
          {(isAr
            ? [
                "خريطة مسارات الإيراد المُتسرِّب",
                "تقييم جودة CRM والمصادر",
                "خريطة حدود الموافقة",
                "Company Brain v1 — لقطة كاملة للشركة",
                "فجوات مسار الأدلة",
                "أعلى ٣ قرارات محكومة بدليل",
                "Proof Pack PDF ثنائي اللغة",
                "توصية Sprint / Retainer",
              ]
            : [
                "Revenue leakage workflow map",
                "CRM & source quality assessment",
                "Approval boundary map",
                "Company Brain v1 — full company snapshot",
                "Evidence trail gaps",
                "Top 3 governed decisions with proof",
                "Bilingual Proof Pack PDF",
                "Sprint / Retainer recommendation",
              ]
          ).map((item) => (
            <div key={item} className="flex items-start gap-2 text-sm">
              <span className="text-emerald-500 mt-0.5 flex-shrink-0">✓</span>
              <span>{item}</span>
            </div>
          ))}
        </div>
      </Card>

      {/* ZATCA Urgency Banner */}
      <div className="rounded-xl border border-amber-500/30 bg-amber-50/50 dark:bg-amber-950/20 p-4">
        <div className="flex items-start gap-3">
          <span className="text-2xl">⚡</span>
          <div>
            <p className="font-semibold text-amber-800 dark:text-amber-300">
              {isAr
                ? "ZATCA Wave 24 — الموعد النهائي ٣٠ يونيو ٢٠٢٦"
                : "ZATCA Wave 24 — Deadline June 30, 2026"}
            </p>
            <p className="text-sm text-amber-700 dark:text-amber-400 mt-1">
              {isAr
                ? "كل شركة تتجاوز ٣٧٥,٠٠٠ ر.س إيراداً ملزمة بالفوترة الإلكترونية. Dealix يجهّزك للامتثال ويحسّن إيراداتك في نفس الوقت."
                : "Every company over 375K SAR revenue must comply with e-invoicing. Dealix gets you compliant while improving your revenue ops."}
            </p>
          </div>
        </div>
      </div>

      <p className="text-xs text-muted-foreground max-w-2xl">
        {isAr
          ? "لا إرسال خارجي آلي · لا ادّعاء إيراد قبل الدفع · كل البيانات تمر من audit log · PDPL compliant"
          : "No automated outbound · No revenue before payment · All data through audit log · PDPL compliant"}
      </p>
    </div>
  );
}
