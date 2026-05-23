import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Dealix — Intelligent Deals. Real Growth.",
  description: "Dealix Founder Console — intelligent deals, real growth.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
