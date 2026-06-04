import type { Metadata } from "next";
import { makeMetadata } from "../_launch/meta";
import { JsonLd, LaunchShell, CtaStrip } from "../_launch/Sections";
import { breadcrumbJsonLd, faqJsonLd } from "../_launch/data";

export const metadata: Metadata = makeMetadata({
  title: "FAQ — Dealix",
  description:
    "Frequently asked questions about Dealix: what it is, how approval works, pricing in SAR, data privacy, and why the system never sends on its own.",
  path: "/faq",
});

const QA = [
  {
    q: "Does Dealix send messages automatically?",
    a: "No. AI drafts, ranks, and recommends. The founder reviews, approves, and sends manually. The system never sends externally.",
  },
  {
    q: "How much does it cost?",
    a: "AI Workflow Audit 499–2,500 SAR; Paid Pilot 5,000–25,000 SAR; Department OS 25,000–150,000 SAR; Monthly Retainer 3,000–25,000 SAR/month; Enterprise Custom OS 150,000+ SAR.",
  },
  {
    q: "Which sectors do you serve first?",
    a: "Facilities Management; Contracting & Project Controls; Real Estate & Property Operations; Legal & Professional Services; Consulting, Training & B2B Services.",
  },
  {
    q: "How do you handle data privacy?",
    a: "We are privacy-first. We do not process personal data before a written agreement, and sensitive sectors get privacy-first handling by default.",
  },
];

export default function FaqPage() {
  return (
    <LaunchShell>
      <JsonLd data={faqJsonLd(QA)} />
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "FAQ", path: "/faq" },
        ])}
      />
      <h1>FAQ — الأسئلة الشائعة</h1>
      <dl>
        {QA.map((x) => (
          <div key={x.q}>
            <dt><strong>{x.q}</strong></dt>
            <dd>{x.a}</dd>
          </div>
        ))}
      </dl>
      <CtaStrip />
    </LaunchShell>
  );
}
