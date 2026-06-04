import type { Metadata } from "next";
import { makeMetadata } from "../_launch/meta";
import { JsonLd, LaunchShell, CtaStrip } from "../_launch/Sections";
import { breadcrumbJsonLd } from "../_launch/data";

export const metadata: Metadata = makeMetadata({
  title: "Contact — Request an AI Workflow Audit",
  description:
    "Contact Dealix to request an AI Workflow Audit, book a diagnostic, or start a pilot. We reply manually; we never auto-send or process data before agreement.",
  path: "/contact",
});

export default function ContactPage() {
  return (
    <LaunchShell>
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "Contact", path: "/contact" },
        ])}
      />
      <h1>Contact — تواصل معنا</h1>
      <p>
        Tell us your sector and the workflow you want to improve. A human reads every message
        and replies manually — no automated sending on our side.
      </p>
      <CtaStrip />
      <p>
        Prefer email? Write to the address published on our official channels. We confirm consent
        before any follow-up.
      </p>
    </LaunchShell>
  );
}
