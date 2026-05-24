import type { ButtonHTMLAttributes } from "react";

export function CtaButton(props: ButtonHTMLAttributes<HTMLButtonElement>) {
  const { className, children, ...rest } = props;
  return (
    <button {...rest} className={`dlx-cta ${className ?? ""}`.trim()}>
      {children}
    </button>
  );
}
