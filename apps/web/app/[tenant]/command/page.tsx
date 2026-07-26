"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import {
  authenticatedFetch,
  clearSession,
  parseApiError,
} from "../../../lib/runtime-api";

interface KPICard {
  label: string;
  label_ar: string;
  value: string | number;
  icon: string;
}

interface DashboardAction {
  id: string;
  label: string;
  label_ar?: string;
  href: string;
}

interface DashboardNotification {
  type: string;
  title: string;
  title_ar?: string;
  action?: {
    label: string;
    label_ar?: string;
    href: string;
  };
}

interface DashboardActivity {
  title: string;
  title_ar?: string;
  timestamp?: string | null;
}

interface DashboardData {
  tenant_name: string;
  plan_name: string;
  subscription_status: string;
  kpi_cards: KPICard[];
  quick_actions: DashboardAction[];
  recent_activity: DashboardActivity[];
  notifications: DashboardNotification[];
}

const subscriptionLabel = (status: string) => {
  if (status === "active") return "نشط";
  if (status === "trialing") return "تجريبي";
  return status || "غير معروف";
};

const subscriptionTone = (status: string) => {
  if (status === "active") return "bg-emerald-100 text-emerald-800 border-emerald-200";
  if (status === "trialing") return "bg-amber-100 text-amber-800 border-amber-200";
  return "bg-red-100 text-red-800 border-red-200";
};

