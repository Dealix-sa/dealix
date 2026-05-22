"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

interface Plan {
  name: string;
  amount_sar: number;
  monthly: boolean;
  kind: string;
  unit?: string;
}

interface PlansResponse {
  currency: string;
  plans: Record<string, Plan>;
}

interface CheckoutResponse {
  invoice_id?: string;
  status?: string;
  amount_sar?: number;
  payment_url?: string;
  plan?: string;
}

interface CheckoutPanelProps {
  locale: string;
}

type CopyStrings = {
  heading: string;
  sub: string;
  loadingPlans: string;
  plansError: string;
  selectPlan: string;
  selected: string;
  monthly: string;
  oneOff: string;
  metered: string;
  emailLabel: string;
  emailPlaceholder: string;
  leadHintLabel: string;
  leadHintPlaceholder: string;
  submit: string;
  submitting: string;
  success: string;
  successCta: string;
  error: string;
  chooseFirst: string;
  invalidEmail: string;
  safety: string;
};

const COPY: { ar: CopyStrings; en: CopyStrings } = {
  ar: {
    heading: "اختر الخطة المناسبة",
    sub: "كل خطة محكومة بمبدأ Dealix: invoice_intent ≠ revenue. لن تُحتسب الإيرادات إلا بعد تأكيد الدفع وتوفر دليل.",
    loadingPlans: "جاري تحميل الخطط…",
    plansError: "تعذر تحميل قائمة الخطط. حاول مرة أخرى.",
    selectPlan: "اختر هذه الخطة",
    selected: "محدد",
    monthly: "/شهرياً",
    oneOff: "مرة واحدة",
    metered: "حسب الاستهلاك",
    emailLabel: "البريد الإلكتروني للشركة",
    emailPlaceholder: "you@company.com",
    leadHintLabel: "معرّف اللّيد (اختياري)",
    leadHintPlaceholder: "lead_id إن وُجد",
    submit: "إنشاء رابط الدفع",
    submitting: "جاري إنشاء الرابط…",
    success: "تم إنشاء فاتورة Moyasar. اضغط للمتابعة لصفحة الدفع.",
    successCta: "متابعة إلى Moyasar",
    error: "فشل إنشاء الفاتورة. تأكد من البيانات أو حاول لاحقاً.",
    chooseFirst: "اختر خطة أولاً.",
    invalidEmail: "أدخل بريداً إلكترونياً صالحاً.",
    safety: "لن نأخذ أي مبلغ قبل أن تكمل عملية الدفع على Moyasar.",
  },
  en: {
    heading: "Pick your plan",
    sub: "Every plan respects the Dealix rule: invoice_intent ≠ revenue. Nothing is counted until payment is confirmed with evidence.",
    loadingPlans: "Loading plans…",
    plansError: "Could not load plans. Try again.",
    selectPlan: "Select this plan",
    selected: "Selected",
    monthly: "/mo",
    oneOff: "one-off",
    metered: "metered",
    emailLabel: "Business email",
    emailPlaceholder: "you@company.com",
    leadHintLabel: "Lead ID (optional)",
    leadHintPlaceholder: "lead_id if available",
    submit: "Create payment link",
    submitting: "Creating link…",
    success: "Moyasar invoice created. Click to continue to checkout.",
    successCta: "Continue to Moyasar",
    error: "Failed to create the invoice. Check details or try again later.",
    chooseFirst: "Pick a plan first.",
    invalidEmail: "Enter a valid email address.",
    safety: "No charge will happen until you complete payment on Moyasar.",
  },
};

function planSubtitle(plan: Plan, t: CopyStrings): string {
  if (plan.kind === "subscription") return t.monthly;
  if (plan.kind === "metered") {
    return plan.unit ? `${t.metered} · ${plan.unit}` : t.metered;
  }
  return t.oneOff;
}

