import type { Metadata } from "next";
import Link from "next/link";
import { PublicLaunchShell } from "@/components/brand/PublicLaunchShell";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "terms");
}

type Section = { h: string; items: string[] };

const SECTIONS_AR: Section[] = [
  {
    h: "1. قبول الشروط",
    items: [
      "باستخدامك لموقع Dealix أو طلب أي خدمة، فإنك توافق على هذه الشروط.",
      "إذا كنت تتعاقد نيابة عن شركة، فأنت تُقرّ بأنك مُخوّل بذلك.",
    ],
  },
  {
    h: "2. الخدمات والأسعار",
    items: [
      "نقدّم سلّم خدمات: التشخيص المجاني، سبرنت إثبات الإيرادات (٤٩٩ ر.س)، حزمة البيانات إلى الإيراد (١٥٠٠ ر.س)، عمليات النمو الشهرية (٢٩٩٩ ر.س/شهر)، غرفة قيادة الإدارة (٧٥٠٠ ر.س/شهر)، والبناء المخصّص (حسب النطاق).",
      "كل الأسعار بالريال السعودي وقابلة للتحديث؛ السعر المعتمد هو المذكور في عرض السعر المرسل إليك.",
      "البناء المخصّص يبدأ بنطاق وتقدير مكتوب — لا التزام مالي قبل موافقتك.",
    ],
  },
  {
    h: "3. التسليم والالتزامات",
    items: [
      "نعمل بلغة الالتزام لا الضمان: نلتزم بمخرجات محدّدة ضمن مدة محدّدة لكل خدمة.",
      "إذا لم يتحقق التزام KPI المذكور في الخدمة، نواصل العمل وفق سياسة كل باقة حتى يتحقق أو نطبّق سياسة الاسترداد.",
      "لا ندّعي أو نضمن مبالغ إيراد محدّدة — كل رقم يُقدَّم له مصدر.",
    ],
  },
  {
    h: "4. الدفع والفوترة",
    items: [
      "يتم الدفع عبر Moyasar (مزوّد دفع سعودي). تصلك فاتورة متوافقة مع ZATCA بعد الدفع.",
      "بعض الخدمات تُدفع على دفعتين (٥٠٪ عند البدء، ٥٠٪ عند التسليم) حسب العرض.",
      "الاشتراكات الشهرية تُجدَّد شهرياً ويمكن إيقافها وفق شروط كل باقة.",
    ],
  },
  {
    h: "5. سياسة الاسترداد",
    items: [
      "سبرنت إثبات الإيرادات: استرداد كامل ١٠٠٪ خلال ١٤ يوماً، بدون أسئلة.",
      "حزمة البيانات إلى الإيراد: استرداد ٧٥٪ إذا لم يتحقق التزام KPI خلال ٢١ يوماً.",
      "الاشتراكات الشهرية: استرداد تناسبي للأشهر غير المستخدمة عند عدم تحقيق الالتزام.",
    ],
  },
  {
    h: "6. الاستخدام المقبول والحوكمة",
    items: [
      "كل إجراء خارجي حسّاس (إرسال بريد/رسالة) يمرّ عبر موافقة بشرية — لا أتمتة بلا مراجعة.",
      "لا نُرسل رسائل باردة (cold) ولا نُنفّذ أتمتة على LinkedIn، ولا نقوم بأي scraping أو شراء قوائم.",
      "يلتزم العميل بأن أي بيانات يزوّدنا بها جُمِعت بشكل مشروع وبموافقة أصحابها.",
    ],
  },
  {
    h: "7. مسؤوليات العميل",
    items: [
      "تزويدنا ببيانات دقيقة وصلاحيات الوصول اللازمة لتنفيذ الخدمة.",
      "مراجعة المسودّات واعتمادها قبل أي إرسال خارجي.",
      "الالتزام بالأنظمة المعمول بها في المملكة العربية السعودية.",
    ],
  },
  {
    h: "8. الملكية الفكرية",
    items: [
      "المخرجات المُسلَّمة (Proof Pack، التقارير، المسودّات) مرخّصة لك لاستخدامك التجاري.",
      "تحتفظ Dealix بمنهجيتها وأدواتها وبرمجياتها الأساسية وأي مكوّنات قابلة لإعادة الاستخدام.",
      "لا يُنشَر أي Case Study باسمك إلا بموافقة موقّعة منك.",
    ],
  },
  {
    h: "9. السرّية وحماية البيانات",
    items: [
      "نعامل بياناتك التجارية بسرّية ولا نشاركها مع طرف ثالث بلا موافقة صريحة.",
      "معالجة البيانات الشخصية تتم وفق نظام حماية البيانات الشخصية (PDPL).",
    ],
  },
  {
    h: "10. حدود المسؤولية",
    items: [
      "نقدّم الخدمة بأفضل جهد مهني؛ لا نتحمّل مسؤولية نتائج تجارية خارجة عن سيطرتنا.",
      "لا تتجاوز مسؤوليتنا الإجمالية قيمة المبلغ المدفوع مقابل الخدمة محل النزاع.",
    ],
  },
  {
    h: "11. المدة والإنهاء",
    items: [
      "يمكن لأي طرف إنهاء الخدمات المتكررة وفق شروط الإشعار في الباقة.",
      "تبقى بنود السرّية والملكية الفكرية سارية بعد الإنهاء.",
    ],
  },
  {
    h: "12. القانون الحاكم والتعديلات",
    items: [
      "تخضع هذه الشروط لأنظمة المملكة العربية السعودية.",
      "قد نُحدّث هذه الشروط؛ ويُعلَن أي تغيير جوهري عبر الموقع. استمرار استخدامك يعني الموافقة.",
    ],
  },
];

