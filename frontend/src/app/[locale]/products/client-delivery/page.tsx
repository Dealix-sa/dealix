import type { Metadata } from "next";
import { ProductPageLayout } from "@/components/products/ProductPageLayout";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "تسليم العميل — Dealix" : "Client Delivery OS — Dealix",
    description: isAr
      ? "تتبع مشاريع العميل عبر مراحل: استيعاب، تشخيص، مخطط، بناء، QA، UAT، إطلاق، تدريب، إثبات."
      : "Track client projects across stages: intake, diagnosis, blueprint, build, QA, UAT, launch, training, proof.",
    alternates: { canonical: `https://dealix.me/${locale}/products/client-delivery` },
  };
}

export default function ClientDeliveryProductPage() {
  return (
    <ProductPageLayout
      nameAr="تسليم العميل"
      nameEn="Client Delivery OS"
      taglineAr="كل مشروع عميل من الاستيعاب إلى الإثبات — مراحل واضحة وحالة قابلة للتتبع."
      taglineEn="Every client project from intake to proof — clear stages and trackable status."
      problemAr="مشاريع العميل تضيع بين المراحل. لا أحد يعرف أين المشروع الآن. التسليم يتأخر بدون إنذار مبكر."
      problemEn="Client projects get lost between stages. No one knows where a project stands. Delivery slips without early warning."
      whatItDoesAr={[
        "مراحل موحدة: استيعاب، تشخيص، مخطط، بناء، QA، UAT، إطلاق، تدريب، إثبات",
        "حالة كل مرحلة مع المسؤول والموعد",
        "تنبيهات للتأخير والانسداد",
        "ربط التسليم بـ Proof Pack",
      ]}
      whatItDoesEn={[
        "Unified stages: intake, diagnosis, blueprint, build, QA, UAT, launch, training, proof",
        "Stage status with owner and due date",
        "Delay and bottleneck alerts",
        "Link delivery to Proof Pack",
      ]}
      deliverables={[
        {
          days: "7",
          titleAr: "الأسبوع الأول — التركيب",
          titleEn: "Week 1 — Setup",
          itemsAr: [
            "تعريف المراحل التسع",
            "لوحة مشاريع العميل حية",
            "ربط المشروع بالعميل",
          ],
          itemsEn: [
            "Define the nine stages",
            "Client projects board live",
            "Link project to client",
          ],
        },
        {
          days: "14",
          titleAr: "الأسبوع الثاني — التتبع",
          titleEn: "Week 2 — Tracking",
          itemsAr: [
            "حالة كل مرحلة مع المسؤول",
            "تنبيهات التأخير مفعّلة",
            "ربط بـ Proof Pack",
          ],
          itemsEn: [
            "Stage status with owner",
            "Delay alerts active",
            "Link to Proof Pack",
          ],
        },
        {
          days: "30",
          titleAr: "اليوم ٣٠ — التشغيل",
          titleEn: "Day 30 — Ops",
          itemsAr: [
            "تقرير تسليم شهري بالأدلة",
            "أرشيف مشاريع قابل للبحث",
            "تكامل مع Company Brain",
          ],
          itemsEn: [
            "Monthly delivery report with evidence",
            "Searchable project archive",
            "Integration with Company Brain",
          ],
        },
      ]}
      pricingHintAr="ضمن Managed Ops — تتبع كامل لمشاريع العميل."
      pricingHintEn="Within Managed Ops — full client project tracking."
    />
  );
}