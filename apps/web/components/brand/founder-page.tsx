import type { ReactNode } from "react";
import { FounderShell } from "../founder-shell";
import { SectionHeading } from "./section-heading";
import { BrandCard } from "./brand-card";

export type Block = { title: string; body: ReactNode };

export function FounderPage({
  title,
  subtitle,
  source = "api / private_ops_csv",
  blocks,
  children,
}: {
  title: string;
  subtitle: string;
  source?: string;
  blocks?: Block[];
  children?: ReactNode;
}) {
  const today = new Date().toISOString().slice(0, 10);
  return (
    <FounderShell>
      <SectionHeading title={title} subtitle={subtitle} />
      {blocks?.map((b) => (
        <BrandCard key={b.title} title={b.title} source={source} freshness={today}>
          {b.body}
        </BrandCard>
      ))}
      {children}
    </FounderShell>
  );
}
