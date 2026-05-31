import type { Metadata } from "next";

const SITE = "https://dealix.me";

const OG_DEFAULT = [{ url: `${SITE}/brand/og-dealix.svg`, width: 1200, height: 630, alt: "Dealix — Saudi B2B Revenue OS" }];
const OG_DIAGNOSTIC = [{ url: `${SITE}/brand/og-diagnostic.svg`, width: 1200, height: 630, alt: "Dealix — تشخيص ٧ أيام" }];
const OG_SERVICES = [{ url: `${SITE}/brand/og-services.svg`, width: 1200, height: 630, alt: "Dealix — خطوط الخدمات الخمس" }];

type FunnelKey = "diagnostic" | "proof-pack" | "risk-score" | "partners" | "learn" | "privacy";

const FUNNEL_META: Record<FunnelKey, { path: string; titleAr: string; titleEn: string; descAr: string; descEn: string; og: typeof OG_DEFAULT }> = {
  diagnostic: {
    path: "/dealix-diagnostic",
    titleAr: "Dealix — تشخيص ٧ أيام · Proof Pack بالدليل",
    titleEn: "Dealix — 7-Day Diagnostic · Evidence Proof Pack",
    descAr: "نكشف فجوات الإيراد وCRM وAI خلال ٧ أيام مع أول ٣ قرارات قابلة للتنفيذ بدليل موثّق.",
    descEn: "Map revenue, CRM, and AI governance gaps in 7 days with top 3 documented executable decisions.",
    og: OG_DIAGNOSTIC,
  },
  "proof-pack": {
    path: "/proof-pack",
    titleAr: "Dealix — عيّنة Proof Pack",
    titleEn: "Dealix — Sample Proof Pack",
    descAr: "شاهد كيف يبدو Proof Pack الحقيقي بعد تشخيص ٧ أيام.",
    descEn: "See what a real Proof Pack looks like after a 7-day diagnostic.",
    og: OG_DEFAULT,
  },
  "risk-score": {
    path: "/risk-score",
    titleAr: "Dealix — Risk Score المجاني",
    titleEn: "Dealix — Free Risk Score",
    descAr: "احصل على تقييم مخاطر مجاني لعمليات شركتك.",
    descEn: "Get a free risk assessment for your company operations.",
    og: OG_DEFAULT,
  },
  partners: {
    path: "/partners",
    titleAr: "Dealix — برنامج الشراكة",
    titleEn: "Dealix — Partner Program",
    descAr: "انضم لشبكة شركاء Dealix — تحضر العملاء، نحن ننفذ، نتقاسم الإيراد.",
    descEn: "Join the Dealix partner network — you bring clients, we deliver, we share revenue.",
    og: OG_DEFAULT,
  },
  learn: {
    path: "/learn",
    titleAr: "Dealix — مكتبة Revenue Ops",
    titleEn: "Dealix — Revenue Ops Library",
    descAr: "مقالات عملية عن تشغيل الإيراد، الحوكمة، وCRM في السوق السعودي.",
    descEn: "Practical articles on revenue operations, governance, and CRM in the Saudi market.",
    og: OG_DEFAULT,
  },
  privacy: {
    path: "/privacy",
    titleAr: "Dealix — سياسة الخصوصية وحماية البيانات",
    titleEn: "Dealix — Privacy & Data Protection Policy",
    descAr: "Dealix مبني أصلاً على PDPL — لا outreach بارد، موافقة قبل أي إرسال.",
    descEn: "Dealix is built natively on PDPL — no cold outreach, approval before any external send.",
    og: OG_DEFAULT,
  },
};

export function buildFunnelMetadata(locale: string, key: FunnelKey): Metadata {
  const isAr = locale === "ar";
  const meta = FUNNEL_META[key];
  const url = `${SITE}/${locale}${meta.path}`;
  const title = isAr ? meta.titleAr : meta.titleEn;
  const description = isAr ? meta.descAr : meta.descEn;
  return {
    title,
    description,
    openGraph: { title, description, url, images: meta.og },
    alternates: { canonical: url },
  };
}

export function buildServicesMetadata(locale: string): Metadata {
  const isAr = locale === "ar";
  const url = `${SITE}/${locale}/services`;
  const title = isAr ? "Dealix — خطوط الخدمات الخمس" : "Dealix — Five Service Lines";
  const description = isAr
    ? "تشخيص، Sprint، حزمة بيانات، تشغيل مُدار، مشاريع AI مخصصة — كل رتبة تُفتح بعد دليل موثّق."
    : "Diagnostic, Sprint, Data Pack, Managed Ops, Custom AI — each rung unlocks only after documented proof.";
  return {
    title,
    description,
    openGraph: { title, description, url, images: OG_SERVICES },
    alternates: { canonical: url },
  };
}

export function buildArticleMetadata(
  locale: string,
  titleAr: string,
  titleEn: string,
  descriptionAr: string,
  descriptionEn: string,
  slug: string,
): Metadata {
  const isAr = locale === "ar";
  const title = isAr ? `Dealix — ${titleAr}` : `Dealix — ${titleEn}`;
  const description = isAr ? descriptionAr : descriptionEn;
  const url = `${SITE}/${locale}/learn/${slug}`;
  return {
    title,
    description,
    openGraph: { title, description, url, images: OG_DEFAULT },
    alternates: { canonical: url },
  };
}

export function buildHomeMetadata(locale: string): Metadata {
  const isAr = locale === "ar";
  const title = isAr ? "Dealix — نظام التشغيل الإيرادي · السعودية أولاً" : "Dealix — Saudi-First B2B Revenue OS";
  const description = isAr
    ? "وحّد قرار الإيراد. أثبت كل لمسة. PDPL native · ZATCA ready · Approval-first."
    : "Unify revenue decisions. Prove every touch. PDPL native · ZATCA ready · Approval-first.";
  const url = `${SITE}/${locale}`;
  return {
    title,
    description,
    openGraph: { title, description, url, images: OG_DEFAULT, siteName: "Dealix" },
    alternates: { canonical: url },
    icons: { icon: "/brand/logo-mark.svg" },
  };
}
