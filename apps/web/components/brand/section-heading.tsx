import type { JSX, ReactNode } from "react";

interface SectionHeadingProps {
  title: string;
  subtitle?: ReactNode;
}

export function SectionHeading({ title, subtitle }: SectionHeadingProps): JSX.Element {
  return (
    <div className="dealix-section-heading">
      <h2>{title}</h2>
      <span className="dealix-section-heading__rule" />
      {subtitle ? (
        <span style={{ fontSize: 13, color: "var(--dealix-soft-silver)" }}>{subtitle}</span>
      ) : null}
    </div>
  );
}
