"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function CheckoutPanel({ plan, planLabel, priceHint, isAr }: { plan: string; planLabel: string; priceHint: string; isAr: boolean }) {
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const pay = async () => {
    setBusy(true);
    try {
      const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${base}/api/v1/checkout`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ plan, email }) });
      const data = await res.json();
      if (data.payment_url) window.location.href = data.payment_url;
    } finally { setBusy(false); }
  };
  return (
    <div className="mt-4 space-y-2 rounded border p-3 text-sm">
      <p className="font-medium">{planLabel} — {priceHint}</p>
      <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@company.sa" />
      <Button className="w-full" disabled={busy || !email} onClick={pay}>{isAr ? "ادفع عبر Moyasar" : "Pay via Moyasar"}</Button>
    </div>
  );
}
