"use client";

/**
 * AI Stack Demo Run Form — bilingual diagnostic intake → live run → results.
 *
 * The form runs the free_diagnostic tier through the live AI Stack, which
 * is rate-limited and PII-light by design. The result panel shows the
 * eleven layer outcomes, the proof score, the recommended next offer, and
 * a collapsible Markdown preview of the Proof Pack.
 */

import { useState } from "react";
import {
  AIStackResult,
  LayerResult,
  runDemo,
  type OfferTier,
} from "@/lib/aiStackClient";

interface RunDemoFormProps {
  locale: "ar" | "en";
}

interface FormState {
  company_name: string;
  sector: string;
  challenge_ar: string;
  challenge_en: string;
}

const INITIAL_STATE: FormState = {
  company_name: "",
  sector: "technology",
  challenge_ar: "",
  challenge_en: "",
};

const LABELS = {
  ar: {
    company: "اسم الشركة",
    sector: "القطاع",
    challenge_ar: "التحدي بالعربية",
    challenge_en: "التحدي بالإنجليزية (اختياري)",
    submit: "شغّل التشخيص المجاني",
    submitting: "جارٍ تشغيل الستاك…",
    success: "اكتمل التشغيل عبر الـ 11 طبقة",
    error: "حدث خطأ — حاول مرة أخرى",
    proof_score: "درجة الإثبات",
    recommended: "التوصية القادمة",
    governance_blocked: "محجوب من قِبَل الحوكمة",
    doctrine_clean: "خالٍ من خرق Doctrine",
    duration: "الزمن",
    proof_pack_preview: "معاينة Proof Pack (Markdown)",
    expand: "اعرض المسودة",
    collapse: "أخفِ المسودة",
  },
  en: {
    company: "Company name",
    sector: "Sector",
    challenge_ar: "Challenge (Arabic)",
    challenge_en: "Challenge (English, optional)",
    submit: "Run free diagnostic",
    submitting: "Running the stack…",
    success: "Completed across all 11 layers",
    error: "Something failed — try again",
    proof_score: "Proof score",
    recommended: "Next recommendation",
    governance_blocked: "Blocked by governance",
    doctrine_clean: "Doctrine clean",
    duration: "Duration",
    proof_pack_preview: "Proof Pack preview (Markdown)",
    expand: "Show draft",
    collapse: "Hide draft",
  },
};

export function RunDemoForm({ locale }: RunDemoFormProps) {
  const labels = LABELS[locale];
  const [form, setForm] = useState<FormState>(INITIAL_STATE);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<AIStackResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showMarkdown, setShowMarkdown] = useState(false);

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setResult(null);
    setBusy(true);
    try {
      const tenant_id = `demo_${slugify(form.company_name) || "guest"}`;
      const payload = {
        tenant_id,
        customer_handle: tenant_id,
        company_name: form.company_name,
        sector: form.sector || "general",
        challenge_ar: form.challenge_ar,
        challenge_en: form.challenge_en,
        offer_tier: "free_diagnostic" as OfferTier,
        source_passport: {
          source_id: `intake_demo_${Date.now()}`,
          source_type: "public_demo_form",
          owner: tenant_id,
          allowed_use: ["ai_assist"],
          contains_pii: false,
          sensitivity: "internal",
          retention_policy: "30d",
          ai_access_allowed: true,
          external_use_allowed: false,
        },
        actor: "ai_stack_demo_ui",
        locale_primary: locale,
      };
      const response = await runDemo(payload);
      setResult(response);
    } catch (err) {
      setError((err as Error).message || labels.error);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-6">
      <form
        onSubmit={onSubmit}
        className="grid gap-4 rounded-xl border border-border bg-card p-6"
      >
        <Field
          label={labels.company}
          required
          value={form.company_name}
          onChange={(value) =>
            setForm((prev) => ({ ...prev, company_name: value }))
          }
        />
        <Field
          label={labels.sector}
          value={form.sector}
          onChange={(value) => setForm((prev) => ({ ...prev, sector: value }))}
        />
        <Field
          label={labels.challenge_ar}
          required
          multiline
          value={form.challenge_ar}
          onChange={(value) =>
            setForm((prev) => ({ ...prev, challenge_ar: value }))
          }
        />
        <Field
          label={labels.challenge_en}
          multiline
          value={form.challenge_en}
          onChange={(value) =>
            setForm((prev) => ({ ...prev, challenge_en: value }))
          }
        />
        <button
          type="submit"
          disabled={busy || !form.company_name || form.challenge_ar.length < 3}
          className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 font-semibold text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {busy ? labels.submitting : labels.submit}
        </button>
        {error ? (
          <div className="rounded-md bg-rose-500/10 px-3 py-2 text-sm text-rose-400">
            {error}
          </div>
        ) : null}
      </form>

      {result ? (
        <ResultPanel
          result={result}
          labels={labels}
          locale={locale}
          showMarkdown={showMarkdown}
          onToggleMarkdown={() => setShowMarkdown((prev) => !prev)}
        />
      ) : null}
    </div>
  );
}

