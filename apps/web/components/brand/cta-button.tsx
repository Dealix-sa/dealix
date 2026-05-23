import type { ReactNode } from "react";

type Variant = "primary" | "ghost";

interface CtaButtonProps {
  href?: string;
  variant?: Variant;
  children: ReactNode;
}

export function CtaButton({ href = "#", variant = "primary", children }: CtaButtonProps) {
  const cls = variant === "ghost" ? "dx-button dx-button--ghost" : "dx-button";
  return (
    <a className={cls} href={href}>
      {children}
    </a>
  );
}

export default CtaButton;
