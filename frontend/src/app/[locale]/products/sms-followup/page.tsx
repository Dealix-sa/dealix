import type { Metadata } from "next";
import { ProductPageLayout } from "@/components/products/ProductPageLayout";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "متابعة الرسائل النصية — Dealix" : "SMS Follow-up OS — Dealix",
    description: isAr
      ? "متابعة واشعارات عبر SMS بموافقة صريحة وSTOP/opt-out — مسودة، مراجعة، موافقة."
      : "SMS follow-up and notifications with explicit consent and STOP/opt-out — draft, review, approve.",
    alternates: { canonical: `https://dealix.me/${locale}/products/sms-followup` },
  };
}

export default function SmsFollowupPage() {
  return (
    <ProductPageLayout
      nameAr="متابعة الرسائل النصية"
      nameEn="SMS Notification/Follow-up OS"
      taglineAr="إشعارات ومتابعة عبر SMS — بموافقة، بوقف اختياري، بمراجعة بشرية أولاً."
      taglineEn="SMS notifications and follow-up — with consent, opt-out, and human review first."
      problemAr="الـ SMS بدون موافقة صريحة وآلية STOP ينتهك اللوائح ويضر الثقة. الإرسال العشوائي يهدر المال ويغضب العميل."
      problemEn="SMS without explicit consent and a STOP mechanism violates regulations and hurts trust. Random sends waste money and anger customers."
      whatItDoesAr={[
        "توليد مسودة SMS مخصصة لكل متابعة",
        "فحص الموافقة (consent) وآلية STOP/opt-out قبل الإرسال",
        "طابور مراجعة بشرية — لا إرسال قبل الموافقة",
        "تتبع حالة كل رسالة وموافقتها",
      ]}
      whatItDoesEn={[
        "Generate a tailored SMS draft per follow-up",
        "Verify consent and STOP/opt-out before send",
        "Human review queue — no send before approval",
        "Track each message's status and approval",
      ]}
      deliverables={[
        {
          days: "7",
          titleAr: "الأسبوع الأول — التركيب",
          titleEn: "Week 1 — Setup",
          itemsAr: [
            "توليد مسودات SMS يبدأ",
            "طابور المراجعة حي",
            "فحص الموافقة مفعّل",
          ],
          itemsEn: [
            "SMS draft generation starts",
            "Review queue live",
            "Consent check active",
          ],
        },
        {
          days: "14",
          titleAr: "الأسبوع الثاني — البوابات",
          titleEn: "Week 2 — Gates",
          itemsAr: [
            "آلية STOP/opt-out مفعّلة ومسجّلة",
            "حالة مسودة/مراجعة/موافق/مرفوض",
            "تنبيهات للمسودات بدون موافقة",
          ],
          itemsEn: [
            "STOP/opt-out mechanism active and logged",
            "Draft/review/approved/rejected status",
            "Alerts for drafts without consent",
          ],
        },
        {
          days: "30",
          titleAr: "اليوم ٣٠ — التشغيل",
          titleEn: "Day 30 — Ops",
          itemsAr: [
            "تقرير شهري لمعدل الموافقة والإلغاء",
            "تكامل مع pipeline والعملاء",
            "أرشيف SMS قابل للبحث",
          ],
          itemsEn: [
            "Monthly approval and opt-out rate report",
            "Integration with pipeline and clients",
            "Searchable SMS archive",
          ],
        },
      ]}
      pricingHintAr="ضمن Managed Ops — SMS معطّل افتراضياً حتى استيفاء بوابات الموافقة."
      pricingHintEn="Within Managed Ops — SMS disabled by default until consent gates are met."
      outboundNote
    />
  );
}