"use client";

import { useState } from "react";

const REQUEST_TYPES = ["access", "rectify", "port", "erase"] as const;
type RequestType = (typeof REQUEST_TYPES)[number];

interface DsarFormProps {
  locale: string;
}

interface SubmissionResult {
  status: string;
  request_id: string;
  request_type: string;
  submitted_at: string;
  sla_business_days?: number;
  next_step?: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const LABELS = {
  ar: {
    email: "البريد الإلكتروني المسجل",
    emailHint: "نفس البريد الذي استخدمته في تسجيل حسابك أو في التواصل معنا.",
    requestType: "نوع الطلب",
    types: {
      access: "الوصول — تصدير كل بياناتك التي لدينا",
      rectify: "التصحيح — تعديل حقل معين",
      port: "النقل — تصدير قابل للنقل لجهة أخرى",
      erase: "الحذف — حذف بياناتك (مع استبقاءات نظامية)",
    },
    field: "اسم الحقل المطلوب تصحيحه",
    newValue: "القيمة الجديدة الصحيحة",
    reason: "سبب الطلب (اختياري)",
    submit: "تقديم الطلب",
    submitting: "جاري الإرسال…",
    success: "تم استلام طلبك",
    requestId: "رقم الطلب",
    sla: "نرد خلال",
    days: "أيام عمل",
    error: "حدث خطأ. حاول مرة أخرى أو راسلنا على privacy@dealix.sa",
  },
  en: {
    email: "Registered email address",
    emailHint: "The same email you used to sign up or to contact us.",
    requestType: "Request type",
    types: {
      access: "Access — export all data we hold about you",
      rectify: "Rectify — correct a specific field",
      port: "Port — exportable copy for another controller",
      erase: "Erase — delete your data (with statutory retention exceptions)",
    },
    field: "Field name to correct",
    newValue: "Correct new value",
    reason: "Reason for the request (optional)",
    submit: "Submit request",
    submitting: "Submitting…",
    success: "Request received",
    requestId: "Request ID",
    sla: "We reply within",
    days: "business days",
    error: "Something went wrong. Please try again or email privacy@dealix.sa",
  },
} as const;

export function DsarForm({ locale }: DsarFormProps) {
  const isAr = locale === "ar";
  const L = isAr ? LABELS.ar : LABELS.en;

  const [email, setEmail] = useState("");
  const [requestType, setRequestType] = useState<RequestType>("access");
  const [reason, setReason] = useState("");
  const [field, setField] = useState("");
  const [newValue, setNewValue] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<SubmissionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const isRectify = requestType === "rectify";

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    const body: Record<string, string> = {
      email,
      request_type: requestType,
    };
    if (reason) body.reason = reason;
    if (isRectify) {
      body.rectification_field = field;
      body.rectification_new_value = newValue;
    }

    try {
      const res = await fetch(`${API_BASE}/api/v1/pdpl/dsar/request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        const detail = await res.text();
        throw new Error(detail || `HTTP ${res.status}`);
      }
      const data: SubmissionResult = await res.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : L.error);
    } finally {
      setSubmitting(false);
    }
  }

  if (result) {
    return (
      <section className="mt-10 rounded-lg border border-primary/40 bg-primary/5 p-6">
        <h2 className="text-xl font-semibold">{L.success} ✓</h2>
        <dl className="mt-4 space-y-2 text-sm">
          <div>
            <dt className="inline font-medium">{L.requestId}: </dt>
            <dd className="inline font-mono text-primary">{result.request_id}</dd>
          </div>
          {result.sla_business_days !== undefined && (
            <div>
              <dt className="inline font-medium">{L.sla}: </dt>
              <dd className="inline">{result.sla_business_days} {L.days}</dd>
            </div>
          )}
          {result.next_step && (
            <p className="mt-4 text-muted-foreground leading-relaxed">{result.next_step}</p>
          )}
        </dl>
      </section>
    );
  }

  return (
    <form onSubmit={submit} className="mt-10 space-y-6">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">{L.email}</label>
        <input
          id="email"
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="mt-2 w-full rounded-md border border-border bg-card/40 px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
          placeholder="founder@example.sa"
        />
        <p className="mt-1 text-xs text-muted-foreground">{L.emailHint}</p>
      </div>

      <div>
        <label htmlFor="requestType" className="block text-sm font-medium">{L.requestType}</label>
        <select
          id="requestType"
          required
          value={requestType}
          onChange={(e) => setRequestType(e.target.value as RequestType)}
          className="mt-2 w-full rounded-md border border-border bg-card/40 px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
        >
          {REQUEST_TYPES.map((t) => (
            <option key={t} value={t}>{L.types[t]}</option>
          ))}
        </select>
      </div>

      {isRectify && (
        <div className="space-y-4 rounded-md border border-border/60 bg-card/20 p-4">
          <div>
            <label htmlFor="field" className="block text-sm font-medium">{L.field}</label>
            <input
              id="field"
              type="text"
              required={isRectify}
              maxLength={128}
              value={field}
              onChange={(e) => setField(e.target.value)}
              className="mt-2 w-full rounded-md border border-border bg-card/40 px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
          <div>
            <label htmlFor="newValue" className="block text-sm font-medium">{L.newValue}</label>
            <input
              id="newValue"
              type="text"
              required={isRectify}
              maxLength={2000}
              value={newValue}
              onChange={(e) => setNewValue(e.target.value)}
              className="mt-2 w-full rounded-md border border-border bg-card/40 px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
        </div>
      )}

      <div>
        <label htmlFor="reason" className="block text-sm font-medium">{L.reason}</label>
        <textarea
          id="reason"
          maxLength={2000}
          rows={3}
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          className="mt-2 w-full rounded-md border border-border bg-card/40 px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
        />
      </div>

      {error && (
        <div className="rounded-md border border-destructive/50 bg-destructive/10 px-4 py-3 text-sm text-destructive">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={submitting}
        className="inline-flex items-center justify-center rounded-md bg-primary px-6 py-2.5 text-sm font-medium text-primary-foreground transition hover:bg-primary/90 disabled:opacity-50"
      >
        {submitting ? L.submitting : L.submit}
      </button>
    </form>
  );
}
