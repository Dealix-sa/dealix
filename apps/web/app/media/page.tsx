import type { Metadata } from "next";
import { makeMetadata } from "../_launch/meta";
import { JsonLd, LaunchShell, CtaStrip } from "../_launch/Sections";
import { breadcrumbJsonLd, orgJsonLd } from "../_launch/data";

export const metadata: Metadata = makeMetadata({
  title: "Media & Press — Dealix",
  description:
    "Dealix media and press resources: company boilerplate, founder bio, and launch announcement for Saudi and GCC B2B audiences. Manual outreach only.",
  path: "/media",
});

export default function MediaPage() {
  return (
    <LaunchShell>
      <JsonLd data={orgJsonLd()} />
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "Media", path: "/media" },
        ])}
      />
      <h1>Media &amp; Press — الإعلام</h1>
      <h2>Boilerplate — نبذة</h2>
      <p>
        Dealix is an AI revenue &amp; operations OS for Saudi and GCC B2B companies. It drafts,
        ranks, and recommends work while keeping approval and sending under human control.
      </p>
      <p dir="rtl">
        Dealix نظام تشغيل للإيرادات والعمليات بالذكاء الاصطناعي للشركات السعودية والخليجية، يبقي
        الاعتماد والإرسال تحت تحكم بشري.
      </p>
      <CtaStrip />
    </LaunchShell>
  );
}
