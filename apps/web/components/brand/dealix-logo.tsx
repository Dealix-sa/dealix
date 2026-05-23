import type { CSSProperties, JSX } from "react";
import { GrowthArrow } from "./growth-arrow";

type LogoSize = "sm" | "md" | "lg";

interface DealixLogoProps {
  size?: LogoSize;
  monochrome?: boolean;
  style?: CSSProperties;
}

export function DealixLogo({ size = "md", monochrome = false, style }: DealixLogoProps): JSX.Element {
  return (
    <span className={`dealix-wordmark dealix-wordmark--${size}`} style={style} aria-label="Dealix">
      <span>DEAL</span>
      <span className={monochrome ? undefined : "dealix-wordmark__accent"}>IX</span>
      {size !== "sm" ? (
        <GrowthArrow color={monochrome ? "currentColor" : undefined} size={size === "lg" ? 18 : 14} />
      ) : null}
    </span>
  );
}
