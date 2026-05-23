import type { ReactNode } from "react";

export function BrandCard({
  title,
  subtitle,
  actions,
  children,
}: {
  title?: string;
  subtitle?: string;
  actions?: ReactNode;
  children: ReactNode;
}) {
  return (
    <section className="dx-card">
      {(title || actions) && (
        <header className="dx-card__header">
          <div>
            {title ? <h2 className="dx-card__title">{title}</h2> : null}
            {subtitle ? <p className="dx-card__subtitle">{subtitle}</p> : null}
          </div>
          {actions ? <div>{actions}</div> : null}
        </header>
      )}
      {children}
    </section>
  );
}
