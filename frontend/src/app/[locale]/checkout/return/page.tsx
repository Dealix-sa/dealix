import type { Metadata } from "next";
import Link from "next/link";
import { PublicLaunchShell } from "@/components/brand/PublicLaunchShell";

type Props = {
  params: Promise<{ locale: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "Dealix — حالة الدفع" : "Dealix — Payment Status",
    robots: { index: false, follow: false },
  };
}

function first(v: string | string[] | undefined): string {
  return Array.isArray(v) ? (v[0] ?? "") : (v ?? "");
}

export default async function CheckoutReturnPage({ params, searchParams }: Props) {
  const { locale } = await params;
  const sp = await searchParams;
  const isAr = locale === "ar";
  const base = `/${locale}`;

  const status = first(sp.status).toLowerCase();
  const invoiceId = first(sp.id) || first(sp.invoice_id);
  const paid = status === "paid";
  const failed = status === "failed";

  const heading = paid
    ? isAr
      ? "تم الدفع بنجاح ✅"
      : "Payment successful ✅"
    : failed
      ? isAr
        ? "لم تكتمل عملية الدفع"
        : "Payment did not complete"
      : isAr
        ? "نُعالج حالة الدفع"
        : "Processing your payment";

  const body = paid
    ? isAr
      ? "استلمنا دفعتك. سيتواصل معك فريق Dealix خلال ٢٤ ساعة لبدء التنفيذ، وتصلك فاتورة ZATCA على بريدك."
      : "We received your payment. The Dealix team will contact you within 24 hours to begin, and a ZATCA invoice will be emailed to you."
    : failed
      ? isAr
        ? "يبدو أن العملية لم تكتمل. تقدر تعيد المحاولة من صفحة الأسعار أو تتواصل معنا وبنساعدك."
        : "It looks like the transaction didn't complete. You can retry from the pricing page or contact us and we'll help."
      : isAr
        ? "إذا تم الخصم، ستصلك رسالة تأكيد قريباً. إن لم تصلك خلال دقائق، تواصل معنا بالمرجع أدناه."
        : "If you were charged, you'll receive a confirmation shortly. If not within a few minutes, contact us with the reference below.";

  return (
    <PublicLaunchShell compactNav>
      <main className="mx-auto max-w-xl px-6 py-20 text-center" dir={isAr ? "rtl" : "ltr"}>
        <div className="text-5xl mb-4">{paid ? "✅" : failed ? "⚠️" : "⏳"}</div>
        <h1 className="text-3xl font-bold">{heading}</h1>
        <p className="mt-4 text-muted-foreground leading-relaxed">{body}</p>
        {invoiceId && (
          <p className="mt-3 text-xs text-muted-foreground">
            {isAr ? "رقم المرجع:" : "Reference:"} <span className="font-mono">{invoiceId}</span>
          </p>
        )}
        <div className="mt-8 flex flex-wrap justify-center gap-3">
          {paid ? (
            <Link
              href={base}
              className="inline-flex items-center rounded-lg bg-primary text-primary-foreground px-5 py-2.5 text-sm font-medium hover:bg-primary/90 transition-colors"
            >
              {isAr ? "العودة للرئيسية" : "Back to home"}
            </Link>
          ) : (
            <Link
              href={`${base}/pricing`}
              className="inline-flex items-center rounded-lg bg-primary text-primary-foreground px-5 py-2.5 text-sm font-medium hover:bg-primary/90 transition-colors"
            >
              {isAr ? "العودة للأسعار" : "Back to pricing"}
            </Link>
          )}
          <Link
            href={`${base}/contact`}
            className="inline-flex items-center rounded-lg border border-border bg-card px-5 py-2.5 text-sm font-medium hover:bg-muted/30 transition-colors"
          >
            {isAr ? "تواصل معنا" : "Contact us"}
          </Link>
        </div>
      </main>
    </PublicLaunchShell>
  );
}
