"use client";

import { useLocale } from "next-intl";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function PartnerApplyForm() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [form, setForm] = useState({
    name: "",
    email: "",
    company: "",
    partner_type: "referral",
    message: "",
    consent: false,
  });
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.consent) {
      setStatus(isAr ? "الموافقة مطلوبة." : "Consent required.");
      return;
    }
    setBusy(true);
    setStatus("");
    const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    try {
      const res = await fetch(`${base}/api/v1/public/partner-apply`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "failed");
      setStatus(
        isAr
          ? `تم الاستلام — ${data.lead_id}. ${data.policy_ar || ""}`
          : `Received — ${data.lead_id}`,
      );
    } catch {
      setStatus(isAr ? "تعذّر الإرسال." : "Submit failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="max-w-md mx-auto space-y-4" dir={isAr ? "rtl" : "ltr"}>
      <h1 className="text-2xl font-bold">{isAr ? "برنامج الشركاء" : "Partner program"}</h1>
      <p className="text-sm text-muted-foreground">
        {isAr
          ? "Dealix تشخّص · الشريك ينفّذ · العميل يحصل على إثبات."
          : "Dealix diagnoses · partner implements · client gets proof."}
      </p>
      {(
        [
          ["name", isAr ? "الاسم" : "Name"],
          ["email", isAr ? "البريد" : "Email"],
          ["company", isAr ? "الشركة" : "Company"],
        ] as const
      ).map(([k, label]) => (
        <div key={k}>
          <Label htmlFor={k}>{label}</Label>
          <Input
            id={k}
            required={k !== "company"}
            value={form[k]}
            onChange={(e) => setForm((f) => ({ ...f, [k]: e.target.value }))}
          />
        </div>
      ))}
      <div>
        <Label htmlFor="partner_type">{isAr ? "نوع الشراكة" : "Partner type"}</Label>
        <select
          id="partner_type"
          className="w-full mt-1 rounded-md border border-input bg-background px-3 py-2 text-sm"
          value={form.partner_type}
          onChange={(e) => setForm((f) => ({ ...f, partner_type: e.target.value }))}
        >
          <option value="referral">Referral</option>
          <option value="implementation">Implementation</option>
          <option value="co_sell">Co-sell pilot</option>
        </select>
      </div>
      <div>
        <Label htmlFor="message">{isAr ? "رسالة" : "Message"}</Label>
        <Input
          id="message"
          value={form.message}
          onChange={(e) => setForm((f) => ({ ...f, message: e.target.value }))}
        />
      </div>
      <label className="flex gap-2 text-sm items-center">
        <input
          type="checkbox"
          checked={form.consent}
          onChange={(e) => setForm((f) => ({ ...f, consent: e.target.checked }))}
        />
        {isAr ? "أوافق على التواصل والمراجعة اليدوية" : "I consent to manual review contact"}
      </label>
      <Button type="submit" disabled={busy} className="w-full">
        {isAr ? "إرسال" : "Submit"}
      </Button>
      {status && <p className="text-sm">{status}</p>}
    </form>
  );
}
