"use client";

import Link from "next/link";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

type Question = {
  id: string;
  ar: string;
  en: string;
  options: { value: number; ar: string; en: string }[];
};

const QUESTIONS: Question[] = [
  {
    id: "revenue",
    ar: "ما مستوى الإيرادات السنوية لشركتك؟",
    en: "What is your company's annual revenue level?",
    options: [
      { value: 0, ar: "أقل من ٣٧٥٬٠٠٠ ريال", en: "Below 375,000 SAR" },
      { value: 2, ar: "٣٧٥٬٠٠٠ — ١٠ مليون ريال", en: "375,000 — 10M SAR" },
      { value: 3, ar: "أكثر من ١٠ مليون ريال", en: "Above 10M SAR" },
    ],
  },
  {
    id: "einvoice",
    ar: "هل تستخدم حالياً فاتورة إلكترونية متوافقة مع ZATCA؟",
    en: "Are you currently using ZATCA-compliant e-invoicing?",
    options: [
      { value: 3, ar: "نعم — مُتكامل ومُعتمد", en: "Yes — integrated and certified" },
      { value: 1, ar: "جزئياً — في مرحلة التطبيق", en: "Partially — in implementation" },
      { value: 0, ar: "لا — لا نزال نستخدم أساليب تقليدية", en: "No — still using traditional methods" },
    ],
  },
  {
    id: "crn",
    ar: "هل سجّلت الشركة في بوابة ZATCA Fatoorah؟",
    en: "Has the company registered on the ZATCA Fatoorah portal?",
    options: [
      { value: 3, ar: "نعم — لدينا CSID ومعتمدون", en: "Yes — we have CSID and are certified" },
      { value: 1, ar: "في المراحل الأولى", en: "In early stages" },
      { value: 0, ar: "لا", en: "No" },
    ],
  },
  {
    id: "data",
    ar: "كيف تحتفظ ببيانات الفواتير حالياً؟",
    en: "How do you currently store invoice data?",
    options: [
      { value: 3, ar: "نظام ERP / محاسبة رقمي متكامل", en: "Integrated digital ERP / accounting system" },
      { value: 1, ar: "برنامج محاسبة بسيط أو جداول بيانات", en: "Basic accounting software or spreadsheets" },
      { value: 0, ar: "ورق أو طرق يدوية", en: "Paper or manual methods" },
    ],
  },
  {
    id: "timeline",
    ar: "متى تخطط لإتمام الامتثال الكامل لـ ZATCA Phase 2؟",
    en: "When do you plan to complete full ZATCA Phase 2 compliance?",
    options: [
      { value: 3, ar: "قبل ٣٠ يونيو ٢٠٢٦ (الإلزامي)", en: "Before June 30, 2026 (mandatory)" },
      { value: 1, ar: "لا أعرف — أحتاج مساعدة", en: "I don't know — need help" },
      { value: 0, ar: "لم أبدأ التخطيط بعد", en: "Haven't started planning yet" },
    ],
  },
];

type Answers = Record<string, number>;

function calcScore(answers: Answers): number {
  const total = Object.values(answers).reduce((s, v) => s + v, 0);
  const max = QUESTIONS.reduce((s, q) => s + Math.max(...q.options.map((o) => o.value)), 0);
  return max > 0 ? Math.round((total / max) * 100) : 0;
}

function scoreLabel(score: number, isAr: boolean): { label: string; color: string; advice: string } {
  if (score >= 80) return {
    label: isAr ? "جاهز جيداً" : "Well prepared",
    color: "text-green-600",
    advice: isAr ? "شركتك في وضع قوي. تحقق من التفاصيل الفنية لضمان التكامل الكامل." : "Your company is in a strong position. Verify technical details for full integration.",
  };
  if (score >= 50) return {
    label: isAr ? "جاهزية جزئية" : "Partially ready",
    color: "text-amber-600",
    advice: isAr ? "لديك قاعدة جيدة لكن تحتاج خطوات إضافية قبل الموعد النهائي." : "You have a good base but need additional steps before the deadline.",
  };
  return {
    label: isAr ? "مخاطرة عالية" : "High risk",
    color: "text-red-600",
    advice: isAr ? "شركتك في خطر حقيقي. الموعد النهائي ٣٠ يونيو ٢٠٢٦ — ابدأ الآن." : "Your company faces real risk. Deadline is June 30, 2026 — start now.",
  };
}

