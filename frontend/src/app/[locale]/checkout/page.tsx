import type { Metadata } from "next";
import { CheckoutPanel } from "@/components/gtm/CheckoutPanel";

export const metadata: Metadata = {
  title: "Checkout · Dealix",
  description: "Pick a Dealix plan and complete payment via Moyasar.",
};

type Params = { locale: string };

type Plan = {
  id: string;
  label_ar: string;
  label_en: string;
  price_ar: string;
  price_en: string;
  blurb_ar: string;
  blurb_en: string;
  recommended?: boolean;
};

const PLANS: Plan[] = [
  {
    id: "pilot_1sar",
    label_ar: "تجربة بريال واحد",
    label_en: "1-SAR pilot",
    price_ar: "١ ر.س — تجربة الإطلاق",
    price_en: "1 SAR — launch trial",
    blurb_ar: "تجربة الدفع الكاملة بريال واحد قبل الالتزام بأي خطة.",
    blurb_en: "Verify the full Moyasar flow with a 1 SAR transaction.",
  },
  {
    id: "pilot_managed",
    label_ar: "Sprint مُدار — ٧ أيام",
    label_en: "Managed Sprint — 7 days",
    price_ar: "٤٩٩ ر.س لمرة واحدة",
    price_en: "499 SAR one-off",
    blurb_ar: "تقرير Diagnostic + Proof Pack أولي في أسبوع.",
    blurb_en: "Diagnostic report + initial Proof Pack in one week.",
    recommended: true,
  },
  {
    id: "starter",
    label_ar: "Starter شهري",
    label_en: "Starter monthly",
    price_ar: "٩٩٩ ر.س / شهر",
    price_en: "999 SAR/mo",
    blurb_ar: "خطة دخول مع Lead intelligence أساسي.",
    blurb_en: "Entry tier with baseline Lead intelligence.",
  },
  {
    id: "growth",
    label_ar: "Growth شهري",
    label_en: "Growth monthly",
    price_ar: "٢٩٩٩ ر.س / شهر",
    price_en: "2,999 SAR/mo",
    blurb_ar: "Managed Revenue Ops مع تقرير أسبوعي + proof curation.",
    blurb_en: "Managed Revenue Ops + weekly report + proof curation.",
  },
  {
    id: "scale",
    label_ar: "Scale شهري",
    label_en: "Scale monthly",
    price_ar: "٧٩٩٩ ر.س / شهر",
    price_en: "7,999 SAR/mo",
    blurb_ar: "Executive Command Center + قرارات استراتيجية أسبوعية.",
    blurb_en: "Executive Command Center + weekly strategy decisions.",
  },
];

export default async function CheckoutPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <main
      dir={isAr ? "rtl" : "ltr"}
      className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:py-16"
    >
      <header className="mb-10 text-center">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
          {isAr ? "اختر خطتك" : "Choose your plan"}
        </h1>
        <p className="mt-3 text-sm text-muted-foreground sm:text-base">
          {isAr
            ? "كل خطة تبدأ بـ Diagnostic مجاني — الدفع عبر Moyasar (مدى/Visa/Mastercard/Apple Pay)."
            : "Every plan starts with a free Diagnostic — payment via Moyasar (Mada/Visa/Mastercard/Apple Pay)."}
        </p>
        <p className="mt-2 text-xs text-muted-foreground">
          {isAr
            ? "كل المعاملات بالريال السعودي وتشمل ضريبة القيمة المضافة وفق ZATCA."
            : "All amounts in SAR and inclusive of VAT per ZATCA rules."}
        </p>
      </header>

      <section className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {PLANS.map((plan) => (
          <article
            key={plan.id}
            className={`rounded-lg border p-5 ${
              plan.recommended
                ? "border-emerald-500 ring-1 ring-emerald-500/30"
                : "border-border"
            }`}
            data-test={`checkout-plan-${plan.id}`}
          >
            {plan.recommended && (
              <span className="mb-2 inline-block rounded bg-emerald-50 px-2 py-0.5 text-xs font-medium text-emerald-700">
                {isAr ? "الأكثر اختياراً" : "Most chosen"}
              </span>
            )}
            <h2 className="text-lg font-semibold">
              {isAr ? plan.label_ar : plan.label_en}
            </h2>
            <p className="mt-1 text-sm font-medium text-foreground/80">
              {isAr ? plan.price_ar : plan.price_en}
            </p>
            <p className="mt-3 text-sm text-muted-foreground">
              {isAr ? plan.blurb_ar : plan.blurb_en}
            </p>
            <CheckoutPanel
              plan={plan.id}
              planLabel={isAr ? plan.label_ar : plan.label_en}
              priceHint={isAr ? plan.price_ar : plan.price_en}
              isAr={isAr}
            />
          </article>
        ))}
      </section>

      <footer className="mt-10 rounded-md border border-dashed p-4 text-xs text-muted-foreground">
        {isAr ? (
          <>
            <strong>ملاحظة:</strong> الاشتراكات الشهرية (Starter/Growth/Scale)
            تتجدّد بدورة شهرية حتى تطلب الإلغاء. الدفعات لمرة واحدة (Sprint/تجربة
            بريال) لا تتجدّد. كل العمليات مسجَّلة في proof pack ledger.
          </>
        ) : (
          <>
            <strong>Note:</strong> Monthly plans (Starter/Growth/Scale) renew
            until you request cancellation. One-off charges (Sprint, 1-SAR
            pilot) do not renew. Every transaction is logged to the proof-pack
            ledger.
          </>
        )}
      </footer>
    </main>
  );
}
