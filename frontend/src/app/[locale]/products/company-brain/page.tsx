import type { Metadata } from "next";
import { ProductPageLayout } from "@/components/products/ProductPageLayout";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "عقل الشركة — Dealix" : "Company Brain OS — Dealix",
    description: isAr
      ? "ذاكرة مؤسسة موحدة: القرار اليومي، رادار المستقبل، مذكرة المجلس، وخطة ٣٠ يوماً."
      : "Unified company memory: daily decision, future radar, board memo, and 30-day plan.",
    alternates: { canonical: `https://dealix.me/${locale}/products/company-brain` },
  };
}

export default function CompanyBrainProductPage() {
  return (
    <ProductPageLayout
      nameAr="عقل الشركة"
      nameEn="Company Brain OS"
      taglineAr="ذاكرة مؤسسة حية — القرار، السياق، المستقبل، والخطة في مكان واحد."
      taglineEn="A living company memory — decision, context, future, and plan in one place."
      problemAr="القرارات تتكرر لأن السياق يُفقد. الاجتماعات تنتهي بدون مذكرة. المؤسس يعيد اكتشاف نفس المعلومات كل أسبوع."
      problemEn="Decisions repeat because context is lost. Meetings end without a memo. The founder rediscovers the same information every week."
      whatItDoesAr={[
        "تسجيل القرار اليومي مع السياق والمصدر",
        "رادار المستقبل: مخاطر وفرص قادمة خلال ٣٠–٩٠ يوماً",
        "مذكرة مجلس تنفيذية أسبوعية تلقائية",
        "خطة ٣٠ يوماً قابلة للتتبع مع الحالة",
      ]}
      whatItDoesEn={[
        "Record the daily decision with context and source",
        "Future radar: risks and opportunities in 30–90 days",
        "Automatic weekly executive board memo",
        "Trackable 30-day plan with status",
      ]}
      deliverables={[
        {
          days: "7",
          titleAr: "الأسبوع الأول — الذاكرة",
          titleEn: "Week 1 — Memory",
          itemsAr: [
            "تسجيل القرارات اليومية يبدأ",
            "ربط Company Brain بمصادر البيانات",
            "لوحة القرار الأخير حية",
          ],
          itemsEn: [
            "Daily decision logging starts",
            "Company Brain connected to data sources",
            "Latest decision board live",
          ],
        },
        {
          days: "14",
          titleAr: "الأسبوع الثاني — الرادار",
          titleEn: "Week 2 — Radar",
          itemsAr: [
            "رادار المستقبل مفعّل",
            "مذكرة مجلس أسبوعية أولى",
            "خطة ٣٠ يوماً مسودة قابلة للمراجعة",
          ],
          itemsEn: [
            "Future radar active",
            "First weekly board memo",
            "Draft 30-day plan ready for review",
          ],
        },
        {
          days: "30",
          titleAr: "اليوم ٣٠ — التشغيل",
          titleEn: "Day 30 — Ops",
          itemsAr: [
            "تقارير Company Brain أرشيفية قابلة للبحث",
            "تنبيهات الرادار مفعّلة",
            "تكامل مع Revenue Command Room",
          ],
          itemsEn: [
            "Searchable Company Brain report archive",
            "Radar alerts active",
            "Integration with Revenue Command Room",
          ],
        },
      ]}
      pricingHintAr="ضمن خطة Managed Ops — يُفعّل بعد التشخيص."
      pricingHintEn="Within the Managed Ops plan — activated after diagnostic."
    />
  );
}