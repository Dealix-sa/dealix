import type { Metadata } from "next";
import { ProductPageLayout } from "@/components/products/ProductPageLayout";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "الاتصال الخارجي المُوجَّه — Dealix" : "Controlled Live Outbound OS — Dealix",
    description: isAr
      ? "اتصال خارجي حي تحت السيطرة — مسودة، مراجعة، موافقة، بوابات أمان، ثم إرسال محدود."
      : "Controlled live outbound — draft, review, approval, safety gates, then bounded send.",
    alternates: { canonical: `https://dealix.me/${locale}/products/controlled-outbound` },
  };
}

export default function ControlledOutboundPage() {
  return (
    <ProductPageLayout
      nameAr="الاتصال الخارجي المُوجَّه"
      nameEn="Controlled Live Outbound OS"
      taglineAr="اتصال خارجي حي — تحت سيطرة كاملة، ببوابات أمان، وبموافقة بشرية أولاً."
      taglineEn="Live outbound — fully controlled, with safety gates and human approval first."
      problemAr="الاتصال الخارجي غير المنضبط يعرّض الشركة للحظر، الغرامات، وتدمير السمعة. لا أحد يضبط الحجم أو المصدر أو الموافقة."
      problemEn="Uncontrolled outbound exposes the company to bans, fines, and reputation destruction. No one governs volume, source, or consent."
      whatItDoesAr={[
        "كل رسالة خارجية تمر بمراجعة بشرية وموافقة صريحة",
        "بوابات أمان لكل قناة (إيميل/واتساب/SMS) معروضة",
        "حدود حجم يومية قابلة للتكوين فقط من قبل المؤسس",
        "OUTBOUND_MODE=draft_only افتراضياً — لا إرسال حي دون تفعيل واعٍ"
      ]}
      whatItDoesEn={[
        "Every outbound message goes through human review and explicit approval",
        "Per-channel safety gates (email/WhatsApp/SMS) displayed",
        "Daily volume limits configurable only by the founder",
        "OUTBOUND_MODE=draft_only by default — no live send without conscious enablement"
      ]}
      deliverables={[
        {
          days: "7",
          titleAr: "الأسبوع الأول — المسودات",
          titleEn: "Week 1 — Drafts",
          itemsAr: [
            "توليد المسودات لكل قناة يبدأ",
            "طابور المراجعة حي",
            "OUTBOUND_MODE=draft_only مفعّل",
          ],
          itemsEn: [
            "Draft generation per channel starts",
            "Review queue live",
            "OUTBOUND_MODE=draft_only enabled",
          ],
        },
        {
          days: "14",
          titleAr: "الأسبوع الثاني — البوابات",
          titleEn: "Week 2 — Gates",
          itemsAr: [
            "بوابات الأمان لكل قناة معروضة",
            "حالة كل مسودة وموافقتها",
            "تنبيهات للمسودات بدون بوابات كاملة",
          ],
          itemsEn: [
            "Safety gates per channel displayed",
            "Every draft and approval status",
            "Alerts for drafts with incomplete gates",
          ],
        },
        {
          days: "30",
          titleAr: "اليوم ٣٠ — التحكم",
          titleEn: "Day 30 — Control",
          itemsAr: [
            "حدود الحجم اليومية قابلة للتكوين",
            "تقرير شهري لمعدل الموافقة والبوابات",
            "لا زر 'إرسال الآن' — موافقة مسودة فقط",
          ],
          itemsEn: [
            "Daily volume limits configurable",
            "Monthly approval and gate rate report",
            "No 'send now' button — draft approval only",
          ],
        },
      ]}
      pricingHintAr="ضمن Managed Ops — الإرسال الحي يتطلب تفعيل واعٍ وبوابات كاملة."
      pricingHintEn="Within Managed Ops — live send requires conscious enablement and full gates."
      outboundNote
    />
  );
}