"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const CHECKLIST = [
  "Scope named, time-bounded, measurable",
  "Pricing recorded against docs/revenue/PRICING_AND_PACKAGING.md",
  "Discount maps to a documented reason (logo / multi-year / volume)",
  "Payment terms align with docs/revenue/INVOICE_FLOW.md",
  "Trust gates pass — docs/00_constitution/NON_NEGOTIABLES.md",
  "Close plan exists — docs/revenue/CLOSE_PLAN_TEMPLATE.md",
];

export function DealDeskPanel() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Deal Desk</CardTitle>
          <CardDescription>
            Approves any deal departing from the standard offer. Records intent
            only — money movement still flows through docs/revenue/INVOICE_FLOW.md
            and Moyasar verifier.
          </CardDescription>
        </CardHeader>
        <CardContent className="text-sm space-y-3">
          <div>
            <div className="font-medium mb-2">Approval checklist</div>
            <ul className="space-y-1">
              {CHECKLIST.map((item, i) => (
                <li key={i} className="flex gap-2">
                  <span>•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="text-xs text-muted-foreground">
            Walk:{" "}
            <Link className="underline" href="/strategy">
              Strategy
            </Link>{" "}
            ·{" "}
            <Link className="underline" href="/capital-allocation">
              Capital Allocation
            </Link>{" "}
            · docs/revenue/DEAL_DESK_SYSTEM.md
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
