import type { Metadata } from "next";
import { ProductPageLayout } from "@/components/products/ProductPageLayout";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "الثقة والامتثال بالذكاء الاصطناعي — Dealix" : "AI Trust & Compliance OS — Dealix",
    description: isAr
      ? "سلامة الادعاءات، PDPL، موافقة بشرية، وحقوق العميل — في نظام واحد قابل للتدقيق."
      : "Claim safety, PDPL, human approval, and client rights — in one auditable system.",
    alternates: { canonical: `https://dealix.me/${locale}/products/ai-trust` },
  };
}

export default function AiTrustPage() {
  return (
    <ProductPageLayout
      nameAr="الثقة والامتثال بالذكاء الاصطناعي"
      nameEn="AI Trust & Compliance OS"
      taglineAr="كل ادعاء موثّق، كل إرسال بموافقة، كل عملية قابلة للتدقيق."
      taglineEn="Every claim cited, every send approved, every operation auditable."
      problemAr="الـ AI بدون ضوابط ينتج ادعاءات كاذبة، يرسل بيانات بدون موافقة، ويعرّض الشركة لمخاطر قانونية وسمعة."
      problemEn="Unguarded AI produces false claims, sends data without consent, and exposes the company to legal and reputational risk."
      whatItDoesAr={[
        "فحص سلامة الادعاءات قبل أي مخرج خارجي",
        "توثيق المصادر لكل ادعاء (L0–L5)",
        "موافقة بشرية إلزامية قبل أي إرسال أو إجراء",
        "سجل تدقيق كامل لكل عملية",
      ]}
      whatItDoesEn={[
        "Claim safety check before any external output",
        "Source citation for every claim (L0–L5)",
        "Mandatory human approval before any send or action",
        "Full audit log for every operation",
      ]}
      deliverables={[
        {
          days: "7",
          titleAr: "الأسبوع الأول — الأساس",
          titleEn: "Week 1 — Foundation",
          itemsAr: [
            "فحص سلامة الادعاءات مفعّل",
            "سجل التدقيق يبدأ التسجيل",
            "بوابات الموافقة الإلزامية مفعّلة",
          ],
          itemsEn: [
            "Claim safety check active",
            "Audit log starts recording",
            "Mandatory approval gates active",
          ],
        },
        {
          days: "14",
          titleAr: "الأسبوع الثاني — PDPL",
          titleEn: "Week 2 — PDPL",
          itemsAr: [
            "فحص PDPL لكل مخرج",
            "توثيق المصادر L0–L5 معروض",
            "تنبيهات للمخالفات المحتملة",
          ],
          itemsEn: [
            "PDPL check for every output",
            "L0–L5 source citation displayed",
            "Alerts for potential violations",
          ],
        },
        {
          days: "30",
          titleAr: "اليوم ٣٠ — التشغيل",
          titleEn: "Day 30 — Ops",
          itemsAr: [
            "تقرير امتثال شهري قابل للتدقيق",
            "تكامل مع كل منتجات التواصل",
            "أرشيف تدقيق قابل للبحث",
          ],
          itemsEn: [
            "Auditable monthly compliance report",
            "Integration with all outreach products",
            "Searchable audit archive",
          ],
        },
      ]}
      pricingHintAr="ضمن Managed Ops — أساسي لكل تشغيل خارجي."
      pricingHintEn="Within Managed Ops — foundational for any external operation."
    />
  );
}