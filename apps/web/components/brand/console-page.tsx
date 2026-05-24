import type { ReactNode } from "react";
import { BrandCard } from "./brand-card";
import { SectionHeading } from "./section-heading";
import { StatusBadge } from "./status-badge";

interface ConsoleSection {
  title: string;
  description?: string;
  bullets?: string[];
  status?: "ok" | "warn" | "danger" | "info" | "neutral";
  statusLabel?: string;
}

interface ConsolePageProps {
  eyebrow: string;
  title: string;
  description: string;
  status?: { tone: "ok" | "warn" | "danger" | "info" | "neutral"; label: string };
  sections: ConsoleSection[];
  api?: { method: string; path: string; note?: string }[];
  trustNote?: string;
  related?: { href: string; label: string }[];
  children?: ReactNode;
}

export function ConsolePage({
  eyebrow,
  title,
  description,
  status,
  sections,
  api,
  trustNote,
  related,
  children,
}: ConsolePageProps) {
  return (
    <div className="dx-grid" style={{ gap: 24 }}>
      <header className="dx-card dx-card--elevated">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 16 }}>
          <div>
            <div
              style={{
                color: "var(--dx-accent)",
                fontSize: "0.72rem",
                fontWeight: 700,
                letterSpacing: "0.24em",
                textTransform: "uppercase",
                marginBottom: 8,
              }}
            >
              {eyebrow}
            </div>
            <h1
              className="dx-heading"
              style={{ margin: 0, fontSize: "1.875rem", letterSpacing: "-0.01em" }}
            >
              {title}
            </h1>
            <p className="dx-muted" style={{ margin: "8px 0 0 0", maxWidth: 720 }}>
              {description}
            </p>
          </div>
          {status ? <StatusBadge tone={status.tone} label={status.label} /> : null}
        </div>
      </header>

      <div className="dx-grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))" }}>
        {sections.map((s) => (
          <BrandCard
            key={s.title}
            eyebrow={s.statusLabel}
            title={s.title}
            description={s.description}
          >
            {s.bullets ? (
              <ul style={{ margin: 0, paddingInlineStart: 18, color: "var(--dx-text-secondary)" }}>
                {s.bullets.map((b) => (
                  <li key={b} style={{ marginBottom: 4 }}>{b}</li>
                ))}
              </ul>
            ) : null}
          </BrandCard>
        ))}
      </div>

      {api && api.length ? (
        <section>
          <SectionHeading eyebrow="API surface" title="Endpoints" description="Read-only signal endpoints exposed to the founder console. Trust-gated writes require approval." />
          <div className="dx-grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))" }}>
            {api.map((a) => (
              <div key={`${a.method} ${a.path}`} className="dx-card">
                <code style={{ color: "var(--dx-accent)" }}>{a.method}</code>{" "}
                <code style={{ color: "var(--dx-text)" }}>{a.path}</code>
                {a.note ? (
                  <p className="dx-muted" style={{ margin: "6px 0 0 0", fontSize: "0.85rem" }}>{a.note}</p>
                ) : null}
              </div>
            ))}
          </div>
        </section>
      ) : null}

      {trustNote ? (
        <section className="dx-card">
          <div style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
            <StatusBadge tone="info" label="Trust" />
            <p className="dx-muted" style={{ margin: 0 }}>{trustNote}</p>
          </div>
        </section>
      ) : null}

      {related && related.length ? (
        <section>
          <SectionHeading eyebrow="Related" title="Other surfaces" />
          <div className="dx-row">
            {related.map((r) => (
              <a key={r.href} href={r.href} className="dx-button dx-button--ghost">{r.label}</a>
            ))}
          </div>
        </section>
      ) : null}

      {children}
    </div>
  );
}

export default ConsolePage;
