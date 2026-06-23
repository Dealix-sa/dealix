"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import {
  ShieldAlert,
  ShieldCheck,
  Mail,
  MessageCircle,
  Smartphone,
  AlertTriangle,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

type DraftStatus = "draft" | "review" | "approved" | "rejected";
type Channel = "email" | "whatsapp" | "sms";

interface DraftRow {
  id: string;
  channel: Channel;
  titleAr: string;
  titleEn: string;
  status: DraftStatus;
  missingGatesAr: string[];
  missingGatesEn: string[];
}

interface ChannelReadiness {
  channel: Channel;
  labelAr: string;
  labelEn: string;
  icon: React.ComponentType<{ className?: string }>;
  gates: { key: string; labelAr: string; labelEn: string; ready: boolean }[];
}

const STATUS_VARIANT: Record<DraftStatus, "outline" | "blue" | "emerald" | "red"> = {
  draft: "outline",
  review: "blue",
  approved: "emerald",
  rejected: "red",
};

const STATUS_LABEL_AR: Record<DraftStatus, string> = {
  draft: "مسودة",
  review: "قيد المراجعة",
  approved: "موافق",
  rejected: "مرفوض",
};

const STATUS_LABEL_EN: Record<DraftStatus, string> = {
  draft: "Draft",
  review: "Review",
  approved: "Approved",
  rejected: "Rejected",
};

const CHANNEL_READINESS: ChannelReadiness[] = [
  {
    channel: "email",
    labelAr: "الإيميل",
    labelEn: "Email",
    icon: Mail,
    gates: [
      { key: "spf", labelAr: "SPF مُعدّ", labelEn: "SPF configured", ready: false },
      { key: "dkim", labelAr: "DKIM مُعدّ", labelEn: "DKIM configured", ready: false },
      { key: "dmarc", labelAr: "DMARC مُعدّ", labelEn: "DMARC configured", ready: false },
    ],
  },
  {
    channel: "whatsapp",
    labelAr: "واتساب",
    labelEn: "WhatsApp",
    icon: MessageCircle,
    gates: [
      { key: "optin", labelAr: "موافقة العميل (opt-in)", labelEn: "Customer opt-in", ready: false },
      { key: "template", labelAr: "قالب معتمد", labelEn: "Approved template", ready: false },
      { key: "window24h", labelAr: "نافذة ٢٤ ساعة", labelEn: "24h window", ready: false },
    ],
  },
  {
    channel: "sms",
    labelAr: "الرسائل النصية",
    labelEn: "SMS",
    icon: Smartphone,
    gates: [
      { key: "consent", labelAr: "موافقة صريحة", labelEn: "Explicit consent", ready: false },
      { key: "stop", labelAr: "آلية STOP", labelEn: "STOP mechanism", ready: false },
      { key: "optout", labelAr: "إلغاء الاشتراك", labelEn: "Opt-out", ready: false },
    ],
  },
];

// No fake drafts — empty by default. Shows the review queue structure.
const INITIAL_DRAFTS: DraftRow[] = [];

