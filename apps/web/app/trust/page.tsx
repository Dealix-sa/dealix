import type { Metadata } from "next";
import { makeMetadata } from "../_launch/meta";
import { JsonLd, LaunchShell, PrinciplesRow, CtaStrip } from "../_launch/Sections";
import { breadcrumbJsonLd } from "../_launch/data";

export const metadata: Metadata = makeMetadata({
  title: "Trust — Approval-first, human-in-the-loop",
  description:
    "How Dealix keeps you in control: AI drafts and recommends, you approve, sending stays manual. Privacy-first for sensitive sectors. No blind automation.",
  path: "/trust",
});

export default function TrustPage() {
  return (
    <LaunchShell>
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "Trust", path: "/trust" },
        ])}
      />
      <h1>Trust — الثقة</h1>
      <PrinciplesRow />
      <h2>Our governing rule — قاعدتنا الحاكمة</h2>
      <p>
        AI drafts, ranks, and recommends. The founder reviews, approves, and sends manually.
        The system never sends externally.
      </p>
      <p dir="rtl">
        الذكاء الاصطناعي يصيغ ويرتّب ويوصي. المؤسس يراجع ويعتمد ويرسل يدويًا. النظام لا يرسل خارجيًا.
      </p>
      <ul>
        <li>No automated email, WhatsApp, or LinkedIn outreach.</li>
        <li>No website form auto-submit, no scraping, no bulk sending.</li>
        <li>Privacy-first: we do not process personal data before a written agreement.</li>
      </ul>
      <CtaStrip />
    </LaunchShell>
  );
}
