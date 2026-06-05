import { Section } from "@/components/wave3/Section";
import { PrimaryCta } from "@/components/wave3/PrimaryCta";

const COMMITMENTS = [
  { ar: "موافقة بشرية قبل أي إجراء خارجي", en: "Human approval before any external action" },
  { ar: "لا إرسال تلقائي ولا واتساب بارد", en: "No auto-send, no cold WhatsApp" },
  { ar: "لا scraping ولا قوائم مشتراة", en: "No scraping, no purchased lists" },
  { ar: "لا تُستخدم بيانات العملاء لتدريب النماذج", en: "Customer data is never used to train models" },
  { ar: "لا دراسة حالة عامة بدون موافقة", en: "No public case study without approval" },
  { ar: "سجل ادعاءات يمنع الوعود المضمونة", en: "A claims register that blocks guaranteed promises" },
];

export function SecurityPage({ locale }: { locale: string }) {
  const isAr = locale === "ar";
  return (
    <div className={isAr ? "text-right" : "text-left"}>
      <h1 className="text-4xl font-bold font-display leading-tight">
        {isAr ? "الأمان والحوكمة" : "Security & Governance"}
      </h1>
      <p className="mt-4 text-lg text-muted-foreground leading-relaxed">
        {isAr
          ? "دييلكس مبني للسوق السعودي مع احترام الخصوصية والموافقة أولاً. الأمان ليس إضافة — هو طبقة أساسية."
          : "Dealix is built for the Saudi market with privacy respect and an approval-first design. Safety is not an add-on — it is a core layer."}
      </p>

      <Section eyebrow={isAr ? "التزاماتنا" : "Our commitments"} title={isAr ? "ما نلتزم به دائماً" : "What we always do"}>
        <ul className="grid gap-2 sm:grid-cols-2">
          {COMMITMENTS.map((c, i) => (
            <li key={i} className="rounded-lg border border-border px-4 py-3 text-sm text-muted-foreground">
              ✓ {isAr ? c.ar : c.en}
            </li>
          ))}
        </ul>
      </Section>

      <div className="mt-6">
        <PrimaryCta locale={locale} href="/dealix-diagnostic" labelAr="احجز تشخيصاً" labelEn="Book Diagnostic" />
      </div>
    </div>
  );
}
