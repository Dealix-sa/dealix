import type { Metadata } from "next";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "الشروط والأحكام — Dealix" : "Terms & Conditions — Dealix",
    description: isAr
      ? "شروط استخدام خدمات Dealix — التسعير، الدفع، الاسترداد، حماية البيانات، والقانون الحاكم."
      : "Terms for using Dealix services — pricing, payment, refunds, data protection, and governing law.",
    alternates: { canonical: `https://dealix.me/${locale}/terms` },
  };
}

const CLAUSES: { h: { ar: string; en: string }; b: { ar: string; en: string } }[] = [
  {
    h: { ar: "١. الخدمات", en: "1. Services" },
    b: {
      ar: "تقدّم Dealix خدمات استخبارات إيراد وحوكمة ذكاء اصطناعي للشركات في السعودية — تشخيص، حِزم إثبات (Proof Packs)، تشغيل مُدار، ومشاريع AI مخصصة. الخدمات استشارية وتشغيلية ولا تشكّل استشارة قانونية أو محاسبية.",
      en: "Dealix provides AI revenue-intelligence and governance services for companies in Saudi Arabia — diagnostics, Proof Packs, managed operations, and custom AI projects. Services are advisory and operational and do not constitute legal or accounting advice.",
    },
  },
  {
    h: { ar: "٢. سلم العروض والتسعير", en: "2. Offer ladder & pricing" },
    b: {
      ar: "تُقدَّم الخدمات عبر سلم من خمسة مستويات، يفتح كل مستوى بعد إثبات قيمة المستوى السابق. جميع الأسعار بالريال السعودي وقد تخضع لضريبة القيمة المضافة. الأسعار المعلنة قد تتغيّر، والسعر المطبّق هو المثبت في عرض السعر أو الفاتورة.",
      en: "Services are offered via a five-tier ladder; each tier unlocks after the prior tier proves value. All prices are in Saudi Riyal (SAR) and may be subject to VAT. Published prices may change; the applicable price is the one stated in your quote or invoice.",
    },
  },
  {
    h: { ar: "٣. الدفع", en: "3. Payment" },
    b: {
      ar: "يتم الدفع عبر رابط دفع آمن أو تحويل بنكي حسب الفاتورة. لا يتم تحصيل أي مبلغ دون طلبك. يبدأ التنفيذ بعد تأكيد الدفع أو الاتفاق الكتابي.",
      en: "Payment is made via a secure payment link or bank transfer per the invoice. No amount is charged without your request. Delivery begins after payment confirmation or written agreement.",
    },
  },
  {
    h: { ar: "٤. الاسترداد", en: "4. Refunds" },
    b: {
      ar: "لباقة الـ Sprint (499 ر.س): نافذة استرداد سبعة (7) أيام من تاريخ التسليم إذا لم تُسلَّم المخرجات المتفق عليها. الخدمات المخصصة والشهرية تخضع لشروط الاسترداد المذكورة في اتفاقها الخاص.",
      en: "For the Sprint package (499 SAR): a seven (7) day refund window from delivery if the agreed deliverables were not provided. Custom and monthly services follow the refund terms in their specific agreement.",
    },
  },
  {
    h: { ar: "٥. لا ضمان للنتائج", en: "5. No guaranteed outcomes" },
    b: {
      ar: "نلتزم بتسليم المخرجات والمنهجية المتفق عليها بجودة مهنية، لكننا لا نضمن نتائج مبيعات أو إيراد محدّدة. أي رقم تقديري ليس قيمة مُتحقَّقة ما لم يُوثَّق بمصدر ويُؤكَّد منك.",
      en: "We commit to delivering the agreed deliverables and methodology to a professional standard, but we do not guarantee specific sales or revenue outcomes. Any estimated figure is not a verified value unless sourced and confirmed by you.",
    },
  },
  {
    h: { ar: "٦. الموافقة أولاً", en: "6. Approval-first" },
    b: {
      ar: "لا تُنفَّذ أي إجراءات خارجية (رسائل، عروض، التزامات) نيابةً عنك دون موافقتك الصريحة المسبقة. لا نقوم بأي تسويق بارد آلي ولا scraping.",
      en: "No external actions (messages, offers, commitments) are executed on your behalf without your explicit prior approval. We do not perform automated cold outreach or scraping.",
    },
  },
  {
    h: { ar: "٧. البيانات وحماية الخصوصية (PDPL)", en: "7. Data & privacy (PDPL)" },
    b: {
      ar: "نعالج البيانات وفق نظام حماية البيانات الشخصية (PDPL) وسياسة الخصوصية لدينا. تبقى بياناتك ملكك، ويمكنك طلب الوصول أو الحذف عبر مسؤول حماية البيانات: dpo@dealix.me.",
      en: "We process data under the Personal Data Protection Law (PDPL) and our Privacy Policy. Your data remains yours; you may request access or deletion via our Data Protection Officer: dpo@dealix.me.",
    },
  },
  {
    h: { ar: "٨. الملكية الفكرية", en: "8. Intellectual property" },
    b: {
      ar: "تملك مخرجات مشروعك وبياناتك. تحتفظ Dealix بمنهجيتها وأدواتها ونماذجها العامة. لا يُنشر اسم أي عميل أو نتائجه دون إذن كتابي.",
      en: "You own your project deliverables and data. Dealix retains its methodology, tools, and generic models. No client name or results are published without written permission.",
    },
  },
  {
    h: { ar: "٩. القانون الحاكم", en: "9. Governing law" },
    b: {
      ar: "تخضع هذه الشروط لأنظمة المملكة العربية السعودية، وتختص بها الجهات القضائية المختصة في المملكة.",
      en: "These terms are governed by the laws of the Kingdom of Saudi Arabia, under the jurisdiction of the competent Saudi authorities.",
    },
  },
  {
    h: { ar: "١٠. التواصل", en: "10. Contact" },
    b: {
      ar: "للاستفسارات: hello@dealix.me · لطلبات البيانات: dpo@dealix.me.",
      en: "Inquiries: hello@dealix.me · Data requests: dpo@dealix.me.",
    },
  },
];

export default async function TermsRoute({ params }: Props) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <PublicGtmShell>
      <div
        className={`mx-auto max-w-3xl px-6 py-12 space-y-8 ${isAr ? "text-right" : "text-left"}`}
        dir={isAr ? "rtl" : "ltr"}
      >
        <header className="space-y-2">
          <h1 className="text-3xl font-bold">{isAr ? "الشروط والأحكام" : "Terms & Conditions"}</h1>
          <p className="text-sm text-muted-foreground">
            {isAr ? "آخر تحديث: يونيو 2026" : "Last updated: June 2026"}
          </p>
        </header>

        <div className="space-y-6">
          {CLAUSES.map((c, i) => (
            <section key={i} className="space-y-2">
              <h2 className="text-lg font-semibold">{isAr ? c.h.ar : c.h.en}</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">{isAr ? c.b.ar : c.b.en}</p>
            </section>
          ))}
        </div>

        <footer className="rounded-xl border border-border/60 bg-muted/20 p-5 text-xs text-muted-foreground leading-relaxed">
          {isAr
            ? "هذا ملخّص بلغة واضحة لشروط الخدمة، ويخضع للمراجعة القانونية النهائية. لا يشكّل استشارة قانونية. عند وجود اتفاق موقّع خاص بالمشروع، تكون بنوده هي المرجع."
            : "This is a plain-language summary of service terms, pending final legal review. It is not legal advice. Where a signed project-specific agreement exists, its terms prevail."}
        </footer>
      </div>
    </PublicGtmShell>
  );
}
