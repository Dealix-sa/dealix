"use client";

import { useLocale } from "next-intl";
import { PublicLaunchShell } from "@/components/brand/PublicLaunchShell";
import { CustomerPortalDashboard } from "@/components/portal/CustomerPortalDashboard";

export default function CustomerPortalPage() {
  const locale = useLocale();
  const isAr = locale === "ar";

  return (
    <PublicLaunchShell compactNav>
      <div className="mx-auto max-w-4xl px-6 py-10" dir={isAr ? "rtl" : "ltr"}>
        <CustomerPortalDashboard />
      </div>
    </PublicLaunchShell>
  );
}
