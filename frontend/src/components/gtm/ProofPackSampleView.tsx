"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

type SectionRow = { id: string; title_ar: string; status?: string };

type SamplePayload = {
  title_ar?: string;
  title_en?: string;
  outline?: string[];
  disclaimer_ar?: string;
  disclaimer_en?: string;
  draft?: { sections?: SectionRow[] };
};

export function ProofPackSampleView() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [data, setData] = useState<SamplePayload | null>(null);

  useEffect(() => {
    const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${base}/api/v1/public/proof-pack/sample?locale=${locale}`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => setData(null));
  }, [locale]);

  const rows: SectionRow[] =
    data?.draft?.sections ??
    (data?.outline ?? []).map((t, i) => ({ id: String(i), title_ar: t, status: "pending_inputs" }));

  return (
    <div className="max-w-2xl mx-auto space-y-6" dir={isAr ? "rtl" : "ltr"}>
      <header className={isAr ? "text-right" : ""}>
        <h1 className="text-2xl font-bold">
          {isAr ? data?.title_ar ?? "عيّنة Proof Pack" : data?.title_en ?? "Proof Pack sample"}
        </h1>
        <p className="mt-2 text-sm text-muted-foreground">
          {isAr ? data?.disclaimer_ar : data?.disclaimer_en}
        </p>
      </header>

      <Card className="p-4 space-y-3">
        {rows.map((s) => (
          <div key={s.id} className="border-b border-border/50 pb-2 last:border-0">
            <p className="font-medium">{s.title_ar}</p>
            {s.status && <p className="text-xs text-muted-foreground">{s.status}</p>}
          </div>
        ))}
      </Card>

      <div className="flex gap-2 flex-wrap">
        <Button asChild>
          <Link href={`/${locale}/risk-score`}>Risk Score</Link>
        </Button>
        <Button asChild variant="outline">
          <Link href={`/${locale}/dealix-diagnostic`}>
            {isAr ? "طلب Diagnostic" : "Request Diagnostic"}
          </Link>
        </Button>
      </div>
    </div>
  );
}
