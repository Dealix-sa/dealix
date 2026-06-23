"use client";

import { useLocale } from "next-intl";
import { FileText, Inbox } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

type ProposalStatus = "draft" | "sent" | "negotiating" | "won" | "lost";

interface Proposal {
  id: string;
  clientName: string;
  valueSAR: number;
  stage: ProposalStatus;
}

const STATUS_VARIANT: Record<ProposalStatus, "outline" | "blue" | "gold" | "emerald" | "red"> = {
  draft: "outline",
  sent: "blue",
  negotiating: "gold",
  won: "emerald",
  lost: "red",
};

const STATUS_LABEL_AR: Record<ProposalStatus, string> = {
  draft: "مسودة",
  sent: "مُرسل",
  negotiating: "تفاوض",
  won: "فوز",
  lost: "خسارة",
};

const STATUS_LABEL_EN: Record<ProposalStatus, string> = {
  draft: "Draft",
  sent: "Sent",
  negotiating: "Negotiating",
  won: "Won",
  lost: "Lost",
};

// No fake client data — empty by default.
const PROPOSALS: Proposal[] = [];

export function ProposalQueueContent() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const emptyTitle = isAr ? "لا توجد عروض بعد" : "No proposals yet";
  const emptyHint = isAr
    ? "عندما تنشئ عروضاً ستظهر هنا بالحالة والقيمة والمرحلة. لا بيانات وهمية."
    : "When you create proposals they'll appear here with status, value, and stage. No fake data.";

  const totalValue = PROPOSALS.reduce((sum, p) => sum + p.valueSAR, 0);

  return (
    <div className="space-y-6">
      {/* Summary */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="py-5">
            <p className="text-sm text-muted-foreground">{isAr ? "إجمالي العروض" : "Total proposals"}</p>
            <p className="text-2xl font-bold">{PROPOSALS.length}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-5">
            <p className="text-sm text-muted-foreground">{isAr ? "القيمة الإجمالية" : "Total value"}</p>
            <p className="text-2xl font-bold">
              {new Intl.NumberFormat(isAr ? "ar-SA" : "en-US").format(totalValue)}{" "}
              {isAr ? "ر.س" : "SAR"}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-5">
            <p className="text-sm text-muted-foreground">{isAr ? "الفوز" : "Won"}</p>
            <p className="text-2xl font-bold">
              {PROPOSALS.filter((p) => p.stage === "won").length}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Queue */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="size-5 text-gold-400" />
            {isAr ? "طابور العروض" : "Proposal queue"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {PROPOSALS.length === 0 ? (
            <div className="rounded-lg border border-dashed border-border p-10 text-center">
              <Inbox className="mx-auto size-10 text-muted-foreground/50 mb-3" />
              <p className="text-sm font-medium text-muted-foreground">{emptyTitle}</p>
              <p className="mt-1 text-xs text-muted-foreground/70 max-w-md mx-auto">{emptyHint}</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border text-muted-foreground">
                    <th className="py-2 text-start font-medium">{isAr ? "العميل" : "Client"}</th>
                    <th className="py-2 text-start font-medium">{isAr ? "القيمة" : "Value"}</th>
                    <th className="py-2 text-start font-medium">{isAr ? "المرحلة" : "Stage"}</th>
                  </tr>
                </thead>
                <tbody>
                  {PROPOSALS.map((p) => (
                    <tr key={p.id} className="border-b border-border/50">
                      <td className="py-3">{p.clientName}</td>
                      <td className="py-3">
                        {new Intl.NumberFormat(isAr ? "ar-SA" : "en-US").format(p.valueSAR)}{" "}
                        {isAr ? "ر.س" : "SAR"}
                      </td>
                      <td className="py-3">
                        <Badge variant={STATUS_VARIANT[p.stage]}>
                          {isAr ? STATUS_LABEL_AR[p.stage] : STATUS_LABEL_EN[p.stage]}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

export default ProposalQueueContent;