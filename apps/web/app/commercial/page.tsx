import type { Metadata } from "next";
import { makeMetadata } from "../_launch/meta";
import {
  Hero,
  JsonLd,
  LaunchShell,
  OffersTable,
  ProblemSolution,
  VerticalsGrid,
} from "../_launch/Sections";
import {
  breadcrumbJsonLd,
  orgJsonLd,
  serviceJsonLd,
  websiteJsonLd,
} from "../_launch/data";

export const metadata: Metadata = makeMetadata({
  title: "Commercial — AI Revenue & Operations OS",
  description:
    "Dealix is an AI revenue & operations OS for Saudi and GCC B2B companies. AI drafts and ranks; you review, approve, and send manually.",
  path: "/commercial",
});

export default function CommercialPage() {
  return (
    <LaunchShell>
      <JsonLd data={orgJsonLd()} />
      <JsonLd data={websiteJsonLd()} />
      <JsonLd data={serviceJsonLd()} />
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "Commercial", path: "/commercial" },
        ])}
      />
      <Hero lang="en" />
      <ProblemSolution />
      <VerticalsGrid />
      <OffersTable />
    </LaunchShell>
  );
}
