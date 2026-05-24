import type { CSSProperties } from "react";

export function DealixLogo({ size = 18, style }: { size?: number; style?: CSSProperties }) {
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 8, ...style }}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <rect x="2" y="2" width="20" height="20" rx="5" fill="#0B1B2E" />
        <path d="M7 7h6a5 5 0 1 1 0 10H7V7z" fill="#D6DCE4" />
      </svg>
      <span style={{ fontWeight: 700, letterSpacing: "0.04em", fontSize: size }}>Dealix</span>
    </span>
  );
}
