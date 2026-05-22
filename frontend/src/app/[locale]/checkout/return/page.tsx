import type { Metadata } from "next";
import Link from "next/link";

interface ReturnPageProps {
  params: Promise<{ locale: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}

export async function generateMetadata({
  params,
}: ReturnPageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "Dealix — تأكيد الدفع" : "Dealix — Payment confirmation",
    robots: { index: false, follow: false },
  };
}

function firstString(value: string | string[] | undefined): string | null {
  if (!value) return null;
  if (Array.isArray(value)) return value[0] ?? null;
  return value;
}

export default async function CheckoutReturnPage({
  params,
  searchParams,
}: ReturnPageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const query = await searchParams;

  const status = (firstString(query.status) || "").toLowerCase();
  const invoiceId = firstString(query.id) || firstString(query.invoice_id);
  const message = firstString(query.message);

  const isPaid = status === "paid" || status === "approved" || status === "captured";
  const isFailed = status === "failed" || status === "rejected" || status === "voided";

  if (isAr) {
    return (
      <div className="min-h-screen bg-background grid-pattern">
        <div
          className="mx-auto max-w-2xl px-6 py-16 text-right"
          dir="rtl"
        >
          <p className="text-sm font-medium text-muted-foreground">
            Dealix — الفوترة
          </p>

          {isPaid && (
            <>
              <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
                تم استلام الدفع ✓
              </h1>
              <p className="mt-4 text-muted-foreground leading-relaxed">
                Moyasar أكّد العملية وأرسل لنا التأكيد عبر webhook.
                سنراجع الدليل ونؤكد الفاتورة كإيراد محسوب، ثم تبدأ مرحلة
                التسليم خلال 24 ساعة. تتلقى رسالة بالتفاصيل على بريدك.
              </p>
            </>
          )}

          {isFailed && (
            <>
              <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
                لم تكتمل عملية الدفع
              </h1>
              <p className="mt-4 text-muted-foreground leading-relaxed">
                {message
                  ? message
                  : "تعذّر إتمام الدفع. تستطيع المحاولة مرة أخرى أو التواصل معنا."}
              </p>
            </>
          )}

          {!isPaid && !isFailed && (
            <>
              <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
                حالة الدفع قيد المعالجة
              </h1>
              <p className="mt-4 text-muted-foreground leading-relaxed">
                نستلم التأكيد النهائي من Moyasar عبر webhook موقّع. لا داعي
                لإعادة المحاولة الآن — سنراسلك بمجرد تأكيد العملية.
              </p>
            </>
          )}

          {invoiceId && (
            <p className="mt-6 rounded-lg border border-border bg-card/40 p-3 text-xs text-muted-foreground">
              رقم الفاتورة:{" "}
              <code className="text-foreground" dir="ltr">
                {invoiceId}
              </code>
            </p>
          )}

          <div className="mt-10 flex flex-wrap gap-3">
            <Link
              href={`/${locale}/billing`}
              className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow hover:opacity-90"
            >
              العودة للفوترة
            </Link>
            <Link
              href={`/${locale}/services`}
              className="inline-flex items-center justify-center rounded-lg border border-border bg-card/40 px-5 py-2.5 text-sm font-medium text-foreground hover:border-primary/50"
            >
              تصفّح الخدمات
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background grid-pattern">
      <div className="mx-auto max-w-2xl px-6 py-16 text-left" dir="ltr">
        <p className="text-sm font-medium text-muted-foreground">
          Dealix — Billing
        </p>

        {isPaid && (
          <>
            <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
              Payment received ✓
            </h1>
            <p className="mt-4 text-muted-foreground leading-relaxed">
              Moyasar confirmed the charge and pushed the webhook to us.
              We&apos;ll verify the evidence and mark the invoice as
              counted revenue, then delivery kicks off within 24 hours.
              You&apos;ll get an email with the details.
            </p>
          </>
        )}

        {isFailed && (
          <>
            <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
              Payment didn&apos;t go through
            </h1>
            <p className="mt-4 text-muted-foreground leading-relaxed">
              {message
                ? message
                : "We couldn't complete the payment. Feel free to retry or get in touch."}
            </p>
          </>
        )}

        {!isPaid && !isFailed && (
          <>
            <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
              Payment status is processing
            </h1>
            <p className="mt-4 text-muted-foreground leading-relaxed">
              We get the final confirmation from Moyasar via signed
              webhook. No need to retry now — we&apos;ll reach out as
              soon as the charge clears.
            </p>
          </>
        )}

        {invoiceId && (
          <p className="mt-6 rounded-lg border border-border bg-card/40 p-3 text-xs text-muted-foreground">
            Invoice id: <code className="text-foreground">{invoiceId}</code>
          </p>
        )}

        <div className="mt-10 flex flex-wrap gap-3">
          <Link
            href={`/${locale}/billing`}
            className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow hover:opacity-90"
          >
            Back to billing
          </Link>
          <Link
            href={`/${locale}/services`}
            className="inline-flex items-center justify-center rounded-lg border border-border bg-card/40 px-5 py-2.5 text-sm font-medium text-foreground hover:border-primary/50"
          >
            Browse services
          </Link>
        </div>
      </div>
    </div>
  );
}
