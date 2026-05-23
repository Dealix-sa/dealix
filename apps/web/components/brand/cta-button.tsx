import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
  onClick?: () => void;
  href?: string;
  variant?: "primary" | "secondary";
  disabled?: boolean;
};

export function CTAButton({ children, onClick, href, variant = "primary", disabled }: Props) {
  const cls = variant === "secondary" ? "dealix-cta secondary" : "dealix-cta";
  if (href) {
    return (
      <a className={cls} href={href} aria-disabled={disabled}>
        {children}
      </a>
    );
  }
  return (
    <button type="button" className={cls} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}
