import type { ReactNode } from "react";

interface BrandCardProps {
  title?: string;
  eyebrow?: string;
  description?: string;
  footer?: ReactNode;
  elevated?: boolean;
  children?: ReactNode;
}

export function BrandCard({
  title,
  eyebrow,
  description,
  footer,
  elevated,
  children,
}: BrandCardProps) {
  return (
    <section className={`dx-card ${elevated ? "dx-card--elevated" : ""}`}>
      {eyebrow ? (
        <div
          style={{
            color: "var(--dx-accent)",
            fontSize: "0.75rem",
            fontWeight: 700,
            letterSpacing: "0.18em",
            textTransform: "uppercase",
            marginBottom: 6,
          }}
        >
          {eyebrow}
        </div>
      ) : null}
      {title ? (
        <h2 className="dx-heading" style={{ margin: "0 0 8px 0", fontSize: "1.25rem" }}>
          {title}
        </h2>
      ) : null}
      {description ? (
        <p className="dx-muted" style={{ margin: "0 0 12px 0" }}>
          {description}
        </p>
      ) : null}
      {children}
      {footer ? <div style={{ marginTop: 12 }}>{footer}</div> : null}
    </section>
  );
}

export default BrandCard;
