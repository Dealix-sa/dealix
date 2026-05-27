"use client";
import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import type { ReactNode } from "react";
import { BrandLogo } from "@/components/brand/BrandLogo";
import { LocaleToggle } from "@/components/layout/LocaleToggle";

export function PublicLaunchShell({ children, compactNav = false }: { children: ReactNode; compactNav?: boolean }) {
  const locale = useLocale();
  const t = useTranslations("commercialLaunch");
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const adminKey = typeof window !== "undefined" ? process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || "" : "";
  return (
    <div className="dealix-public min-h-screen flex flex-col" dir={isAr ? "rtl" : "ltr"}>
      <header className="border-b border-[var(--dealix-deep-green)]/15 bg-white/90 sticky top-0 z-20">
        <div className="mx-auto max-w-6xl px-6 py-4 flex items-center justify-between gap-4">
          <Link href={base}><BrandLogo variant="full" priority className="h-8" /></Link>
          {!compactNav ? (
            <nav className="flex flex-wrap items-center gap-3 text-sm">
              <Link href={`${base}/dealix-diagnostic`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)]">{isAr ? "تشخيص" : "Diagnostic"}</Link>
              <Link href={`${base}/risk-score`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)]">{t("ctaRiskScore")}</Link>
              <Link href={`${base}/proof-pack`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)]">{t("ctaSampleProof")}</Link>
              <Link href={`${base}/learn`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)]">{t("navLearn")}</Link>
              <Link href={`${base}/partners`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)]">{t("ctaPartners")}</Link>
              <Link href={`${base}/services`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)]">{t("navServices")}</Link>
              <Link href={`${base}/login`} className="font-medium text-[var(--dealix-deep-green)]">{t("navLogin")}</Link>
              {adminKey ? <Link href={`${base}/ops/founder`} className="text-[var(--dealix-gold)]">{isAr ? "تشغيل المؤسس" : "Founder ops"}</Link> : null}
              <LocaleToggle />
            </nav>
          ) : (
            <div className="flex gap-3"><Link href={base}>{isAr ? "الرئيسية" : "Home"}</Link><LocaleToggle /></div>
          )}
        </div>
      </header>
      <div className="flex-1">{children}</div>
      <footer className="border-t py-10 px-6 text-sm max-w-6xl mx-auto w-full">
        <p className="font-semibold text-[var(--dealix-deep-green)]">{t("footer")}</p>
        <p className="mt-2 text-muted-foreground">{t("footerPositioning")}</p>
        <p className="mt-2 text-xs text-muted-foreground">{t("footerTrustPdpl")}</p>
        <Link href={`${base}/privacy`} className="mt-2 inline-block text-xs text-[var(--dealix-deep-green)] hover:underline">
          {isAr ? "سياسة الخصوصية" : "Privacy policy"}
        </Link>
      </footer>
    </div>
  );
}