interface FieldProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  required?: boolean;
  multiline?: boolean;
}

function Field({ label, value, onChange, required, multiline }: FieldProps) {
  return (
    <label className="grid gap-1.5">
      <span className="text-sm font-medium text-foreground">
        {label}
        {required ? <span className="text-rose-500"> *</span> : null}
      </span>
      {multiline ? (
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          rows={3}
          className="rounded-md border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/40"
          required={required}
        />
      ) : (
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="rounded-md border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/40"
          required={required}
        />
      )}
    </label>
  );
}

interface ResultPanelProps {
  result: AIStackResult;
  labels: typeof LABELS.ar;
  locale: "ar" | "en";
  showMarkdown: boolean;
  onToggleMarkdown: () => void;
}

function ResultPanel({
  result,
  labels,
  locale,
  showMarkdown,
  onToggleMarkdown,
}: ResultPanelProps) {
  return (
    <div className="space-y-4 rounded-xl border border-emerald-500/30 bg-emerald-500/5 p-6">
      <div className="grid grid-cols-2 gap-3 text-sm sm:grid-cols-4">
        <Stat
          label={labels.proof_score}
          value={`${result.proof_score}/100`}
          tone={result.proof_score >= 70 ? "good" : "warn"}
        />
        <Stat
          label={labels.duration}
          value={`${result.duration_ms}ms`}
        />
        <Stat
          label={labels.recommended}
          value={result.recommended_offer || "—"}
        />
        <Stat
          label={labels.doctrine_clean}
          value={result.doctrine_clean ? "✓" : "✗"}
          tone={result.doctrine_clean ? "good" : "bad"}
        />
      </div>

      <div className="space-y-1.5">
        {result.layers.map((layer) => (
          <LayerRow key={layer.layer} layer={layer} locale={locale} />
        ))}
      </div>

      <div>
        <button
          type="button"
          onClick={onToggleMarkdown}
          className="rounded-md border border-border bg-background px-3 py-1.5 text-sm font-medium hover:bg-muted"
        >
          {showMarkdown ? labels.collapse : labels.expand}
        </button>
        {showMarkdown ? (
          <pre className="mt-3 max-h-96 overflow-y-auto rounded-md border border-border bg-background p-4 text-xs leading-relaxed whitespace-pre-wrap">
            {result.proof_pack_markdown}
          </pre>
        ) : null}
      </div>
    </div>
  );
}

interface StatProps {
  label: string;
  value: string;
  tone?: "good" | "warn" | "bad";
}

function Stat({ label, value, tone }: StatProps) {
  const toneClass =
    tone === "good"
      ? "text-emerald-400"
      : tone === "warn"
      ? "text-amber-400"
      : tone === "bad"
      ? "text-rose-400"
      : "text-foreground";
  return (
    <div className="rounded-md bg-background/40 p-3">
      <div className="text-[11px] uppercase tracking-wide text-muted-foreground">
        {label}
      </div>
      <div className={`mt-0.5 text-base font-semibold ${toneClass}`}>
        {value}
      </div>
    </div>
  );
}

interface LayerRowProps {
  layer: LayerResult;
  locale: "ar" | "en";
}

function LayerRow({ layer, locale }: LayerRowProps) {
  const summary = locale === "ar" ? layer.summary_ar : layer.summary_en;
  const statusColor =
    layer.status === "ok"
      ? "text-emerald-400"
      : layer.status === "skipped"
      ? "text-amber-400"
      : layer.status === "blocked"
      ? "text-rose-400"
      : layer.status === "error"
      ? "text-rose-400"
      : "text-muted-foreground";
  return (
    <div className="flex items-center justify-between gap-3 rounded-md border border-border/50 bg-background/30 px-3 py-2 text-sm">
      <span className="font-mono text-xs text-muted-foreground">
        {layer.layer}
      </span>
      <span className="flex-1 truncate">{summary}</span>
      <span className={`font-mono text-xs ${statusColor}`}>
        {layer.status}
      </span>
      <span className="font-mono text-xs text-muted-foreground/70">
        {layer.duration_ms}ms
      </span>
    </div>
  );
}

function slugify(input: string): string {
  return input
    .toLowerCase()
    .replace(/[^a-z0-9؀-ۿ]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 32);
}
