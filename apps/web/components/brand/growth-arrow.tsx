import type { JSX } from "react";

interface GrowthArrowProps {
  size?: number;
  color?: string;
}

export function GrowthArrow({ size = 14, color = "#00D1A1" }: GrowthArrowProps): JSX.Element {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth={2.5}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M4 18 L12 10 L16 14 L22 6" />
      <path d="M16 6 L22 6 L22 12" />
    </svg>
  );
}
