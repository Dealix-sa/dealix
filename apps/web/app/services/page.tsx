import type { Metadata } from "next";
import { makeMetadata } from "../_launch/meta";
import { JsonLd, LaunchShell, OffersTable, CtaStrip } from "../_launch/Sections";
import { breadcrumbJsonLd, serviceJsonLd } from "../_launch/data";

export const metadata: Metadata = makeMetadata({
  title: "Services — Audit, Pilot, Department OS, Retainer",
  description:
    "Dealix services for Saudi and GCC B2B: AI Workflow Audit, Paid Pilot, Department OS, Monthly Retainer, and Enterprise Custom OS. Approval-first delivery.",
  path: "/services",
});

export default function ServicesPage() {
  return (
    <LaunchShell>
      <JsonLd data={serviceJsonLd()} />
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "Services", path: "/services" },
        ])}
      />
      <h1>Services — الخدمات</h1>
      <p>
        Every engagement is approval-first and human-in-the-loop. AI drafts, ranks, and
        recommends; your team reviews and approves; the system never sends externally.
      </p>
      <OffersTable />
      <h2>How we deliver — كيف نُسلّم</h2>
      <ol>
        <li>Diagnostic / Audit — map two or three quick wins.</li>
        <li>Paid Pilot — ship one measurable workflow with approval gates.</li>
        <li>Department OS — operate one department end to end.</li>
        <li>Retainer — run, tune, and report on live workflows.</li>
      </ol>
      <CtaStrip />
    </LaunchShell>
  );
}
