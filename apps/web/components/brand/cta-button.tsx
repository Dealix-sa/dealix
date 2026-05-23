import type { ReactNode, MouseEvent } from "react";

type CtaProps = {
  children: ReactNode;
  href?: string;
  variant?: "primary" | "ghost";
  onClick?: (e: MouseEvent<HTMLButtonElement | HTMLAnchorElement>) => void;
  type?: "button" | "submit";
  disabled?: boolean;
};

export function CtaButton({
  children,
  href,
  variant = "primary",
  onClick,
  type = "button",
  disabled,
}: CtaProps) {
  const cls = variant === "ghost" ? "dlx-cta dlx-cta--ghost" : "dlx-cta";

  if (href) {
    return (
      <a className={cls} href={href} onClick={onClick} aria-disabled={disabled || undefined}>
        {children}
      </a>
    );
  }

  return (
    <button className={cls} type={type} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}
