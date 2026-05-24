// Founder Console shell — common header + source/freshness pill.

import type { ReactNode } from "react";
import { brandTokens as t } from "../lib/brand-tokens";

type Props = {
  titleEn: string;
  titleAr: string;
  source: "api" | "fallback";
  freshness: string;
  isEstimate: boolean;
  children: ReactNode;
};

export function FounderShell({
  titleEn,
  titleAr,
  source,
  freshness,
  isEstimate,
  children,
}: Props) {
  const pillBg = source === "api" ? t.colors.accentMuted : t.colors.warn;
  const pillText = source === "api" ? "source=api" : "source=fallback";
  return (
    <main
      style={{
        background: t.colors.bg,
        color: t.colors.text,
        fontFamily: t.font.sans,
        minHeight: "100vh",
        padding: t.space.lg,
      }}
    >
      <nav
        style={{
          display: "flex",
          gap: t.space.md,
          marginBottom: t.space.lg,
          flexWrap: "wrap",
          fontSize: 14,
        }}
      >
        <a href="/ceo" style={{ color: t.colors.accent }}>CEO</a>
        <a href="/capital-allocation" style={{ color: t.colors.accent }}>Capital</a>
        <a href="/market-attack" style={{ color: t.colors.accent }}>Market</a>
        <a href="/ai-governance" style={{ color: t.colors.accent }}>AI Gov</a>
        <a href="/trust" style={{ color: t.colors.accent }}>Trust</a>
        <a href="/audit" style={{ color: t.colors.accent }}>Audit</a>
      </nav>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          paddingBottom: t.space.md,
          borderBottom: `1px solid ${t.colors.border}`,
          marginBottom: t.space.lg,
        }}
      >
        <div>
          <h1 style={{ margin: 0, fontSize: 22 }}>{titleEn}</h1>
          <div style={{ color: t.colors.textMuted, marginTop: 4 }} dir="rtl">
            {titleAr}
          </div>
        </div>
        <div style={{ display: "flex", gap: t.space.sm, alignItems: "center" }}>
          <span
            style={{
              background: pillBg,
              color: "#0b0f14",
              padding: "4px 10px",
              borderRadius: t.radius.sm,
              fontSize: 12,
              fontFamily: t.font.mono,
            }}
          >
            {pillText}
          </span>
          {isEstimate && (
            <span
              style={{
                background: t.colors.warn,
                color: "#0b0f14",
                padding: "4px 10px",
                borderRadius: t.radius.sm,
                fontSize: 12,
                fontFamily: t.font.mono,
              }}
            >
              is_estimate=true
            </span>
          )}
          <span
            style={{
              color: t.colors.textMuted,
              fontSize: 12,
              fontFamily: t.font.mono,
            }}
          >
            {freshness}
          </span>
        </div>
      </header>
      <section>{children}</section>
      <footer
        style={{
          marginTop: t.space.xl,
          paddingTop: t.space.md,
          borderTop: `1px solid ${t.colors.border}`,
          color: t.colors.textMuted,
          fontSize: 12,
        }}
      >
        Internal Founder Console — read-only. Honors the 11 non-negotiables.
      </footer>
    </main>
  );
}

export function DataTable({ rows }: { rows: Array<Record<string, string>> }) {
  if (!rows || rows.length === 0) {
    return <p style={{ color: t.colors.textMuted }}>no rows</p>;
  }
  const keys = Object.keys(rows[0]);
  return (
    <div style={{ overflowX: "auto" }}>
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          fontSize: 14,
          fontFamily: t.font.mono,
        }}
      >
        <thead>
          <tr>
            {keys.map((k) => (
              <th
                key={k}
                style={{
                  textAlign: "left",
                  padding: t.space.sm,
                  borderBottom: `1px solid ${t.colors.border}`,
                  color: t.colors.textMuted,
                }}
              >
                {k}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i}>
              {keys.map((k) => (
                <td
                  key={k}
                  style={{
                    padding: t.space.sm,
                    borderBottom: `1px solid ${t.colors.border}`,
                    verticalAlign: "top",
                  }}
                >
                  {String(row[k] ?? "")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
