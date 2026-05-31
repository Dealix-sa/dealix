// from __future__ import annotations
"use client";

import { useLocale } from "next-intl";
import { Check, X, Minus } from "lucide-react";
import { Card } from "@/components/ui/card";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type CellValue = "yes" | "no" | "partial" | string;

interface ComparisonRow {
  id: string;
  label: { ar: string; en: string };
  dealix: CellValue;
  intlCrm: CellValue;
  localConsulting: CellValue;
}

// ---------------------------------------------------------------------------
// Data
// ---------------------------------------------------------------------------

const ROWS: ComparisonRow[] = [
  {
    id: "price",
    label: { ar: "سعر الدخول", en: "Entry Price" },
    dealix: "499 SAR",
    intlCrm: "3,000+ SAR/mo",
    localConsulting: "15,000+ SAR project",
  },
  {
    id: "rtl",
    label: { ar: "دعم RTL عربي أصيل", en: "Arabic RTL Native" },
    dealix: "yes",
    intlCrm: "partial",
    localConsulting: "partial",
  },
  {
    id: "zatca",
    label: { ar: "ZATCA Phase 2 مدمج", en: "ZATCA Phase 2 Built-in" },
    dealix: "yes",
    intlCrm: "no",
    localConsulting: "no",
  },
  {
    id: "pdpl",
    label: { ar: "بنية PDPL أصيلة", en: "PDPL Native Architecture" },
    dealix: "yes",
    intlCrm: "partial",
    localConsulting: "no",
  },
  {
    id: "delivery",
    label: { ar: "تسليم الدليل في 7 أيام", en: "7-Day Proof Delivery" },
    dealix: "yes",
    intlCrm: "no",
    localConsulting: "no",
  },
  {
    id: "governed_ai",
    label: { ar: "AI محكوم (بدون إرسال مستقل)", en: "Governed AI (No Autonomous Sends)" },
    dealix: "yes",
    intlCrm: "no",
    localConsulting: "no",
  },
  {
    id: "source_passport",
    label: { ar: "Source Passport لحوكمة البيانات", en: "Source Passport Data Governance" },
    dealix: "yes",
    intlCrm: "no",
    localConsulting: "no",
  },
  {
    id: "recurring",
    label: { ar: "تركيز على الإيراد المتكرر", en: "Recurring Revenue Focus" },
    dealix: "yes",
    intlCrm: "partial",
    localConsulting: "no",
  },
  {
    id: "icp",
    label: { ar: "تخصص B2B السعودي", en: "Saudi B2B ICP Specialization" },
    dealix: "yes",
    intlCrm: "no",
    localConsulting: "partial",
  },
  {
    id: "proof_pack",
    label: { ar: "Proof Pack عام", en: "Public Proof Pack" },
    dealix: "yes",
    intlCrm: "no",
    localConsulting: "no",
  },
  {
    id: "lock_in",
    label: { ar: "شهر بشهر (بدون ارتباط)", en: "Month-to-Month (No Lock-in)" },
    dealix: "yes",
    intlCrm: "no",
    localConsulting: "no",
  },
  {
    id: "onboarding",
    label: { ar: "وقت الإعداد", en: "Onboarding Time" },
    dealix: "1 Day",
    intlCrm: "2-6 Weeks",
    localConsulting: "4-8 Weeks",
  },
];

// ---------------------------------------------------------------------------
// Cell renderer
// ---------------------------------------------------------------------------

