import type { Metadata } from "next";
import Link from "next/link";
import { DsarForm } from "./DsarForm";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "طلب حقوق البيانات (DSAR) — Dealix" : "Data Subject Request (DSAR) — Dealix",
    description: isAr
      ? "PDPL مادة 12-15 و GDPR: حقك في الوصول، التصحيح، الحذف، أو نقل بياناتك. نرد خلال 5 أيام عمل."
      : "PDPL Art. 12-15 and GDPR: your right to access, rectify, delete, or port your data. We reply within 5 business days.",
  };
}

export default async function DsarPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const base = `/${locale}`;

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>
      <header className="border-b border-border/60">
        <div className="mx-auto max-w-3xl px-6 py-4 flex flex-wrap gap-4 text-sm">
          <Link href={base} className="text-muted-foreground hover:text-foreground">
            {isAr ? "← الرئيسية" : "← Home"}
          </Link>
          <Link href={`${base}/legal/privacy`} className="text-muted-foreground hover:text-foreground">
            {isAr ? "سياسة الخصوصية" : "Privacy Policy"}
          </Link>
          <Link href={`${base}/legal/terms`} className="text-muted-foreground hover:text-foreground">
            {isAr ? "شروط الخدمة" : "Terms of Service"}
          </Link>
        </div>
      </header>

      <article className={`mx-auto max-w-2xl px-6 py-12 ${isAr ? "text-right" : "text-left"}`}>
        <h1 className="text-3xl font-bold">
          {isAr ? "طلب حقوق البيانات الشخصية (DSAR)" : "Data Subject Access Request (DSAR)"}
        </h1>
        <p className="mt-3 text-muted-foreground leading-relaxed">
          {isAr
            ? "نظام حماية البيانات الشخصية السعودي (PDPL) المواد 12-15 و GDPR يمنحانك حقوقاً صريحة على بياناتك الشخصية. هذا النموذج هو القناة الرسمية لممارستها. نرد خلال 5 أيام عمل (الحد الأقصى النظامي 30 يوماً)."
            : "Saudi PDPL Art. 12–15 and GDPR grant you explicit rights over your personal data. This form is the official channel to exercise them. We reply within 5 business days (statutory maximum 30 days)."}
        </p>

        <section className="mt-8 rounded-lg border border-border/60 bg-card/30 p-5 text-sm leading-relaxed">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
            {isAr ? "ما الذي يحدث بعد الإرسال" : "What happens next"}
          </h2>
          <ol className={`mt-3 space-y-2 ${isAr ? "pr-5" : "pl-5"} list-decimal`}>
            <li>{isAr ? "تستلم بريد تحقق على نفس البريد الإلكتروني." : "You receive a verification email at the same address."}</li>
            <li>{isAr ? "اضغط رابط التحقق خلال 24 ساعة لإثبات الهوية." : "Click the link within 24 hours to confirm your identity."}</li>
            <li>{isAr ? "ننفذ طلبك خلال 5 أيام عمل ونرسل التأكيد." : "We fulfill the request within 5 business days and email confirmation."}</li>
          </ol>
        </section>

        <DsarForm locale={locale} />

        <footer className="mt-10 border-t border-border/60 pt-6 text-sm text-muted-foreground">
          {isAr ? (
            <>للأسئلة قبل تقديم الطلب: <a href="mailto:privacy@dealix.sa" className="text-primary underline">privacy@dealix.sa</a> (مسؤول حماية البيانات).</>
          ) : (
            <>Questions before filing: <a href="mailto:privacy@dealix.sa" className="text-primary underline">privacy@dealix.sa</a> (Data Protection Officer).</>
          )}
        </footer>
      </article>
    </div>
  );
}
