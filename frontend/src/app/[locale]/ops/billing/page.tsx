"use client";

import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";

/* ─── Types ─────────────────────────────────────────────────────────── */

interface Invoice {
  id: string;
  client_name: string;
  client_email: string;
  amount_sar: number;
  offer_tier: string;
  description: string;
  status: "paid" | "pending" | "failed";
  payment_link: string | null;
  created_at: string;
}

interface BillingStats {
  total_invoiced_sar: number;
  paid_sar: number;
  pending_sar: number;
  failed_sar: number;
}

/* ─── Helpers ─────────────────────────────────────────────────────────*/

function formatSAR(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}K`;
  return n.toLocaleString();
}

const STATUS_STYLES: Record<string, string> = {
  paid: "bg-emerald-500/20 text-emerald-400",
  pending: "bg-amber-500/20 text-amber-400",
  failed: "bg-red-500/20 text-red-400",
};

const OFFER_TIERS = [
  { value: "free", label: "Free" },
  { value: "sprint_499", label: "499 SAR Sprint" },
  { value: "pack_1500", label: "1,500 SAR Pack" },
  { value: "managed_2999", label: "2,999 SAR Managed" },
  { value: "managed_4999", label: "4,999 SAR Managed+" },
  { value: "custom_ai", label: "Custom AI" },
];

/* ─── Page component ─────────────────────────────────────────────────*/

export default function BillingPage() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [stats, setStats] = useState<BillingStats>({
    total_invoiced_sar: 0,
    paid_sar: 0,
    pending_sar: 0,
    failed_sar: 0,
  });
  const [invoices, setInvoices] = useState<Invoice[]>([]);

  /* Form state */
  const [form, setForm] = useState({
    client_name: "",
    client_email: "",
    amount_sar: "",
    offer_tier: "sprint_499",
    description: "",
  });

  /* UI state */
  const [generating, setGenerating] = useState(false);
  const [generatedLink, setGeneratedLink] = useState<string | null>(null);
  const [generatedId, setGeneratedId] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [simulating, setSimulating] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  /* Load data */
  const loadData = async () => {
    try {
      const [statsRes, invRes] = await Promise.all([
        fetch("/api/v1/billing/stats"),
        fetch("/api/v1/billing/invoices?limit=50"),
      ]);
      if (statsRes.ok) setStats(await statsRes.json());
      if (invRes.ok) {
        const d = await invRes.json();
        setInvoices(d.items ?? []);
      }
    } catch {
      /* silent */
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  function set(key: string, value: string) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  /* Generate payment link */
  async function handleGenerateLink() {
    setError("");
    setSuccess("");
    setGeneratedLink(null);
    setGeneratedId(null);
    if (!form.client_name.trim()) {
      setError(isAr ? "أدخل اسم العميل" : "Enter client name");
      return;
    }
    if (!form.client_email.trim() || !form.client_email.includes("@")) {
      setError(isAr ? "أدخل بريداً إلكترونياً صحيحاً" : "Enter a valid email");
      return;
    }
    if (!form.amount_sar || Number(form.amount_sar) <= 0) {
      setError(isAr ? "أدخل المبلغ" : "Enter the amount");
      return;
    }
    setGenerating(true);
    try {
      const res = await fetch("/api/v1/billing/create-link", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          client_name: form.client_name.trim(),
          client_email: form.client_email.trim(),
          amount_sar: Number(form.amount_sar),
          offer_tier: form.offer_tier,
          description: form.description.trim(),
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setGeneratedLink(data.payment_link);
      setGeneratedId(data.invoice_id ?? data.id ?? null);
      setSuccess(isAr ? "تم إنشاء رابط الدفع بنجاح." : "Payment link generated successfully.");
      await loadData();
    } catch {
      setError(isAr ? "فشل إنشاء الرابط — تحقق من الاتصال." : "Failed to generate link — check connection.");
    } finally {
      setGenerating(false);
    }
  }

  /* Copy link */
  async function handleCopy() {
    if (!generatedLink) return;
    await navigator.clipboard.writeText(generatedLink);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  /* Simulate payment */
  async function handleSimulate(id: string) {
    setSimulating(id);
    setError("");
    setSuccess("");
    try {
      const res = await fetch(`/api/v1/billing/simulate-success/${id}`, { method: "POST" });
      if (!res.ok) throw new Error(await res.text());
      setSuccess(isAr ? "تمت محاكاة الدفع بنجاح." : "Payment simulated successfully.");
      await loadData();
    } catch {
      setError(isAr ? "فشلت محاكاة الدفع." : "Payment simulation failed.");
    } finally {
      setSimulating(null);
    }
  }

  return (
    <AppLayout
      title={isAr ? "بوابة الفواتير" : "Billing Gateway"}
      subtitle={isAr ? "إنشاء الفواتير وإدارة المدفوعات" : "Invoice management & payment links"}
    >
      <div className="space-y-8" dir={isAr ? "rtl" : "ltr"}>
        {/* ─── Stats ────────────────────────────────────────────────────── */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            {
              label: isAr ? "إجمالي الفواتير (ريال)" : "Total Invoiced (SAR)",
              value: `${formatSAR(stats.total_invoiced_sar)} SAR`,
              color: "from-violet-500/20 to-transparent",
            },
            {
              label: isAr ? "مدفوع (ريال)" : "Paid (SAR)",
              value: `${formatSAR(stats.paid_sar)} SAR`,
              color: "from-emerald-500/20 to-transparent",
            },
            {
              label: isAr ? "معلق (ريال)" : "Pending (SAR)",
              value: `${formatSAR(stats.pending_sar)} SAR`,
              color: "from-amber-500/20 to-transparent",
            },
            {
              label: isAr ? "فاشل (ريال)" : "Failed (SAR)",
              value: `${formatSAR(stats.failed_sar)} SAR`,
              color: "from-red-500/20 to-transparent",
            },
          ].map(({ label, value, color }) => (
            <div
              key={label}
              className={`bg-gradient-to-br ${color} bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-6`}
            >
              <p className="text-xs text-muted-foreground uppercase tracking-wide">{label}</p>
              <p className="text-2xl font-bold mt-1 tabular-nums">{value}</p>
            </div>
          ))}
        </div>

        {/* ─── Create Invoice Form ─────────────────────────────────────── */}
        <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-6 space-y-5">
          <h2 className="text-lg font-semibold">
            {isAr ? "إنشاء فاتورة جديدة" : "Create Invoice"}
          </h2>

          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-1">
              <label className="text-xs text-muted-foreground">
                {isAr ? "اسم العميل" : "Client Name"}
              </label>
              <input
                type="text"
                value={form.client_name}
                onChange={(e) => set("client_name", e.target.value)}
                placeholder={isAr ? "مثال: شركة البناء الحديث" : "e.g. Modern Build Co."}
                className="w-full rounded-lg bg-background/40 border border-white/10 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted-foreground/50"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs text-muted-foreground">
                {isAr ? "البريد الإلكتروني" : "Email"}
              </label>
              <input
                type="email"
                value={form.client_email}
                onChange={(e) => set("client_email", e.target.value)}
                placeholder="client@company.sa"
                className="w-full rounded-lg bg-background/40 border border-white/10 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted-foreground/50"
                dir="ltr"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs text-muted-foreground">
                {isAr ? "المبلغ (ريال)" : "Amount (SAR)"}
              </label>
              <input
                type="number"
                min="0"
                value={form.amount_sar}
                onChange={(e) => set("amount_sar", e.target.value)}
                placeholder="1500"
                className="w-full rounded-lg bg-background/40 border border-white/10 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted-foreground/50"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs text-muted-foreground">
                {isAr ? "باقة العرض" : "Offer Tier"}
              </label>
              <select
                value={form.offer_tier}
                onChange={(e) => set("offer_tier", e.target.value)}
                className="w-full rounded-lg bg-background/40 border border-white/10 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
              >
                {OFFER_TIERS.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-1 sm:col-span-2">
              <label className="text-xs text-muted-foreground">
                {isAr ? "الوصف (اختياري)" : "Description (optional)"}
              </label>
              <textarea
                rows={2}
                value={form.description}
                onChange={(e) => set("description", e.target.value)}
                placeholder={isAr ? "تفاصيل الخدمة أو الاشتراك…" : "Service or subscription details…"}
                className="w-full rounded-lg bg-background/40 border border-white/10 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted-foreground/50 resize-none"
              />
            </div>
          </div>

          {error && <p className="text-sm text-destructive">{error}</p>}
          {success && <p className="text-sm text-emerald-400">{success}</p>}

          <button
            onClick={handleGenerateLink}
            disabled={generating}
            className="rounded-xl bg-primary px-6 py-2.5 text-sm font-semibold text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-colors"
          >
            {generating
              ? isAr ? "جارٍ الإنشاء…" : "Generating…"
              : isAr ? "إنشاء رابط الدفع" : "Generate Payment Link"}
          </button>

          {/* Link result */}
          {generatedLink && (
            <div className="bg-background/30 border border-emerald-500/30 rounded-xl p-4 flex flex-wrap items-center gap-3">
              <span
                className="text-sm text-emerald-400 break-all flex-1 font-mono"
                dir="ltr"
              >
                {generatedLink}
              </span>
              <div className="flex gap-2 shrink-0">
                <button
                  onClick={handleCopy}
                  className="rounded-lg border border-white/10 px-3 py-1.5 text-xs font-medium hover:bg-white/5 transition-colors"
                >
                  {copied ? (isAr ? "تم النسخ ✓" : "Copied ✓") : isAr ? "نسخ" : "Copy"}
                </button>
                {generatedId && (
                  <button
                    onClick={() => handleSimulate(generatedId)}
                    disabled={simulating === generatedId}
                    className="rounded-lg bg-amber-500/20 border border-amber-500/30 text-amber-400 px-3 py-1.5 text-xs font-medium hover:bg-amber-500/30 disabled:opacity-50 transition-colors"
                  >
                    {simulating === generatedId
                      ? isAr ? "جارٍ المحاكاة…" : "Simulating…"
                      : isAr ? "محاكاة الدفع" : "Simulate Payment"}
                  </button>
                )}
              </div>
            </div>
          )}
        </div>

        {/* ─── Invoices Table ───────────────────────────────────────────── */}
        <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-semibold">
            {isAr ? "الفواتير" : "Invoices"}
          </h2>
          <div className="overflow-x-auto rounded-xl border border-white/10">
            <table className="w-full text-sm">
              <thead className="bg-white/5">
                <tr>
                  {[
                    isAr ? "العميل" : "Client",
                    isAr ? "الباقة" : "Tier",
                    isAr ? "المبلغ (ريال)" : "Amount (SAR)",
                    isAr ? "الحالة" : "Status",
                    isAr ? "التاريخ" : "Date",
                    isAr ? "إجراء" : "Action",
                  ].map((h) => (
                    <th key={h} className="p-3 text-start text-xs text-muted-foreground font-medium">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {invoices.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="p-6 text-center text-muted-foreground text-sm">
                      {isAr ? "لا توجد فواتير بعد." : "No invoices yet."}
                    </td>
                  </tr>
                ) : (
                  invoices.map((inv) => (
                    <tr key={inv.id} className="border-t border-white/5 hover:bg-white/5 transition-colors">
                      <td className="p-3">
                        <p className="font-medium">{inv.client_name}</p>
                        <p className="text-xs text-muted-foreground">{inv.client_email}</p>
                      </td>
                      <td className="p-3 text-muted-foreground text-xs">{inv.offer_tier}</td>
                      <td className="p-3 tabular-nums font-medium">{formatSAR(inv.amount_sar)} SAR</td>
                      <td className="p-3">
                        <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_STYLES[inv.status] ?? "bg-white/10 text-muted-foreground"}`}>
                          {isAr
                            ? inv.status === "paid" ? "مدفوع" : inv.status === "pending" ? "معلق" : "فاشل"
                            : inv.status.charAt(0).toUpperCase() + inv.status.slice(1)}
                        </span>
                      </td>
                      <td className="p-3 text-xs text-muted-foreground">
                        {new Date(inv.created_at).toLocaleDateString()}
                      </td>
                      <td className="p-3">
                        {inv.status === "pending" && (
                          <button
                            onClick={() => handleSimulate(inv.id)}
                            disabled={simulating === inv.id}
                            className="rounded-lg bg-amber-500/20 border border-amber-500/30 text-amber-400 px-2.5 py-1 text-xs font-medium hover:bg-amber-500/30 disabled:opacity-50 transition-colors"
                          >
                            {simulating === inv.id
                              ? isAr ? "جارٍ…" : "Running…"
                              : isAr ? "محاكاة" : "Simulate"}
                          </button>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
