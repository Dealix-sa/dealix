"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

type Decision = { title_ar?: string; title_en?: string; priority?: string; confidence?: number };
type ProofSummary = { score?: number; tier?: string; pack_ready?: boolean };
type PaymentState = { status?: string; plan?: string; mrr_sar?: number; next_renewal_at?: string };
type Deliverable = { name?: string; status?: string; description?: string };

type PortalData = {
  customer_handle: string;
  promise_ar?: string;
  promise_en?: string;
  sections?: {
    "5_deliverables"?: { deliverables?: Deliverable[]; status?: string };
    "6_proof_pack"?: { download_url?: string; available?: boolean; sections?: string[] };
    "2_seven_day_plan"?: { status?: string; days_remaining?: number; current_phase?: string };
    "8_next_decision"?: { decision?: string; cta?: string };
  };
  enriched_view?: {
    next_3_decisions?: { decisions?: Decision[] };
    proof_summary?: ProofSummary;
    payment_state?: PaymentState;
  };
};

const API_BASE = typeof window !== "undefined"
  ? (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000")
  : "http://localhost:8000";

export default function CustomerPortalPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [handle, setHandle] = useState("");
  const [data, setData] = useState<PortalData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Auto-load from URL query param if present
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const h = params.get("handle");
    if (h) {
      setHandle(h);
      loadPortal(h);
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  async function loadPortal(h: string) {
    if (!h.trim()) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/api/v1/customer-portal/${encodeURIComponent(h.trim())}`);
      if (!res.ok) throw new Error(`status ${res.status}`);
      setData(await res.json() as PortalData);
    } catch (e) {
      setError(isAr ? "تعذّر تحميل بيانات بوابة العميل." : "Could not load portal data.");
    } finally {
      setLoading(false);
    }
  }

  const proof = data?.enriched_view?.proof_summary;
  const proofSection = data?.sections?.["6_proof_pack"];
  const sprintSection = data?.sections?.["2_seven_day_plan"];
  const deliverables = data?.sections?.["5_deliverables"]?.deliverables ?? [];
  const decisions: Decision[] = data?.enriched_view?.next_3_decisions?.decisions ?? [];
  const payment = data?.enriched_view?.payment_state;
  const nextAction = data?.sections?.["8_next_decision"];

  function proofTierColor(tier?: string): "default" | "secondary" | "outline" {
    if (!tier) return "secondary";
    if (tier.includes("strong")) return "default";
    if (tier.includes("moderate")) return "outline";
    return "secondary";
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-2xl mx-auto px-6 py-10 space-y-8" dir={isAr ? "rtl" : "ltr"}>
        {/* Header */}
        <div className={isAr ? "text-right" : ""}>
          <h1 className="text-2xl font-bold">
            {isAr ? "بوابة العميل" : "Customer Portal"}
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {isAr ? "تقدّمك، نتائجك، وخطواتك التالية." : "Your progress, results, and next steps."}
          </p>
        </div>

        {/* Handle input */}
        {!data && (
          <Card className="p-5">
            <p className="text-sm font-medium mb-3">
              {isAr ? "أدخل معرّف حسابك" : "Enter your account handle"}
            </p>
            <div className="flex gap-2">
              <Input
                value={handle}
                onChange={(e) => setHandle(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && void loadPortal(handle)}
                placeholder={isAr ? "مثال: acme-sa" : "e.g. acme-sa"}
                dir="ltr"
                className="flex-1"
              />
              <Button onClick={() => void loadPortal(handle)} disabled={loading || !handle.trim()}>
                {loading ? (isAr ? "..." : "...") : (isAr ? "تحميل" : "Load")}
              </Button>
            </div>
            {error && <p className="mt-2 text-xs text-destructive">{error}</p>}
          </Card>
        )}

        {data && (
          <>
            {/* Sprint status */}
            <Card className="p-5 border-primary/20">
              <div className="flex items-center justify-between gap-2 flex-wrap">
                <div>
                  <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">
                    {isAr ? "حالة Sprint" : "Sprint Status"}
                  </p>
                  <p className="text-sm font-medium">
                    {sprintSection?.current_phase
                      ? sprintSection.current_phase
                      : (isAr ? "تحت التحليل" : "Under analysis")}
                  </p>
                </div>
                <Badge variant={sprintSection?.status === "completed" ? "default" : "outline"}>
                  {sprintSection?.status === "completed"
                    ? (isAr ? "مكتمل" : "Completed")
                    : sprintSection?.days_remaining != null
                      ? `${sprintSection.days_remaining}d ${isAr ? "متبقي" : "remaining"}`
                      : (isAr ? "جارٍ" : "In progress")}
                </Badge>
              </div>
              {deliverables.length > 0 && (
                <div className="mt-4 space-y-2">
                  {deliverables.slice(0, 4).map((d, i) => (
                    <div key={i} className="flex items-center gap-2 text-sm">
                      <span className={d.status === "done" ? "text-green-500" : "text-muted-foreground"}>
                        {d.status === "done" ? "✓" : "○"}
                      </span>
                      <span className={d.status === "done" ? "text-foreground" : "text-muted-foreground"}>
                        {d.name ?? "—"}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </Card>

            {/* Proof Pack */}
            <Card className="p-5">
              <div className="flex items-center justify-between gap-3 flex-wrap">
                <div>
                  <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">
                    Proof Pack
                  </p>
                  <div className="flex items-center gap-2">
                    {proof?.score != null && (
                      <Badge variant={proofTierColor(proof.tier)}>
                        {isAr ? "درجة" : "Score"}: {proof.score.toFixed(1)}
                      </Badge>
                    )}
                    {proof?.tier && (
                      <span className="text-xs text-muted-foreground">{proof.tier.replace(/_/g, " ")}</span>
                    )}
                  </div>
                </div>
                {proofSection?.available ? (
                  <Button asChild size="sm">
                    <a href={proofSection.download_url ?? `${API_BASE}/api/v1/sprint/render/pdf`} download>
                      {isAr ? "⬇ تحميل PDF" : "⬇ Download PDF"}
                    </a>
                  </Button>
                ) : (
                  <Badge variant="outline" className="text-xs">
                    {isAr ? "قريباً" : "Coming soon"}
                  </Badge>
                )}
              </div>
              {proofSection?.sections && proofSection.sections.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-1">
                  {proofSection.sections.slice(0, 5).map((s, i) => (
                    <Badge key={i} variant="secondary" className="text-xs">{s}</Badge>
                  ))}
                </div>
              )}
            </Card>

            {/* Top 3 Decisions */}
            {decisions.length > 0 && (
              <div>
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3">
                  {isAr ? "أهم ٣ قرارات" : "Top 3 Decisions"}
                </p>
                <div className="space-y-2">
                  {decisions.slice(0, 3).map((d, i) => (
                    <Card key={i} className="p-4 border-border/50">
                      <div className="flex items-start gap-3">
                        <span className="text-sm font-bold text-primary/50 shrink-0">{i + 1}</span>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium">
                            {isAr ? (d.title_ar ?? d.title_en) : (d.title_en ?? d.title_ar)}
                          </p>
                        </div>
                        {d.priority && (
                          <Badge variant={d.priority === "high" ? "destructive" : "outline"} className="text-xs shrink-0">
                            {d.priority}
                          </Badge>
                        )}
                      </div>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {/* Subscription / Payment state */}
            {payment?.status && (
              <Card className="p-4 border-border/50">
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                  {isAr ? "الاشتراك" : "Subscription"}
                </p>
                <div className="flex items-center gap-3 flex-wrap">
                  <Badge variant={payment.status === "active" ? "default" : "secondary"}>
                    {payment.status}
                  </Badge>
                  {payment.plan && <span className="text-sm">{payment.plan}</span>}
                  {payment.mrr_sar != null && payment.mrr_sar > 0 && (
                    <span className="text-sm font-medium">{payment.mrr_sar.toLocaleString()} SAR/mo</span>
                  )}
                </div>
              </Card>
            )}

            {/* Upgrade CTA */}
            <Card className="p-5 border-primary/30 bg-primary/5">
              <p className="text-sm font-semibold mb-1">
                {isAr ? "ارتقِ إلى Retainer الشهري" : "Upgrade to Monthly Retainer"}
              </p>
              <p className="text-xs text-muted-foreground mb-3">
                {isAr
                  ? "٢٩٩٩ ر.س/شهر — عمليات إيراد محكومة مستمرة مع مراجعة أسبوعية."
                  : "2,999 SAR/month — ongoing governed revenue ops with weekly review."}
              </p>
              <Button asChild size="sm">
                <Link href={`/${locale}/offer`}>
                  {isAr ? "اعرف المزيد ←" : "Learn More →"}
                </Link>
              </Button>
            </Card>

            {/* Promise footer */}
            <p className="text-xs text-muted-foreground text-center">
              {isAr ? data.promise_ar : data.promise_en}
            </p>

            {/* Reset */}
            <button
              className="text-xs text-muted-foreground underline"
              onClick={() => { setData(null); setHandle(""); }}
            >
              {isAr ? "تغيير الحساب" : "Change account"}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
