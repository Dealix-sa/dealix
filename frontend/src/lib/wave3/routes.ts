import type { CtaRoute } from "@/lib/wave3/scoring";

/** The only three destinations a growth asset / tool CTA may route to. */
export function routeToHref(route: CtaRoute): string {
  switch (route) {
    case "business-os-score":
      return "/tools/business-os-score";
    case "diagnostic":
      return "/dealix-diagnostic";
    case "command-sprint":
      return "/command-sprint";
  }
}

/** Canonical bilingual CTA label for each route. */
export function ctaLabelFor(route: CtaRoute): { ar: string; en: string } {
  switch (route) {
    case "business-os-score":
      return { ar: "احصل على Business OS Score", en: "Get Business OS Score" };
    case "diagnostic":
      return { ar: "احجز تشخيصاً", en: "Book Diagnostic" };
    case "command-sprint":
      return { ar: "ابدأ Command Sprint", en: "Start Command Sprint" };
  }
}
