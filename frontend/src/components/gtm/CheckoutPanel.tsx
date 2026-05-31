"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function CheckoutPanel({
  plan,
  planLabel,
  priceHint,
  isAr,
  initialEmail = "",
  initialReferralCode = "",
}: {
  plan: string;
  planLabel: string;
  priceHint: string;
  isAr: boolean;
  initialEmail?: string;
  initialReferralCode?: string;
}) {
  const [email, setEmail] = useState(initialEmail);
  const [referralCode, setReferralCode] = useState(initialReferralCode);
  const [showReferral, setShowReferral] = useState(!!initialReferralCode);
  const [busy, setBusy] = useState(false);
  const [referralApplied, setReferralApplied] = useState<boolean | null>(null);

  const pay = async () => {
    if (!name.trim() || !email.trim()) return;
    setBusy(true);
    setError("");
    try {
      const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const body: Record<string, string> = { plan, email };
      if (referralCode.trim()) body.referral_code = referralCode.trim().toUpperCase();
      const res = await fetch(`${base}/api/v1/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json() as { payment_url?: string; referral_applied?: boolean };
      if (data.referral_applied !== undefined) setReferralApplied(data.referral_applied);
      if (data.payment_url) window.location.href = data.payment_url;
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mt-4 space-y-2 rounded border p-3 text-sm">
      <p className="font-medium">{planLabel} — {priceHint}</p>
      <Input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@company.sa"
      />
      {showReferral ? (
        <div className="space-y-1">
          <Input
            value={referralCode}
            onChange={(e) => setReferralCode(e.target.value.toUpperCase())}
            placeholder={isAr ? "كود الإحالة — مثال: REF-AB12CD34" : "Referral code — e.g. REF-AB12CD34"}
            className="font-mono text-xs"
          />
          {referralApplied === true && (
            <p className="text-xs text-green-600">
              {isAr ? "✓ كود الإحالة مفعَّل — خصم ٥٠٪ الشهر الأول" : "✓ Referral applied — 50% off first month"}
            </p>
          )}
          {referralApplied === false && referralCode && (
            <p className="text-xs text-muted-foreground">
              {isAr ? "كود غير صالح أو منتهي الصلاحية" : "Code invalid or expired"}
            </p>
          )}
        </div>
      ) : (
        <button
          type="button"
          className="text-xs text-muted-foreground underline"
          onClick={() => setShowReferral(true)}
        >
          {isAr ? "لديك كود إحالة؟" : "Have a referral code?"}
        </button>
      )}
      <Button className="w-full" disabled={busy || !email} onClick={pay}>
        {isAr ? "ادفع عبر Moyasar" : "Pay via Moyasar"}
      </Button>
    </div>
  );
}
