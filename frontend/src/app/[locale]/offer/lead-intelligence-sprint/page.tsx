"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useState } from "react";
import { CheckoutPanel } from "@/components/gtm/CheckoutPanel";

const DELIVERABLES_AR = [
  { icon: "🗺", title: "خريطة تسرّب الإيراد", desc: "نحدد أين يضيع الإيراد في كل مرحلة من pipeline" },
  { icon: "📊", title: "تقييم CRM والبيانات", desc: "جودة البيانات، التكرار، الفجوات في المعلومات" },
  { icon: "🤖", title: "خريطة AI Governance", desc: "أي استخدامات AI غير محكومة وما المخاطر" },
  { icon: "🧾", title: "ZATCA Readiness Check", desc: "هل أنت جاهز لـ Wave 24 قبل يونيو 2026؟" },
  { icon: "🧠", title: "Company Brain v1", desc: "لقطة كاملة للشركة — السياق، الهيكل، الأولويات" },
  { icon: "✅", title: "أعلى 3 قرارات بدليل", desc: "قرارات قابلة للتنفيذ فوراً مع Proof Pack موثَّق" },
  { icon: "📄", title: "Proof Pack PDF ثنائي اللغة", desc: "وثيقة كاملة تُشارَك مع الإدارة أو المستثمرين" },
  { icon: "🎯", title: "توصية الخطوة التالية", desc: "هل تحتاج Retainer أم هذا كافٍ؟ قرار شفاف" },
];

const DELIVERABLES_EN = [
  { icon: "🗺", title: "Revenue leakage map", desc: "Pinpoints where revenue is lost at every pipeline stage" },
  { icon: "📊", title: "CRM & data assessment", desc: "Data quality, duplication, information gaps" },
  { icon: "🤖", title: "AI Governance map", desc: "Which AI uses are ungoverned and what the risks are" },
  { icon: "🧾", title: "ZATCA Readiness Check", desc: "Are you ready for Wave 24 before June 2026?" },
  { icon: "🧠", title: "Company Brain v1", desc: "Full company snapshot — context, structure, priorities" },
  { icon: "✅", title: "Top 3 governed decisions", desc: "Immediately executable actions with documented Proof Pack" },
  { icon: "📄", title: "Bilingual Proof Pack PDF", desc: "Complete document shareable with management or investors" },
  { icon: "🎯", title: "Next step recommendation", desc: "Do you need a Retainer or is this enough? Transparent decision" },
];

const TIMELINE_AR = [
  { day: "اليوم 1-2", title: "جمع البيانات", desc: "استلام مصادر CRM، pipeline، AI، الفواتير" },
  { day: "اليوم 3-4", title: "التحليل والخرائط", desc: "تسرّب الإيراد، فجوات governance، ZATCA check" },
  { day: "اليوم 5-6", title: "توثيق الأدلة", desc: "بناء evidence trail لكل قرار في Proof Pack" },
  { day: "اليوم 7", title: "التسليم والمراجعة", desc: "Proof Pack PDF + مكالمة مراجعة 30 دقيقة" },
];

const TIMELINE_EN = [
  { day: "Day 1-2", title: "Data collection", desc: "Receive CRM, pipeline, AI, and invoice sources" },
  { day: "Day 3-4", title: "Analysis & mapping", desc: "Revenue leakage, governance gaps, ZATCA check" },
  { day: "Day 5-6", title: "Evidence documentation", desc: "Build evidence trail for every Proof Pack decision" },
  { day: "Day 7", title: "Delivery & review", desc: "Proof Pack PDF + 30-minute review call" },
];

const FAQS_AR = [
  { q: "من يحتاج هذا Sprint؟", a: "أي شركة B2B سعودية تتجاوز 500,000 ريال إيراداً أو تستخدم AI أو تحتاج جهوزية ZATCA Wave 24 قبل يونيو 2026." },
  { q: "ما المطلوب مني في 7 أيام؟", a: "ساعة واحدة فقط في اليوم الأول لتوجيه البيانات. الباقي نتولاه بالكامل. اليوم السابع: مكالمة 30 دقيقة للمراجعة." },
  { q: "هل النتيجة ضمانة أرباح؟", a: "لا. Dealix يقدّم أدلة وقرارات موثَّقة — ليس وعوداً بإيراد. كل نتيجة مرتبطة بمستوى دليل واضح (L0-L5)." },
  { q: "ماذا بعد الـ Sprint؟", a: "لديك ثلاثة خيارات: تنفّذ بنفسك (مجاناً)، أو Retainer شهري 2,999 ريال، أو Proof Pack أعمق 1,500 ريال. لا ضغط." },
  { q: "هل يمكن الاسترداد؟", a: "إذا سلّمنا أقل من 6 من 8 مخرجات، ندفع كامل المبلغ. الشفافية في العقد." },
];

