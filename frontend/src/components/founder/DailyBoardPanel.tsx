"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

interface Candidate {
  name: string;
  sector?: string;
  domain?: string;
}
interface BoardLead {
  rank: number;
  candidate: Candidate;
  composite_score: number;
  priority: string;
  why_now_ar: string;
  why_now_en: string;
  recommended_action_ar: string;
  recommended_action_en: string;
  action_mode: string;
  blockers?: string[];
}
interface Board {
  on_date: string;
  season_context?: { season?: string; implication_ar?: string; implication_en?: string; recommended_offer_pivot?: string };
  candidates_count: number;
  leads_returned: number;
  top_leads: BoardLead[];
  bilingual_summary?: { ar?: string; en?: string };
  next_founder_action?: string;
}
interface BoardResponse {
  ok: boolean;
  generated: boolean;
  board_date?: string;
  board: Board | null;
  hint_ar?: string;
  hint_en?: string;
  next_action_ar?: string;
  next_action_en?: string;
}

const PRIORITY_STYLE: Record<string, string> = {
  P0_NOW: "border-red-500 text-red-600 bg-red-50 dark:bg-red-950/30",
  P1_THIS_WEEK: "border-amber-500 text-amber-600 bg-amber-50 dark:bg-amber-950/30",
  P2_NURTURE: "border-blue-400 text-blue-600 bg-blue-50 dark:bg-blue-950/30",
  P3_LOW_PRIORITY: "border-border text-muted-foreground",
  BLOCKED: "border-red-700 text-red-700 bg-red-100 dark:bg-red-950/50",
};

export function DailyBoardPanel() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [resp, setResp] = useState<BoardResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getFounderDailyBoard()
      .then((r) => setResp(r.data as BoardResponse))
      .catch(() => setResp(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary/30 border-t-primary" />
      </div>
    );
  }

  if (!resp || !resp.generated || !resp.board) {
    return (
      <Card className="p-8 text-center text-muted-foreground" dir={isAr ? "rtl" : "ltr"}>
        <p className="font-semibold mb-2">{isAr ? "لا توجد لوحة بعد" : "No board yet"}</p>
        <p className="text-sm">{(isAr ? resp?.hint_ar : resp?.hint_en) || (isAr ? "شغّل المحرّك اليومي." : "Run the daily engine.")}</p>
      </Card>
    );
  }

  const b = resp.board;
  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      <Card>
        <CardHeader>
          <div className="flex flex-wrap items-center justify-between gap-2">
            <CardTitle className="text-lg">
              {isAr ? "لوحة اليوم" : "Today's board"} — {b.on_date}
            </CardTitle>
            <Badge variant="outline">
              {b.leads_returned}/{b.candidates_count} {isAr ? "مرشّح" : "candidates"}
            </Badge>
          </div>
          {b.season_context?.season && (
            <p className="text-sm text-muted-foreground mt-1">
              {isAr ? "الموسم:" : "Season:"} <code className="text-xs">{b.season_context.season}</code>
              {" — "}
              {isAr ? b.season_context.implication_ar : b.season_context.implication_en}
            </p>
          )}
        </CardHeader>
        <CardContent>
          <p className="text-sm">{isAr ? b.bilingual_summary?.ar : b.bilingual_summary?.en}</p>
          {b.next_founder_action && (
            <div className="mt-3 rounded-lg bg-primary/5 border border-primary/20 p-3 text-sm">
              <span className="font-semibold">{isAr ? "الخطوة التالية: " : "Next action: "}</span>
              {b.next_founder_action}
            </div>
          )}
          <p className="mt-3 text-xs text-muted-foreground">
            {isAr
              ? "كل المخرجات مسودّات — اعتمد ثم أرسل يدوياً. لا إرسال تلقائي."
              : "All outputs are drafts — approve, then send manually. No auto-send."}
          </p>
        </CardContent>
      </Card>

      <div className="space-y-3">
        {b.top_leads.map((lead) => (
          <Card key={lead.rank} className="p-4">
            <div className="flex items-start gap-3">
              <span className="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-bold text-primary">
                {lead.rank}
              </span>
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <p className="font-semibold truncate">{lead.candidate.name}</p>
                  <Badge variant="outline" className={`text-xs ${PRIORITY_STYLE[lead.priority] || ""}`}>
                    {lead.priority}
                  </Badge>
                  <Badge variant="secondary" className="text-xs">{lead.action_mode}</Badge>
                  {lead.candidate.sector && (
                    <span className="text-xs text-muted-foreground">{lead.candidate.sector}</span>
                  )}
                </div>
                <p className="mt-1 text-sm text-muted-foreground">
                  {isAr ? lead.why_now_ar : lead.why_now_en}
                </p>
                <p className="mt-1 text-sm">
                  <span className="font-medium">{isAr ? "موصى: " : "Recommended: "}</span>
                  {isAr ? lead.recommended_action_ar : lead.recommended_action_en}
                </p>
                {lead.blockers && lead.blockers.length > 0 && (
                  <p className="mt-1 text-xs text-red-500">⚠️ {lead.blockers.join(", ")}</p>
                )}
              </div>
              <span className="flex-shrink-0 text-xs text-muted-foreground">
                {(lead.composite_score * 100).toFixed(0)}
              </span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
