import type { ButtonHTMLAttributes } from "react";

type Variant = "primary" | "ghost";

export function CTAButton({
  variant = "primary",
  children,
  ...rest
}: { variant?: Variant; children: React.ReactNode } & ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button className={`dx-btn dx-btn--${variant}`} {...rest}>
      {children}
    </button>
  );
}
