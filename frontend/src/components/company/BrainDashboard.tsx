"use client";

import { useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";
import {
  BrainCircuit,
  CalendarClock,
  FileText,
  ListChecks,
  AlertTriangle,
  ArrowLeft,
  ArrowRight,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface BrainDecision {
  id: string;
  date: string;
  titleAr: string;
  titleEn: string;
  summaryAr: string;
  summaryEn: string;
  sourceAr: string;
  sourceEn: string;
}

interface RadarItem {
  id: string;
  horizonDays: number;
  titleAr: string;
  titleEn: string;
  kind: "risk" | "opportunity";
}

interface PlanItem {
  id: string;
  day: number;
  textAr: string;
  textEn: string;
  done: boolean;
}

export function BrainDashboard() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;

  // No fake live company data — empty state by default. UI shows the structure.
  const [decisions] = useState<BrainDecision[]>([]);
  const [radar] = useState<RadarItem[]>([]);
  const [memoAr] = useState<string>("");
  const [memoEn] = useState<string>("");
  const [plan] = useState<PlanItem[]>([]);

  const emptyText = isAr ? "لا توجد بيانات بعد" : "No data yet";
  const emptyHint = isAr
    ? "سيبدأ التسجيل بعد ربط Company Brain بمصادر البيانات."
    : "Logging starts after Company Brain is connected to data sources.";

  return (
    <div className="space-y-6">
      {/* Outbound / safety banner */}
      <div className="flex items-start gap-3 rounded-xl border border-amber-500/30 bg-amber-500/5 p-4">
        <AlertTriangle className="size-5 text-amber-400 shrink-0 mt-0.5" />
        <div className="text-sm text-amber-200/90">
          {isAr
            ? "Company Brain يعمل بوضع القراءة فقط. لا إجراء خارجي دون موافقتك."
            : "Company Brain runs in read-only mode. No external action without your approval."}
        </div>
      </div>

      {/* Latest daily decision */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BrainCircuit className="size-5 text-gold-400" />
            {isAr ? "القرار اليومي الأخير" : "Latest daily decision"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {decisions.length === 0 ? (
            <EmptyState text={emptyText} hint={emptyHint} />
          ) : (
            <ul className="space-y-3">
              {decisions.map((d) => (
                <li key={d.id} className="rounded-lg border border-border p-3">
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{isAr ? d.titleAr : d.titleEn}</span>
                    <Badge variant="outline">{d.date}</Badge>
                  </div>
                  <p className="mt-1 text-sm text-muted-foreground">
                    {isAr ? d.summaryAr : d.summaryEn}
                  </p>
                  <p className="mt-1 text-xs text-muted-foreground/70">
                    {isAr ? `المصدر: ${d.sourceAr}` : `Source: ${d.sourceEn}`}
                  </p>
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Future radar */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CalendarClock className="size-5 text-emerald-400" />
              {isAr ? "رادار المستقبل" : "Future radar"}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {radar.length === 0 ? (
              <EmptyState text={emptyText} hint={emptyHint} />
            ) : (
              <ul className="space-y-2">
                {radar.map((r) => (
                  <li key={r.id} className="flex items-center justify-between text-sm">
                    <span>{isAr ? r.titleAr : r.titleEn}</span>
                    <Badge variant={r.kind === "risk" ? "red" : "emerald"}>
                      {isAr ? `${r.horizonDays} يوم` : `${r.horizonDays}d`}
                    </Badge>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>

        {/* Board memo */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="size-5 text-blue-400" />
              {isAr ? "مذكرة المجلس" : "Board memo"}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {(isAr ? memoAr : memoEn).length === 0 ? (
              <EmptyState text={emptyText} hint={emptyHint} />
            ) : (
              <p className="text-sm text-muted-foreground whitespace-pre-line">
                {isAr ? memoAr : memoEn}
              </p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* 30-day plan */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ListChecks className="size-5 text-gold-400" />
            {isAr ? "خطة ٣٠ يوماً" : "30-day plan"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {plan.length === 0 ? (
            <EmptyState text={emptyText} hint={emptyHint} />
          ) : (
            <ul className="space-y-2">
              {plan.map((p) => (
                <li key={p.id} className="flex items-center gap-3 text-sm">
                  <Badge variant={p.done ? "emerald" : "outline"}>
                    {isAr ? `يوم ${p.day}` : `Day ${p.day}`}
                  </Badge>
                  <span className={p.done ? "line-through text-muted-foreground" : ""}>
                    {isAr ? p.textAr : p.textEn}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>

      {/* Links to brain reports */}
      <div className="flex flex-wrap gap-3">
        <Button asChild variant="outline">
          <Link href={`${base}/products/company-brain`}>
            {isAr ? "عن منتج Company Brain" : "About Company Brain product"}
            {isAr ? <ArrowLeft className="size-4" /> : <ArrowRight className="size-4" />}
          </Link>
        </Button>
        <Button asChild variant="outline">
          <Link href={`${base}/book-call`}>
            {isAr ? "احجز تشخيص" : "Book a diagnostic"}
          </Link>
        </Button>
      </div>
    </div>
  );
}

function EmptyState({ text, hint }: { text: string; hint: string }) {
  return (
    <div className="rounded-lg border border-dashed border-border p-6 text-center">
      <p className="text-sm font-medium text-muted-foreground">{text}</p>
      <p className="mt-1 text-xs text-muted-foreground/70">{hint}</p>
    </div>
  );
}

export default BrainDashboard;