import type { ReactNode } from "react";
import { ConsoleShell } from "./ConsoleShell";
import { BrandCard } from "../brand/BrandCard";
import { SectionHeading } from "../brand/SectionHeading";
import { DataSourceTag } from "../brand/DataSourceTag";

export function ConsolePage({
  active,
  title,
  subtitle,
  source = "fallback",
  intro,
  children,
}: {
  active: string;
  title: string;
  subtitle?: string;
  source?: "api" | "fallback";
  intro?: ReactNode;
  children: ReactNode;
}) {
  return (
    <ConsoleShell active={active}>
      <BrandCard
        title={title}
        subtitle={subtitle}
        actions={<DataSourceTag source={source} />}
      >
        {intro ?? (
          <p style={{ color: "var(--dx-text-secondary)", margin: 0 }}>
            Read-only surface. Actions taken from this page are queued for
            founder approval. Automation never sends externally without
            policy + audit clearance.
          </p>
        )}
      </BrandCard>
      {children}
    </ConsoleShell>
  );
}

export function SafeList({ items }: { items: string[] }) {
  return (
    <ul style={{ margin: 0, paddingInlineStart: 20, color: "var(--dx-text-secondary)" }}>
      {items.map((item) => (
        <li key={item} style={{ marginBottom: 6 }}>
          {item}
        </li>
      ))}
    </ul>
  );
}

export function PlaceholderTable({
  columns,
  emptyLabel = "No data yet — bootstrap private ops runtime to populate.",
}: {
  columns: string[];
  emptyLabel?: string;
}) {
  return (
    <table className="dx-table">
      <thead>
        <tr>
          {columns.map((c) => (
            <th key={c}>{c}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        <tr>
          <td colSpan={columns.length} style={{ color: "var(--dx-text-muted)" }}>
            {emptyLabel}
          </td>
        </tr>
      </tbody>
    </table>
  );
}
