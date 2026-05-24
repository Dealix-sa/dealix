// Shared shell for every Founder Console page.
// Provides consistent header + footer (with bilingual disclaimer) and a
// data-source badge ("live" vs "fallback").

import type { ReactNode } from "react";

export type FounderShellProps = {
  title: string;
  subtitle?: string;
  source: "live" | "files" | "fallback";
  children: ReactNode;
};

export function FounderShell({ title, subtitle, source, children }: FounderShellProps) {
  const badgeColor =
    source === "live" ? "#1FB6A8" : source === "files" ? "#0E1F3A" : "#A1A1A1";
  return (
    <main style={{ padding: 24, maxWidth: 1080, margin: "0 auto" }}>
      <header style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div>
          <h1 style={{ margin: 0 }}>{title}</h1>
          {subtitle && <p style={{ marginTop: 4, color: "#555" }}>{subtitle}</p>}
        </div>
        <span
          style={{
            background: badgeColor,
            color: "#fff",
            padding: "4px 10px",
            borderRadius: 12,
            fontSize: 12,
            fontWeight: 600,
          }}
        >
          source={source}
        </span>
      </header>
      <section style={{ marginTop: 24 }}>{children}</section>
      <footer style={{ marginTop: 48, paddingTop: 24, borderTop: "1px solid #e6e6e6", color: "#666", fontSize: 12 }}>
        <em>Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة</em>
      </footer>
    </main>
  );
}