export function OutreachReviewQueue() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [drafts, setDrafts] = useState<DraftRow[]>(INITIAL_DRAFTS);

  const setStatus = (id: string, status: DraftStatus) => {
    setDrafts((prev) => prev.map((d) => (d.id === id ? { ...d, status } : d)));
  };

  const emptyText = isAr ? "لا توجد مسودات للمراجعة" : "No drafts to review";
  const emptyHint = isAr
    ? "ستظهر المسودات هنا عند تفعيل منتجات التواصل. لا إرسال قبل الموافقة وبوابات الأمان."
    : "Drafts appear here when outreach products are active. No send before approval and safety gates.";

  return (
    <div className="space-y-6">
      {/* Disabled warning */}
      <div className="flex items-start gap-3 rounded-xl border border-red-500/30 bg-red-500/5 p-4">
        <ShieldAlert className="size-5 text-red-400 shrink-0 mt-0.5" />
        <div className="text-sm text-red-200/90">
          {isAr
            ? "الاتصال الخارجي معطّل (OUTBOUND_MODE=draft_only). لا يوجد زر 'إرسال الآن' — استخدم 'موافقة على المسودة' أو 'مراجعة'."
            : "Outbound is disabled (OUTBOUND_MODE=draft_only). There is no 'send now' button — use 'Approve draft' or 'Review'."}
        </div>
      </div>

      {/* Channel readiness */}
      <div className="grid gap-4 md:grid-cols-3">
        {CHANNEL_READINESS.map((ch) => {
          const allReady = ch.gates.every((g) => g.ready);
          const Icon = ch.icon;
          return (
            <Card key={ch.channel}>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center gap-2">
                    <Icon className="size-4" />
                    {isAr ? ch.labelAr : ch.labelEn}
                  </span>
                  <Badge variant={allReady ? "emerald" : "red"}>
                    {allReady
                      ? isAr ? "جاهز" : "Ready"
                      : isAr ? "غير جاهز" : "Not ready"}
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  {ch.gates.map((g) => (
                    <li key={g.key} className="flex items-center justify-between">
                      <span className="text-muted-foreground">{isAr ? g.labelAr : g.labelEn}</span>
                      {g.ready ? (
                        <ShieldCheck className="size-4 text-emerald-400" />
                      ) : (
                        <AlertTriangle className="size-4 text-amber-400" />
                      )}
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Draft queue */}
      <Card>
        <CardHeader>
          <CardTitle>{isAr ? "طابور المراجعة" : "Review queue"}</CardTitle>
        </CardHeader>
        <CardContent>
          {drafts.length === 0 ? (
            <div className="rounded-lg border border-dashed border-border p-8 text-center">
              <p className="text-sm font-medium text-muted-foreground">{emptyText}</p>
              <p className="mt-1 text-xs text-muted-foreground/70 max-w-md mx-auto">{emptyHint}</p>
            </div>
          ) : (
            <div className="space-y-3">
              {drafts.map((d) => {
                const hasMissing = d.missingGatesAr.length > 0;
                return (
                  <div key={d.id} className="rounded-lg border border-border p-4">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div>
                        <span className="font-medium">{isAr ? d.titleAr : d.titleEn}</span>
                        <Badge variant="outline" className="ml-2">
                          {isAr
                            ? CHANNEL_READINESS.find((c) => c.channel === d.channel)?.labelAr
                            : CHANNEL_READINESS.find((c) => c.channel === d.channel)?.labelEn}
                        </Badge>
                      </div>
                      <Badge variant={STATUS_VARIANT[d.status]}>
                        {isAr ? STATUS_LABEL_AR[d.status] : STATUS_LABEL_EN[d.status]}
                      </Badge>
                    </div>

                    {hasMissing && (
                      <div className="mt-2 flex items-start gap-2 rounded-md bg-amber-500/5 p-2 text-xs text-amber-200/90">
                        <AlertTriangle className="size-3.5 shrink-0 mt-0.5" />
                        <span>
                          {isAr
                            ? `بوابات ناقصة: ${d.missingGatesAr.join("، ")}`
                            : `Missing gates: ${d.missingGatesEn.join(", ")}`}
                        </span>
                      </div>
                    )}

                    <div className="mt-3 flex gap-2">
                      <Button
                        size="sm"
                        variant="emerald"
                        disabled={hasMissing}
                        onClick={() => setStatus(d.id, "approved")}
                      >
                        {isAr ? "موافقة على المسودة" : "Approve draft"}
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setStatus(d.id, "review")}
                      >
                        {isAr ? "مراجعة" : "Review"}
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => setStatus(d.id, "rejected")}
                      >
                        {isAr ? "رفض" : "Reject"}
                      </Button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

export default OutreachReviewQueue;