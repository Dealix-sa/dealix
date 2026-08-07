"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Button } from "@/components/ui/button";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

export function PricingPage() {
  const isAr = useLocale() === "ar";
  const base = isAr ? "/ar" : "/en";

  return (
    <PublicGtmShell>
      <div className="mx-auto max-w-5xl space-y-10 px-4 py-14">
        <section className="space-y-5 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[#C9974B]">
            Revenue Command Pilot
          </p>
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            {isAr ? "السعر والنطاق بعد جلسة الاكتشاف" : "Scope and price follow discovery"}
          </h1>
          <p className="mx-auto max-w-2xl text-lg text-muted-foreground">
            {isAr
              ? "نبدأ بتشخيص مختصر ومحدود، ثم نجهّز نطاق Pilot لمدة 30 يومًا وعرض سعر موثق للمراجعة. لا سعر ثابت، لا خصم، ولا وعد بنتيجة إيراد."
              : "We start with a bounded diagnostic, then prepare a 30-day Pilot scope and documented quote for review. No fixed public price, discount, or revenue guarantee."}
          </p>
        </section>

        <section className="grid gap-4 md:grid-cols-3">
          {[
            {
              n: "1",
              ar: "جلسة اكتشاف لفهم المسار الحالي والقيود.",
              en: "Discovery to understand the current workflow and constraints.",
            },
            {
              n: "2",
              ar: "نطاق تشغيل واحد، baseline واضح، وأقل بيانات وصلاحيات ممكنة.",
              en: "One operating scope, a clear baseline, and minimum data and permissions.",
            },
            {
              n: "3",
              ar: "عرض موثق يحدد السعر والنطاق وشروط التسليم قبل أي دفع.",
              en: "A documented quote defines price, scope, and delivery terms before payment.",
            },
          ].map((step) => (
            <article key={step.n} className="rounded-xl border border-border bg-card p-6">
              <span className="text-2xl font-bold text-[#C9974B]">{step.n}</span>
              <p className="mt-3 text-sm leading-6">{isAr ? step.ar : step.en}</p>
            </article>
          ))}
        </section>

        <section className="rounded-2xl bg-[#0A1628] px-8 py-10 text-center text-white">
          <h2 className="text-2xl font-bold">
            {isAr ? "ابدأ بالتشخيص، بدون ربط أنظمة أو إرسال خارجي" : "Start with discovery, without integrations or external sends"}
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-white/70">
            {isAr
              ? "أي ربط لاحق يبدأ بأقل بيانات وصلاحيات ممكنة وبعد موافقة صريحة."
              : "Any later integration starts with the minimum data and permissions, after explicit approval."}
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