function CellContent({ value }: { value: CellValue }) {
  if (value === "yes") {
    return (
      <span className="inline-flex items-center justify-center">
        <Check className="w-4 h-4 text-[var(--dealix-success)]" aria-label="Yes" />
      </span>
    );
  }
  if (value === "no") {
    return (
      <span className="inline-flex items-center justify-center">
        <X className="w-4 h-4 text-[var(--dealix-error)]" aria-label="No" />
      </span>
    );
  }
  if (value === "partial") {
    return (
      <span className="inline-flex items-center justify-center">
        <Minus className="w-4 h-4 text-[var(--dealix-warning)]" aria-label="Partial" />
      </span>
    );
  }
  return <span className="text-sm font-medium">{value}</span>;
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

interface ComparisonTableProps {
  className?: string;
}

export function ComparisonTable({ className = "" }: ComparisonTableProps) {
  const locale = useLocale();
  const isAr = locale === "ar";

  const t = {
    title: isAr ? "مقارنة Dealix مع البدائل" : "Dealix vs Alternatives",
    subtitle: isAr
      ? "مقارنة مبنية على معايير موضوعية — تحقق من أي معيار يهمك"
      : "Comparison built on objective criteria — verify any criterion that matters to you",
    dealix: "Dealix",
    intlCrm: isAr ? "CRM دولي (Salesforce/HubSpot)" : "International CRM (Salesforce/HubSpot)",
    localConsulting: isAr ? "استشارات محلية" : "Local Consulting",
    criterion: isAr ? "المعيار" : "Criterion",
    legend: {
      yes: isAr ? "متوفر" : "Available",
      partial: isAr ? "جزئي / يتطلب إعداداً" : "Partial / Requires config",
      no: isAr ? "غير متوفر" : "Not available",
    },
  };

  return (
    <section
      className={`space-y-6 ${className}`}
      dir={isAr ? "rtl" : "ltr"}
    >
      {/* Header */}
      <div className={isAr ? "text-right" : "text-left"}>
        <h2 className="text-2xl font-bold text-[var(--dealix-navy)]">{t.title}</h2>
        <p className="mt-1 text-sm text-muted-foreground">{t.subtitle}</p>
      </div>

      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-muted/30">
                <th className="py-4 px-4 font-medium text-muted-foreground text-start w-[40%]">
                  {t.criterion}
                </th>
                {/* Dealix column — highlighted */}
                <th className="py-4 px-4 font-semibold text-center bg-[var(--dealix-gold)]/15 text-[var(--dealix-navy)] border-x border-[var(--dealix-gold)]/30 w-[20%]">
                  {t.dealix}
                </th>
                <th className="py-4 px-4 font-medium text-center text-muted-foreground w-[20%]">
                  {t.intlCrm}
                </th>
                <th className="py-4 px-4 font-medium text-center text-muted-foreground w-[20%]">
                  {t.localConsulting}
                </th>
              </tr>
            </thead>
            <tbody>
              {ROWS.map((row, idx) => (
                <tr
                  key={row.id}
                  className={idx % 2 === 0 ? "bg-background" : "bg-muted/10"}
                >
                  <td className="py-3 px-4 text-start border-b border-border/30">
                    <span className="font-medium">{isAr ? row.label.ar : row.label.en}</span>
                  </td>
                  {/* Dealix — highlighted column */}
                  <td className="py-3 px-4 text-center border-b border-border/30 bg-[var(--dealix-gold)]/10 border-x border-[var(--dealix-gold)]/30">
                    <CellContent value={row.dealix} />
                  </td>
                  <td className="py-3 px-4 text-center border-b border-border/30">
                    <CellContent value={row.intlCrm} />
                  </td>
                  <td className="py-3 px-4 text-center border-b border-border/30">
                    <CellContent value={row.localConsulting} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Legend */}
      <div className="flex flex-wrap gap-4 text-xs text-muted-foreground">
        <span className="flex items-center gap-1.5">
          <Check className="w-3.5 h-3.5 text-[var(--dealix-success)]" />
          {t.legend.yes}
        </span>
        <span className="flex items-center gap-1.5">
          <Minus className="w-3.5 h-3.5 text-[var(--dealix-warning)]" />
          {t.legend.partial}
        </span>
        <span className="flex items-center gap-1.5">
          <X className="w-3.5 h-3.5 text-[var(--dealix-error)]" />
          {t.legend.no}
        </span>
      </div>
    </section>
  );
}
