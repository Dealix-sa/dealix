"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

interface CheckoutPanelProps {
  locale: string;
}

interface Plan {
  sku: string;
  nameAr: string;
  nameEn: string;
  amountSar: number;
  cadence: "one_off" | "monthly";
  blurbAr: string;
  blurbEn: string;
}

// Mirrors api/routers/pricing.py:PLANS. Public-facing names; the canonical
// SKU is what the backend validates against. Hidden SKUs (pilot_1sar, LaaS
// metered plans) are intentionally excluded from this UI.
const PUBLIC_PLANS: Plan[] = [
  {
    sku: "pilot_managed",
    nameAr: "تشخيص مُدار (7 أيام)",
    nameEn: "Managed Diagnostic (7 days)",
    amountSar: 499,
    cadence: "one_off",
    blurbAr: "Risk Score + عينة Proof Pack على 10 leads من نظامك. تسليم خلال 7 أيام.",
    blurbEn: "Risk Score + sample Proof Pack on 10 of your leads. Delivered in 7 days.",
  },
  {
    sku: "starter",
    nameAr: "Starter (شهري)",
    nameEn: "Starter (monthly)",
    amountSar: 999,
    cadence: "monthly",
    blurbAr: "Post-Lead Revenue Ops أساسي لفريق واحد. تقرير أسبوعي + Proof Pack شهري.",
    blurbEn: "Core Post-Lead Revenue Ops for a single team. Weekly report + monthly Proof Pack.",
  },
  {
    sku: "growth",
    nameAr: "Growth (شهري)",
    nameEn: "Growth (monthly)",
    amountSar: 2999,
    cadence: "monthly",
    blurbAr: "تشغيل كامل لـ Post-Lead Ops + استخبارات سوق + جلسة استراتيجية شهرية.",
    blurbEn: "Full Post-Lead Ops + market intelligence + monthly strategy session.",
  },
  {
    sku: "scale",
    nameAr: "Scale (شهري)",
    nameEn: "Scale (monthly)",
    amountSar: 7999,
    cadence: "monthly",
    blurbAr: "Sovereign Growth OS — تشغيل سيادي لفرق متعددة + SLA + DSAR كأولوية.",
    blurbEn: "Sovereign Growth OS — multi-team operation + SLA + DSAR priority lane.",
  },
];

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface CheckoutResponse {
  invoice_id?: string;
  payment_url?: string;
  detail?: string;
}

