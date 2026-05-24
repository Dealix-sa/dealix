"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const STAGES = [
  "discovery",
  "validation",
  "procurement",
  "security_review",
  "proposal",
  "negotiation",
  "signed",
];

export function EnterpriseSalesPanel() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Enterprise Sales Motion</CardTitle>
          <CardDescription>
            Discovery → Validation → Procurement → Security Review → Proposal
            → Negotiation → Signed. Every stage has an entry and exit condition.
          </CardDescription>
        </CardHeader>
        <CardContent className="text-sm space-y-3">
          <ol className="list-decimal ml-5 space-y-1">
            {STAGES.map((stage) => (
              <li key={stage}>{stage}</li>
            ))}
          </ol>
          <div className="text-xs text-muted-foreground">
            Walk: docs/enterprise/ENTERPRISE_SALES_MOTION.md ·
            docs/enterprise/MULTI_THREADING_SYSTEM.md ·
            docs/enterprise/SECURITY_REVIEW_PACKET.md
          </div>
          <div className="flex gap-3 text-xs">
            <Link className="underline" href="/deal-desk">
              Deal Desk
            </Link>
            <Link className="underline" href="/strategy">
              Strategy
            </Link>
            <Link className="underline" href="/capital-allocation">
              Capital Allocation
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
