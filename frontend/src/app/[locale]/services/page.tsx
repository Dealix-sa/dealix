import Link from "next/link";
import { ServicesSprintPanelDynamic } from "@/components/services/ServicesSprintPanelDynamic";

interface ServicesHubProps {
  params: Promise<{ locale: string }>;
}

export default async function ServicesHubPage({ params }: ServicesHubProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  if (isAr) {
    return (
      <div className="min-h-screen bg-background grid-pattern">
        <div className="mx-auto max-w-4xl px-6 py-16 text-right" dir="rtl">
          <p className="text-sm font-medium text-muted-foreground">
            Dealix — AI Operating Partner
          </p>
          <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
            خطوط الخدمات الخمس
          </h1>
          <div className="mt-8 grid gap-4 sm:grid-cols-3">
            <div className="rounded-lg border border-primary/30 bg-card/60 p-4">
              <p className="text-xs text-muted-foreground">10-Lead Audit</p>
              <p className="mt-1 font-semibold">من 499 ر.س</p>
              <Link href={`/${locale}/risk-score`} className="mt-3 inline-block text-sm text-primary hover:underline">
                Risk Score
              </Link>
            </div>
            <div className="rounded-lg border border-border bg-card/40 p-4">
              <p className="text-xs text-muted-foreground">Agency Proof Pack</p>
              <p className="mt-1 font-semibold">من 1,500 ر.س</p>
              <Link href={`/${locale}/proof-pack`} className="mt-3 inline-block text-sm text-primary hover:underline">
                عيّنة Proof Pack
              </Link>
            </div>
            <div className="rounded-lg border border-border bg-card/40 p-4">
              <p className="text-xs text-muted-foreground">تشخيص تشغيلي Ops</p>
              <p className="mt-1 font-semibold">من 4,999 ر.س</p>
              <p className="mt-1 text-xs text-muted-foreground">R1 Sprint: من 499 ر.س</p>
              <Link href={`/${locale}/dealix-diagnostic`} className="mt-3 inline-block text-sm text-primary hover:underline">
                مسار 7 أيام
              </Link>
            </div>
          </div>
          <p className="mt-8 text-muted-foreground leading-relaxed">
            كل باب يربط تشغيل الشركة بنتائج واضحة، وليس بـ«ذكاء عام» بدون
            تسليم. <strong>المدخل التجاري الوحيد الآن:</strong>{" "}
            <Link
              href={`/${locale}/dealix-diagnostic`}
              className="text-primary font-medium hover:underline"
            >
              تشخيص ٧ أيام — Governed Revenue &amp; AI Ops
            </Link>
            . التفاصيل في{" "}
            <code className="rounded bg-muted px-1 py-0.5 text-foreground">
              docs/commercial/
            </code>
            .
          </p>

          <ul className="mt-10 space-y-6 text-base leading-relaxed">
            <li className="rounded-lg border border-border bg-card/40 p-5">
              <h2 className="text-lg font-semibold text-foreground">
                1) Grow Revenue — نمو الإيراد
              </h2>
              <p className="mt-2 text-muted-foreground">
                تنظيف وترتيب الحسابات، scoring، مسودات outreach آمنة،
                pipeline أوضح.
              </p>
              <Link
                href={`/${locale}/offer/lead-intelligence-sprint`}
                className="mt-3 inline-block text-sm font-medium text-primary hover:underline"
              >
                عرض Lead Intelligence Sprint
              </Link>
            </li>
            <li className="rounded-lg border border-border bg-card/40 p-5">
              <h2 className="text-lg font-semibold text-foreground">
                2) Serve Customers — خدمة العملاء
              </h2>
              <p className="mt-2 text-muted-foreground">
                تصنيف، مسودات رد، SLA، تقارير شكاوى — موافقة بشرية أولاً.
              </p>
              <p className="mt-2 text-xs text-muted-foreground">
                API: <code className="rounded bg-muted px-1">/api/v1/customer-inbox-v10</code> —{" "}
                <code className="rounded bg-muted px-1">GET /sla-policy</code>
              </p>
            </li>
            <li className="rounded-lg border border-border bg-card/40 p-5">
              <h2 className="text-lg font-semibold text-foreground">
                3) Automate Operations — أتمتة التشغيل
              </h2>
              <p className="mt-2 text-muted-foreground">
                workflow واحد متكرر مع مراجعة وتدقيق.
              </p>
            </li>
            <li className="rounded-lg border border-border bg-card/40 p-5">
              <h2 className="text-lg font-semibold text-foreground">
                4) Build Company Brain — المعرفة الموثقة
              </h2>
              <p className="mt-2 text-muted-foreground">
                إجابات بمصادر — بدون مصدر لا إجابة.
              </p>
            </li>
            <li className="rounded-lg border border-border bg-card/40 p-5">
              <h2 className="text-lg font-semibold text-foreground">
                5) Govern AI — الحوكمة والامتثال
              </h2>
              <p className="mt-2 text-muted-foreground">
                سياسات استخدام، موافقات، PDPL، سجلات تدقيق.
              </p>
            </li>
          </ul>

          <ServicesSprintPanelDynamic locale={locale} />

          <div className="mt-12">
            <Link
              href={`/${locale}/login`}
              className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90"
            >
              تسجيل الدخول
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background grid-pattern">
      <div className="mx-auto max-w-4xl px-6 py-16 text-left" dir="ltr">
        <p className="text-sm font-medium text-muted-foreground">
          Dealix — AI Operating Partner
        </p>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
          Five service lines
        </h1>
        <div className="mt-8 grid gap-4 sm:grid-cols-3">
          <div className="rounded-lg border border-primary/30 bg-card/60 p-4">
            <p className="text-xs text-muted-foreground">10-Lead Audit</p>
            <p className="mt-1 font-semibold">From 499 SAR</p>
            <Link href={`/${locale}/risk-score`} className="mt-3 inline-block text-sm text-primary hover:underline">
              Risk Score
            </Link>
          </div>
          <div className="rounded-lg border border-border bg-card/40 p-4">
            <p className="text-xs text-muted-foreground">Agency Proof Pack</p>
            <p className="mt-1 font-semibold">From 1,500 SAR</p>
            <Link href={`/${locale}/proof-pack`} className="mt-3 inline-block text-sm text-primary hover:underline">
              Sample Proof Pack
            </Link>
          </div>
            <div className="rounded-lg border border-border bg-card/40 p-4">
              <p className="text-xs text-muted-foreground">Ops diagnostic</p>
              <p className="mt-1 font-semibold">From 4,999 SAR</p>
              <p className="mt-1 text-xs text-muted-foreground">R1 Sprint: from 499 SAR</p>
              <Link href={`/${locale}/dealix-diagnostic`} className="mt-3 inline-block text-sm text-primary hover:underline">
                7-day path
              </Link>
            </div>
        </div>
        <p className="mt-8 text-muted-foreground leading-relaxed">
          Each line ties AI work to measurable delivery — not generic
          &quot;AI consulting&quot;. <strong>Primary commercial entry:</strong>{" "}
          <Link
            href={`/${locale}/dealix-diagnostic`}
            className="text-primary font-medium hover:underline"
          >
            7-Day Governed Revenue &amp; AI Ops Diagnostic
          </Link>
          . Full catalog:{" "}
          <code className="rounded bg-muted px-1 py-0.5 text-foreground">
            docs/commercial/
          </code>
          .
        </p>

        <ul className="mt-10 space-y-6 text-base leading-relaxed">
          <li className="rounded-lg border border-border bg-card/40 p-5">
            <h2 className="text-lg font-semibold text-foreground">
              1) Grow Revenue
            </h2>
            <p className="mt-2 text-muted-foreground">
              Clean accounts, scoring, safe outreach drafts, clearer
              pipeline.
            </p>
            <Link
              href={`/${locale}/offer/lead-intelligence-sprint`}
              className="mt-3 inline-block text-sm font-medium text-primary hover:underline"
            >
              Lead Intelligence Sprint offer
            </Link>
          </li>
          <li className="rounded-lg border border-border bg-card/40 p-5">
            <h2 className="text-lg font-semibold text-foreground">
              2) Serve Customers
            </h2>
            <p className="mt-2 text-muted-foreground">
              Classification, reply drafts, SLA, issue reports — human
              approval first.
            </p>
            <p className="mt-2 text-xs text-muted-foreground">
              API: <code className="rounded bg-muted px-1">/api/v1/customer-inbox-v10</code> —{" "}
              <code className="rounded bg-muted px-1">GET /sla-policy</code>
            </p>
          </li>
          <li className="rounded-lg border border-border bg-card/40 p-5">
            <h2 className="text-lg font-semibold text-foreground">
              3) Automate Operations
            </h2>
            <p className="mt-2 text-muted-foreground">
              One clear recurring workflow with review and audit.
            </p>
          </li>
          <li className="rounded-lg border border-border bg-card/40 p-5">
            <h2 className="text-lg font-semibold text-foreground">
              4) Build Company Brain
            </h2>
            <p className="mt-2 text-muted-foreground">
              Answers with citations — no source, no answer.
            </p>
          </li>
          <li className="rounded-lg border border-border bg-card/40 p-5">
            <h2 className="text-lg font-semibold text-foreground">
              5) Govern AI
            </h2>
            <p className="mt-2 text-muted-foreground">
              Usage policies, approvals, PDPL alignment, audit trails.
            </p>
          </li>
        </ul>

        <ServicesSprintPanelDynamic locale={locale} />

        <div className="mt-12">
          <Link
            href={`/${locale}/login`}
            className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90"
          >
            Log in
          </Link>
        </div>
      </div>
    </div>
  );
}
