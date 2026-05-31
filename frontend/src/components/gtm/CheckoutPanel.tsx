"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

// ---------------------------------------------------------------------------
// Tier definitions
// ---------------------------------------------------------------------------

interface ServiceTier {
  id: string;
  name_ar: string;
  name_en: string;
  price_sar: number;
  description_ar: string;
  description_en: string;
}

const SERVICE_TIERS: ServiceTier[] = [
  {
    id: "sprint",
    name_ar: "Sprint — الانطلاق",
    name_en: "Sprint — Starter",
    price_sar: 499,
    description_ar: "تشخيص 7 أيام + Proof Pack + توصيات فورية",
    description_en: "7-day diagnostic + Proof Pack + immediate recommendations",
  },
  {
    id: "data_pack",
    name_ar: "Data Pack — حزمة البيانات",
    name_en: "Data Pack — Analytics",
    price_sar: 1500,
    description_ar: "Sprint + أتمتة التقارير + لوحة بيانات مخصصة",
    description_en: "Sprint + report automation + custom dashboard",
  },
  {
    id: "managed_ops",
    name_ar: "Managed Ops — إدارة كاملة",
    name_en: "Managed Ops — Full Management",
    price_sar: 2999,
    description_ar: "إدارة عمليات شهرية كاملة + Retainer + امتثال ZATCA",
    description_en: "Full monthly operations management + Retainer + ZATCA compliance",
  },
];

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

