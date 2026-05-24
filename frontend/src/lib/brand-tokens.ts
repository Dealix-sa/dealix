import tokensJson from "./brand-tokens.json";

export type BrandColor =
  | "deepNavy"
  | "emeraldTeal"
  | "softSilver"
  | "slate"
  | "white";

export interface BrandTokens {
  color: Record<BrandColor, string>;
  type: {
    fontFamily: string;
    scale: Record<"xs" | "sm" | "md" | "lg" | "xl" | "display", string>;
    weight: Record<"regular" | "medium" | "semibold" | "bold", number>;
  };
  spacing: Record<"xs" | "sm" | "md" | "lg" | "xl" | "xxl", string>;
  radius: Record<"sm" | "md" | "lg" | "xl", string>;
  shadow: Record<"card" | "raised", string>;
  doctrine: {
    appliesTo: string[];
    doesNotReplace: string;
  };
}

export const brandTokens = tokensJson as BrandTokens;

export function color(name: BrandColor): string {
  return brandTokens.color[name];
}
