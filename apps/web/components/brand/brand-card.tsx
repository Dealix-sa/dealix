import type { JSX, ReactNode } from "react";

interface BrandCardProps {
  title?: string;
  source?: "api" | "fallback" | string;
  actions?: ReactNode;
  children: ReactNode;
}

export function BrandCard({ title, source, actions, children }: BrandCardProps): JSX.Element {
  const isFallback = source === "fallback";
  return (
    <section className="dealix-card">
      {(title || source || actions) && (
        <header className="dealix-card__header">
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            {title ? <span className="dealix-card__title">{title}</span> : null}
            {source ? (
              <span
                className={`dealix-source-pill${isFallback ? " dealix-source-pill--fallback" : ""}`}
              >
                source: {source}
              </span>
            ) : null}
          </div>
          {actions ? <div>{actions}</div> : null}
        </header>
      )}
      <div className="dealix-card__body">{children}</div>
    </section>
  );
}
