"use client";

import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { CheckSquare, Shield, Sparkles, TrendingUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function ExecutiveCommandStrip() {
  const t = useTranslations("dashboard.command");
  const locale = useLocale();
  const isAr = locale === "ar";

  const actions = [
    {
      href: `/${locale}/approvals`,
      icon: CheckSquare,
      label: t("approvals"),
    },
    {
      href: `/${locale}/trust-check`,
      icon: Shield,
      label: t("trust"),
    },
    {
      href: `/${locale}/pipeline`,
      icon: TrendingUp,
      label: t("pipeline"),
    },
    {
      href: `/${locale}/founder`,
      icon: Sparkles,
      label: t("founder"),
    },
  ];

  return (
    <div
      className={cn(
        "mb-8 rounded-2xl border border-border/70 bg-gradient-to-r from-secondary/15 via-card to-primary/10 p-4 md:p-5 card-glass",
        isAr ? "text-right" : "text-left",
      )}
      dir={isAr ? "rtl" : "ltr"}
    >
      <p className="text-xs font-semibold uppercase tracking-wider text-primary mb-1">
        {t("eyebrow")}
      </p>
      <p className="text-sm text-muted-foreground mb-4 max-w-2xl">{t("hint")}</p>
      <div className={cn("flex flex-wrap gap-2", isAr && "justify-end")}>
        {actions.map(({ href, icon: Icon, label }) => (
          <Button key={href} variant="outline" size="sm" className="rounded-xl" asChild>
            <Link href={href}>
              <Icon className="w-4 h-4 me-1.5" aria-hidden />
              {label}
            </Link>
          </Button>
        ))}
      </div>
    </div>
  );
}
