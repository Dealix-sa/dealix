import Link from "next/link";
import { PublicShell } from "@/components/layout/PublicShell";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

interface MarketingPageProps {
  locale: string;
  isAr: boolean;
  eyebrow: string;
  title: string;
  lead?: ReactNode;
  children: ReactNode;
  ctaHref?: string;
  ctaLabel?: string;
  footer?: ReactNode;
  maxWidth?: "md" | "lg" | "xl";
}

const maxWidthClass = {
  md: "max-w-3xl",
  lg: "max-w-4xl",
  xl: "max-w-5xl",
};

export function MarketingPage({
  isAr,
  eyebrow,
  title,
  lead,
  children,
  ctaHref,
  ctaLabel,
  footer,
  maxWidth = "lg",
}: MarketingPageProps) {
  return (
    <PublicShell>
      <div
        className={cn(
          "page-container page-content mx-auto",
          maxWidthClass[maxWidth],
          isAr ? "text-right" : "text-left",
        )}
        dir={isAr ? "rtl" : "ltr"}
      >
        <p className="text-sm font-medium text-primary/90 tracking-wide uppercase">
          {eyebrow}
        </p>
        <h1 className="mt-3 text-3xl md:text-4xl font-bold tracking-tight text-foreground font-display">
          {title}
        </h1>
        {lead && (
          <div className="mt-4 text-muted-foreground leading-relaxed">{lead}</div>
        )}

        <div className="mt-10">{children}</div>

        {ctaHref && ctaLabel && (
          <div className={cn("mt-12 flex flex-wrap gap-4", isAr && "justify-end")}>
            <Button variant="gold" size="lg" asChild>
              <Link href={ctaHref}>{ctaLabel}</Link>
            </Button>
          </div>
        )}

        {footer && <div className="mt-10 text-xs text-muted-foreground">{footer}</div>}
      </div>
    </PublicShell>
  );
}
