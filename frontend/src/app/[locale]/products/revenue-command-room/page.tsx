import type { Metadata } from "next";
import { ProductPageLayout } from "@/components/products/ProductPageLayout";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "غرفة قيادة الإيراد — Dealix"
      : "Revenue Command Room — Dealix",
    description: isAr
      ? "لوحة قيادة موحدة للإيراد: pipeline، أداء الحملات، المخاطر، والقرارات اليومية في مكان واحد."
      : "Unified revenue command room: pipeline, campaign performance, risks, and daily decisions in one place.",
    alternates: { canonical: `https://dealix.me/${locale}/products/revenue-command-room` },
  };
}

export default function RevenueCommandRoomPage() {
  return (
    <ProductPageLayout
      nameAr="غرفة قيادة الإيراد"
      nameEn="Revenue Command Room OS"
      taglineAr="مصدر واحد للحقيقة لكل قرار إيراد — pipeline، أداء، مخاطر، خطوات تالية."
      taglineEn="One source of truth for every revenue decision — pipeline, performance, risk, next steps."
      problemAr="بيانات الإيراد متناثرة على CRM والإيميل وواتساب وملفات Excel. مؤسس واحد لا يستطيع رؤية الصورة كاملة، فيتخذ قرارات متأخرة أو مكررة."
      problemEn="Revenue data is scattered across CRM, email, WhatsApp, and spreadsheets. A founder can't see the full picture, so decisions are delayed or duplicated."
      whatItDoesAr={[
        "توحيد pipeline والمراحل والقيم في لوحة واحدة حية",
        "ربط أداء الحملات بمصادر الإيراد الفعلية",
        "تنبيهات استباقية للمخاطر والتأخير والانسداد",
        "ملخص يومي للقرار الأهم ومقدمة للFounder Decision Desk",
      ]}
      whatItDoesEn={[
        "Unify pipeline, stages, and values into one live board",
        "Connect campaign performance to actual revenue sources",
        "Proactive alerts for risks, delays, and bottlenecks",
        "Daily summary of the top decision fed to Founder Decision Desk",
      ]}
      deliverables={[
        {
          days: "7",
          titleAr: "الأسبوع الأول — التركيب",
          titleEn: "Week 1 — Setup",
          itemsAr: [
            "ربط مصادر البيانات (CRM، spreadsheet، إيميل)",
            "تعريف مراحل pipeline والقيم",
            "لوحة قيادة أولية حية",
          ],
          itemsEn: [
            "Connect data sources (CRM, spreadsheet, email)",
            "Define pipeline stages and values",
            "Initial live command board",
          ],
        },
        {
          days: "14",
          titleAr: "الأسبوع الثاني — الأداء",
          titleEn: "Week 2 — Performance",
          itemsAr: [
            "تنبيهات المخاطر والتأخير مفعّلة",
            "ربط الحملات بمصادر الإيراد",
            "ملخص يومي للقرار الأهم",
          ],
          itemsEn: [
            "Risk and delay alerts active",
            "Campaigns linked to revenue sources",
            "Daily top-decision summary",
          ],
        },
        {
          days: "30",
          titleAr: "اليوم ٣٠ — التشغيل الكامل",
          titleEn: "Day 30 — Full ops",
          itemsAr: [
            "تقرير شهري للإيراد مع الدلائل",
            "توقعات الإيراد بناءً على البيانات",
            "تكامل مع Company Brain وFounder Decision Desk",
          ],
          itemsEn: [
            "Monthly revenue report with evidence",
            "Revenue forecasts grounded in data",
            "Integration with Company Brain and Founder Decision Desk",
          ],
        },
      ]}
      pricingHintAr="يبدأ ضمن خطة Managed Ops الشهرية — سعر مخصص بعد التشخيص."
      pricingHintEn="Starts within the monthly Managed Ops plan — custom price after diagnostic."
    />
  );
}