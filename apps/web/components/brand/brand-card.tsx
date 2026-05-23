import type { ReactNode } from "react";

export function BrandCard({
  title,
  subtitle,
  children,
  source,
}: {
  title?: string;
  subtitle?: string;
  children: ReactNode;
  source?: "api" | "fallback";
}) {
  return (
    <section className="dealix-card">
      {(title || subtitle || source) && (
        <header style={{ marginBottom: 12, display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }}>
          <div>
            {title && <h2 className="dealix-section-heading">{title}</h2>}
            {subtitle && <p className="dealix-section-sub">{subtitle}</p>}
          </div>
          {source && (
            <span className={source === "api" ? "dealix-source-api" : "dealix-source-fallback"}>
              source: {source}
            </span>
          )}
        </header>
      )}
      {children}
    </section>
  );
}
