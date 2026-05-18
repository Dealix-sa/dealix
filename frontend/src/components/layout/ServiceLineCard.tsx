import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

interface ServiceLineCardProps {
  title: string;
  children: ReactNode;
  footer?: ReactNode;
  className?: string;
}

export function ServiceLineCard({
  title,
  children,
  footer,
  className,
}: ServiceLineCardProps) {
  return (
    <li
      className={cn(
        "rounded-2xl border border-border/80 bg-card/60 p-5 md:p-6 card-glass transition-colors hover:border-primary/30",
        className,
      )}
    >
      <h2 className="text-lg font-semibold text-foreground">{title}</h2>
      <div className="mt-2 text-muted-foreground leading-relaxed">{children}</div>
      {footer && <div className="mt-3">{footer}</div>}
    </li>
  );
}
