import type { ReactNode } from "react";

export function BrandCard({
  title,
  source,
  freshness,
  children,
}: {
  title?: string;
  source?: string;
  freshness?: string;
  children: ReactNode;
}) {
  return (
    <section className="dlx-card">
      {title ? <h2>{title}</h2> : null}
      {children}
      {(source || freshness) && (
        <div className="dlx-source">
          {source ? <>source: {source}</> : null}
          {source && freshness ? " · " : null}
          {freshness ? <>freshness: {freshness}</> : null}
        </div>
      )}
    </section>
  );
}
