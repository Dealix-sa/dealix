"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Button } from "@/components/ui/button";

export function PricingPlans() {
  const isAr = useLocale() === "ar";
  const locale = isAr ? "ar" : "en";

  return (
    <section className="mx-auto max-w-4xl space-y-8 px-4 py-12">
      <div className="text-center">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[#C9974B]">
          Revenue Command Pilot · 30 days
        </p>
        <h1 className="mt-3 text-4xl font-bold">
          {isAr ? "Quote موثق بعد discovery" : "Documented quote after discovery"}
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-muted-foreground">
          {isAr
            ? "لا توجد باقة مدفوعة عامة أو checkout حي. نحدد نطاقًا واحدًا بعد التشخيص، ثم نوثق السعر وشروط التسليم قبل أي دفع."
            : "There is no public paid package or live checkout. We define one scope after discovery, then document price and delivery terms before any payment."}
        </p>
      </div>

      <div className="rounded-2xl border border-border bg-card p-8">
        <h2 className="text-2xl font-bold">
          {isAr ? "تسلسل الاعتماد" : "Approval sequence"}
        </h2>
        <ol className="mt-5 space-y-3 text-sm leading-6">
          <li>{isAr ? "1. تشخيص مختصر ومحدود." : "1. Bounded diagnostic."}</li>
          <li>{isAr ? "2. نطاق Pilot واحد لمدة 30 يومًا." : "2. One 30-day Pilot scope."}</li>
          <li>{isAr ? "3. Quote موثق للمراجعة والموافقة." : "3. Documented quote for review and approval."}</li>
          <li>{isAr ? "4. لا دفع أو ربط قبل اكتمال الاعتمادات." : "4. No payment or integration before approvals are complete."}</li>
        </ol>
        <Button asChild size="lg" className="mt-7 bg-[#C9974B] font-bold text-[#0A1628] hover:bg-[#b8863a]">
          <Link href={`/${locale}/dealix-diagnostic`}>
            {isAr ? "احجز جلسة الاكتشاف" : "Book discovery"}
          </Link>
        </Button>
      </div>
    </section>
  );
}
