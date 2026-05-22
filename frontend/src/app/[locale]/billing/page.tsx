import type { Metadata } from "next";
import Link from "next/link";
import { CheckoutPanel } from "./CheckoutPanel";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "الفوترة والاشتراك — Dealix" : "Billing & Checkout — Dealix",
    description: isAr
      ? "ادفع عبر Moyasar بالريال السعودي. روابط دفع آمنة، فواتير ZATCA-متوافقة، استرداد خلال 7 أيام للتشخيص."
      : "Pay in SAR via Moyasar. Secure checkout links, ZATCA-compliant invoices, 7-day diagnostic refund window.",
  };
}

export default async function BillingPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const base = `/${locale}`;

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>
      <header className="border-b border-border/60">
        <div className="mx-auto max-w-4xl px-6 py-4 flex flex-wrap gap-4 text-sm">
          <Link href={base} className="text-muted-foreground hover:text-foreground">
            {isAr ? "← الرئيسية" : "← Home"}
          </Link>
          <Link href={`${base}/legal/terms`} className="text-muted-foreground hover:text-foreground">
            {isAr ? "الشروط" : "Terms"}
          </Link>
          <Link href={`${base}/legal/privacy`} className="text-muted-foreground hover:text-foreground">
            {isAr ? "الخصوصية" : "Privacy"}
          </Link>
        </div>
      </header>

      <main className={`mx-auto max-w-4xl px-6 py-12 ${isAr ? "text-right" : "text-left"}`}>
        <h1 className="text-3xl font-bold">
          {isAr ? "الفوترة والاشتراك" : "Billing & Checkout"}
        </h1>
        <p className="mt-3 text-muted-foreground leading-relaxed">
          {isAr
            ? "ادفع مرة واحدة عبر Moyasar للحصول على رابط دفع آمن. فاتورة ZATCA متوافقة تصل لبريدك خلال دقائق من نجاح الدفع."
            : "Pay once via Moyasar to receive a secure checkout link. A ZATCA-compliant invoice arrives in your inbox minutes after a successful payment."}
        </p>

        <CheckoutPanel locale={locale} />

        <section className="mt-12 rounded-lg border border-border/60 bg-card/30 p-5 text-sm leading-relaxed">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
            {isAr ? "ما الذي تتوقعه" : "What to expect"}
          </h2>
          <ul className={`mt-3 space-y-2 ${isAr ? "pr-5" : "pl-5"} list-disc text-muted-foreground`}>
            <li>
              {isAr
                ? "تستلم رابط Moyasar الآمن مباشرة في المتصفح + نسخة على بريدك."
                : "You receive a secure Moyasar link in-browser and a copy by email."}
            </li>
            <li>
              {isAr
                ? "نصدر فاتورة متوافقة مع نظام الفوترة الإلكترونية السعودي (ZATCA Phase 2)."
                : "We issue an invoice compliant with Saudi e-invoicing (ZATCA Phase 2)."}
            </li>
            <li>
              {isAr
                ? "Diagnostic (499 ر.س): استرداد خلال 7 أيام إذا لم تُسلَّم العينة."
                : "Diagnostic (499 SAR): 7-day refund if no sample is delivered."}
            </li>
            <li>
              {isAr
                ? "Managed Ops (شهرياً): إلغاء بإشعار 30 يوم قبل التجديد، لا استرداد للأشهر المنقضية."
                : "Managed Ops (monthly): cancel with 30 days notice, no refund on elapsed months."}
            </li>
          </ul>
        </section>
      </main>
    </div>
  );
}
