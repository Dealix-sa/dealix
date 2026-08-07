"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

interface Plan {
  id: string;
  name_ar: string;
  name_en: string;
  slug: string;
  price_sar_monthly: number;
  features: Record<string, boolean>;
}

interface Subscription {
  id: string;
  plan_id: string;
  billing_cycle: string;
  status: string;
  trial_ends_at: string | null;
  current_period_end: string;
  seat_count: number;
  mrr_sar: number;
}

interface Invoice {
  id: string;
  invoice_number: string;
  status: string;
  total_sar: number;
  due_date: string | null;
  paid_at: string | null;
  created_at: string;
}

export default function BillingSettingsPage() {
  const params = useParams();
  const tenant = params.tenant as string;
  const [plans, setPlans] = useState<Plan[]>([]);
  const [sub, setSub] = useState<Subscription | null>(null);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [upgrading, setUpgrading] = useState(false);

  useEffect(() => {
    Promise.all([
      fetch("/api/v1/billing/plans").then((r) => r.json()),
      fetch("/api/v1/billing/subscription", { headers: { "x-tenant-id": tenant } }).then((r) =>
        r.ok ? r.json() : null
      ),
      fetch("/api/v1/billing/invoices", { headers: { "x-tenant-id": tenant } }).then((r) =>
        r.ok ? r.json() : []
      ),
    ]).then(([p, s, i]) => {
      setPlans(p);
      setSub(s);
      setInvoices(i);
      setLoading(false);
    });
  }, [tenant]);

  const handleUpgrade = async (planSlug: string) => {
    setUpgrading(true);
    try {
      const res = await fetch("/api/v1/billing/upgrade", {
        method: "POST",
        headers: { "Content-Type": "application/json", "x-tenant-id": tenant },
        body: JSON.stringify({ plan_slug: planSlug }),
      });
      if (res.ok) {
        const updated = await res.json();
        setSub(updated);
        alert("تمت الترقية بنجاح!");
      }
    } catch (err) {
      console.error(err);
    } finally {
      setUpgrading(false);
    }
  };

  const handleCancel = async () => {
    if (!confirm("هل أنت متأكد من إلغاء الاشتراك؟")) return;
    try {
      const res = await fetch("/api/v1/billing/cancel", {
        method: "POST",
        headers: { "Content-Type": "application/json", "x-tenant-id": tenant },
        body: JSON.stringify({ immediate: false }),
      });
      if (res.ok) {
        alert("سيتم إلغاء الاشتراك في نهاية الفترة");
      }
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-emerald-600 text-xl font-semibold">جاري التحميل...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50" dir="rtl">
      <div className="max-w-5xl mx-auto p-8">
        <h1 className="text-2xl font-bold text-slate-900 mb-8">الفوترة والاشتراك</h1>

        {/* Current Subscription */}
        {sub && (
          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 mb-8">
            <h2 className="text-lg font-bold text-slate-900 mb-4">الاشتراك الحالي</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="p-4 bg-slate-50 rounded-lg">
                <p className="text-sm text-slate-500">الخطة</p>
                <p className="text-lg font-semibold text-slate-900">
                  {plans.find((p) => p.id === sub.plan_id)?.name_ar || sub.plan_id}
                </p>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg">
                <p className="text-sm text-slate-500">الحالة</p>
                <p className="text-lg font-semibold text-slate-900">
                  {sub.status === "active" ? "نشط" : sub.status === "trialing" ? "تجريبي" : sub.status}
                </p>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg">
                <p className="text-sm text-slate-500">التجديد القادم</p>
                <p className="text-lg font-semibold text-slate-900">
                  {new Date(sub.current_period_end).toLocaleDateString("ar-SA")}
                </p>
              </div>
            </div>
            <button
              onClick={handleCancel}
              className="text-red-600 text-sm font-medium hover:underline"
            >
              إلغاء الاشتراك
            </button>
          </div>
        )}

        {/* Plans */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 mb-8">
          <h2 className="text-lg font-bold text-slate-900 mb-4">الخطط المتاحة</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {plans.map((plan) => (
              <div
                key={plan.id}
                className={`p-4 border-2 rounded-xl ${
                  sub?.plan_id === plan.id
                    ? "border-emerald-500 bg-emerald-50"
                    : "border-slate-200"
                }`}
              >
                <p className="font-bold text-slate-900">{plan.name_ar}</p>
                <p className="text-2xl font-bold text-emerald-600 mt-2">
                  {plan.price_sar_monthly === 0
                    ? "مجاني"
                    : `${plan.price_sar_monthly} ر.س`}
                </p>
                <p className="text-xs text-slate-400 mb-4">/شهر</p>
                <div className="space-y-1 text-sm text-slate-600 mb-4">
                  {Object.entries(plan.features || {}).map(([key, enabled]) => (
                    <div key={key} className="flex items-center gap-2">
                      <span className={enabled ? "text-emerald-500" : "text-slate-300"}>
                        {enabled ? "✓" : "—"}
                      </span>
                      <span className={enabled ? "" : "text-slate-400 line-through"}>
                        {key}
                      </span>
                    </div>
                  ))}
                </div>
                {sub?.plan_id !== plan.id && (
                  <button
                    onClick={() => handleUpgrade(plan.slug)}
                    disabled={upgrading}
                    className="w-full bg-emerald-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-emerald-700 transition disabled:opacity-50"
                  >
                    {upgrading ? "جاري..." : "ترقية"}
                  </button>
                )}
                {sub?.plan_id === plan.id && (
                  <div className="w-full bg-slate-100 text-slate-500 py-2 rounded-lg text-sm font-medium text-center">
                    الخطة الحالية
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Invoices */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
          <h2 className="text-lg font-bold text-slate-900 mb-4">الفواتير</h2>
          {invoices.length === 0 ? (
            <p className="text-slate-400">لا توجد فواتير</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-100">
                    <th className="text-right py-2 text-slate-500">رقم الفاتورة</th>
                    <th className="text-right py-2 text-slate-500">المبلغ</th>
                    <th className="text-right py-2 text-slate-500">الحالة</th>
                    <th className="text-right py-2 text-slate-500">تاريخ الاستحقاق</th>
                  </tr>
                </thead>
                <tbody>
                  {invoices.map((inv) => (
                    <tr key={inv.id} className="border-b border-slate-50">
                      <td className="py-3 font-medium">{inv.invoice_number}</td>
                      <td className="py-3">{inv.total_sar} ر.س</td>
                      <td className="py-3">
                        <span
                          className={`px-2 py-0.5 rounded text-xs font-medium ${
                            inv.status === "paid"
                              ? "bg-emerald-100 text-emerald-700"
                              : inv.status === "open"
                              ? "bg-amber-100 text-amber-700"
                              : "bg-slate-100 text-slate-600"
                          }`}
                        >
                          {inv.status === "paid"
                            ? "مدفوعة"
                            : inv.status === "open"
                            ? "مفتوحة"
                            : inv.status}
                        </span>
                      </td>
                      <td className="py-3">
                        {inv.due_date
                          ? new Date(inv.due_date).toLocaleDateString("ar-SA")
                          : "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
