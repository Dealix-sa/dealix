import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { LayerCard } from "@/components/ai-stack/LayerCard";
import { RunDemoForm } from "@/components/ai-stack/RunDemoForm";
import { fetchStackStatus } from "@/lib/aiStackClient";

type PageProps = { params: Promise<{ locale: string }> };

export const dynamic = "force-dynamic";

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const ar = locale === "ar";
  return {
    title: ar
      ? "ستاك الذكاء الصناعي — Dealix"
      : "Dealix AI Stack — L1..L11",
    description: ar
      ? "الـ 11 طبقة من ستاك الدليل: من جواز المصدر إلى التحسين الذاتي"
      : "Dealix's eleven-layer AI Stack — from Source Passport to Self-Evolving",
  };
}

const COPY = {
  ar: {
    hero_title: "ستاك الذكاء الصناعي في Dealix",
    hero_subtitle:
      "إحدى عشرة طبقة منضبطة من جواز المصدر إلى التحسين الذاتي — كل قرار محكوم وموثّق",
    health_title: "حالة الطبقات الـ 11",
    health_healthy: "كل الطبقات تعمل",
    health_degraded: "هناك طبقة تحتاج مراجعة",
    snapshot_at: "آخر فحص",
    demo_title: "جرّب التشخيص المجاني",
    demo_subtitle:
      "املأ النموذج التالي لتشغيل الستاك الكامل على عميل وهمي — يستغرق أقل من ثانية، ولا يخزّن بيانات شخصية",
    gates_title: "الضمانات الصارمة",
  },
  en: {
    hero_title: "Dealix AI Stack",
    hero_subtitle:
      "Eleven disciplined layers from Source Passport to Self-Evolving — every decision governed and audited",
    health_title: "Eleven-layer health snapshot",
    health_healthy: "All layers healthy",
    health_degraded: "One or more layers need attention",
    snapshot_at: "Snapshot at",
    demo_title: "Try the free diagnostic",
    demo_subtitle:
      "Fill the form below to run the full stack against a dummy customer — sub-second response, no PII stored",
    gates_title: "Hard gates",
  },
};

const GATES_LABELS_AR: Record<string, string> = {
  no_live_send: "لا إرسال مباشر",
  no_live_charge: "لا تحصيل دفع مباشر",
  no_invented_kpis: "لا KPIs مخترعة",
  no_revenue_before_invoice_paid: "لا إيراد قبل invoice_paid",
  source_passport_required: "جواز المصدر إلزامي",
  bilingual_required: "ثنائي اللغة (AR + EN) إلزامي",
  self_evolving_shadow_only: "التحسين الذاتي يعمل بوضع الظل فقط",
};

export default async function AIStackPage({ params }: PageProps) {
  const { locale } = await params;
  if (locale !== "ar" && locale !== "en") {
    notFound();
  }
  const isAr = locale === "ar";
  const copy = COPY[isAr ? "ar" : "en"];

  let status: Awaited<ReturnType<typeof fetchStackStatus>> | null = null;
  let statusError: string | null = null;
  try {
    status = await fetchStackStatus();
  } catch (err) {
    statusError = (err as Error).message;
  }

  return (
    <main className="container mx-auto px-4 py-10 sm:px-6 lg:px-8">
      <header className="mx-auto max-w-3xl text-center">
        <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
          {copy.hero_title}
        </h1>
        <p className="mt-3 text-lg text-muted-foreground">
          {copy.hero_subtitle}
        </p>
      </header>

      <section className="mx-auto mt-12 max-w-6xl">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-xl font-semibold">{copy.health_title}</h2>
          {status ? (
            <span
              className={`rounded-full px-3 py-1 text-xs font-semibold ${
                status.overall_healthy
                  ? "bg-emerald-500/10 text-emerald-300"
                  : "bg-rose-500/10 text-rose-300"
              }`}
            >
              {status.overall_healthy
                ? copy.health_healthy
                : copy.health_degraded}
            </span>
          ) : null}
        </div>

        {statusError ? (
          <div className="rounded-md border border-rose-500/30 bg-rose-500/5 p-4 text-sm text-rose-300">
            {statusError}
          </div>
        ) : null}

        {status ? (
          <>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {status.layers.map((layer) => (
                <LayerCard
                  key={layer.layer}
                  layer={layer}
                  locale={isAr ? "ar" : "en"}
                />
              ))}
            </div>
            <div className="mt-4 text-right text-xs text-muted-foreground">
              {copy.snapshot_at}: {status.snapshot_at}
            </div>
          </>
        ) : null}
      </section>

      {status ? (
        <section className="mx-auto mt-10 max-w-6xl">
          <h2 className="mb-4 text-xl font-semibold">{copy.gates_title}</h2>
          <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-4">
            {Object.entries(status.hard_gates).map(([gate, enabled]) => (
              <div
                key={gate}
                className={`rounded-md border px-3 py-2 text-sm ${
                  enabled
                    ? "border-emerald-500/30 bg-emerald-500/5"
                    : "border-rose-500/30 bg-rose-500/5"
                }`}
              >
                <span className="mr-2 font-mono text-xs">
                  {enabled ? "✓" : "✗"}
                </span>
                {isAr ? (GATES_LABELS_AR[gate] ?? gate) : gate}
              </div>
            ))}
          </div>
        </section>
      ) : null}

      <section className="mx-auto mt-16 max-w-3xl">
        <div className="mb-6 text-center">
          <h2 className="text-2xl font-bold">{copy.demo_title}</h2>
          <p className="mt-2 text-sm text-muted-foreground">
            {copy.demo_subtitle}
          </p>
        </div>
        <RunDemoForm locale={isAr ? "ar" : "en"} />
      </section>
    </main>
  );
}