export function ZatcaReadinessQuiz({ locale }: { locale: string }) {
  const isAr = locale === "ar";
  const [answers, setAnswers] = useState<Answers>({});
  const [submitted, setSubmitted] = useState(false);

  const allAnswered = QUESTIONS.every((q) => answers[q.id] !== undefined);
  const score = calcScore(answers);
  const { label, color, advice } = scoreLabel(score, isAr);
  const daysLeft = Math.max(0, Math.ceil((new Date("2026-06-30").getTime() - Date.now()) / 86400000));

  return (
    <div className="max-w-2xl mx-auto px-6 py-12 space-y-8" dir={isAr ? "rtl" : "ltr"}>

      {/* Urgency banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
        <Badge variant="destructive" className="text-xs shrink-0">
          {isAr ? `⚠ ZATCA موجة ٢٤ — متبقي ${daysLeft} يوم` : `⚠ ZATCA Wave 24 — ${daysLeft} days left`}
        </Badge>
        <Badge variant="outline" className="text-xs">
          {isAr ? "إلزامي لـ +٣٧٥٬٠٠٠ ريال" : "Mandatory for 375,000+ SAR"}
        </Badge>
      </div>

      <div className="space-y-2">
        <h1 className="text-3xl font-extrabold tracking-tight">
          {isAr ? "اختبار جاهزية ZATCA Phase 2" : "ZATCA Phase 2 Readiness Check"}
        </h1>
        <p className="text-muted-foreground text-sm">
          {isAr
            ? "٥ أسئلة · ٦٠ ثانية · تقييم فوري لمستوى امتثالك."
            : "5 questions · 60 seconds · instant compliance assessment."}
        </p>
      </div>

      {!submitted ? (
        <div className="space-y-6">
          {QUESTIONS.map((q, qi) => (
            <Card key={q.id} className="p-5">
              <p className="font-semibold text-sm mb-3">
                <span className="text-muted-foreground">{qi + 1}. </span>
                {isAr ? q.ar : q.en}
              </p>
              <div className="space-y-2">
                {q.options.map((opt) => (
                  <button
                    key={opt.value + opt.en}
                    type="button"
                    onClick={() => setAnswers((prev) => ({ ...prev, [q.id]: opt.value }))}
                    className={[
                      "w-full text-start rounded-lg border px-4 py-2.5 text-sm transition-colors",
                      answers[q.id] === opt.value
                        ? "border-primary bg-primary/10 text-primary font-medium"
                        : "border-border hover:border-primary/40 hover:bg-muted/30",
                    ].join(" ")}
                  >
                    {isAr ? opt.ar : opt.en}
                  </button>
                ))}
              </div>
            </Card>
          ))}

          <Button
            className="w-full"
            disabled={!allAnswered}
            onClick={() => setSubmitted(true)}
          >
            {isAr ? "اعرف نتيجتي ←" : "See my result →"}
          </Button>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Score card */}
          <Card className="p-8 text-center space-y-3">
            <div className={`text-6xl font-extrabold ${color}`}>{score}%</div>
            <div className={`text-xl font-bold ${color}`}>{label}</div>
            <p className="text-sm text-muted-foreground max-w-sm mx-auto">{advice}</p>
          </Card>

          {/* Next steps */}
          <div className="space-y-3">
            <p className="font-semibold">
              {isAr ? "خطواتك التالية" : "Your next steps"}
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <Link href={`/${locale}/dealix-diagnostic`}>
                <Card className="p-4 hover:border-primary/50 transition-colors cursor-pointer">
                  <p className="font-medium text-sm">
                    {isAr ? "تشخيص مجاني كامل" : "Full free diagnostic"}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    {isAr ? "اكتشف الفجوات الدقيقة في عملياتك" : "Discover exact gaps in your operations"}
                  </p>
                </Card>
              </Link>
              <Link href={`/${locale}/offer/lead-intelligence-sprint`}>
                <Card className="p-4 hover:border-primary/50 transition-colors cursor-pointer border-primary/20 bg-primary/5">
                  <p className="font-medium text-sm">
                    {isAr ? "Sprint ٤٩٩ ريال — ٧ أيام" : "499 SAR Sprint — 7 days"}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    {isAr ? "خطة امتثال + تحسين إيراد في وقت واحد" : "Compliance plan + revenue improvement together"}
                  </p>
                </Card>
              </Link>
            </div>
          </div>

          {/* PDPL note */}
          <p className="text-xs text-muted-foreground text-center">
            {isAr
              ? "ملاحظة: هذا التقييم استرشادي. للامتثال الرسمي استشر مستشاراً ضريبياً معتمداً."
              : "Note: This assessment is indicative. For official compliance, consult a certified tax advisor."}
          </p>

          <button
            type="button"
            className="text-xs text-muted-foreground underline w-full text-center"
            onClick={() => { setAnswers({}); setSubmitted(false); }}
          >
            {isAr ? "أعِد الاختبار" : "Retake quiz"}
          </button>
        </div>
      )}
    </div>
  );
}
