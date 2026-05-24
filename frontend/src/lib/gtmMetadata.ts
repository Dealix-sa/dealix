import type { Metadata } from "next";
const SITE = "https://dealix.me";
const OG = [{ url: `${SITE}/brand/og-dealix.svg`, width: 1200, height: 630, alt: "Dealix" }];

export function buildFunnelMetadata(locale: string, key: "diagnostic" | "proof-pack" | "risk-score" | "partners"): Metadata {
  const paths = { diagnostic: "/dealix-diagnostic", "proof-pack": "/proof-pack", "risk-score": "/risk-score", partners: "/partners" };
  const url = `${SITE}/${locale}${paths[key]}`;
  return { title: `Dealix — ${key}`, openGraph: { url, images: OG }, alternates: { canonical: url } };
}

export function buildHomeMetadata(locale: string): Metadata {
  const isAr = locale === "ar";
  const title = isAr ? "Dealix — نظام إيرادات B2B سعودي" : "Dealix — Saudi B2B Revenue OS";
  const description = isAr ? "وحّد قرار الإيراد. أثبت كل لمسة. وسّع فقط بعد Proof." : "Unify revenue decisions. Prove every touch. Expand only after proof.";
  const url = `${SITE}/${locale}`;
  return { title, description, openGraph: { title, description, url, images: OG }, alternates: { canonical: url }, icons: { icon: "/brand/logo-mark.svg" } };
}
