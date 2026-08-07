import type { Metadata } from "next";
import { ProductPageLayout } from "@/components/products/ProductPageLayout";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "مراجعة التواصل بالإيميل — Dealix" : "Email Outreach Review OS — Dealix",
    description: isAr
      ? "مراجعة مسودات الإيميل قبل الإرسال — سلامة الادعاءات، توثيق مصادر، موافقة بشرية."
      : "Review email drafts before send — claim safety, source citation, human approval.",
    alternates: { canonical: `https://dealix.me/${locale}/products/email-outreach-review` },
  };
}

export default function EmailOutreachReviewPage() {
  return (
    <ProductPageLayout
      nameAr="مراجعة التواصل بالإيميل"
      nameEn="Email Outreach Review OS"
      taglineAr="كل إيميل خارجي يُراجع أولاً — سلامة، دقة، موافقة، ثم إرسال."
      taglineEn="Every outbound email is reviewed first — safety, accuracy, approval, then send."
      problemAr="الإيميل الجماعي بدون مراجعة يعرّض السمعة للخطر وينتهك قواعد النطاق (SPF/DKIM/DMARC). الادعاءات غير الموثقة تضر الثقة."
      problemEn="Mass email without review damages reputation and violates domain rules (SPF/DKIM/DMARC). Uncited claims hurt trust."
      whatItDoesAr={[
        "توليد مسودة إيميل لكل هدف بسياق مخصص",
        "فحص سلامة الادعاءات والمصادر قبل المراجعة",
        "طابور مراجعة بشرية مع حالة لكل مسودة",
        "بوابات جاهزية النطاق (SPF/DKIM/DMARC) معروضة",
      ]}
      whatItDoesEn={[
        "Generate an email draft per target with tailored context",
        "Check claim safety and sources before review",
        "Human review queue with per-draft status",
        "Domain readiness gates (SPF/DKIM/DMARC) displayed",
      ]}
      deliverables={[
        {
          days: "7",
          titleAr: "الأسبوع الأول — التركيب",
          titleEn: "Week 1 — Setup",
          itemsAr: [
            "توليد مسودات الإيميل يبدأ",
            "طابور المراجعة حي",
            "فحص سلامة الادعاءات مفعّل",
          ],
          itemsEn: [
            "Email draft generation starts",
            "Review queue live",
            "Claim safety check active",
          ],
        },
        {
          days: "14",
          titleAr: "الأسبوع الثاني — البوابات",
          titleEn: "Week 2 — Gates",
          itemsAr: [
            "فحص SPF/DKIM/DMARC معروض لكل نطاق",
            "حالة مسودة/مراجعة/موافق/مرفوض",
            "تنبيهات للمسودات المتأخرة",
          ],
          itemsEn: [
            "SPF/DKIM/DMARC check shown per domain",
            "Draft/review/approved/rejected status",
            "Overdue draft alerts",
          ],
        },
        {
          days: "30",
          titleAr: "اليوم ٣٠ — التشغيل",
          titleEn: "Day 30 — Ops",
          itemsAr: [
            "تقرير شهري لمعدل الموافقة والمراجعة",
            "تكامل مع pipeline",
            "أرشيف المسودات القابل للبحث",
          ],
          itemsEn: [
            "Monthly approval and review rate report",
            "Integration with pipeline",
            "Searchable draft archive",
          ],
        },
      ]}
      pricingHintAr="ضمن Managed Ops — الإرسال معطّل افتراضياً (draft_only)."
      pricingHintEn="Within Managed Ops — sending disabled by default (draft_only)."
      outboundNote
    />
  );
}