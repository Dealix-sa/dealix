"use client";

import { cn } from "@/lib/utils";

export type BrandLogoVariant = "full" | "mark";

interface BrandLogoProps {
  variant?: BrandLogoVariant;
  className?: string;
  priority?: boolean;
}

const sources: Record<BrandLogoVariant, { src: string; width: number; height: number }> = {
  full: { src: "/brand/logo.svg", width: 140, height: 34 },
  mark: { src: "/brand/logo-mark.svg", width: 36, height: 36 },
};

export function BrandLogo({
  variant = "full",
  className,
  priority = false,
}: BrandLogoProps) {
  const { src, width, height } = sources[variant];

  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={src}
      alt="Dealix"
      width={width}
      height={height}
      loading={priority ? "eager" : "lazy"}
      decoding="async"
      className={cn("h-auto w-auto object-contain", className)}
    />
  );
}
