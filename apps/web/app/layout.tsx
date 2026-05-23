import "./globals.css";
import type { ReactNode } from "react";
import { DEALIX_BRAND } from "../lib/brand-tokens";

export const metadata = {
  title: `${DEALIX_BRAND.name} — ${DEALIX_BRAND.tagline}`,
  description:
    "Saudi B2B revenue intelligence with AI assistance and human approval on every outbound action."
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
