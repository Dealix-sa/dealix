"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

interface KPICard {
  label: string;
  label_ar: string;
  value: string | number;
  icon: string;
}

interface DashboardData {
  tenant_name: string;
  plan_name: string;
  subscription_status: string;
  kpi_cards: KPICard[];
  quick_actions: any[];
  recent_activity: any[];
  notifications: any[];
}

export default function DashboardPage() {
  const params = useParams();
  const tenant = params.tenant as string;
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/v1/customer/dashboard/", {
      headers: { "x-tenant-id": tenant },
    })
      .then((r) => r.json())
      .then((d) => {
        setData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [tenant]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-emerald-600 text-xl font-semibold">جاري التحميل...</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-red-500">فشل تحميل البيانات</div>
      </div>
    );
  }

  const iconMap: Record<string, string> = {
    users: "👥",
    briefcase: "💼",
    "trending-up": "📈",
    "check-circle": "✅",
    package: "📦",
  };

  return (
    <div className="min-h-screen bg-slate-50" dir="rtl">
      {/* Sidebar + Main */}
      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-white border-l border-slate-200 min-h-screen p-6 hidden lg:block">
          <div className="text-2xl font-bold text-emerald-600 mb-8">Dealix</div>
          <nav className="space-y-2">
            {[
              { label: "الرئيسية", href: `/${tenant}/dashboard` },
              { label: "CRM", href: `/${tenant}/crm` },
              { label: "المشاريع", href: `/${tenant}/projects` },
              { label: "الدعم", href: `/${tenant}/support` },
              { label: "المستندات", href: `/${tenant}/documents` },
              { label: "الإعدادات", href: `/${tenant}/settings/billing` },
            ].map((item) => (
              <a
                key={item.label}
                href={item.href}
                className="block px-4 py-2 rounded-lg text-slate-600 hover:bg-slate-100 hover:text-emerald-600 transition"
              >
                {item.label}
              </a>
            ))}
          </nav>
        </aside>

        {/* Main */}
        <main className="flex-1 p-8">
          <header className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">
                مرحباً، {data.tenant_name}
              </h1>
              <p className="text-slate-500 text-sm">
                الخطة: {data.plan_name} —{" "}
                <span
                  className={`px-2 py-0.5 rounded text-xs font-medium ${
                    data.subscription_status === "active"
                      ? "bg-emerald-100 text-emerald-700"
                      : data.subscription_status === "trialing"
                      ? "bg-amber-100 text-amber-700"
                      : "bg-red-100 text-red-700"
                  }`}
                >
                  {data.subscription_status === "active"
                    ? "نشط"
                    : data.subscription_status === "trialing"
                    ? "تجريبي"
                    : data.subscription_status}
                </span>
              </p>
            </div>
          </header>

          {/* Notifications */}
          {data.notifications.length > 0 && (
            <div className="mb-6 space-y-3">
              {data.notifications.map((n, i) => (
                <div
                  key={i}
                  className={`p-4 rounded-xl border-r-4 ${
                    n.type === "warning"
                      ? "bg-amber-50 border-amber-500"
                      : "bg-red-50 border-red-500"
                  }`}
                >
                  <p className="font-semibold text-slate-800">{n.title_ar || n.title}</p>
                  {n.action && (
                    <a
                      href={n.action.href}
                      className="text-emerald-600 text-sm font-medium mt-1 inline-block hover:underline"
                    >
                      {n.action.label_ar || n.action.label} →
                    </a>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">
            {data.kpi_cards.map((kpi, i) => (
              <div
                key={i}
                className="bg-white p-6 rounded-xl shadow-sm border border-slate-100"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-2xl">{iconMap[kpi.icon] || "📊"}</span>
                </div>
                <p className="text-slate-500 text-sm">{kpi.label_ar}</p>
                <p className="text-2xl font-bold text-slate-900">{kpi.value}</p>
              </div>
            ))}
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 mb-8">
            <h2 className="text-lg font-bold text-slate-900 mb-4">إجراءات سريعة</h2>
            <div className="flex flex-wrap gap-3">
              {data.quick_actions.map((action) => (
                <a
                  key={action.id}
                  href={action.href}
                  className="px-4 py-2 bg-emerald-50 text-emerald-700 rounded-lg font-medium hover:bg-emerald-100 transition"
                >
                  {action.label_ar || action.label}
                </a>
              ))}
            </div>
          </div>

          {/* Recent Activity */}
          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
            <h2 className="text-lg font-bold text-slate-900 mb-4">آخر النشاطات</h2>
            {data.recent_activity.length === 0 ? (
              <p className="text-slate-400">لا توجد نشاطات حديثة</p>
            ) : (
              <div className="space-y-3">
                {data.recent_activity.map((act, i) => (
                  <div
                    key={i}
                    className="flex items-center justify-between p-3 bg-slate-50 rounded-lg"
                  >
                    <div>
                      <p className="font-medium text-slate-800">
                        {act.title_ar || act.title}
                      </p>
                      <p className="text-xs text-slate-400">
                        {act.timestamp
                          ? new Date(act.timestamp).toLocaleDateString("ar-SA")
                          : ""}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
