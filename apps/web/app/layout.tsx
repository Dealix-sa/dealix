import "./globals.css";
import "../styles/brand.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Dealix Founder Console",
  description: "Revenue Intelligence for Saudi B2B — internal command center.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
