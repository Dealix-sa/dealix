import type { ReactNode } from "react";

/** Consistent marketing section scaffold (navy/gold brand tokens). */
export function Section({
  eyebrow,
  title,
  children,
  id,
}: {
  eyebrow?: string;
  title?: string;
  children: ReactNode;
  id?: string;
}) {
  return (
    <section id={id} className="py-12 md:py-16 border-b border-border/40 last:border-0">
      {eyebrow && (
        <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-gold-500">
          {eyebrow}
        </p>
      )}
      {title && (
        <h2 className="mb-6 text-2xl font-bold leading-tight md:text-3xl font-display">
          {title}
        </h2>
      )}
      {children}
    </section>
  );
}
