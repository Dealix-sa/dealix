import type { Metadata } from "next";
import { makeMetadata } from "../_launch/meta";
import { JsonLd, LaunchShell, OffersTable, CtaStrip } from "../_launch/Sections";
import { VERTICALS, breadcrumbJsonLd, serviceJsonLd } from "../_launch/data";

export function verticalMetadata(slug: string): Metadata {
  const v = VERTICALS.find((x) => x.slug === slug);
  const name = v ? v.en : "Vertical";
  return makeMetadata({
    title: `${name} — Dealix`,
    description: v
      ? `Dealix for ${v.en}: ${v.painEn} Approval-first, human-in-the-loop, no blind automation.`
      : "Dealix vertical playbook.",
    path: `/verticals/${slug}`,
  });
}

export function VerticalDetail({ slug }: { slug: string }) {
  const v = VERTICALS.find((x) => x.slug === slug);
  if (!v) {
    return (
      <LaunchShell>
        <h1>Vertical not found</h1>
      </LaunchShell>
    );
  }
  return (
    <LaunchShell>
      <JsonLd data={serviceJsonLd()} />
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "Verticals", path: "/verticals" },
          { name: v.en, path: `/verticals/${v.slug}` },
        ])}
      />
      <h1>
        {v.en} — {v.ar}
      </h1>
      <h2>Where we help — أين نساعد</h2>
      <p>{v.painEn}</p>
      <p dir="rtl">{v.painAr}</p>
      <h2>How it works — كيف يعمل</h2>
      <p>
        Dealix drafts and ranks the outreach and operations work for your team. You review and
        approve every step; sending stays manual. The system never sends externally.
      </p>
      <OffersTable />
      <CtaStrip />
    </LaunchShell>
  );
}