const FAQS_EN = [
  { q: "Who needs this Sprint?", a: "Any Saudi B2B company with 500K+ SAR revenue, AI usage, or needing ZATCA Wave 24 readiness before June 2026." },
  { q: "What's required from me in 7 days?", a: "One hour on Day 1 to point us to your data. We handle everything else. Day 7: a 30-minute review call." },
  { q: "Does this guarantee revenue uplift?", a: "No. Dealix delivers documented evidence and decisions — not revenue promises. Every output is tied to a clear evidence level (L0-L5)." },
  { q: "What happens after the Sprint?", a: "Three choices: implement yourself (free), monthly Retainer at 2,999 SAR, or deeper Proof Pack at 1,500 SAR. No pressure." },
  { q: "Is there a refund policy?", a: "If we deliver fewer than 6 of 8 outputs, full refund. Transparency is in the contract." },
];

export default function SprintOfferPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const deliverables = isAr ? DELIVERABLES_AR : DELIVERABLES_EN;
  const timeline = isAr ? TIMELINE_AR : TIMELINE_EN;
  const faqs = isAr ? FAQS_AR : FAQS_EN;
  const [openFaq, setOpenFaq] = useState<number | null>(null);
  const [showCheckout, setShowCheckout] = useState(false);

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>

      {/* Nav */}
      <header className="sticky top-0 z-20 border-b border-border/60 bg-background/95 backdrop-blur">
        <div className="mx-auto max-w-4xl px-6 py-3 flex items-center justify-between">
          <Link href={`/${locale}`} className="font-bold text-lg tracking-tight" style={{ color: "#001F3F" }}>
            Dealix
          </Link>
          <div className="flex items-center gap-3">
            <Link href={`/${locale}/services`} className="text-sm text-muted-foreground hover:text-foreground hidden sm:block">
              {isAr ? "الخدمات" : "Services"}
            </Link>
            <button
              onClick={() => setShowCheckout(true)}
              className="rounded-lg px-4 py-2 text-sm font-semibold text-white transition-colors"
              style={{ backgroundColor: "#D4AF37", color: "#001F3F" }}
            >
              {isAr ? "ابدأ — 499 ريال" : "Start — SAR 499"}
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-6 py-12 space-y-16">

        {/* Hero */}
        <section className="text-center space-y-4">
          <div className="inline-flex items-center gap-2 rounded-full border border-red-500/30 bg-red-50/50 dark:bg-red-950/20 px-4 py-1.5 text-sm font-medium text-red-700 dark:text-red-400">
            <span className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />
            {isAr ? "ZATCA Wave 24 — 31 يوم متبق" : "ZATCA Wave 24 — 31 days remaining"}
          </div>
          <h1 className="text-4xl font-black md:text-5xl" style={{ color: "#001F3F" }}>
            {isAr ? "Sprint 7 أيام" : "7-Day Sprint"}
          </h1>
          <p className="text-5xl font-black" style={{ color: "#D4AF37" }}>
            499 {isAr ? "ريال" : "SAR"}
          </p>
          <p className="text-lg text-muted-foreground max-w-xl mx-auto leading-relaxed">
            {isAr
              ? "اكشف أين يضيع إيراد شركتك — Proof Pack بدليل حقيقي، يشمل ZATCA readiness، في 7 أيام."
              : "Uncover where your company's revenue is lost — a Proof Pack with real evidence, including ZATCA readiness, in 7 days."}
          </p>
          <div className="flex flex-wrap justify-center gap-3 pt-2">
            <button
              onClick={() => setShowCheckout(true)}
              className="rounded-xl px-8 py-3.5 text-base font-bold shadow-lg transition-all hover:-translate-y-0.5 hover:shadow-xl"
              style={{ backgroundColor: "#001F3F", color: "white" }}
            >
              {isAr ? "ابدأ Sprint الآن ←" : "Start Sprint Now →"}
            </button>
            <Link
              href={`/${locale}/dealix-diagnostic`}
              className="rounded-xl border border-border bg-card px-8 py-3.5 text-base font-medium hover:bg-muted/30 transition-colors"
            >
              {isAr ? "تشخيص مجاني أولاً" : "Free diagnostic first"}
            </Link>
          </div>
          <p className="text-xs text-muted-foreground">
            {isAr ? "لا عقد طويل · لا أتمتة · PDPL compliant" : "No long contract · No automation · PDPL compliant"}
          </p>
        </section>

        {/* Trust bar */}
        <div className="flex flex-wrap justify-center gap-x-8 gap-y-3 text-xs text-muted-foreground border-y border-border/40 py-4">
          {(isAr ? [
            "✓ لا إرسال تلقائي",
            "✓ موافقة بشرية لكل إجراء",
            "✓ PDPL محكوم",
            "✓ Audit Trail كامل",
            "✓ Soft deletes — لا حذف مادي",
          ] : [
            "✓ No automated outbound",
            "✓ Human approval for every action",
            "✓ PDPL governed",
            "✓ Full Audit Trail",
            "✓ Soft deletes — no physical deletion",
          ]).map((t) => <span key={t}>{t}</span>)}
        </div>

        {/* Deliverables */}
        <section>
          <h2 className="text-2xl font-bold mb-2 text-center">
            {isAr ? "ما تستلمه في 7 أيام" : "What You Receive in 7 Days"}
          </h2>
          <p className="text-center text-sm text-muted-foreground mb-8">
            {isAr ? "8 مخرجات موثَّقة — كل واحدة مرتبطة بمستوى دليل من L0 إلى L5" : "8 documented outputs — each tied to an evidence level L0 to L5"}
          </p>
          <div className="grid gap-4 sm:grid-cols-2">
            {deliverables.map((d, i) => (
              <div key={i} className="flex gap-4 rounded-xl border border-border/60 bg-card/50 p-4 hover:border-border transition-colors">
                <span className="text-2xl flex-shrink-0">{d.icon}</span>
                <div>
                  <p className="font-semibold text-sm">{d.title}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{d.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Timeline */}
        <section>
          <h2 className="text-2xl font-bold mb-8 text-center">
            {isAr ? "خط زمني يوم بيوم" : "Day-by-Day Timeline"}
          </h2>
          <div className="relative">
            <div className="absolute top-5 bottom-5 w-px bg-gradient-to-b from-[#D4AF37] to-transparent" style={{ left: isAr ? "auto" : "1.25rem", right: isAr ? "1.25rem" : "auto" }} />
            <div className="space-y-6">
              {timeline.map((t, i) => (
                <div key={i} className={`flex gap-4 ${isAr ? "flex-row-reverse" : ""}`}>
                  <div className="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center font-bold text-xs text-white z-10 relative" style={{ backgroundColor: "#D4AF37", color: "#001F3F" }}>
                    {i + 1}
                  </div>
                  <div className="flex-1 rounded-xl border border-border/50 bg-card/50 px-4 py-3">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-bold" style={{ color: "#D4AF37" }}>{t.day}</span>
                    </div>
                    <p className="font-semibold text-sm">{t.title}</p>
                    <p className="text-xs text-muted-foreground mt-0.5">{t.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Comparison */}
        <section className="rounded-2xl border border-border/60 bg-card/30 p-6 overflow-x-auto">
          <h2 className="text-xl font-bold mb-6 text-center">
            {isAr ? "مقارنة الخيارات" : "Compare your options"}
          </h2>
          <table className="w-full text-sm min-w-[400px]">
            <thead>
              <tr>
                <th className="pb-3 text-start font-medium text-muted-foreground">{isAr ? "الميزة" : "Feature"}</th>
                <th className="pb-3 text-center font-medium text-muted-foreground">{isAr ? "بمفردك" : "DIY"}</th>
                <th className="pb-3 text-center font-bold rounded-t-lg" style={{ color: "#001F3F", background: "rgba(212,175,55,0.1)" }}>Sprint 499</th>
                <th className="pb-3 text-center font-medium text-muted-foreground">{isAr ? "بدون شيء" : "Do nothing"}</th>
              </tr>
            </thead>
            <tbody>
              {(isAr ? [
                ["خريطة تسرّب الإيراد", "أسابيع", "✓ 7 أيام", "✗"],
                ["ZATCA Readiness", "غير موثوق", "✓ محكوم", "✗ خطر غرامة"],
                ["Proof Pack للإدارة", "صعب", "✓ PDF جاهز", "✗"],
                ["AI Governance map", "غير متاح", "✓ مضمّن", "✗"],
                ["تكلفة", "وقت + خطأ", "499 ريال", "غرامة ZATCA"],
              ] : [
                ["Revenue leakage map", "Weeks", "✓ 7 days", "✗"],
                ["ZATCA Readiness", "Unreliable", "✓ Governed", "✗ Fine risk"],
                ["Proof Pack for mgmt", "Hard", "✓ PDF ready", "✗"],
                ["AI Governance map", "Not available", "✓ Included", "✗"],
                ["Cost", "Time + errors", "SAR 499", "ZATCA fine"],
              ]).map(([feature, diy, sprint, nothing]) => (
                <tr key={feature} className="border-t border-border/30">
                  <td className="py-2.5 font-medium text-xs">{feature}</td>
                  <td className="py-2.5 text-center text-xs text-muted-foreground">{diy}</td>
                  <td className="py-2.5 text-center text-xs font-semibold" style={{ background: "rgba(212,175,55,0.05)", color: "#10b981" }}>{sprint}</td>
                  <td className="py-2.5 text-center text-xs text-red-500">{nothing}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        {/* Checkout CTA */}
        <section className="rounded-2xl text-white p-8 text-center space-y-4" style={{ background: "linear-gradient(135deg, #001F3F 0%, #0a2040 100%)" }}>
          <h2 className="text-2xl font-bold">
            {isAr ? "ابدأ Sprint الآن" : "Start Your Sprint Now"}
          </h2>
          <p className="text-white/70 text-sm">
            {isAr ? "31 يوم فقط قبل موعد ZATCA Wave 24 — احجز مكانك اليوم" : "Only 31 days before ZATCA Wave 24 deadline — reserve your spot today"}
          </p>
          <p className="text-4xl font-black" style={{ color: "#D4AF37" }}>
            499 {isAr ? "ريال" : "SAR"}
          </p>
          {showCheckout ? (
            <div className="max-w-sm mx-auto mt-4 rounded-xl bg-white/10 p-4">
              <CheckoutPanel
                plan="sprint_499"
                planLabel={isAr ? "Sprint 7 أيام" : "7-Day Sprint"}
                priceHint={isAr ? "499 ريال" : "SAR 499"}
                isAr={isAr}
              />
            </div>
          ) : (
            <div className="flex flex-wrap justify-center gap-3">
              <button
                onClick={() => setShowCheckout(true)}
                className="rounded-xl px-8 py-3.5 text-base font-bold transition-all hover:-translate-y-0.5"
                style={{ backgroundColor: "#D4AF37", color: "#001F3F" }}
              >
                {isAr ? "ادفع 499 ريال وابدأ ←" : "Pay SAR 499 & Start →"}
              </button>
              <Link
                href={`/${locale}/dealix-diagnostic`}
                className="rounded-xl border border-white/20 bg-white/10 px-8 py-3.5 text-base font-medium text-white hover:bg-white/20 transition-colors"
              >
                {isAr ? "أسئلة أولاً" : "Questions first"}
              </Link>
            </div>
          )}
        </section>

        {/* FAQs */}
        <section>
          <h2 className="text-xl font-bold mb-6 text-center">
            {isAr ? "أسئلة شائعة" : "Frequently Asked Questions"}
          </h2>
          <div className="space-y-2">
            {faqs.map((f, i) => (
              <div key={i} className="rounded-xl border border-border/60 bg-card/50 overflow-hidden">
                <button
                  onClick={() => setOpenFaq(openFaq === i ? null : i)}
                  className={`w-full flex items-center justify-between px-5 py-4 text-sm font-medium text-${isAr ? "right" : "left"} hover:bg-muted/20 transition-colors`}
                >
                  <span>{f.q}</span>
                  <span className="flex-shrink-0 ms-3 text-muted-foreground">{openFaq === i ? "−" : "+"}</span>
                </button>
                {openFaq === i && (
                  <div className="px-5 pb-4 text-sm text-muted-foreground leading-relaxed">{f.a}</div>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* Non-negotiables footer */}
        <div className="rounded-xl border border-border/40 bg-muted/20 p-4 text-xs text-muted-foreground space-y-1.5">
          <p className="font-semibold text-foreground text-sm">{isAr ? "المبادئ غير القابلة للتنازل" : "Non-negotiable principles"}</p>
          {(isAr ? [
            "لا إرسال WhatsApp أو LinkedIn آلي لأي عميل محتمل",
            "لا اقتناء قوائم contacts أو بيانات",
            "كل إجراء حرج يمر عبر Approval Center أولاً",
            "الأسعار بالريال السعودي دائماً — لا overclaim",
            "Proof Pack لا يُشارَك قبل موافقتك الصريحة",
          ] : [
            "No automated WhatsApp or LinkedIn to any prospect",
            "No purchasing contact lists or data",
            "Every critical action goes through Approval Center first",
            "Prices always in SAR — no overclaim",
            "Proof Pack not shared without your explicit consent",
          ]).map((p) => (
            <div key={p} className="flex items-center gap-2">
              <span className="text-emerald-500 flex-shrink-0">✓</span>
              <span>{p}</span>
            </div>
          ))}
        </div>

      </main>
    </div>
  );
}
