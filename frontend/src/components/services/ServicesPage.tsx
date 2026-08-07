"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Button } from "@/components/ui/button";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

export function ServicesPage() {
  const isAr = useLocale() === "ar";
  const base = isAr ? "/ar" : "/en";

  return (
    <PublicGtmShell>
      <div className="mx-auto max-w-5xl space-y-10 px-4 py-14">
        <section className="space-y-5 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[#C9974B]">
            Revenue Command Pilot · 30 days
          </p>
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            {isAr ? "مسار تجاري واحد يبدأ بالاكتشاف" : "One commercial path, starting with discovery"}
          </h1>
          <p className="mx-auto max-w-2xl text-lg text-muted-foreground">
            {isAr
              ? "نشخّص مسار الإيراد، نختار نقطة تشغيل واحدة، ثم نعرض نطاق Pilot لمدة 30 يومًا. السعر يحدد في quote موثق بعد فهم الحالة."
              : "We diagnose the revenue workflow, choose one operating point, then propose a 30-day Pilot. Price is set in a documented quote after discovery."}
          </p>
        </section>

        <section className="rounded-2xl border border-border bg-card p-8">
          <h2 className="text-2xl font-bold">
            {isAr ? "ما الذي يشمله نطاق المراجعة؟" : "What does the review scope cover?"}
          </h2>
          <ul className="mt-5 grid gap-3 text-sm leading-6 md:grid-cols-2">
            {(isAr
              ? [
                  "مسار واحد ومالك قرار واضح",
                  "baseline ومقياس تشغيل متفق عليه",
                  "مسودات خاضعة للموافقة فقط",
                  "أقل بيانات وصلاحيات ممكنة",
                  "مراجعة أسبوعية للأدلة والقرارات",
                  "قرار نهاية المدة: توقف، تعديل، أو توسع موثق",
                ]
              : [
                  "One workflow and a clear decision owner",
                  "An agreed baseline and operating measure",
                  "Approval-gated drafts only",
                  "Minimum data and permissions",
                  "Weekly evidence and decision review",
                  "End decision: stop, adjust, or document expansion",
                ]).map((item) => (
              <li key={item} className="rounded-lg bg-muted/50 px-4 py-3">{item}</li>
            ))}
          </ul>
        </section>

        <section className="rounded-2xl bg-[#0A1628] px-8 py-10 text-center text-white">
          <h2 className="text-2xl font-bold">
            {isAr ? "لا ضمان مبيعات ولا ربط تلقائي" : "No sales guarantee or automatic integration"}
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-white/70">
            {isAr
              ? "نقيس التشغيل والأدلة داخل النطاق؛ الإيراد والمبيعات خارج الالتزام."
              : "We measure operations and evidence within scope; revenue and sales remain outside the commitment."}
          </p>
          <Button asChild size="lg" className="mt-6 bg-[#C9974B] font-bold text-[#0A1628] hover:bg-[#b8863a]">
            <Link href={`${base}/dealix-diagnostic`}>
              {isAr ? "احجز جلسة الاكتشاف" : "Book discovery"}
            </Link>
          </Button>
        </section>
      </div>
    </PublicGtmShell>
  );
}