export default function CompanyCommandPage() {
  const params = useParams();
  const router = useRouter();
  const tenant = String(params.tenant || "workspace");
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    const loadCommandState = async () => {
      try {
        const response = await authenticatedFetch("/api/v1/customer/dashboard/");
        if (response.status === 401 || response.status === 403) {
          clearSession();
          router.replace("/login");
          return;
        }
        if (!response.ok) throw new Error(await parseApiError(response));

        const payload: DashboardData = await response.json();
        if (active) setData(payload);
      } catch (err: unknown) {
        if (active) {
          setError(err instanceof Error ? err.message : "تعذر تحميل غرفة القيادة");
        }
      } finally {
        if (active) setLoading(false);
      }
    };

    void loadCommandState();
    return () => {
      active = false;
    };
  }, [router]);

  const commandState = useMemo(() => {
    if (!data) return null;

    const pendingDecisions = data.notifications.length;
    const availableMoves = data.quick_actions.length;
    const recentSignals = data.recent_activity.length;
    const needsAttention = pendingDecisions > 0 || data.subscription_status === "past_due";

    return {
      pendingDecisions,
      availableMoves,
      recentSignals,
      needsAttention,
      headline: needsAttention ? "توجد نقاط تحتاج قرارك" : "التشغيل مستقر ولا توجد قرارات عاجلة",
    };
  }, [data]);

  const workspaceHref = (path: string) =>
    `/${encodeURIComponent(tenant)}${path.startsWith("/") ? path : `/${path}`}`;

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center" dir="rtl">
        <div className="border border-slate-800 bg-slate-900 px-6 py-4 text-slate-200">
          جاري بناء صورة التشغيل الحالية...
        </div>
      </div>
    );
  }

  if (!data || !commandState) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4" dir="rtl">
        <div className="max-w-md border border-red-900 bg-red-950/40 p-6 text-center">
          <p className="mb-4 text-red-200">{error || "تعذر تحميل بيانات غرفة القيادة"}</p>
          <button
            type="button"
            onClick={() => router.replace("/login")}
            className="border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
          >
            العودة لتسجيل الدخول
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100" dir="rtl">
      <div className="mx-auto max-w-[1600px] px-4 py-4 md:px-6 lg:px-8">
        <header className="mb-4 border border-slate-800 bg-slate-900/80 p-4 md:p-5">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="mb-2 flex flex-wrap items-center gap-2 text-xs text-slate-400">
                <span>DEALIX COMPANY COMMAND</span>
                <span className="text-slate-700">/</span>
                <span>{tenant}</span>
              </div>
              <h1 className="text-2xl font-semibold tracking-tight text-white md:text-3xl">
                غرفة قيادة {data.tenant_name}
              </h1>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
                ما الذي يحدث الآن، هل يحتاج تدخلًا، وما القرار أو الحركة التالية؟
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <span className={`border px-3 py-1 text-xs font-semibold ${subscriptionTone(data.subscription_status)}`}>
                {subscriptionLabel(data.subscription_status)}
              </span>
              <span className="border border-slate-700 bg-slate-950 px-3 py-1 text-xs text-slate-300">
                الخطة: {data.plan_name}
              </span>
              <a
                href={workspaceHref("/dashboard")}
                className="border border-slate-700 bg-slate-900 px-3 py-1 text-xs font-semibold text-slate-200 hover:border-emerald-500 hover:text-emerald-300"
              >
                اللوحة المختصرة
              </a>
            </div>
          </div>
        </header>

        <section className="mb-4 grid gap-4 xl:grid-cols-[1.6fr_1fr]">
          <div className={`border p-5 ${commandState.needsAttention ? "border-amber-700 bg-amber-950/20" : "border-emerald-800 bg-emerald-950/20"}`}>
            <div className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
              <span className={`h-2 w-2 rounded-full ${commandState.needsAttention ? "bg-amber-400" : "bg-emerald-400"}`} />
              حالة المشغل
            </div>
            <h2 className="text-xl font-semibold text-white">{commandState.headline}</h2>
            <p className="mt-2 text-sm leading-6 text-slate-400">
              تم اشتقاق هذه الحالة من التنبيهات الحالية، حالة الاشتراك، والأعمال المتاحة في بيانات العميل الفعلية فقط.
            </p>
          </div>

          <div className="grid grid-cols-3 border border-slate-800 bg-slate-900/70">
            {[
              ["قرارات معلقة", commandState.pendingDecisions],
              ["حركات متاحة", commandState.availableMoves],
              ["إشارات حديثة", commandState.recentSignals],
            ].map(([label, value]) => (
              <div key={label} className="border-l border-slate-800 p-4 last:border-l-0">
                <div className="text-2xl font-semibold tabular-nums text-white">{value}</div>
                <div className="mt-1 text-xs text-slate-500">{label}</div>
              </div>
            ))}
          </div>
        </section>

        <section className="mb-4 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {data.kpi_cards.map((kpi) => (
            <article key={`${kpi.label}-${kpi.label_ar}`} className="border border-slate-800 bg-slate-900/70 p-4">
              <div className="mb-5 text-xs uppercase tracking-[0.16em] text-slate-500">
                {kpi.label}
              </div>
              <div className="text-3xl font-semibold tabular-nums text-white">{kpi.value}</div>
              <div className="mt-2 text-sm text-slate-400">{kpi.label_ar}</div>
            </article>
          ))}
        </section>

        <section className="grid gap-4 xl:grid-cols-[1.1fr_1fr_1fr]">
          <article className="border border-slate-800 bg-slate-900/70">
            <div className="border-b border-slate-800 px-4 py-3">
              <h2 className="font-semibold text-white">رادار المخاطر والقرارات</h2>
              <p className="mt-1 text-xs text-slate-500">العناصر التي تحتاج تدخلك قبل أن تصبح إجراءً خارجيًا.</p>
            </div>
            <div className="divide-y divide-slate-800">
              {data.notifications.length === 0 ? (
                <div className="p-5 text-sm text-slate-500">لا توجد تنبيهات معلقة في البيانات الحالية.</div>
              ) : (
                data.notifications.map((notification, index) => (
                  <div key={`${notification.type}-${index}`} className="p-4">
                    <div className="mb-2 flex items-center justify-between gap-3">
                      <span className="text-sm font-semibold text-slate-200">
                        {notification.title_ar || notification.title}
                      </span>
                      <span className={`border px-2 py-0.5 text-[11px] ${notification.type === "warning" ? "border-amber-700 text-amber-300" : "border-red-800 text-red-300"}`}>
                        {notification.type === "warning" ? "مراجعة" : "عالي"}
                      </span>
                    </div>
                    {notification.action && (
                      <a
                        href={workspaceHref(notification.action.href)}
                        className="text-xs font-semibold text-emerald-300 hover:text-emerald-200"
                      >
                        {notification.action.label_ar || notification.action.label}
                      </a>
                    )}
                  </div>
                ))
              )}
            </div>
          </article>

          <article className="border border-slate-800 bg-slate-900/70">
            <div className="border-b border-slate-800 px-4 py-3">
              <h2 className="font-semibold text-white">حركات التشغيل التالية</h2>
              <p className="mt-1 text-xs text-slate-500">اختصارات إلى مسارات موجودة، وليست إجراءات آلية.</p>
            </div>
            <div className="divide-y divide-slate-800">
              {data.quick_actions.length === 0 ? (
                <div className="p-5 text-sm text-slate-500">لا توجد حركات متاحة حاليًا.</div>
              ) : (
                data.quick_actions.map((action, index) => (
                  <a
                    key={action.id}
                    href={workspaceHref(action.href)}
                    className="group flex items-center justify-between gap-4 p-4 hover:bg-slate-800/60"
                  >
                    <div>
                      <div className="text-sm font-semibold text-slate-200 group-hover:text-white">
                        {action.label_ar || action.label}
                      </div>
                      <div className="mt-1 text-xs text-slate-500">خطوة تشغيل رقم {index + 1}</div>
                    </div>
                    <span className="text-emerald-400">←</span>
                  </a>
                ))
              )}
            </div>
          </article>

          <article className="border border-slate-800 bg-slate-900/70">
            <div className="border-b border-slate-800 px-4 py-3">
              <h2 className="font-semibold text-white">نبض النشاط</h2>
              <p className="mt-1 text-xs text-slate-500">آخر الأحداث التي أعادها مسار العميل الموثق.</p>
            </div>
            <div className="max-h-[420px] divide-y divide-slate-800 overflow-auto">
              {data.recent_activity.length === 0 ? (
                <div className="p-5 text-sm text-slate-500">لا توجد أحداث حديثة.</div>
              ) : (
                data.recent_activity.map((activity, index) => (
                  <div key={`${activity.title}-${index}`} className="p-4">
                    <div className="text-sm font-medium text-slate-200">
                      {activity.title_ar || activity.title}
                    </div>
                    <div className="mt-2 text-xs tabular-nums text-slate-600">
                      {activity.timestamp
                        ? new Date(activity.timestamp).toLocaleString("ar-SA")
                        : "لا يوجد وقت مسجل"}
                    </div>
                  </div>
                ))
              )}
            </div>
          </article>
        </section>

        <footer className="mt-4 flex flex-col gap-2 border border-slate-800 bg-slate-900/50 px-4 py-3 text-xs text-slate-500 md:flex-row md:items-center md:justify-between">
          <span>هذه الواجهة تقرأ فقط من مسار العميل الحالي ولا تنفذ إرسالًا أو دفعًا أو تغيير إنتاج.</span>
          <span>القرارات الخارجية تبقى خلف بوابة الموافقة.</span>
        </footer>
      </div>
    </div>
  );
}
