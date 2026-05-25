import Link from "next/link";
import { PublicLaunchShell } from "@/components/brand/PublicLaunchShell";

type Props = { params: Promise<{ locale: string }> };

export default async function PrivacyPage({ params }: Props) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const base = `/${locale}`;

  return (
    <PublicLaunchShell compactNav>
      <main className="mx-auto max-w-3xl px-6 py-16 prose prose-sm dark:prose-invert">
        <h1>{isAr ? "سياسة الخصوصية — PDPL" : "Privacy & PDPL Policy"}</h1>
        <p className="text-muted-foreground">
          {isAr
            ? "Dealix — نظام إيراد B2B سعودي. لا outreach بارد. لا scraping. موافقة قبل أي إرسال خارجي."
            : "Dealix — Saudi B2B Revenue OS. No cold outreach. No scraping. Approval before any external send."}
        </p>
        <h2>{isAr ? "حقوق صاحب البيانات" : "Data subject rights"}</h2>
        <ul>
          <li>{isAr ? "الوصول والتصحيح والحذف والتصدير — خلال 30 يوماً" : "Access, correction, deletion, export — within 30 days"}</li>
          <li>{isAr ? "سحب الموافقة — فوري عند الطلب" : "Withdraw consent — immediate upon request"}</li>
        </ul>
        <h2>{isAr ? "ما لا نفعله" : "What we do not do"}</h2>
        <ul>
          <li>{isAr ? "لا مشاركة بيانات مع طرف ثالث بدون موافقة صريحة" : "No third-party sharing without explicit consent"}</li>
          <li>{isAr ? "لا WhatsApp/LinkedIn آلي للعملاء الباردين" : "No automated cold WhatsApp/LinkedIn"}</li>
        </ul>
        <p>
          <Link href={base} className="text-primary hover:underline">
            {isAr ? "← الرئيسية" : "← Home"}
          </Link>
        </p>
        <p className="text-xs text-muted-foreground">
          {isAr ? "النسخة الكاملة:" : "Full policy:"}{" "}
          docs/knowledge-base/privacy_pdpl_ar_en.md
        </p>
      </main>
    </PublicLaunchShell>
  );
}
