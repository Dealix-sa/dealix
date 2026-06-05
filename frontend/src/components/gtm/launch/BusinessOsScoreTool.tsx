"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { Button } from "@/components/ui/button";
import { useBi, StatusPill, type Bi } from "@/components/gtm/launch/kit";

// ---------------------------------------------------------------------------
// Business OS Score — a free, illustrative self-assessment. Runs entirely in
// the browser. No data is sent anywhere. The score is ESTIMATED, never a
// verified or guaranteed result. Routes to a single next step.
// ---------------------------------------------------------------------------

type Dimension = {
  key: string;
  label: Bi;
  question: Bi;
};

const DIMENSIONS: Dimension[] = [
  { key: "visibility", label: { ar: "الرؤية", en: "Visibility" }, question: { ar: "هل لديك صورة واحدة موحّدة لما يحدث في شركتك الآن؟", en: "Do you have one unified picture of what's happening in your company right now?" } },
  { key: "priority", label: { ar: "الأولويات", en: "Prioritization" }, question: { ar: "هل تُبنى أولوياتك على دليل وبيانات، لا على الانطباع؟", en: "Are your priorities built on evidence and data, not gut feel?" } },
  { key: "approval", label: { ar: "الموافقات", en: "Approvals" }, question: { ar: "هل يمرّ كل التزام خارجي بموافقة بشرية موثّقة؟", en: "Does every external commitment pass a logged human approval?" } },
  { key: "evidence", label: { ar: "الدليل", en: "Evidence" }, question: { ar: "هل كل ادعاء عن قيمتك مربوط بدليل ومستوى تحقّق؟", en: "Is every claim about your value tied to evidence and a verification tier?" } },
  { key: "action", label: { ar: "الإجراء التالي", en: "Next action" }, question: { ar: "هل يعرف فريقك دائمًا الإجراء التالي ومن يملكه؟", en: "Does your team always know the next action and who owns it?" } },
  { key: "memory", label: { ar: "ذاكرة العميل", en: "Client memory" }, question: { ar: "هل تاريخ العميل محفوظ ومحكوم، لا مبعثر في واتساب وإكسل؟", en: "Is client history saved and governed, not scattered across WhatsApp and Excel?" } },
];

const CHOICES: { value: number; label: Bi }[] = [
  { value: 0, label: { ar: "لا", en: "No" } },
  { value: 1, label: { ar: "جزئيًا", en: "Partly" } },
  { value: 2, label: { ar: "نعم", en: "Yes" } },
];

function band(pct: number): { label: Bi; note: Bi; tone: string } {
  if (pct < 40)
    return {
      label: { ar: "مبعثر", en: "Scattered" },
      note: { ar: "العمل يعتمد على الذاكرة والانطباع. الإسفين الأول (Command Sprint) يبني لك الإيقاع.", en: "Work relies on memory and gut feel. The first wedge (Command Sprint) builds your rhythm." },
      tone: "text-red-300",
    };
  if (pct < 70)
    return {
      label: { ar: "ناشئ", en: "Emerging" },
      note: { ar: "لديك أساس، لكن الدليل والموافقات والإجراء التالي غير محكومة بالكامل بعد.", en: "You have a foundation, but evidence, approvals and next actions aren't fully governed yet." },
      tone: "text-gold-300",
    };
  return {
    label: { ar: "محكوم", en: "Governed" },
    note: { ar: "أنت قريب من إيقاع تشغيل واحد. Command Sprint يثبت القيمة ويكشف آخر الفجوات.", en: "You're close to one operating rhythm. A Command Sprint proves the value and surfaces the last gaps." },
    tone: "text-emerald-300",
  };
}