export function CheckoutPanel({ locale }: CheckoutPanelProps) {
  const t = locale === "ar" ? COPY.ar : COPY.en;
  const isAr = locale === "ar";

  const [plans, setPlans] = useState<PlansResponse | null>(null);
  const [loadingPlans, setLoadingPlans] = useState(true);
  const [plansError, setPlansError] = useState(false);

  const [selectedPlan, setSelectedPlan] = useState<string | null>(null);
  const [email, setEmail] = useState("");
  const [leadId, setLeadId] = useState("");

  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [checkout, setCheckout] = useState<CheckoutResponse | null>(null);

  useEffect(() => {
    let active = true;
    api
      .getPricingPlans()
      .then((res) => {
        if (!active) return;
        setPlans(res.data as PlansResponse);
        setPlansError(false);
      })
      .catch(() => {
        if (!active) return;
        setPlansError(true);
      })
      .finally(() => {
        if (active) setLoadingPlans(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError(null);
    setCheckout(null);
    if (!selectedPlan) {
      setSubmitError(t.chooseFirst);
      return;
    }
    if (!email.includes("@") || email.length < 5) {
      setSubmitError(t.invalidEmail);
      return;
    }
    setSubmitting(true);
    try {
      const res = await api.postCheckout({
        plan: selectedPlan,
        email,
        ...(leadId ? { lead_id: leadId } : {}),
      });
      setCheckout(res.data as CheckoutResponse);
    } catch {
      setSubmitError(t.error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="mt-10" dir={isAr ? "rtl" : "ltr"}>
      <h2 className="text-2xl font-bold tracking-tight text-foreground">
        {t.heading}
      </h2>
      <p className="mt-2 text-sm text-muted-foreground">{t.sub}</p>

      {loadingPlans && (
        <p className="mt-6 text-sm text-muted-foreground">{t.loadingPlans}</p>
      )}

      {plansError && (
        <p className="mt-6 text-sm text-destructive">{t.plansError}</p>
      )}

      {plans && (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Object.entries(plans.plans).map(([key, plan]) => {
            const isSelected = selectedPlan === key;
            return (
              <button
                key={key}
                type="button"
                onClick={() => setSelectedPlan(key)}
                aria-pressed={isSelected}
                className={`rounded-lg border p-5 text-start transition ${
                  isSelected
                    ? "border-primary bg-primary/10"
                    : "border-border bg-card/40 hover:border-primary/50"
                }`}
              >
                <p className="text-xs uppercase tracking-wide text-muted-foreground">
                  {key}
                </p>
                <p className="mt-1 text-base font-semibold text-foreground">
                  {plan.name}
                </p>
                <p className="mt-3 text-2xl font-bold text-foreground">
                  {plan.amount_sar.toLocaleString(isAr ? "ar-SA" : "en-US")}{" "}
                  <span className="text-sm font-normal text-muted-foreground">
                    SAR{planSubtitle(plan, t)}
                  </span>
                </p>
                {isSelected && (
                  <p className="mt-3 text-xs font-medium text-primary">
                    ✓ {t.selected}
                  </p>
                )}
              </button>
            );
          })}
        </div>
      )}

      <form onSubmit={handleSubmit} className="mt-8 space-y-4">
        <div>
          <label
            htmlFor="billing-email"
            className="block text-sm font-medium text-foreground"
          >
            {t.emailLabel}
          </label>
          <input
            id="billing-email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder={t.emailPlaceholder}
            className="mt-1 block w-full rounded-lg border border-border bg-background px-3 py-2 text-sm text-foreground focus:border-primary focus:outline-none"
            required
            autoComplete="email"
            dir="ltr"
          />
        </div>

        <div>
          <label
            htmlFor="billing-lead"
            className="block text-sm font-medium text-foreground"
          >
            {t.leadHintLabel}
          </label>
          <input
            id="billing-lead"
            type="text"
            value={leadId}
            onChange={(e) => setLeadId(e.target.value)}
            placeholder={t.leadHintPlaceholder}
            className="mt-1 block w-full rounded-lg border border-border bg-background px-3 py-2 text-sm text-foreground focus:border-primary focus:outline-none"
            dir="ltr"
          />
        </div>

        <button
          type="submit"
          disabled={submitting || !selectedPlan}
          className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {submitting ? t.submitting : t.submit}
        </button>

        {submitError && (
          <p className="text-sm text-destructive" role="alert">
            {submitError}
          </p>
        )}

        {checkout?.payment_url && (
          <div className="mt-4 rounded-lg border border-primary/40 bg-primary/5 p-4">
            <p className="text-sm font-medium text-foreground">{t.success}</p>
            <a
              href={checkout.payment_url}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-3 inline-flex items-center justify-center rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:opacity-90"
            >
              {t.successCta} →
            </a>
            {checkout.invoice_id && (
              <p className="mt-2 text-xs text-muted-foreground">
                invoice_id: <code>{checkout.invoice_id}</code>
              </p>
            )}
          </div>
        )}

        <p className="text-xs text-muted-foreground">{t.safety}</p>
      </form>
    </div>
  );
}
