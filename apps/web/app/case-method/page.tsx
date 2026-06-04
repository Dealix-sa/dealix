import type { Metadata } from "next";
import { makeMetadata } from "../_launch/meta";
import { JsonLd, LaunchShell, CtaStrip } from "../_launch/Sections";
import { breadcrumbJsonLd } from "../_launch/data";

export const metadata: Metadata = makeMetadata({
  title: "Case Method — how we evidence value",
  description:
    "The Dealix case method: how we document before/after workflows and evidence opportunities without guarantees. Modest, defensible claims only.",
  path: "/case-method",
});

export default function CaseMethodPage() {
  return (
    <LaunchShell>
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "Case Method", path: "/case-method" },
        ])}
      />
      <h1>Case Method — منهجية الحالات</h1>
      <p>
        We document the workflow before, the change we shipped, and what was observed after —
        with the customer&apos;s approval. We describe evidenced opportunities, not promised numbers.
      </p>
      <ol>
        <li>Baseline — map the current workflow and time spent.</li>
        <li>Change — ship one approval-gated AI workflow.</li>
        <li>Evidence — record observed deltas and customer sign-off.</li>
      </ol>
      <CtaStrip />
    </LaunchShell>
  );
}