export interface CheckoutPanelProps {
  /** Pre-selected plan id. If not provided, renders a tier selector. */
  plan?: string;
  planLabel?: string;
  priceHint?: string;
  isAr: boolean;
  customerName?: string;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export function CheckoutPanel({
  plan: initialPlan,
  planLabel,
  priceHint,
  isAr,
  customerName = "",
}: CheckoutPanelProps) {
  const [selectedTierId, setSelectedTierId] = useState<string>(
    initialPlan ?? SERVICE_TIERS[0].id,
  );
  const [email, setEmail] = useState("");
  const [name, setName] = useState(customerName);
  const [pdplConsent, setPdplConsent] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const selectedTier =
    SERVICE_TIERS.find((t) => t.id === selectedTierId) ?? SERVICE_TIERS[0];

  const effectivePlanLabel =
    planLabel ?? (isAr ? selectedTier.name_ar : selectedTier.name_en);
  const effectivePriceHint =
    priceHint ??
    `${selectedTier.price_sar.toLocaleString("ar-SA")} ${isAr ? "ر.س" : "SAR"}`;

  const pay = async () => {
    if (!name.trim() || !email.trim() || !pdplConsent) return;
    setBusy(true);
    setError("");
    try {
      const base = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
      const adminKey = process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY ?? "";
      const res = await fetch(`${base}/api/v1/commercial/payment/link`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(adminKey ? { "X-Admin-API-Key": adminKey } : {}),
        },
        body: JSON.stringify({
          service_tier: selectedTierId,
          customer_name: name,
          customer_email: email,
        }),
      });
      const data = (await res.json()) as { payment_url?: string; detail?: string };
      if (data.payment_url) {
        window.location.href = data.payment_url;
      } else {
        setError(
          data.detail ??
            (isAr ? "حدث خطأ — حاول لاحقاً" : "Error — try again"),
        );
      }
    } catch {
      setError(
        isAr ? "تعذّر الاتصال بالخادم" : "Could not reach server",
      );
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-5" dir={isAr ? "rtl" : "ltr"}>
      {/* Tier selector — shown when no plan is pre-selected */}
      {!initialPlan && (
        <div className="space-y-2">
          <p className="text-sm font-medium">
            {isAr ? "اختر الخطة" : "Select plan"}
          </p>
          <div className="grid gap-2">
            {SERVICE_TIERS.map((tier) => (
              <button
                key={tier.id}
                onClick={() => setSelectedTierId(tier.id)}
                className={`w-full text-start rounded-lg border p-3 transition-colors ${
                  selectedTierId === tier.id
                    ? "border-[var(--dealix-deep-green)] bg-[var(--dealix-deep-green)]/5"
                    : "border-border hover:border-[var(--dealix-deep-green)]/40"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-semibold">
                    {isAr ? tier.name_ar : tier.name_en}
                  </span>
                  <Badge variant="outline" className="text-xs font-bold">
                    {tier.price_sar.toLocaleString("ar-SA")}{" "}
                    {isAr ? "ر.س" : "SAR"}
                  </Badge>
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  {isAr ? tier.description_ar : tier.description_en}
                </p>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Selected plan summary */}
      <Card className="p-4 border-[var(--dealix-deep-green)]/20 bg-[var(--dealix-deep-green)]/5">
        <p className="text-sm font-semibold">
          {effectivePlanLabel} — {effectivePriceHint}
        </p>
        <p className="text-xs text-muted-foreground mt-1">
          {isAr ? selectedTier.description_ar : selectedTier.description_en}
        </p>
      </Card>

      {/* Customer info */}
      <div className="space-y-3">
        <Input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder={isAr ? "اسمك أو اسم الشركة" : "Your name or company"}
        />
        <Input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@company.sa"
        />
      </div>

      {/* PDPL consent */}
      <label className="flex gap-3 items-start text-sm cursor-pointer">
        <input
          type="checkbox"
          checked={pdplConsent}
          onChange={(e) => setPdplConsent(e.target.checked)}
          className="mt-0.5 accent-[var(--dealix-deep-green)]"
        />
        <span className="leading-relaxed">
          {isAr ? (
            <>
              أوافق على{" "}
              <a
                href="/ar/privacy"
                className="text-[var(--dealix-deep-green)] underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                سياسة الخصوصية
              </a>{" "}
              وشروط الخدمة. البيانات محمية وفق نظام PDPL السعودي.
            </>
          ) : (
            <>
              I agree to the{" "}
              <a
                href="/en/privacy"
                className="text-[var(--dealix-deep-green)] underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                Privacy Policy
              </a>{" "}
              and Terms of Service. Data is protected under Saudi PDPL.
            </>
          )}
        </span>
      </label>

      {/* What happens after payment */}
      <details className="rounded-lg border border-border/60 p-3">
        <summary className="text-sm font-medium cursor-pointer">
          {isAr ? "ما الذي يحدث بعد الدفع؟" : "What happens after payment?"}
        </summary>
        <div className="mt-3 space-y-2 text-xs text-muted-foreground">
          {(isAr
            ? [
                "سيتواصل معك فريق Dealix خلال 24 ساعة لتأكيد البداية.",
                "ستحصل على رابط بوابة العميل لمتابعة Sprint.",
                "سيُراجع المؤسس كل خطوة قبل إرسالها إليك.",
                "لن يُرسَل أي شيء دون موافقة صريحة منك.",
              ]
            : [
                "The Dealix team will contact you within 24 hours to confirm the start.",
                "You will receive a customer portal link to follow your Sprint.",
                "The founder reviews every step before it is sent to you.",
                "Nothing is sent without your explicit approval.",
              ]
          ).map((line, i) => (
            <div key={i} className="flex gap-2">
              <span className="text-[var(--dealix-deep-green)] font-bold">{i + 1}.</span>
              <span>{line}</span>
            </div>
          ))}
        </div>
      </details>

      {/* Governance note */}
      <p className="text-xs text-muted-foreground border-t border-border/40 pt-3">
        {isAr
          ? "لن يُرسَل أي شيء دون مراجعة المؤسس — APPROVAL_FIRST"
          : "Nothing is sent without founder review — APPROVAL_FIRST"}
      </p>

      {error && <p className="text-red-600 text-xs">{error}</p>}

      <Button
        className="w-full bg-[var(--dealix-deep-green)] hover:bg-[var(--dealix-deep-green)]/90"
        disabled={busy || !email.trim() || !name.trim() || !pdplConsent}
        onClick={() => void pay()}
      >
        {busy
          ? isAr
            ? "جارٍ المعالجة…"
            : "Processing…"
          : isAr
          ? "ادفع عبر Moyasar"
          : "Pay via Moyasar"}
      </Button>
    </div>
  );
}
