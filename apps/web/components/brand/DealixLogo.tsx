import type { CSSProperties } from "react";

type Variant = "full" | "wordmark" | "icon" | "monochrome";

const SOURCES: Record<Variant, string> = {
  full: "/brand/dealix-logo.svg",
  wordmark: "/brand/dealix-wordmark.svg",
  icon: "/brand/dealix-icon.svg",
  monochrome: "/brand/dealix-wordmark-mono.svg",
};

export function DealixLogo({
  variant = "full",
  height = 36,
  alt = "Dealix",
  style,
}: {
  variant?: Variant;
  height?: number;
  alt?: string;
  style?: CSSProperties;
}) {
  return (
    <img
      src={SOURCES[variant]}
      alt={alt}
      height={height}
      style={{ height, width: "auto", display: "block", ...style }}
    />
  );
}
