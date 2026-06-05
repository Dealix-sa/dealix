import type { ReactNode } from "react";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

/** Public marketing wrapper for multi-section Wave 3 pages. */
export function MarketingShell({
  locale,
  children,
}: {
  locale: string;
  children: ReactNode;
}) {
  const isAr = locale === "ar";
  return (
    <PublicGtmShell>
      <div
        className="mx-auto max-w-5xl px-6 py-10"
        dir={isAr ? "rtl" : "ltr"}
      >
        {children}
      </div>
    </PublicGtmShell>
  );
}