export function CheckoutPanel({ locale }: CheckoutPanelProps) {
  const isAr = locale === "ar";
  const sp = useSearchParams();
  const initialSku = sp.get("sku");
  const initialPlan = PUBLIC_PLANS.find((p) => p.sku === initialSku) ?? PUBLIC_PLANS[0];

  const [selected, setSelected] = useState<Plan>(initialPlan);
  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<CheckoutResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const sku = sp.get("sku");
    if (sku) {
      const match = PUBLIC_PLANS.find((p) => p.sku === sku);
      if (match) setSelected(match);
    }
  }, [sp]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    setResult(null);
    try {
      const res = await fetch(`${API_BASE}/api/v1/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plan: selected.sku, email }),
      });
      const data = (await res.json().catch(() => ({}))) as CheckoutResponse;
      if (!res.ok) {
        throw new Error(data.detail || `HTTP ${res.status}`);
      }
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : (isAr ? "تعذّر إنشاء الفاتورة" : "Could not create checkout"));
    } finally {
      setSubmitting(false);
    }
  }

  const fmt = new Intl.NumberFormat(isAr ? "ar-SA" : "en-US");

  return (
    <div className="mt-10 grid gap-6 lg:grid-cols-[2fr_1fr]">
      {/* Plans list */}
      <section className="space-y-3">
        {PUBLIC_PLANS.map((plan) => {
          const isSel = plan.sku === selected.sku;
          return (
            <button
              type="button"
              key={plan.sku}
              onClick={() => setSelected(plan)}
              className={`w-full rounded-lg border p-5 text-${isAr ? "right" : "left"} transition ${
                isSel
                  ? "border-primary/70 bg-primary/5 ring-1 ring-primary/40"
                  : "border-border/60 bg-card/30 hover:border-border"
              }`}
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h3 className="font-semibold">{isAr ? plan.nameAr : plan.nameEn}</h3>
                  <p className="mt-1 text-sm text-muted-foreground leading-relaxed">
                    {isAr ? plan.blurbAr : plan.blurbEn}
                  </p>
                </div>
                <div className={`shrink-0 text-${isAr ? "left" : "right"}`}>
                  <div className="text-lg font-bold">
                    {fmt.format(plan.amountSar)} {isAr ? "ر.س" : "SAR"}
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {plan.cadence === "monthly"
                      ? (isAr ? "شهرياً" : "/month")
                      : (isAr ? "مرة واحدة" : "one-off")}
                  </div>
                </div>
              </div>
            </button>
          );
        })}
      </section>

      {/* Checkout form */}
      <aside className="rounded-lg border border-border/60 bg-card/30 p-6 h-fit sticky top-6">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          {isAr ? "إنشاء رابط الدفع" : "Generate checkout link"}
        </h3>

        {result?.payment_url ? (
          <div className="mt-4 space-y-3 text-sm">
            <p className="text-primary font-medium">✓ {isAr ? "الرابط جاهز" : "Link ready"}</p>
            <a
              href={result.payment_url}
              target="_blank"
              rel="noopener noreferrer"
              className="block break-all rounded-md border border-primary/40 bg-primary/5 px-3 py-2 text-xs font-mono text-primary hover:bg-primary/10"
            >
              {result.payment_url}
            </a>
            {result.invoice_id && (
              <p className="text-xs text-muted-foreground">
                {isAr ? "رقم الفاتورة: " : "Invoice ID: "}
                <code className="font-mono">{result.invoice_id}</code>
              </p>
            )}
            <p className="text-xs text-muted-foreground leading-relaxed">
              {isAr
                ? "افتح الرابط بنفسك لإكمال الدفع. سيصلك إيصال ZATCA من Moyasar."
                : "Open the link yourself to complete payment. You will receive a ZATCA receipt from Moyasar."}
            </p>
          </div>
        ) : (
          <form onSubmit={submit} className="mt-4 space-y-4">
            <div>
              <label className="block text-xs uppercase tracking-wider text-muted-foreground">
                {isAr ? "الباقة المختارة" : "Selected plan"}
              </label>
              <p className="mt-1 text-sm font-medium">{isAr ? selected.nameAr : selected.nameEn}</p>
              <p className="text-xs text-muted-foreground">
                {fmt.format(selected.amountSar)} {isAr ? "ر.س" : "SAR"}
                {selected.cadence === "monthly" && (isAr ? " شهرياً" : " /month")}
              </p>
            </div>

            <div>
              <label htmlFor="checkout-email" className="block text-xs uppercase tracking-wider text-muted-foreground">
                {isAr ? "بريد الفاتورة" : "Billing email"}
              </label>
              <input
                id="checkout-email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="founder@example.sa"
                className="mt-2 w-full rounded-md border border-border bg-card/40 px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>

            {error && (
              <div className="rounded-md border border-destructive/50 bg-destructive/10 px-3 py-2 text-xs text-destructive">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={submitting}
              className="w-full rounded-md bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground transition hover:bg-primary/90 disabled:opacity-50"
            >
              {submitting
                ? (isAr ? "جاري الإنشاء…" : "Generating…")
                : (isAr ? "إنشاء رابط Moyasar" : "Generate Moyasar link")}
            </button>

            <p className="text-xs text-muted-foreground leading-relaxed">
              {isAr
                ? "بالضغط فوق، أنت توافق على شروط الخدمة. الدفع آمن عبر Moyasar — لا نخزن بيانات بطاقتك."
                : "By clicking, you accept the Terms of Service. Payment is secured by Moyasar — no card data is stored by us."}
            </p>
          </form>
        )}
      </aside>
    </div>
  );
}
