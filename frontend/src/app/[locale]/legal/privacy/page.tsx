import type { Metadata } from "next";
import Link from "next/link";
import { PRIVACY_POLICY } from "@/content/legal/policies";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? `${PRIVACY_POLICY.titleAr} — Dealix` : `${PRIVACY_POLICY.titleEn} — Dealix`,
    description: isAr ? PRIVACY_POLICY.tldrAr[0] : PRIVACY_POLICY.tldrEn[0],
  };
}

export default async function PrivacyPolicyPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const sections = isAr ? PRIVACY_POLICY.sections.ar : PRIVACY_POLICY.sections.en;
  const tldr = isAr ? PRIVACY_POLICY.tldrAr : PRIVACY_POLICY.tldrEn;

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>
      <header className="border-b border-border/60">
        <div className="mx-auto max-w-3xl px-6 py-4 flex flex-wrap gap-4 text-sm">
          <Link href={base} className="text-muted-foreground hover:text-foreground">
            {isAr ? "← الرئيسية" : "← Home"}
          </Link>
          <Link href={`${base}/legal/terms`} className="text-muted-foreground hover:text-foreground">
            {isAr ? "شروط الخدمة" : "Terms of Service"}
          </Link>
          <Link href={`${base}/legal/dsar`} className="text-muted-foreground hover:text-foreground">
            {isAr ? "طلب حقوق البيانات (DSAR)" : "Data Subject Request (DSAR)"}
          </Link>
        </div>
      </header>

      <article className={`mx-auto max-w-3xl px-6 py-12 ${isAr ? "text-right" : "text-left"}`}>
        <h1 className="text-3xl font-bold">{isAr ? PRIVACY_POLICY.titleAr : PRIVACY_POLICY.titleEn}</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          {isAr ? "يسري من" : "Effective"}: {PRIVACY_POLICY.effectiveDate}
          {" · "}
          {isAr ? "متوافق مع PDPL + GDPR" : "PDPL + GDPR aligned"}
        </p>

        <section className="mt-8 rounded-lg border border-border/60 bg-card/30 p-5">
          <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
            {isAr ? "ملخص تنفيذي" : "TL;DR"}
          </h2>
          <ul className="mt-3 space-y-2 text-sm leading-relaxed">
            {tldr.map((line, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-primary">•</span>
                <span>{line}</span>
              </li>
            ))}
          </ul>
        </section>

        <div className="mt-10 space-y-8">
          {sections.map((s) => (
            <section key={s.heading}>
              <h2 className="text-xl font-semibold">{s.heading}</h2>
              <p className="mt-2 text-muted-foreground leading-relaxed whitespace-pre-line">{s.body}</p>
            </section>
          ))}
        </div>

        <footer className="mt-12 border-t border-border/60 pt-6 text-sm text-muted-foreground">
          {isAr ? (
            <>
              للأسئلة أو ممارسة حقوقك: <a href="mailto:privacy@dealix.sa" className="text-primary underline">privacy@dealix.sa</a>
              {" · "}
              <Link href={`${base}/legal/dsar`} className="text-primary underline">قدّم طلب DSAR</Link>
            </>
          ) : (
            <>
              For questions or to exercise your rights: <a href="mailto:privacy@dealix.sa" className="text-primary underline">privacy@dealix.sa</a>
              {" · "}
              <Link href={`${base}/legal/dsar`} className="text-primary underline">File a DSAR</Link>
            </>
          )}
        </footer>
      </article>
    </div>
  );
}