const SECTIONS_EN: Section[] = [
  {
    h: "1. Acceptance of Terms",
    items: [
      "By using the Dealix website or requesting any service, you agree to these Terms.",
      "If you contract on behalf of a company, you confirm you are authorized to do so.",
    ],
  },
  {
    h: "2. Services & Pricing",
    items: [
      "We offer a service ladder: Free Diagnostic, Revenue Proof Sprint (499 SAR), Data-to-Revenue Pack (1,500 SAR), Growth Ops Monthly (2,999 SAR/mo), Executive Command Center (7,500 SAR/mo), and Custom Build (scoped).",
      "All prices are in SAR and may be updated; the price that applies is the one in the quote sent to you.",
      "Custom builds start with a written scope and estimate — no financial commitment before your approval.",
    ],
  },
  {
    h: "3. Delivery & Commitments",
    items: [
      "We use commitment language, not guarantees: we commit to defined deliverables within a defined timeframe per service.",
      "If a stated KPI commitment is not met, we continue per each package's policy until met, or apply the refund policy.",
      "We do not claim or guarantee specific revenue amounts — every number is sourced.",
    ],
  },
  {
    h: "4. Payment & Invoicing",
    items: [
      "Payment is via Moyasar (a Saudi payment provider). A ZATCA-compliant invoice follows payment.",
      "Some services are paid in two installments (50% at start, 50% on delivery) depending on the offer.",
      "Monthly subscriptions renew monthly and may be stopped per each package's terms.",
    ],
  },
  {
    h: "5. Refund Policy",
    items: [
      "Revenue Proof Sprint: full 100% refund within 14 days, no questions asked.",
      "Data-to-Revenue Pack: 75% refund if the KPI commitment is unmet within 21 days.",
      "Monthly subscriptions: pro-rata refund of unused months if the commitment is unmet.",
    ],
  },
  {
    h: "6. Acceptable Use & Governance",
    items: [
      "Every sensitive external action (email/message send) passes human approval — no automation without review.",
      "We do not send cold messages, do not automate LinkedIn, and do not scrape or buy lists.",
      "The customer warrants that any data provided was collected lawfully and with the consent of its owners.",
    ],
  },
  {
    h: "7. Customer Responsibilities",
    items: [
      "Provide accurate data and the access needed to deliver the service.",
      "Review and approve drafts before any external send.",
      "Comply with applicable laws in the Kingdom of Saudi Arabia.",
    ],
  },
  {
    h: "8. Intellectual Property",
    items: [
      "Delivered outputs (Proof Pack, reports, drafts) are licensed to you for your commercial use.",
      "Dealix retains its methodology, tools, core software, and any reusable components.",
      "No case study is published under your name without your signed consent.",
    ],
  },
  {
    h: "9. Confidentiality & Data Protection",
    items: [
      "We treat your business data confidentially and never share it with third parties without explicit consent.",
      "Personal data is processed in accordance with the Personal Data Protection Law (PDPL).",
    ],
  },
  {
    h: "10. Limitation of Liability",
    items: [
      "We provide the service with best professional effort; we are not liable for commercial outcomes outside our control.",
      "Our total liability shall not exceed the amount paid for the disputed service.",
    ],
  },
  {
    h: "11. Term & Termination",
    items: [
      "Either party may terminate recurring services per the notice terms in the package.",
      "Confidentiality and intellectual-property clauses survive termination.",
    ],
  },
  {
    h: "12. Governing Law & Changes",
    items: [
      "These Terms are governed by the laws of the Kingdom of Saudi Arabia.",
      "We may update these Terms; any material change is announced on the website. Continued use means acceptance.",
    ],
  },
];

