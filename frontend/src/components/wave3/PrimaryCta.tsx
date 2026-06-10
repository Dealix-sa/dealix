import Link from "next/link";
import { Button } from "@/components/ui/button";

/**
 * The single primary call-to-action for a page.
 * Wave 3 rule: exactly one <PrimaryCta> per page. Secondary links must use
 * a non-primary Button variant (outline / secondary / ghost / link).
 * Enforced by scripts/verify_dealix_cta_map.py and frontend/scripts/verify_wave3_content.mjs.
 */
export function PrimaryCta({
  locale,
  href,
  labelAr,
  labelEn,
  external = false,
}: {
  locale: string;
  /** Route WITHOUT the locale prefix, e.g. "/tools/business-os-score". */
  href: string;
  labelAr: string;
  labelEn: string;
  external?: boolean;
}) {
  const isAr = locale === "ar";
  const label = isAr ? labelAr : labelEn;
  const target = external ? href : `/${locale}${href}`;
  return (
    <Button asChild size="lg" variant="gold" className="font-display">
      <Link href={target} data-primary-cta>
        {label}
      </Link>
    </Button>
  );
}
