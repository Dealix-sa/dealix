import type { Metadata } from "next";
import { makeMetadata } from "../_launch/meta";
import { JsonLd, LaunchShell, OffersTable, CtaStrip } from "../_launch/Sections";
import { breadcrumbJsonLd } from "../_launch/data";

export const metadata: Metadata = makeMetadata({
  title: "Pricing — Dealix offer ladder in SAR",
  description:
    "Dealix pricing in SAR: AI Workflow Audit 499–2,500, Paid Pilot 5,000–25,000, Department OS 25,000–150,000, Retainer 3,000–25,000/mo, Enterprise 150,000+.",
  path: "/pricing",
});

export default function PricingPage() {
  return (
    <LaunchShell>
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "Pricing", path: "/pricing" },
        ])}
      />
      <h1>Pricing — التسعير</h1>
      <p>
        Transparent SAR pricing. We make no income or revenue promises; we map evidenced
        opportunities and you decide.
      </p>
      <OffersTable />
      <CtaStrip />
    </LaunchShell>
  );
}
