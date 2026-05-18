"use client";

import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { usePathname } from "next/navigation";
import { Globe, Menu, X } from "lucide-react";
import { useState } from "react";
import { BrandLogo } from "@/components/brand/BrandLogo";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { PlatformStatusBar } from "@/components/home/PlatformStatusBar";

interface PublicShellProps {
  children: React.ReactNode;
  showStatus?: boolean;
}

export function PublicShell({ children, showStatus = true }: PublicShellProps) {
  const t = useTranslations("public");
  const locale = useLocale();
  const pathname = usePathname();
  const isRTL = locale === "ar";
  const [mobileOpen, setMobileOpen] = useState(false);

  const links = [
    { href: `/${locale}`, label: t("home") },
    { href: `/${locale}/services`, label: t("services") },
    { href: `/${locale}/offer/lead-intelligence-sprint`, label: t("sprint") },
    { href: `/${locale}/founder`, label: t("founder") },
  ];

  const switchLocale = () => {
    const next = locale === "ar" ? "en" : "ar";
    const segments = pathname.split("/");
    segments[1] = next;
    window.location.href = segments.join("/") || `/${next}`;
  };

  return (
    <div className="min-h-screen flex flex-col bg-background grid-pattern">
      <header className="sticky top-0 z-50 border-b border-border/60 bg-background/90 backdrop-blur-md">
        {showStatus && <PlatformStatusBar />}
        <div className="page-container flex h-16 items-center justify-between gap-4 px-6">
          <Link
            href={`/${locale}`}
            className="flex-shrink-0 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-lg"
          >
            <BrandLogo variant="full" priority className="h-8 max-w-[130px]" />
          </Link>

          <nav
            className="hidden lg:flex items-center gap-1"
            aria-label={isRTL ? "التنقل" : "Navigation"}
          >
            {links.map((link) => {
              const active =
                link.href === `/${locale}`
                  ? pathname === `/${locale}` || pathname === `/${locale}/`
                  : pathname.startsWith(link.href);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={cn(
                    "px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                    active
                      ? "bg-primary/15 text-primary"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted/60",
                  )}
                >
                  {link.label}
                </Link>
              );
            })}
          </nav>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={switchLocale}
              className="hidden sm:flex items-center gap-1.5 h-9 px-3 rounded-xl text-sm text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
              aria-label={t("switchLocale")}
            >
              <Globe className="w-3.5 h-3.5" aria-hidden />
              {locale === "ar" ? "EN" : "عربي"}
            </button>
            <Button variant="ghost" size="sm" className="hidden sm:inline-flex" asChild>
              <Link href={`/${locale}/login`}>{t("login")}</Link>
            </Button>
            <Button variant="gold" size="sm" asChild>
              <Link href={`/${locale}/dashboard`}>{t("commandCenter")}</Link>
            </Button>
            <button
              type="button"
              className="lg:hidden w-9 h-9 rounded-xl flex items-center justify-center text-muted-foreground hover:bg-muted"
              onClick={() => setMobileOpen(!mobileOpen)}
              aria-expanded={mobileOpen}
              aria-label={t("menu")}
            >
              {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {mobileOpen && (
          <nav className="lg:hidden border-t border-border/60 px-6 py-4 space-y-1 bg-background">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileOpen(false)}
                className="block px-3 py-2.5 rounded-lg text-sm font-medium text-foreground hover:bg-muted"
              >
                {link.label}
              </Link>
            ))}
            <button
              type="button"
              onClick={switchLocale}
              className="w-full text-start px-3 py-2.5 text-sm text-muted-foreground"
            >
              {locale === "ar" ? "English" : "العربية"}
            </button>
          </nav>
        )}
      </header>

      <main className="flex-1">{children}</main>

      <footer className="border-t border-border/60 bg-card/40 mt-auto">
        <div className="page-container px-6 py-10 flex flex-col md:flex-row gap-6 md:items-center md:justify-between">
          <div className={cn(isRTL ? "text-right" : "text-left")}>
            <BrandLogo variant="mark" className="h-8 w-8 mb-3" />
            <p className="text-sm text-muted-foreground max-w-md leading-relaxed">
              {t("footerTagline")}
            </p>
          </div>
          <div className="flex flex-wrap gap-4 text-sm">
            <Link href={`/${locale}/services`} className="text-muted-foreground hover:text-primary">
              {t("services")}
            </Link>
            <Link
              href={`/${locale}/trust-check`}
              className="text-muted-foreground hover:text-primary"
            >
              {t("trust")}
            </Link>
            <Link href={`/${locale}/login`} className="text-muted-foreground hover:text-primary">
              {t("login")}
            </Link>
          </div>
        </div>
        <p className="text-center text-[10px] text-muted-foreground/70 pb-6">
          © {new Date().getFullYear()} Dealix — {t("rights")}
        </p>
      </footer>
    </div>
  );
}
