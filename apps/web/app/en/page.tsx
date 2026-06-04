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
import { orgJsonLd, websiteJsonLd } from "../_launch/data";

export const metadata: Metadata = makeMetadata({
  title: "Dealix — AI Revenue & Operations OS (English)",
  description:
    "English overview of Dealix: an AI revenue & operations OS for Saudi and GCC B2B companies. Human-in-the-loop, approval-first, no blind automation.",
  path: "/en",
});

export default function EnglishHome() {
  return (
    <LaunchShell>
      <JsonLd data={orgJsonLd()} />
      <JsonLd data={websiteJsonLd()} />
      <Hero lang="en" />
      <ProblemSolution />
      <VerticalsGrid />
      <OffersTable />
    </LaunchShell>
  );
}
