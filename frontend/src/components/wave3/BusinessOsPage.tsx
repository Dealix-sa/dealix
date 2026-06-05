import { Section } from "@/components/wave3/Section";
import { PrimaryCta } from "@/components/wave3/PrimaryCta";

const NOT_LIST = {
  ar: ["CRM", "شات بوت", "بوت واتساب", "وكالة تسويق", "أداة ذكاء اصطناعي عامة", "مجرد محرك استهداف"],
  en: ["a CRM", "a chatbot", "a WhatsApp bot", "a marketing agency", "a generic AI tool", "just a targeting engine"],
};

export function BusinessOsPage({ locale }: { locale: string }) {
  const isAr = locale === "ar";
  const notList = isAr ? NOT_LIST.ar : NOT_LIST.en;
  return (
    <div className={isAr ? "text-right" : "text-left"}>
      <h1 className="text-4xl font-bold font-display leading-tight">
        {isAr ? "Business OS — صورة تشغيل واحدة" : "Business OS — one operating picture"}
      </h1>
      <p className="mt-4 text-lg text-muted-foreground leading-relaxed">
        {isAr
          ? "نحوّل ما بداخل أدواتك إلى صورة قرار: أين تتعطل الفرص، ما الدليل، ما يحتاج موافقة، وما الخطوة التالية."
          : "We turn what's inside your tools into a decision picture: where opportunities stall, what proof exists, what needs approval, and what's next."}
      </p>

      <Section eyebrow={isAr ? "الوضوح" : "Clarity"} title={isAr ? "دييلكس ليس…" : "Dealix is NOT…"}>
        <div className="flex flex-wrap gap-2">
          {notList.map((n, i) => (
            <span key={i} className="rounded-full border border-border px-3 py-1 text-sm text-muted-foreground line-through">
              {n}
            </span>
          ))}
        </div>
        <p className="mt-4 text-muted-foreground">
          {isAr
            ? "دييلكس نظام تشغيل أعمال بالذكاء الاصطناعي، سعودي أولاً — بموافقة بشرية لكل إجراء خارجي."
            : "Dealix is a Saudi-first AI Business Operating System — with human approval for every external action."}
        </p>
      </Section>

      <Section eyebrow={isAr ? "آمن بالتصميم" : "Safe by design"} title={isAr ? "موافقة أولاً" : "Approval-first"}>
        <p className="text-muted-foreground leading-relaxed">
          {isAr
            ? "لا إرسال تلقائي، ولا واتساب بارد، ولا scraping. نجهّز مسودات قابلة للمراجعة وأنت تقرّر."
            : "No auto-send, no cold WhatsApp, no scraping. We prepare review-ready drafts and you decide."}
        </p>
      </Section>

      <div className="mt-6">
        <PrimaryCta locale={locale} href="/dealix-diagnostic" labelAr="احجز تشخيصاً" labelEn="Book Diagnostic" />
      </div>
    </div>
  );
}
