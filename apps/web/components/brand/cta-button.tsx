import type { ButtonHTMLAttributes, JSX, ReactNode } from "react";
import Link from "next/link";

type Variant = "primary" | "ghost";

interface CommonProps {
  variant?: Variant;
  children: ReactNode;
}

interface ButtonProps extends CommonProps, Omit<ButtonHTMLAttributes<HTMLButtonElement>, "children"> {
  as?: "button";
  href?: never;
}

interface LinkProps extends CommonProps {
  as: "link";
  href: string;
}

export function CtaButton(props: ButtonProps | LinkProps): JSX.Element {
  const variant: Variant = props.variant ?? "primary";
  const cls = variant === "primary" ? "dealix-cta-primary" : "dealix-cta-ghost";

  if ("as" in props && props.as === "link") {
    return (
      <Link className={cls} href={props.href}>
        {props.children}
      </Link>
    );
  }

  const { children, variant: _variant, as: _as, ...rest } = props as ButtonProps;
  return (
    <button className={cls} {...rest}>
      {children}
    </button>
  );
}
