"use client";

import { useEffect, useRef, useState } from "react";
import { useLocale } from "next-intl";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type ServiceTier = "sprint" | "data_pack" | "managed_ops" | "";
type LanguagePref = "ar" | "en" | "both" | "";
type RelationshipStatus = "new" | "warm" | "existing" | "";
type DataFormat = "csv" | "excel" | "crm" | "";

interface Step1State {
  company_name: string;
  service_tier: ServiceTier;
  language_pref: LanguagePref;
}

interface Step2State {
  source_id: string;
  owner: string;
  allowed_use: string;
  contains_pii: boolean;
  relationship_status: RelationshipStatus;
}

interface Step3State {
  data_format: DataFormat;
  file_simulated: boolean;
}

interface OnboardingState {
  step: 1 | 2 | 3 | 4;
  step1: Step1State;
  step2: Step2State;
  step3: Step3State;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function isStep1Valid(s: Step1State): boolean {
  return s.company_name.trim().length > 0 && s.service_tier !== "" && s.language_pref !== "";
}

function isStep2Valid(s: Step2State): boolean {
  return (
    s.source_id.trim().length > 0 &&
    s.owner.trim().length > 0 &&
    s.allowed_use.trim().length > 0 &&
    s.relationship_status !== ""
  );
}

function isStep3Valid(s: Step3State): boolean {
  return s.data_format !== "" && s.file_simulated;
}

function estimatedDeliveryDate(isAr: boolean): string {
  const now = new Date();
  const delivery = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
  if (isAr) {
    return delivery.toLocaleDateString("ar-SA", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }
  return delivery.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

// ---------------------------------------------------------------------------
// Step indicator
// ---------------------------------------------------------------------------

const STEP_META: Array<{ label_ar: string; label_en: string }> = [
  { label_ar: "مرحباً", label_en: "Welcome" },
  { label_ar: "مصدر البيانات", label_en: "Data Source" },
  { label_ar: "الرفع الأول", label_en: "First Upload" },
  { label_ar: "بداية السبرينت", label_en: "Sprint Start" },
];

interface StepIndicatorProps {
  current: 1 | 2 | 3 | 4;
  isAr: boolean;
}

function StepIndicator({ current, isAr }: StepIndicatorProps) {
  const pct = ((current - 1) / (STEP_META.length - 1)) * 100;
  return (
    <div className="mb-8">
      <Progress value={pct} className="h-2 mb-4" />
      <div className="flex justify-between text-xs text-muted-foreground">
        {STEP_META.map((m, i) => (
          <span
            key={m.label_en}
            className={
              i + 1 === current
                ? "text-[var(--dealix-navy)] font-semibold"
                : ""
            }
          >
            {isAr ? m.label_ar : m.label_en}
          </span>
        ))}
      </div>
      <p className="text-xs text-muted-foreground text-center mt-2">
        {isAr
          ? `الخطوة ${current} من ${STEP_META.length}`
          : `Step ${current} of ${STEP_META.length}`}
      </p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Animated DQ score counter
// ---------------------------------------------------------------------------

const DQ_TARGET = 72;

function AnimatedDQScore({ isAr }: { isAr: boolean }) {
  const [score, setScore] = useState(0);
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    const start = performance.now();
    const duration = 1500;
    const animate = (now: number) => {
      const elapsed = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - elapsed, 3);
      setScore(Math.round(eased * DQ_TARGET));
      if (elapsed < 1) {
        rafRef.current = requestAnimationFrame(animate);
      }
    };
    rafRef.current = requestAnimationFrame(animate);
    return () => {
      if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);
    };
  }, []);

  const color =
    score >= 70
      ? "text-emerald-600"
      : score >= 50
      ? "text-amber-600"
      : "text-red-600";

  return (
    <div className="text-center py-4">
      <p className="text-xs text-muted-foreground mb-2">
        {isAr ? "معاينة درجة جودة البيانات" : "DQ Score Preview"}
      </p>
      <div className={`text-5xl font-black tabular-nums ${color}`}>{score}</div>
      <div className="text-muted-foreground text-xs mt-1">/100</div>
      <div className="mt-2">
        <Badge variant={score >= 70 ? "emerald" : "outline"} className="text-xs">
          {isAr ? "جودة مقبولة" : "Acceptable Quality"}
        </Badge>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Step 1 — Welcome
// ---------------------------------------------------------------------------

interface Step1Props {
  data: Step1State;
  onChange: (d: Step1State) => void;
  isAr: boolean;
}

const SERVICE_TIERS: Array<{ value: ServiceTier; label_ar: string; label_en: string; price: string }> = [
  { value: "sprint", label_ar: "Revenue Intelligence Sprint", label_en: "Revenue Intelligence Sprint", price: "499 SAR / 7 days" },
  { value: "data_pack", label_ar: "Data Pack — حزمة البيانات", label_en: "Data Pack", price: "1,499 SAR / mo" },
  { value: "managed_ops", label_ar: "Managed Ops — إدارة كاملة", label_en: "Managed Ops", price: "2,999 SAR / mo" },
];

const LANG_PREFS: Array<{ value: LanguagePref; label_ar: string; label_en: string }> = [
  { value: "ar", label_ar: "العربية فقط", label_en: "Arabic only" },
  { value: "en", label_ar: "الإنجليزية فقط", label_en: "English only" },
  { value: "both", label_ar: "ثنائي اللغة", label_en: "Bilingual" },
];

function Step1Form({ data, onChange, isAr }: Step1Props) {
  const set = <K extends keyof Step1State>(key: K, value: Step1State[K]) =>
    onChange({ ...data, [key]: value });

  return (
    <Card className="p-6 space-y-5">
      <CardHeader className="p-0">
        <CardTitle className="text-[var(--dealix-navy)]">
          {isAr ? "مرحباً بك في Dealix" : "Welcome to Dealix"}
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          {isAr
            ? "أدخل معلومات شركتك لبدء إعداد الحساب."
            : "Enter your company details to set up your account."}
        </p>
      </CardHeader>
      <CardContent className="p-0 space-y-4">
        <div className="space-y-1.5">
          <Label htmlFor="company_name">
            {isAr ? "اسم الشركة *" : "Company name *"}
          </Label>
          <Input
            id="company_name"
            value={data.company_name}
            onChange={(e) => set("company_name", e.target.value)}
            placeholder={isAr ? "مثال: شركة النخبة للتقنية" : "e.g. Acme Technology Co."}
          />
        </div>

        <div className="space-y-1.5">
          <Label>{isAr ? "مستوى الخدمة *" : "Service tier *"}</Label>
          <div className="space-y-2">
            {SERVICE_TIERS.map((t) => (
              <label
                key={t.value}
                className={`flex items-start gap-3 rounded-xl border px-4 py-3 cursor-pointer transition-colors ${
                  data.service_tier === t.value
                    ? "border-[var(--dealix-navy)] bg-[var(--dealix-navy)]/5"
                    : "border-border hover:border-[var(--dealix-navy)]/40"
                }`}
              >
                <input
                  type="radio"
                  name="service_tier"
                  checked={data.service_tier === t.value}
                  onChange={() => set("service_tier", t.value)}
                  className="mt-1 accent-[var(--dealix-navy)]"
                />
                <div className="min-w-0">
                  <p className="text-sm font-medium">
                    {isAr ? t.label_ar : t.label_en}
                  </p>
                  <p className="text-xs text-muted-foreground">{t.price}</p>
                </div>
              </label>
            ))}
          </div>
        </div>

        <div className="space-y-1.5">
          <Label>{isAr ? "تفضيل اللغة *" : "Language preference *"}</Label>
          <div className="flex gap-2 flex-wrap">
            {LANG_PREFS.map((lp) => (
              <button
                key={lp.value}
                type="button"
                onClick={() => set("language_pref", lp.value)}
                className={`rounded-lg border px-4 py-2 text-sm transition-colors ${
                  data.language_pref === lp.value
                    ? "border-[var(--dealix-navy)] bg-[var(--dealix-navy)] text-white"
                    : "border-border hover:border-[var(--dealix-navy)]/40"
                }`}
              >
                {isAr ? lp.label_ar : lp.label_en}
              </button>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

// ---------------------------------------------------------------------------
// Step 2 — Data Source
// ---------------------------------------------------------------------------

interface Step2Props {
  data: Step2State;
  onChange: (d: Step2State) => void;
  isAr: boolean;
}

const REL_STATUS_OPTIONS: Array<{ value: RelationshipStatus; label_ar: string; label_en: string }> = [
  { value: "new", label_ar: "جديد — لم نتواصل بعد", label_en: "New — no prior contact" },
  { value: "warm", label_ar: "دافئ — تواصل سابق", label_en: "Warm — prior contact" },
  { value: "existing", label_ar: "عميل حالي", label_en: "Existing client" },
];

function Step2Form({ data, onChange, isAr }: Step2Props) {
  const set = <K extends keyof Step2State>(key: K, value: Step2State[K]) =>
    onChange({ ...data, [key]: value });

  return (
    <Card className="p-6 space-y-5">
      <CardHeader className="p-0">
        <CardTitle className="text-[var(--dealix-navy)]">
          {isAr ? "جواز مصدر البيانات" : "Data Source Passport"}
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          {isAr
            ? "وثّق مصدر البيانات الأول وفق بروتوكول Source Passport."
            : "Document your first data source following the Source Passport protocol."}
        </p>
      </CardHeader>
      <CardContent className="p-0 space-y-4">
        <div className="space-y-1.5">
          <Label htmlFor="source_id">
            {isAr ? "معرّف المصدر *" : "Source ID *"}
          </Label>
          <Input
            id="source_id"
            value={data.source_id}
            onChange={(e) => set("source_id", e.target.value)}
            placeholder={isAr ? "مثال: CRM-2024-Q1" : "e.g. CRM-2024-Q1"}
          />
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="owner">
            {isAr ? "المسؤول *" : "Owner *"}
          </Label>
          <Input
            id="owner"
            value={data.owner}
            onChange={(e) => set("owner", e.target.value)}
            placeholder={isAr ? "مثال: أحمد المطيري" : "e.g. John Smith"}
          />
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="allowed_use">
            {isAr ? "الاستخدام المسموح به *" : "Allowed use *"}
          </Label>
          <Input
            id="allowed_use"
            value={data.allowed_use}
            onChange={(e) => set("allowed_use", e.target.value)}
            placeholder={
              isAr
                ? "مثال: تحليل داخلي للإيرادات فقط"
                : "e.g. Internal revenue analysis only"
            }
          />
        </div>

        <div className="space-y-1.5">
          <Label>{isAr ? "حالة العلاقة *" : "Relationship status *"}</Label>
          <div className="space-y-2">
            {REL_STATUS_OPTIONS.map((opt) => (
              <label
                key={opt.value}
                className={`flex items-center gap-3 rounded-xl border px-4 py-3 cursor-pointer transition-colors ${
                  data.relationship_status === opt.value
                    ? "border-[var(--dealix-navy)] bg-[var(--dealix-navy)]/5"
                    : "border-border hover:border-[var(--dealix-navy)]/40"
                }`}
              >
                <input
                  type="radio"
                  name="relationship_status"
                  checked={data.relationship_status === opt.value}
                  onChange={() => set("relationship_status", opt.value)}
                  className="accent-[var(--dealix-navy)]"
                />
                <span className="text-sm">
                  <span className="font-medium">
                    {isAr ? opt.label_ar : opt.label_en}
                  </span>
                </span>
              </label>
            ))}
          </div>
        </div>

        <label className="flex items-center gap-3 rounded-xl border px-4 py-3 cursor-pointer transition-colors border-border hover:border-[var(--dealix-navy)]/40">
          <input
            type="checkbox"
            checked={data.contains_pii}
            onChange={(e) => set("contains_pii", e.target.checked)}
            className="accent-[var(--dealix-navy)] h-4 w-4"
          />
          <div>
            <p className="text-sm font-medium">
              {isAr ? "يحتوي على بيانات شخصية (PII)" : "Contains personal data (PII)"}
            </p>
            <p className="text-xs text-muted-foreground">
              {isAr
                ? "يستلزم موافقة مسبقة وفق PDPL قبل المعالجة"
                : "Requires prior approval under PDPL before processing"}
            </p>
          </div>
        </label>
      </CardContent>
    </Card>
  );
}

// ---------------------------------------------------------------------------
// Step 3 — First Upload
// ---------------------------------------------------------------------------

interface Step3Props {
  data: Step3State;
  onChange: (d: Step3State) => void;
  isAr: boolean;
}

const FORMAT_OPTIONS: Array<{ value: DataFormat; label: string }> = [
  { value: "csv", label: "CSV" },
  { value: "excel", label: "Excel (.xlsx)" },
  { value: "crm", label: "CRM Export" },
];

function Step3Form({ data, onChange, isAr }: Step3Props) {
  const set = <K extends keyof Step3State>(key: K, value: Step3State[K]) =>
    onChange({ ...data, [key]: value });

  const [dragging, setDragging] = useState(false);

  const handleSimulatedDrop = () => {
    if (data.data_format !== "") {
      set("file_simulated", true);
    }
  };

  return (
    <Card className="p-6 space-y-5">
      <CardHeader className="p-0">
        <CardTitle className="text-[var(--dealix-navy)]">
          {isAr ? "الرفع الأول" : "First Upload"}
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          {isAr
            ? "اختر صيغة الملف ثم قم بمحاكاة رفع البيانات."
            : "Select your file format and simulate a data upload."}
        </p>
      </CardHeader>
      <CardContent className="p-0 space-y-4">
        {/* Format selection */}
        <div className="space-y-1.5">
          <Label>{isAr ? "صيغة البيانات *" : "Data format *"}</Label>
          <div className="flex gap-2 flex-wrap">
            {FORMAT_OPTIONS.map((f) => (
              <button
                key={f.value}
                type="button"
                onClick={() => {
                  set("data_format", f.value);
                  set("file_simulated", false);
                }}
                className={`rounded-lg border px-4 py-2 text-sm font-mono transition-colors ${
                  data.data_format === f.value
                    ? "border-[var(--dealix-navy)] bg-[var(--dealix-navy)] text-white"
                    : "border-border hover:border-[var(--dealix-navy)]/40"
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>
        </div>

        {/* Drag-and-drop simulation area */}
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragging(false);
            handleSimulatedDrop();
          }}
          onClick={handleSimulatedDrop}
          className={`rounded-xl border-2 border-dashed p-8 text-center cursor-pointer transition-colors ${
            data.file_simulated
              ? "border-emerald-500/60 bg-emerald-500/5"
              : dragging
              ? "border-[var(--dealix-navy)]/60 bg-[var(--dealix-navy)]/5"
              : "border-border hover:border-[var(--dealix-navy)]/40"
          }`}
        >
          {data.file_simulated ? (
            <div>
              <p className="text-emerald-600 font-semibold text-sm">
                {isAr ? "تم استلام الملف بنجاح" : "File received successfully"}
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                {isAr
                  ? `صيغة: ${data.data_format?.toUpperCase()}`
                  : `Format: ${data.data_format?.toUpperCase()}`}
              </p>
            </div>
          ) : (
            <div>
              <p className="text-sm text-muted-foreground">
                {isAr
                  ? data.data_format === ""
                    ? "اختر الصيغة أولاً ثم اسحب الملف هنا أو انقر للمحاكاة"
                    : "اسحب الملف هنا أو انقر للمحاكاة"
                  : data.data_format === ""
                  ? "Select format first, then drag a file here or click to simulate"
                  : "Drag a file here or click to simulate"}
              </p>
              <p className="text-xs text-muted-foreground/60 mt-2">
                {isAr
                  ? "(محاكاة فقط — لا يُرفع أي ملف حقيقي)"
                  : "(Simulation only — no real file is uploaded)"}
              </p>
            </div>
          )}
        </div>

        {/* DQ score preview */}
        {data.file_simulated && <AnimatedDQScore isAr={isAr} />}
      </CardContent>
    </Card>
  );
}

// ---------------------------------------------------------------------------
// Step 4 — Sprint Start (success screen)
// ---------------------------------------------------------------------------

const SPRINT_DAYS_PREVIEW: Array<{ day: number; label_ar: string; label_en: string }> = [
  { day: 1, label_ar: "جمع البيانات وجواز المصدر", label_en: "Data Collection & Source Passport" },
  { day: 2, label_ar: "تسجيل جودة البيانات", label_en: "Data Quality Scoring" },
  { day: 3, label_ar: "تسجيل الحسابات ومطابقة ICP", label_en: "Account Scoring & ICP Fit" },
  { day: 4, label_ar: "تجميع حزمة المسودة", label_en: "Draft Pack Assembly" },
  { day: 5, label_ar: "مراجعة الحوكمة", label_en: "Governance Review" },
  { day: 6, label_ar: "بناء Proof Pack", label_en: "Proof Pack Build" },
  { day: 7, label_ar: "تسجيل الأصول وعرض الاحتفاظ", label_en: "Capital Asset Registration + Retainer Pitch" },
];

interface Step4Props {
  companyName: string;
  isAr: boolean;
}

function Step4Success({ companyName, isAr }: Step4Props) {
  const deliveryDate = estimatedDeliveryDate(isAr);

  return (
    <div className="space-y-5">
      <Card className="p-6 border-emerald-500/30 bg-emerald-500/5">
        <div className="text-center space-y-2">
          <Badge variant="emerald" className="text-sm px-4 py-1">
            {isAr ? "السبرينت انطلق" : "Sprint Launched"}
          </Badge>
          <h2 className="text-xl font-bold text-[var(--dealix-navy)]">
            {isAr
              ? `مرحباً ${companyName} — سبرينتك بدأ`
              : `Welcome, ${companyName} — Your sprint has started`}
          </h2>
          <p className="text-sm text-muted-foreground">
            {isAr
              ? "تم تخصيص ممثل حساب لمتابعة سبرينتك."
              : "An account representative has been assigned to your sprint."}
          </p>
        </div>
      </Card>

      <Card className="p-6">
        <CardHeader className="p-0 pb-4">
          <CardTitle className="text-[var(--dealix-navy)] text-base">
            {isAr ? "معلومات السبرينت" : "Sprint Details"}
          </CardTitle>
        </CardHeader>
        <CardContent className="p-0 space-y-3">
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">
              {isAr ? "الممثل المخصص" : "Assigned rep"}
            </span>
            <span className="font-medium">
              {isAr ? "فريق عمليات Dealix" : "Dealix Ops Team"}
            </span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">
              {isAr ? "تاريخ التسليم المتوقع" : "Estimated delivery"}
            </span>
            <span className="font-medium">{deliveryDate}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">
              {isAr ? "السعر" : "Price"}
            </span>
            <span className="font-medium text-[var(--dealix-gold)]">
              499 {isAr ? "ر.س" : "SAR"}
            </span>
          </div>
        </CardContent>
      </Card>

      <Card className="p-6">
        <CardHeader className="p-0 pb-4">
          <CardTitle className="text-[var(--dealix-navy)] text-base">
            {isAr ? "معاينة جدول السبرينت" : "Sprint Timeline Preview"}
          </CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="space-y-2">
            {SPRINT_DAYS_PREVIEW.map((d) => (
              <div
                key={d.day}
                className="flex items-center gap-3 rounded-lg border border-border px-3 py-2"
              >
                <div className="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-full bg-[var(--dealix-navy)]/10 text-xs font-bold text-[var(--dealix-navy)]">
                  {d.day}
                </div>
                <p className="text-sm">
                  {isAr ? d.label_ar : d.label_en}
                </p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="text-center">
        <p className="text-xs text-muted-foreground">
          {isAr
            ? "يمكنك متابعة تقدمك من خلال بوابة العميل"
            : "Track your progress through the customer portal"}
        </p>
        <Button
          variant="outline"
          className="mt-3 border-[var(--dealix-navy)] text-[var(--dealix-navy)]"
          asChild
        >
          <a href="/customer-portal">
            {isAr ? "الذهاب إلى بوابة العميل" : "Go to Customer Portal"}
          </a>
        </Button>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Navigation buttons
// ---------------------------------------------------------------------------

interface NavButtonsProps {
  step: 1 | 2 | 3 | 4;
  canProceed: boolean;
  onBack: () => void;
  onNext: () => void;
  isAr: boolean;
}

function NavButtons({ step, canProceed, onBack, onNext, isAr }: NavButtonsProps) {
  if (step === 4) return null;

  return (
    <div className="flex gap-3 mt-4">
      {step > 1 && (
        <Button variant="outline" className="flex-1" onClick={onBack}>
          {isAr ? "السابق" : "Back"}
        </Button>
      )}
      <Button
        className="flex-1 bg-[var(--dealix-navy)] hover:bg-[var(--dealix-navy-hover)] text-white"
        disabled={!canProceed}
        onClick={onNext}
      >
        {step === 3
          ? isAr
            ? "ابدأ السبرينت"
            : "Start Sprint"
          : isAr
          ? "التالي"
          : "Next"}
      </Button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main export
// ---------------------------------------------------------------------------

export function OnboardingFlow() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [state, setState] = useState<OnboardingState>({
    step: 1,
    step1: { company_name: "", service_tier: "", language_pref: "" },
    step2: {
      source_id: "",
      owner: "",
      allowed_use: "",
      contains_pii: false,
      relationship_status: "",
    },
    step3: { data_format: "", file_simulated: false },
  });

  const setStep = (s: 1 | 2 | 3 | 4) =>
    setState((prev) => ({ ...prev, step: s }));

  const canProceed =
    state.step === 1
      ? isStep1Valid(state.step1)
      : state.step === 2
      ? isStep2Valid(state.step2)
      : state.step === 3
      ? isStep3Valid(state.step3)
      : false;

  const handleNext = () => {
    if (state.step < 4) setStep((state.step + 1) as 1 | 2 | 3 | 4);
  };

  const handleBack = () => {
    if (state.step > 1) setStep((state.step - 1) as 1 | 2 | 3 | 4);
  };

  return (
    <div className="max-w-2xl mx-auto" dir={isAr ? "rtl" : "ltr"}>
      <StepIndicator current={state.step} isAr={isAr} />

      {state.step === 1 && (
        <Step1Form
          data={state.step1}
          onChange={(d) => setState((prev) => ({ ...prev, step1: d }))}
          isAr={isAr}
        />
      )}

      {state.step === 2 && (
        <Step2Form
          data={state.step2}
          onChange={(d) => setState((prev) => ({ ...prev, step2: d }))}
          isAr={isAr}
        />
      )}

      {state.step === 3 && (
        <Step3Form
          data={state.step3}
          onChange={(d) => setState((prev) => ({ ...prev, step3: d }))}
          isAr={isAr}
        />
      )}

      {state.step === 4 && (
        <Step4Success
          companyName={state.step1.company_name}
          isAr={isAr}
        />
      )}

      <NavButtons
        step={state.step}
        canProceed={canProceed}
        onBack={handleBack}
        onNext={handleNext}
        isAr={isAr}
      />
    </div>
  );
}
