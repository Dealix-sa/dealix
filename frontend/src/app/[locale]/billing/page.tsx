import type { Metadata } from "next";
import Link from "next/link";
import { CheckoutPanel } from "@/components/billing/CheckoutPanel";

interface BillingPageProps {
  params: Promise<{ locale: string }>;
}

export async function generateMetadata({
  params,
}: BillingPageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  const title = isAr
    ? "Dealix — الفوترة والاشتراك"
    : "Dealix — Billing & Subscription";
  const description = isAr
    ? "اختر باقة Dealix ادفع بأمان عبر Moyasar. invoice_intent ≠ revenue."
    : "Pick a Dealix plan and pay securely via Moyasar. invoice_intent ≠ revenue.";
  return {
    title,
    description,
    openGraph: {
      title,
      description,
      locale: isAr ? "ar_SA" : "en_US",
      type: "website",
    },
  };
}

export default async function BillingPage({ params }: BillingPageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  if (isAr) {
    return (
      <div className="min-h-screen bg-background grid-pattern">
        <div
          className="mx-auto max-w-4xl px-6 py-16 text-right"
          dir="rtl"
        >
          <p className="text-sm font-medium text-muted-foreground">
            Dealix — AI Operating Partner
          </p>
          <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
            الفوترة الآمنة عبر Moyasar
          </h1>
          <p className="mt-4 text-muted-foreground leading-relaxed">
            كل عملية دفع تتم عبر بوابة Moyasar الرسمية بترخيص ساما. لا
            نخزّن بيانات بطاقتك على خوادم Dealix. الفاتورة لا تُحتسب
            إيراداً إلا بعد تأكيد الدفع ووجود دليل ربط (PDPL aligned).
          </p>

          <div className="mt-6 flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
            <Link
              href={`/${locale}/dealix-diagnostic`}
              className="rounded-lg border border-border bg-card/40 px-3 py-1.5 hover:border-primary/50"
            >
              تشخيص ٧ أيام
            </Link>
            <Link
              href={`/${locale}/risk-score`}
              className="rounded-lg border border-border bg-card/40 px-3 py-1.5 hover:border-primary/50"
            >
              Risk Score
            </Link>
            <Link
              href={`/${locale}/services`}
              className="rounded-lg border border-border bg-card/40 px-3 py-1.5 hover:border-primary/50"
            >
              كل الخدمات
            </Link>
          </div>

          <CheckoutPanel locale={locale} />

          <div className="mt-16 rounded-lg border border-border bg-card/40 p-5 text-sm text-muted-foreground">
            <p className="font-semibold text-foreground">
              ماذا يحدث بعد الدفع؟
            </p>
            <ol className="mt-2 list-decimal space-y-1 pr-5">
              <li>Moyasar يحوّلك لصفحة دفع آمنة (Apple Pay, Mada, Visa…).</li>
              <li>عند نجاح الدفع: webhook موقّع يصلنا ويحدّث الحالة.</li>
              <li>
                نراجع الدليل (PDPL Art. 8) ونؤكد الدفع، ثم تبدأ مرحلة
                التسليم خلال 24 ساعة.
              </li>
              <li>
                إن تأخر تأكيد الدفع لأي سبب: نتواصل معك مباشرة، لا خصم
                صامت.
              </li>
            </ol>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background grid-pattern">
      <div className="mx-auto max-w-4xl px-6 py-16 text-left" dir="ltr">
        <p className="text-sm font-medium text-muted-foreground">
          Dealix — AI Operating Partner
        </p>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
          Secure billing via Moyasar
        </h1>
        <p className="mt-4 text-muted-foreground leading-relaxed">
          Every charge runs through Moyasar — Saudi Central Bank
          licensed. We never store your card on Dealix servers. An
          invoice is not counted as revenue until payment is confirmed
          with linked evidence (PDPL aligned).
        </p>

        <div className="mt-6 flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
          <Link
            href={`/${locale}/dealix-diagnostic`}
            className="rounded-lg border border-border bg-card/40 px-3 py-1.5 hover:border-primary/50"
          >
            7-day Diagnostic
          </Link>
          <Link
            href={`/${locale}/risk-score`}
            className="rounded-lg border border-border bg-card/40 px-3 py-1.5 hover:border-primary/50"
          >
            Risk Score
          </Link>
          <Link
            href={`/${locale}/services`}
            className="rounded-lg border border-border bg-card/40 px-3 py-1.5 hover:border-primary/50"
          >
            All services
          </Link>
        </div>

        <CheckoutPanel locale={locale} />

        <div className="mt-16 rounded-lg border border-border bg-card/40 p-5 text-sm text-muted-foreground">
          <p className="font-semibold text-foreground">
            What happens after payment?
          </p>
          <ol className="mt-2 list-decimal space-y-1 pl-5">
            <li>
              Moyasar takes you to a secure checkout page (Apple Pay,
              Mada, Visa, …).
            </li>
            <li>
              On success: a signed webhook updates our records and
              flips the invoice state.
            </li>
            <li>
              We verify the evidence (PDPL Art. 8) and confirm payment,
              then delivery kicks off within 24 hours.
            </li>
            <li>
              If confirmation gets delayed for any reason, we reach out
              directly — no silent charge.
            </li>
          </ol>
        </div>
      </div>
    </div>
  );
}