export default async function TermsPage({ params }: Props) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const sections = isAr ? SECTIONS_AR : SECTIONS_EN;

  return (
    <PublicLaunchShell compactNav>
      <main className="mx-auto max-w-3xl px-6 py-16" dir={isAr ? "rtl" : "ltr"}>
        <header className={`mb-10 ${isAr ? "text-right" : ""}`}>
          <span className="inline-block rounded-full bg-amber-100 dark:bg-amber-950/30 text-amber-700 dark:text-amber-300 text-xs font-medium px-3 py-1 mb-4">
            {isAr ? "شروط واضحة وعادلة" : "Clear & fair terms"}
          </span>
          <h1 className="text-4xl font-bold">{isAr ? "شروط الخدمة" : "Terms of Service"}</h1>
          <p className="mt-4 text-muted-foreground leading-relaxed text-lg">
            {isAr
              ? "شروط استخدام خدمات Dealix — التسليم، الدفع، الاسترداد، والحوكمة. مكتوبة للسوق السعودي."
              : "Terms for using Dealix services — delivery, payment, refunds, and governance. Written for the Saudi market."}
          </p>
          <p className="mt-2 text-sm text-muted-foreground">
            {isAr ? "آخر تحديث: يونيو 2026" : "Last updated: June 2026"}
          </p>
        </header>

        <div className={`space-y-8 ${isAr ? "text-right" : ""}`}>
          {sections.map((sec) => (
            <section key={sec.h}>
              <h2 className="text-xl font-bold mb-3">{sec.h}</h2>
              <div className="rounded-xl border border-border/60 bg-card/50 p-5 space-y-2 text-sm">
                {sec.items.map((item) => (
                  <div key={item} className="flex items-start gap-2">
                    <span className="text-primary mt-0.5 flex-shrink-0">•</span>
                    <span className="text-muted-foreground">{item}</span>
                  </div>
                ))}
              </div>
            </section>
          ))}

          <section className="rounded-xl border border-border/60 bg-card/50 p-6">
            <h2 className="text-xl font-bold mb-3">{isAr ? "أسئلة؟" : "Questions?"}</h2>
            <p className="text-sm text-muted-foreground">
              {isAr
                ? "لأي استفسار عن هذه الشروط، تواصل معنا. لمعرفة كيف نتعامل مع بياناتك، راجع سياسة الخصوصية."
                : "For any question about these Terms, contact us. To see how we handle your data, review the Privacy Policy."}
            </p>
            <div className="mt-4 flex flex-wrap gap-3">
              <Link
                href={`${base}/contact`}
                className="inline-flex items-center rounded-lg bg-primary text-primary-foreground px-4 py-2 text-sm font-medium hover:bg-primary/90 transition-colors"
              >
                {isAr ? "تواصل معنا" : "Contact Us"}
              </Link>
              <Link
                href={`${base}/privacy`}
                className="inline-flex items-center rounded-lg border border-border bg-card px-4 py-2 text-sm font-medium hover:bg-muted/30 transition-colors"
              >
                {isAr ? "سياسة الخصوصية" : "Privacy Policy"}
              </Link>
            </div>
          </section>
        </div>
      </main>
    </PublicLaunchShell>
  );
}
