import type { ReactNode } from "react";

type SectionHeadingProps = {
  eyebrow?: string;
  title: string;
  description?: string;
  action?: ReactNode;
};

export function SectionHeading({ eyebrow, title, description, action }: SectionHeadingProps) {
  return (
    <header
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-start",
        gap: 16,
        marginBottom: 16,
      }}
    >
      <div>
        {eyebrow && (
          <div
            className="dlx-accent"
            style={{ fontSize: 12, fontWeight: 600, letterSpacing: "0.10em", textTransform: "uppercase" }}
          >
            {eyebrow}
          </div>
        )}
        <h1 className="dlx-heading" style={{ fontSize: 28, margin: "4px 0 0" }}>
          {title}
        </h1>
        {description && (
          <p className="dlx-muted" style={{ margin: "8px 0 0", maxWidth: 720, lineHeight: 1.6 }}>
            {description}
          </p>
        )}
      </div>
      {action && <div>{action}</div>}
    </header>
  );
}
