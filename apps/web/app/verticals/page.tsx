import type { Metadata } from "next";
import { makeMetadata } from "../_launch/meta";
import { JsonLd, LaunchShell, VerticalsGrid, CtaStrip } from "../_launch/Sections";
import { breadcrumbJsonLd } from "../_launch/data";

export const metadata: Metadata = makeMetadata({
  title: "Verticals — First 5 sectors Dealix serves",
  description:
    "Dealix first 5 verticals: Facilities Management, Contracting & Project Controls, Real Estate & Property Operations, Legal & Professional Services, Consulting/Training & B2B.",
  path: "/verticals",
});

export default function VerticalsIndex() {
  return (
    <LaunchShell>
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "Verticals", path: "/verticals" },
        ])}
      />
      <h1>Verticals — القطاعات</h1>
      <VerticalsGrid />
      <CtaStrip />
    </LaunchShell>
  );
}
