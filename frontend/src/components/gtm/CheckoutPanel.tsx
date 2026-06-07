"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

/**
 * Public self-serve checkout. Posts to the unauthenticated
 * `POST /api/v1/checkout` (Moyasar hosted invoice) — NO admin key required.
 * `plan` is a canonical service id from frontend/src/content/pricing.ts.
 */
export function CheckoutPanel({
  plan,
  planLabel,
  priceHint,
  isAr,
  customerName = "",
  leadId,
}: {
  plan: string;
  planLabel: string;
  priceHint: string;
  isAr: boolean;
  customerName?: string;
  leadId?: string;
}) {
  const [email, setEmail] = useState("");
  const [name, setName] = useState(customerName);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const pay = async () => {
    if (!email.trim()) return;
    setBusy(true);
    setError("");
    try {
      const res = await api.createCheckout({
        plan,
        email: email.trim(),
        ...(leadId ? { lead_id: leadId } : {}),
      });
      const data = res.data;
      if (data?.payment_url) {
        window.location.href = data.payment_url;
      } else {
        setError(data?.detail || (isAr ? "حدث خطأ — حاول لاحقاً" : "Error — try again"));
      }
    } catch (err: unknown) {
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || "";
      setError(
        detail === "payment_provider_error"
          ? isAr
            ? "تعذّر إنشاء فاتورة الدفع — تأكد من إعداد Moyasar أو حاول لاحقاً."
            : "Could not create the payment invoice — check Moyasar setup or try later."
          : isAr
            ? "تعذّر الاتصال بالخادم"
            : "Could not reach server",
      );
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mt-4 space-y-2 rounded border p-3 text-sm" dir={isAr ? "rtl" : "ltr"}>
      <p className="font-medium">
        {planLabel} — {priceHint}
      </p>
      <Input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder={isAr ? "اسمك أو اسم الشركة (اختياري)" : "Your name or company (optional)"}
      />
      <Input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@company.sa"
        required
      />
      {error && <p className="text-red-600 text-xs">{error}</p>}
      <Button className="w-full" disabled={busy || !email.trim()} onClick={pay}>
        {busy
          ? isAr
            ? "جارٍ المعالجة…"
            : "Processing…"
          : isAr
            ? "ادفع عبر Moyasar"
            : "Pay via Moyasar"}
      </Button>
      <p className="text-[11px] text-muted-foreground">
        {isAr
          ? "دفع آمن عبر Moyasar. تصلك فاتورة ZATCA بعد الدفع."
          : "Secure payment via Moyasar. A ZATCA invoice follows payment."}
      </p>
    </div>
  );
}
