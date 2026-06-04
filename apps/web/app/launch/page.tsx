import type { Metadata } from "next";
import { makeMetadata } from "../_launch/meta";
import { Hero, JsonLd, LaunchShell, VerticalsGrid, OffersTable } from "../_launch/Sections";
import { breadcrumbJsonLd, orgJsonLd } from "../_launch/data";

export const metadata: Metadata = makeMetadata({
  title: "Launch — Dealix is live for Saudi & GCC B2B",
  description:
    "Dealix launch page: AI Revenue & Operations OS for Saudi and GCC B2B companies. Request an AI Workflow Audit, book a diagnostic, or start a pilot.",
  path: "/launch",
});

export default function LaunchPage() {
  return (
    <LaunchShell>
      <JsonLd data={orgJsonLd()} />
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "Launch", path: "/launch" },
        ])}
      />
      <Hero lang="en" />
      <VerticalsGrid />
      <OffersTable />
    </LaunchShell>
  );
}
