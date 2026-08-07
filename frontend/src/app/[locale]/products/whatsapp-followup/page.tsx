import type { Metadata } from "next";
import { ProductPageLayout } from "@/components/products/ProductPageLayout";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "متابعة واتساب — Dealix" : "WhatsApp/Inbox Follow-up OS — Dealix",
    description: isAr
      ? "متابعة محادثة موحدة على واتساب وإيميل — مسودات، مراجعة بشرية، موافقة قبل الإرسال."
      : "Unified conversation follow-up on WhatsApp and email — drafts, human review, approval before send.",
    alternates: { canonical: `https://dealix.me/${locale}/products/whatsapp-followup` },
  };
}

export default function WhatsappFollowupPage() {
  return (
    <ProductPageLayout
      nameAr="متابعة واتساب والوارد"
      nameEn="WhatsApp/Inbox Follow-up OS"
      taglineAr="متابعة المحادثات دون ضياع فرصة — مسودة، مراجعة، موافقة، ثم إرسال."
      taglineEn="Follow conversations without losing a lead — draft, review, approve, then send."
      problemAr="الفرص تضيع في صندوق الوارد. الردود تتأخر أو تُنسى. لا يوجد متابعة منهجية بعد أول تواصل."
      problemEn="Leads are lost in the inbox. Replies are late or forgotten. No systematic follow-up after first contact."
      whatItDoesAr={[
        "توحيد محادثات واتساب وإيميل في قائمة متابعة واحدة",
        "توليد مسودة رد ذكية بناءً على سياق المحادثة",
        "مراجعة بشرية إلزامية قبل أي إرسال خارجي",
        "تتبع حالة كل محادثة وآخر متابعة",
      ]}
      whatItDoesEn={[
        "Unify WhatsApp and email conversations into one follow-up list",
        "Generate a smart reply draft based on conversation context",
        "Mandatory human review before any external send",
        "Track each conversation's status and last follow-up",
      ]}
      deliverables={[
        {
          days: "7",
          titleAr: "الأسبوع الأول — التركيب",
          titleEn: "Week 1 — Setup",
          itemsAr: [
            "ربط صندوق الوارد وواتساب (مع opt-in)",
            "قائمة متابعة موحدة حية",
            "مسودة رد أولية للمراجعة",
          ],
          itemsEn: [
            "Connect inbox and WhatsApp (with opt-in)",
            "Unified follow-up list live",
            "Initial reply draft for review",
          ],
        },
        {
          days: "14",
          titleAr: "الأسبوع الثاني — المراجعة",
          titleEn: "Week 2 — Review",
          itemsAr: [
            "بوابات أمان واتساب مفعّلة (opt-in, template, 24h)",
            "طابور مراجعة بشرية مع حالة كل مسودة",
            "تنبيهات للمتابعة المتأخرة",
          ],
          itemsEn: [
            "WhatsApp safety gates active (opt-in, template, 24h)",
            "Human review queue with per-draft status",
            "Overdue follow-up alerts",
          ],
        },
        {
          days: "30",
          titleAr: "اليوم ٣٠ — التشغيل",
          titleEn: "Day 30 — Ops",
          itemsAr: [
            "معدل متابعة محسوب بالأدلة",
            "تكامل مع pipeline والعملاء",
            "تقرير شهري للمتابعة",
          ],
          itemsEn: [
            "Follow-up rate measured with evidence",
            "Integration with pipeline and clients",
            "Monthly follow-up report",
          ],
        },
      ]}
      pricingHintAr="ضمن Managed Ops — لا إرسال خارجي قبل الموافقة وبوابات الأمان."
      pricingHintEn="Within Managed Ops — no external send before approval and safety gates."
      outboundNote
    />
  );
}