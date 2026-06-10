"use client";

import { useMemo, useState } from "react";
import { useLocale } from "next-intl";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { PrimaryCta } from "@/components/wave3/PrimaryCta";
import { Disclaimer } from "@/components/wave3/Disclaimer";
import { scoreQuiz } from "@/lib/wave3/scoring";
import { routeToHref } from "@/lib/wave3/routes";
import { captureLead, type LeadForm, type ToolSource } from "@/lib/wave3/leadCapture";
import type { QuizToolDef } from "@/content/wave3/tools/types";

export function ToolRunner({ tool, source }: { tool: QuizToolDef; source: ToolSource }) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitted, setSubmitted] = useState(false);
  const [lead, setLead] = useState<LeadForm>({ name: "", email: "", company: "", consent: false });
  const [leadDone, setLeadDone] = useState(false);
  const [busy, setBusy] = useState(false);

  const allAnswered = tool.questions.every((q) => answers[q.id] !== undefined);
  const result = useMemo(
    () => scoreQuiz(tool.questions, answers),
    [tool.questions, answers],
  );
  const rec = tool.recommended[result.band];

  async function submitLead(e: React.FormEvent) {
    e.preventDefault();
    if (!lead.name || !lead.email || !lead.consent) return;
    setBusy(true);
    await captureLead(source, lead, { score: result.score, band: result.band, locale });
    setBusy(false);
    setLeadDone(true);
  }

  return (
    <div dir={isAr ? "rtl" : "ltr"} className={isAr ? "text-right" : "text-left"}>
      <h1 className="text-3xl font-bold font-display">{isAr ? tool.titleAr : tool.titleEn}</h1>
      <p className="mt-3 text-muted-foreground leading-relaxed">{isAr ? tool.introAr : tool.introEn}</p>

      {!submitted && (
        <div className="mt-8 space-y-6">
          {tool.questions.map((q, i) => (
            <Card key={q.id} className="p-5">
              <p className="font-semibold">
                <span className="text-muted-foreground">{i + 1}. </span>
                {isAr ? q.promptAr : q.promptEn}
              </p>
              <div className="mt-3 grid gap-2">
                {q.options.map((opt, idx) => {
                  const active = answers[q.id] === idx;
                  return (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => setAnswers((a) => ({ ...a, [q.id]: idx }))}
                      className={`rounded-lg border px-4 py-2 text-sm transition-colors ${
                        active
                          ? "border-gold-500 bg-gold-500/10 text-foreground"
                          : "border-border hover:bg-accent"
                      } ${isAr ? "text-right" : "text-left"}`}
                    >
                      {isAr ? opt.labelAr : opt.labelEn}
                    </button>
                  );
                })}
              </div>
            </Card>
          ))}
          <Button
            type="button"
            size="lg"
            disabled={!allAnswered}
            onClick={() => setSubmitted(true)}
          >
            {isAr ? "اعرض النتيجة" : "Show my result"}
          </Button>
        </div>
      )}

      {submitted && (
        <div className="mt-8 space-y-6">
          <Card className="p-6">
            <p className="text-sm text-muted-foreground">{isAr ? "نتيجتك" : "Your score"}</p>
            <p className="text-5xl font-bold font-display text-gold-500">{result.score}</p>
            <p className="mt-1 text-sm text-muted-foreground">/ 100</p>

            {result.gaps.length > 0 && (
              <div className="mt-6">
                <p className="font-semibold">{isAr ? "أهم 3 فجوات" : "Top 3 gaps"}</p>
                <ul className="mt-2 list-disc space-y-1 ps-5 text-sm text-muted-foreground">
                  {result.gaps.map((g, i) => (
                    <li key={i}>{isAr ? g.ar : g.en}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="mt-6">
              <p className="font-semibold">{isAr ? "الطبقة المقترحة" : "Recommended Dealix OS"}</p>
              <p className="mt-1 text-sm text-muted-foreground">{isAr ? rec.osAr : rec.osEn}</p>
            </div>

            <div className="mt-6">
              <p className="font-semibold">{isAr ? "خطوتك التالية" : "Recommended next step"}</p>
              <div className="mt-3">
                <PrimaryCta
                  locale={locale}
                  href={routeToHref(rec.nextStep.route)}
                  labelAr={rec.nextStep.labelAr}
                  labelEn={rec.nextStep.labelEn}
                />
              </div>
            </div>

            <Disclaimer locale={locale} variant={tool.disclaimer} />
          </Card>

          {!leadDone ? (
            <Card className="p-6">
              <p className="font-semibold">
                {isAr ? "ابعث لي النتيجة وملخص الخطوات" : "Send me my result and next steps"}
              </p>
              <form onSubmit={submitLead} className="mt-4 grid gap-3">
                <input
                  className="rounded-lg border border-border bg-background px-3 py-2 text-sm"
                  placeholder={isAr ? "الاسم" : "Name"}
                  value={lead.name}
                  onChange={(e) => setLead({ ...lead, name: e.target.value })}
                  required
                />
                <input
                  type="email"
                  className="rounded-lg border border-border bg-background px-3 py-2 text-sm"
                  placeholder={isAr ? "البريد الإلكتروني" : "Email"}
                  value={lead.email}
                  onChange={(e) => setLead({ ...lead, email: e.target.value })}
                  required
                />
                <input
                  className="rounded-lg border border-border bg-background px-3 py-2 text-sm"
                  placeholder={isAr ? "الشركة (اختياري)" : "Company (optional)"}
                  value={lead.company}
                  onChange={(e) => setLead({ ...lead, company: e.target.value })}
                />
                <label className="flex items-start gap-2 text-xs text-muted-foreground">
                  <input
                    type="checkbox"
                    className="mt-0.5"
                    checked={lead.consent}
                    onChange={(e) => setLead({ ...lead, consent: e.target.checked })}
                    required
                  />
                  <span>
                    {isAr
                      ? "أوافق على التواصل معي يدوياً بخصوص نتيجتي. لن يُرسَل أي شيء تلقائياً."
                      : "I agree to be contacted manually about my result. Nothing is sent automatically."}
                  </span>
                </label>
                <Button type="submit" disabled={busy || !lead.consent}>
                  {busy ? (isAr ? "جارٍ الإرسال…" : "Sending…") : isAr ? "أرسل" : "Send"}
                </Button>
              </form>
            </Card>
          ) : (
            <Card className="p-6 text-sm text-muted-foreground">
              {isAr
                ? "تم استلام طلبك. سنتواصل معك يدوياً — بدون أي إرسال تلقائي."
                : "Got it. We'll reach out manually — with no automated sending."}
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
