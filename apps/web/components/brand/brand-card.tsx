import type { ReactNode } from "react";

type BrandCardProps = {
  title?: string;
  subtitle?: string;
  action?: ReactNode;
  children?: ReactNode;
  raised?: boolean;
  tone?: "default" | "accent" | "warning" | "danger";
};

export function BrandCard({
  title,
  subtitle,
  action,
  children,
  raised,
  tone = "default",
}: BrandCardProps) {
  const toneBorder =
    tone === "accent"
      ? "rgba(0,209,161,0.4)"
      : tone === "warning"
        ? "rgba(242,200,75,0.45)"
        : tone === "danger"
          ? "rgba(255,90,95,0.45)"
          : undefined;

  return (
    <section
      className={raised ? "dlx-card dlx-card--raised" : "dlx-card"}
      style={toneBorder ? { borderColor: toneBorder } : undefined}
    >
      {(title || subtitle || action) && (
        <header style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12, marginBottom: 12 }}>
          <div>
            {title && <h2 className="dlx-heading" style={{ fontSize: 18, margin: 0 }}>{title}</h2>}
            {subtitle && <p className="dlx-muted" style={{ margin: "4px 0 0", fontSize: 13 }}>{subtitle}</p>}
          </div>
          {action && <div>{action}</div>}
        </header>
      )}
      {children}
    </section>
  );
}