export function BusinessOsScoreTool() {
  const { t, base, isAr } = useBi();
  const [answers, setAnswers] = useState<Record<string, number | undefined>>({});
  const [submitted, setSubmitted] = useState(false);

  const answered = DIMENSIONS.filter((d) => answers[d.key] !== undefined).length;
  const complete = answered === DIMENSIONS.length;

  const pct = useMemo(() => {
    const max = DIMENSIONS.length * 2;
    const total = DIMENSIONS.reduce((s, d) => s + (answers[d.key] ?? 0), 0);
    return Math.round((total / max) * 100);
  }, [answers]);

  const result = band(pct);

  return (
    <PublicGtmShell>
      <div
        className="px-6 py-16 md:py-20"
        style={{ background: "linear-gradient(160deg,#00060d 0%,#001226 60%,#001832 100%)" }}
      >
        <div className="mx-auto max-w-2xl">
          <div className="mb-6 flex items-center justify-center gap-3">
            <span className="text-xs font-semibold uppercase tracking-[0.2em] text-gold-300">
              {isAr ? "أداة مجانية" : "Free tool"}
            </span>
            <StatusPill status="BETA" />
          </div>
          <h1 className="text-center font-arabic text-3xl font-bold text-white md:text-4xl">
            Business OS Score
          </h1>
          <p className="mx-auto mt-4 max-w-xl text-center text-white/65">
            {isAr
              ? "ستّة أسئلة، نتيجة تقديرية فورية. يعمل بالكامل في متصفحك — لا تُرسل أي بيانات. التقييم توضيحي وليس قيمة مُتحقَّقة."
              : "Six questions, an instant estimated score. Runs entirely in your browser — no data is sent. The assessment is illustrative, not a verified value."}
          </p>

          {!submitted ? (
            <div className="mt-10 space-y-5">
              {DIMENSIONS.map((d, i) => (
                <div key={d.key} className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
                  <div className="mb-3 flex items-center gap-2">
                    <span className="flex h-7 w-7 items-center justify-center rounded-full bg-gold-500/15 text-xs font-bold text-gold-300">
                      {i + 1}
                    </span>
                    <span className="text-sm font-semibold text-gold-200">{t(d.label)}</span>
                  </div>
                  <p className="mb-4 text-sm text-white/80">{t(d.question)}</p>
                  <div className="flex gap-2">
                    {CHOICES.map((c) => {
                      const active = answers[d.key] === c.value;
                      return (
                        <button
                          key={c.value}
                          type="button"
                          onClick={() => setAnswers((a) => ({ ...a, [d.key]: c.value }))}
                          className={`flex-1 rounded-xl border px-3 py-2 text-sm font-medium transition-colors ${
                            active
                              ? "border-gold-400/50 bg-gold-500/15 text-gold-200"
                              : "border-white/10 bg-white/[0.02] text-white/60 hover:border-white/25"
                          }`}
                        >
                          {t(c.label)}
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}

              <Button
                type="button"
                size="lg"
                disabled={!complete}
                onClick={() => setSubmitted(true)}
                className="w-full bg-gradient-to-r from-gold-500 to-gold-400 font-bold text-navy-500 shadow-lg shadow-gold-500/25 hover:from-gold-400 hover:to-gold-300 disabled:opacity-40"
              >
                {complete
                  ? isAr
                    ? "اعرض نتيجتي"
                    : "Show my score"
                  : isAr
                    ? `أجب على ${DIMENSIONS.length - answered} أسئلة متبقية`
                    : `${DIMENSIONS.length - answered} questions left`}
              </Button>
            </div>
          ) : (
            <div className="mt-10 rounded-2xl border border-white/10 bg-white/[0.04] p-8 text-center">
              <p className="text-sm uppercase tracking-widest text-white/40">
                {isAr ? "نتيجتك التقديرية" : "Your estimated score"}
              </p>
              <div className="my-4 text-6xl font-black text-white">
                {pct}
                <span className="text-2xl text-white/40">/100</span>
              </div>
              <p className={`text-lg font-bold ${result.tone}`}>{t(result.label)}</p>
              <p className="mx-auto mt-3 max-w-md text-sm leading-relaxed text-white/65">
                {t(result.note)}
              </p>

              <div className="mt-8 flex flex-col gap-3">
                <Button
                  asChild
                  size="lg"
                  className="bg-gradient-to-r from-gold-500 to-gold-400 font-bold text-navy-500 shadow-lg shadow-gold-500/25 hover:from-gold-400 hover:to-gold-300"
                >
                  <Link href={`${base}/command-sprint`}>
                    {isAr ? "ابدأ Command Sprint" : "Start Command Sprint"}
                  </Link>
                </Button>
                <button
                  type="button"
                  onClick={() => {
                    setSubmitted(false);
                    setAnswers({});
                  }}
                  className="text-sm text-white/50 hover:text-white/80"
                >
                  {isAr ? "أعد التقييم" : "Retake the assessment"}
                </button>
              </div>

              <p className="mt-6 text-xs text-white/35">
                {isAr
                  ? "نتيجة تقديرية توضيحية. القيمة التقديرية ليست قيمة مُتحقَّقة."
                  : "Illustrative estimated result. Estimated value is not Verified value."}
              </p>
            </div>
          )}
        </div>
      </div>
    </PublicGtmShell>
  );
}
