import type { Metadata } from "next";
import Link from "next/link";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { PartnerApplyForm } from "@/components/gtm/PartnerApplyForm";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const base = buildFunnelMetadata(locale, "partners");
  return {
    ...base,
    title: locale === "ar" ? "برنامج شركاء Dealix — ٣٠٪ عمولة" : "Dealix Partner Program — 30% Commission",
    description:
      locale === "ar"
        ? "أحِل شركة سعودية B2B إلى Dealix واحصل على ٥٠٠٠ ريال رصيد. الشريك يكسب، العميل يكسب."
        : "Refer a Saudi B2B company to Dealix and earn 5,000 SAR credit. Partner wins, client wins.",
  };
}

export default async function PartnersPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <PublicGtmShell compactNav>
      <div className="mx-auto max-w-4xl px-6 py-16 space-y-16" dir={isAr ? "rtl" : "ltr"}>

        {/* Hero */}
        <div className="text-center space-y-4">
          <div className="inline-block rounded-full bg-primary/10 text-primary text-xs font-semibold px-3 py-1">
            {isAr ? "برنامج الشركاء الرسمي" : "Official Partner Program"}
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight">
            {isAr ? "احصل على ٥٠٠٠ ريال لكل عميل تُحيله" : "Earn 5,000 SAR for every client you refer"}
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            {isAr
              ? "أحِل شركة سعودية B2B تحتاج تشغيل إيراد مدعوم بالذكاء الاصطناعي — وكلانا يكسب."
              : "Refer a Saudi B2B company that needs AI-governed revenue ops — and we both win."}
          </p>
        </div>

        {/* Reward cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="rounded-2xl border border-primary/20 bg-primary/5 p-8 space-y-3">
            <div className="text-3xl font-extrabold text-primary">5,000 SAR</div>
            <p className="font-semibold text-lg">
              {isAr ? "مكافأتك كشريك" : "Your reward (referrer)"}
            </p>
            <p className="text-sm text-muted-foreground">
              {isAr
                ? "رصيد اشتراك يُطبَّق على فاتورتك الشهرية التالية عند دفع العميل أول فاتورة ≥ ٩٩٩ ريال."
                : "Subscription credit applied to your next monthly invoice when the referred client pays their first invoice ≥ 999 SAR."}
            </p>
          </div>
          <div className="rounded-2xl border bg-muted/30 p-8 space-y-3">
            <div className="text-3xl font-extrabold">50%</div>
            <p className="font-semibold text-lg">
              {isAr ? "خصم العميل المُحال" : "Referred client discount"}
            </p>
            <p className="text-sm text-muted-foreground">
              {isAr
                ? "العميل الذي تُحيله يحصل على ٥٠٪ خصم على الشهر الأول في أي خطة Growth أو Scale."
                : "The client you refer gets 50% off their first month on any Growth or Scale plan."}
            </p>
          </div>
        </div>

        {/* How it works */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold">{isAr ? "كيف يعمل البرنامج" : "How it works"}</h2>
          <ol className="space-y-4">
            {(isAr ? [
              ["١", "تطبيق للانضمام", "أكمل النموذج أدناه. نراجعه ونُرسل لك كودك خلال 24 ساعة."],
              ["٢", "أحِل شركة", "شارك كودك مع أي شركة سعودية B2B تحتاج إدارة إيراد مدعومة بالذكاء الاصطناعي."],
              ["٣", "يدفع العميل", "عند دفع العميل أول فاتورة — يُضاف رصيدك تلقائياً."],
              ["٤", "كلانا يكسب", "أنت تحصل ٥٠٠٠ ريال، العميل يحصل ٥٠٪ خصم. لا سقف للإحالات."],
            ] : [
              ["1", "Apply to join", "Complete the form below. We review and send your code within 24 hours."],
              ["2", "Refer a company", "Share your code with any Saudi B2B company that needs AI-governed revenue ops."],
              ["3", "Client pays", "When the referred client pays their first invoice — your credit is added automatically."],
              ["4", "Both win", "You get 5,000 SAR credit, they get 50% off. No cap on referrals."],
            ]).map(([num, title, desc]) => (
              <li key={num} className="flex gap-4">
                <span className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 text-primary font-bold text-sm flex items-center justify-center">
                  {num}
                </span>
                <div>
                  <p className="font-semibold">{title}</p>
                  <p className="text-sm text-muted-foreground">{desc}</p>
                </div>
              </li>
            ))}
          </ol>
        </div>

        {/* Ideal partners */}
        <div className="rounded-xl border p-6 space-y-4">
          <h2 className="text-xl font-bold">{isAr ? "مَن هو الشريك المثالي؟" : "Who is the ideal partner?"}</h2>
          <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm text-muted-foreground">
            {(isAr ? [
              "استشاريو CRM و ERP",
              "محامو شركات ومستشارو M&A",
              "وكالات تسويق رقمي",
              "مستشارو امتثال ZATCA / ضريبة",
              "شركاء تقنية سحابية",
              "رواد أعمال سعوديون نشطون",
            ] : [
              "CRM & ERP consultants",
              "Corporate lawyers & M&A advisors",
              "Digital marketing agencies",
              "ZATCA / tax compliance consultants",
              "Cloud technology partners",
              "Active Saudi entrepreneurs",
            ]).map((item) => (
              <li key={item} className="flex items-center gap-2">
                <span className="text-primary">✓</span> {item}
              </li>
            ))}
          </ul>
        </div>

        {/* Program terms link */}
        <p className="text-xs text-muted-foreground text-center">
          {isAr
            ? "للاطلاع على الشروط الكاملة: "
            : "Full program terms: "}
          <Link
            href="/api/v1/referrals/_program-terms"
            className="underline"
            target="_blank"
            rel="noopener noreferrer"
          >
            {isAr ? "شروط البرنامج" : "Program Terms"}
          </Link>
        </p>

        {/* Apply form */}
        <div id="apply">
          <PartnerApplyForm />
        </div>
      </div>
    </PublicGtmShell>
  );
}
