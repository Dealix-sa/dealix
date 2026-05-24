"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const TILES: { href: string; label: string; description: string }[] = [
  { href: "/ceo-os", label: "CEO OS", description: "Daily brief, weekly review, decisions" },
  { href: "/founder-leverage", label: "Founder Leverage", description: "Make / Manage / Move" },
  { href: "/capital-allocation", label: "Capital Allocation", description: "Quarterly buckets, ROI" },
  { href: "/strategy", label: "Strategy", description: "Goal tree, North Star, assumptions" },
  { href: "/deal-desk", label: "Deal Desk", description: "Non-standard deal approval" },
  { href: "/enterprise-sales", label: "Enterprise Sales", description: "Motion + multi-thread" },
  { href: "/metrics", label: "Metrics", description: "Hypergrowth metric tree" },
];

export function CeoOsSection() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>CEO OS — Hypergrowth Operating Layer</CardTitle>
        <CardDescription>
          Founder/CEO rhythm, leverage, and decision discipline. Pure navigation —
          no external actions. Walk docs/founder/INDEX.md.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {TILES.map((tile) => (
            <Link
              key={tile.href}
              href={tile.href}
              className="rounded-xl border border-border p-4 hover:bg-muted/40 transition"
            >
              <div className="font-medium text-sm">{tile.label}</div>
              <div className="text-xs text-muted-foreground mt-1">
                {tile.description}
              </div>
            </Link>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
